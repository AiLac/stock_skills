#!/usr/bin/env python3
"""Render a completed 13-section stock report using Pandoc and WeasyPrint."""
import argparse
from html import escape
import json
from pathlib import Path
import re
import shutil
from string import Template
import subprocess
import tempfile
from urllib.parse import urlsplit

from report_pdf_charts import chart_for_table


ASSETS = Path(__file__).resolve().parents[1] / "assets" / "pdf"
SECTION_COUNT = 13


def executable(name):
    path = shutil.which(name)
    if not path:
        raise ValueError(f"找不到命令 {name}。请先安装该依赖，或指定可执行文件的路径。")
    return path


def run(command, content):
    proc = subprocess.run(command, input=content, encoding="utf-8", capture_output=True,
                          timeout=180, check=False)
    if proc.returncode:
        raise ValueError(f"{Path(command[0]).name} 渲染失败：{proc.stderr.strip()}")
    return proc.stdout


def plain_text(inlines):
    parts = []
    for node in inlines:
        kind = node["t"]
        content = node.get("c")
        if kind == "Str":
            parts.append(content)
        elif kind in ("Space", "SoftBreak", "LineBreak"):
            parts.append(" ")
        elif kind in ("Code", "Math"):
            parts.append(content[1])
        elif kind in ("Link", "Image", "Span", "Quoted", "Cite"):
            parts.append(plain_text(content[1]))
        elif isinstance(content, list) and all(isinstance(item, dict) for item in content):
            parts.append(plain_text(content))
    return "".join(parts).strip()


def header_text(block):
    # The canonical template uses these four pictograms as decorative prefixes.
    return re.sub(r"^(?:🏢|📊|👤|⚠️?)\s*", "", plain_text(block["c"][2]))


def safe_content(value):
    """Keep Markdown formatting and web citations. Attachments are represented by their alt text."""
    if isinstance(value, list):
        return [safe_content(item) for item in value]
    if not isinstance(value, dict):
        return value
    kind = value.get("t")
    content = value.get("c")
    if kind in ("Link", "Image"):
        label = safe_content(content[1])
        target = content[2][0].strip()
        if kind == "Link" and (target.startswith("#") or urlsplit(target).scheme.lower() in ("http", "https", "mailto")):
            return {"t": "Link", "c": [["", [], []], label, [target, content[2][1]]]}
        return {"t": "Span", "c": [["", [], []], label]}
    if kind == "RawInline":
        return {"t": "LineBreak"} if re.fullmatch(r"<br\s*/?>", content[1], re.I) else {"t": "Str", "c": ""}
    if kind == "RawBlock":
        return {"t": "Null"}
    return {key: safe_content(item) for key, item in value.items()}


def raw_html(markup):
    return {"t": "RawBlock", "c": ["html", markup]}


def report_html(markdown, pandoc, language):
    doc = json.loads(run([pandoc, "--from=gfm", "--to=json"], markdown))
    blocks = safe_content(doc["blocks"])
    if not blocks or blocks[0]["t"] != "Header" or blocks[0]["c"][0] != 1:
        raise ValueError("报告须以一级 Markdown 标题（# 报告名称）开头。")
    title = header_text(blocks[0])
    sections = [block for block in blocks if block["t"] == "Header" and block["c"][0] == 2]
    if len(sections) != SECTION_COUNT:
        raise ValueError(f"报告模板含 {SECTION_COUNT} 个二级章节（##），当前识别到 {len(sections)} 个。")

    body = []
    toc = []
    number = 0
    heading = ""
    for block in blocks[1:]:
        if block["t"] == "Header":
            level, attr, _ = block["c"]
            heading = header_text(block)
            if level == 2:
                if number:
                    body.append(raw_html("</section>"))
                number += 1
                label = f"{number:02}"
                anchor = f"s{label}"
                text = escape(heading)
                toc.append(f'<a href="#{anchor}"><span>{label}</span>{text}</a>')
                original_id = escape(attr[0], quote=True)
                alias = f' id="{original_id}"' if original_id and not re.fullmatch(r"s\d\d", original_id) else ""
                body.append(raw_html(
                    f'<section class="report-section" id="{anchor}"><h2{alias}>'
                    f'<span class="section-number">{label}</span> {text}</h2>'
                ))
                continue
            if level == 1:  # A worked example may have an introductory note before its report title.
                block["c"][0] = 3
        body.append(block)
        if block["t"] == "Table" and number:
            graphic = chart_for_table(block, number, heading)
            if graphic:
                body.append(raw_html(graphic))
    body.append(raw_html("</section>"))
    doc.update(meta={}, blocks=body)
    body_html = run([pandoc, "--from=json", "--to=html5", "--wrap=none"], json.dumps(doc))
    layout = Template((ASSETS / "report.html").read_text(encoding="utf-8"))
    return layout.substitute(title=escape(title), lang=escape(language, quote=True),
                             css=(ASSETS / "report.css").read_text(encoding="utf-8"),
                             toc="\n".join(toc), body=body_html)


def render(source, output, pandoc, weasyprint, language):
    if output.suffix.lower() != ".pdf" or source.resolve() == output.resolve():
        raise ValueError("请将输出指定为独立的 .pdf 文件。")
    content = source.read_text(encoding="utf-8-sig")
    html = report_html(content, executable(pandoc), language)
    printer = executable(weasyprint)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".report-pdf-", dir=output.parent) as tmp:
        draft = Path(tmp) / "report.pdf"
        run([printer, "--encoding", "utf-8", "--allowed-protocols", "data",
             "-", str(draft)], html)
        with draft.open("rb") as check:
            if check.read(5) != b"%PDF-":
                raise ValueError("导出失败，渲染器没有生成 PDF。")
        draft.replace(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="UTF-8 Markdown report")
    parser.add_argument("output", type=Path, help="destination PDF")
    parser.add_argument("--lang", default="zh-CN", help="document language, e.g. zh-CN or en")
    parser.add_argument("--pandoc", default="pandoc", help="Pandoc executable")
    parser.add_argument("--weasyprint", default="weasyprint", help="WeasyPrint executable")
    args = parser.parse_args()
    try:
        render(args.report, args.output, args.pandoc, args.weasyprint, args.lang)
    except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"{parser.prog}: {exc}\n")
    print(args.output)


if __name__ == "__main__":
    main()
