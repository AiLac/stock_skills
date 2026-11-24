"""Add bar charts for complete, comparable numeric columns in the report tables."""

from decimal import Decimal
from html import escape
from math import ceil
import re
import unicodedata


def _text(node):
    """Extract display text from the subset of Pandoc markup used in table cells."""
    if isinstance(node, list):
        return "".join(_text(item) for item in node)
    kind = node["t"]
    content = node.get("c", [])
    if kind == "Str":
        return content
    if kind in ("Space", "SoftBreak", "LineBreak"):
        return " "
    if kind in ("Plain", "Para", "Emph", "Strong", "Underline"):
        return _text(content)
    if kind in ("Span", "Link"):
        return _text(content[1])
    if kind == "Code":
        return content[1]
    # Keep unusual expressions in the original table. They must not silently
    # disappear inside a numeric cell (e.g. a footnote qualifying comparability).
    return "�"


def _row_values(row):
    cells = row[1]
    if any(cell[2:4] != [1, 1] for cell in cells):
        return []
    return [_text(cell[4]).strip() for cell in cells]


def _key(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", value).casefold())


def _metric(section, headers):
    """Select the table's metric by explicit column labels, never by position alone."""
    if section == 2 and headers[0] in {"因子", "评分因子", "factor", "factors"}:
        for i, name in enumerate(headers[1:], 1):
            if re.fullmatch(r"(?:评分|打分|score|rating)\(0[-–—~至]5\)", name):
                return i, "rating"
    if section == 3 and headers[0] in {
        "分部", "业务分部", "业务", "分部/业务", "segment", "segment/business", "businesssegment",
    }:
        for i, name in enumerate(headers[1:], 1):
            if name in {"占合并收入%", "占合并营收%", "占比%", "占总收入%", "占总营收%",
                        "%ofrevenue", "%ofconsolidatedrevenue", "shareofrevenue(%)"}:
                return i, "revenue"
    if section == 6 and headers[0] in {"报表科目", "科目", "费用项目", "lineitem", "expense", "expenseitem"}:
        for i, name in enumerate(headers[1:], 1):
            if name in {"占营收%", "占收入%", "占营收%(适用时)", "占营收比例(%)", "%ofrevenue",
                        "%ofrevenue(ifapplicable)", "shareofrevenue(%)"}:
                return i, "cost"
    return None


# Subtotals, nested rows and intersegment eliminations can mix different
# aggregation levels. Their presence makes a chart ambiguous; keep the table.
_NESTED = re.compile(r"其中|含于|已含|已计入|抵销|抵消|小计|subtotal|elimination|ofwhich|includedin|including")
_TOTAL = re.compile(r"合计|总计|^合并(?:营收|收入)$|^(?:总营收|总收入)$|^total|grandtotal$")
_NUMBER = re.compile(r"\d{1,5}(?:\.\d{1,6})?")
_NON_OPERATING_COST = re.compile(
    r"利润|毛利|盈余|亏损|利息|财务费用|融资|所得税|营业外|资本开支|现金流|营业收入|^营收$|"
    r"profit|grossmargin|operatingmargin|earnings|netincome|operatingincome|pretax|taxexpense|incometax|"
    r"loss|interest|financ(?:e|ing)(?:cost|expense)|ebit|capex|cashflow|^revenue$"
)


def _figure(points, metric, chinese):
    titles = {
        "rating": ("因子评分（0–5 分）", "Factor ratings (0–5)"),
        "revenue": ("各业务占合并收入比例", "Share of consolidated revenue"),
        "cost": ("各项经营成本与费用占营收比例", "Operating costs and expenses as a share of revenue"),
    }
    caption = titles[metric][0 if chinese else 1]
    largest = max(value for _, value, _ in points)
    scale = 5 if metric == "rating" else max(100, ceil(largest / 25) * 25)
    if scale > 100:
        caption += f"（0–{scale}%）" if chinese else f" (0–{scale}%)"
    suffix = "" if metric == "rating" else "%"
    result = [f'<figure class="data-figure"><figcaption>{caption}</figcaption>']
    for label, value, raw in points:
        width = format(value / scale * 100, ".3f")
        color = "#263f5d" if metric == "cost" else "#12675f"
        result.append(
            '<div class="chart-row" style="display:table;table-layout:fixed;width:100%">'
            '<span class="chart-label" style="display:table-cell;width:42%;vertical-align:middle">'
            f'{escape(label)}</span>'
            '<span style="display:table-cell;width:45%;vertical-align:middle">'
            '<svg aria-hidden="true" width="100%" height="8" style="width:100%;height:2mm">'
            '<rect width="100%" height="100%" fill="#dae6e4"/>'
            f'<rect width="{width}%" height="100%" fill="{color}"/></svg></span>'
            '<span class="chart-value" style="display:table-cell;width:13%;vertical-align:middle;text-align:right">'
            f'{escape(raw)}{suffix}</span></div>'
        )
    result.append("</figure>")
    return "".join(result)


def chart_for_table(table_block: dict, section_index: int, heading: str) -> str:
    """Draw bars only when a single complete, comparable series is identifiable.

    section_index is one-based in the template. Percentages are taken directly
    from the report; source amounts and all non-charted rows remain in its table.
    """
    if table_block.get("t") != "Table" or section_index not in (2, 3, 6):
        return ""
    _, _, _, head, bodies, foot = table_block["c"]
    if len(head[1]) != 1 or len(bodies) != 1 or bodies[0][2] or foot[1]:
        return ""
    labels = _row_values(head[1][0])
    if not labels:
        return ""
    metric = _metric(section_index, [_key(label) for label in labels])
    if not metric:
        return ""
    column, kind = metric
    points = []
    seen = set()
    for row in bodies[0][3]:
        cells = _row_values(row)
        if len(cells) != len(labels):
            return ""
        label = cells[0]
        key = _key(label)
        if not key or key in seen or "�" in label or _NESTED.search(key):
            return ""
        seen.add(key)
        if kind == "cost" and _NON_OPERATING_COST.search(key):
            return ""
        if _TOTAL.search(key):
            continue
        if kind == "cost" and any(_NESTED.search(_key(cell)) for cell in cells[1:]):
            return ""
        value = unicodedata.normalize("NFKC", cells[column]).strip()
        raw = value.removesuffix("%").strip() if kind != "rating" else value
        if not _NUMBER.fullmatch(raw):
            return ""
        number = Decimal(raw)
        if (kind == "rating" and number > 5) or (kind == "revenue" and number > 100):
            return ""
        points.append((label, number, raw))
    if not 2 <= len(points) <= 12:
        return ""
    if kind == "revenue":
        # Allow modest reporting-rounding differences without inventing a residual.
        if abs(sum(value for _, value, _ in points) - 100) > 1:
            return ""
    return _figure(points, kind, bool(re.search(r"[\u3400-\u9fff]", labels[0] + heading)))
