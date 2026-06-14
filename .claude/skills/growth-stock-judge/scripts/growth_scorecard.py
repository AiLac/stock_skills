#!/usr/bin/env python3
"""Growth-stock judgment scorecard.

Scores a US growth stock 0-100 across growth-investing factors, applies
penalties for risk/利空 (negative catalysts), computes a dual-axis
quality-vs-entry read, and caps the verdict to "avoid/watch" when a red
line (kill-switch) is triggered.

Usage:
  python scripts/growth_scorecard.py --template
  python scripts/growth_scorecard.py scorecard.json --format md
  cat scorecard.json | python scripts/growth_scorecard.py - --format both
"""
from __future__ import annotations

import argparse
import json
import sys

# Factor weights sum to 100. First six are "quality" factors (max 80),
# last two are "entry/price" factors (max 20) so price affects the verdict
# without letting a high price alone veto a great growth company.
QUALITY_WEIGHTS = {
    "revenue_growth_durability": 18,
    "tam_penetration": 14,
    "moat_chain_position": 14,
    "unit_economics_profit_path": 14,
    "product_customer_momentum": 12,
    "management_capital_allocation": 8,
}
ENTRY_WEIGHTS = {
    "valuation_growth_match": 12,
    "entry_expectations": 8,
}
WEIGHTS = {**QUALITY_WEIGHTS, **ENTRY_WEIGHTS}

PENALTY_MULTIPLIER = 2.0
PENALTY_KEYS = [
    "dilution_financing",
    "customer_concentration",
    "accounting_quality",
    "governance",
    "competition_disruption",
    "regulation_geopolitics",
    "liquidity_bubble",
    "lockup_insider_supply",  # 解禁/增发/内部人卖出/降评级 (筹码面)
]

# Red lines force a capped verdict regardless of the numeric score, so a high
# score can never bury a fatal problem.
RED_LINE_KEYS = [
    "accounting_fraud_suspicion",
    "core_customer_loss",
    "growth_engine_broken",
]

CAPPED_VERDICT = "回避 / 观望（红线封顶）"

TEMPLATE = {
    "ticker": "EXAMPLE",
    "company": "Example Co",
    "factors": {key: 0 for key in WEIGHTS},
    "penalties": {key: 0 for key in PENALTY_KEYS},
    "red_lines": {key: False for key in RED_LINE_KEYS},
    "evidence": [
        {"claim": "", "value": "", "source": "",
         "strength": "strong/medium/weak/needs_checking"}
    ],
    "what_could_weaken_view": ["", "", ""],
}


def _num_0_to_5(value, label):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a number from 0 to 5") from None
    if number < 0 or number > 5:
        raise ValueError(f"{label} must be from 0 to 5; got {number}")
    return number


def verdict_for(final_score):
    if final_score >= 85:
        return "强信心值得投资"
    if final_score >= 70:
        return "值得投资"
    if final_score >= 55:
        return "观望 / 建仓试探"
    return "暂不值得 / 回避"


def load_input(path):
    raw = sys.stdin.read() if path == "-" else open(path, "r", encoding="utf-8").read()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Input JSON must be an object")
    return data


def score(data):
    factors = data.get("factors", {})
    penalties = data.get("penalties", {})
    red_lines = data.get("red_lines", {})

    factor_details = {}
    quality_points = 0.0
    entry_points = 0.0
    for key, weight in WEIGHTS.items():
        rating = _num_0_to_5(factors.get(key, 0), f"factors.{key}")
        points = rating / 5.0 * weight
        factor_details[key] = {"rating": rating, "weight": weight,
                               "points": round(points, 2)}
        if key in QUALITY_WEIGHTS:
            quality_points += points
        else:
            entry_points += points

    penalty_details = {}
    penalty_total = 0.0
    for key in PENALTY_KEYS:
        rating = _num_0_to_5(penalties.get(key, 0), f"penalties.{key}")
        points = rating * PENALTY_MULTIPLIER
        penalty_details[key] = {"rating": rating, "points": round(points, 2)}
        penalty_total += points

    raw_total = quality_points + entry_points
    final_score = max(0.0, min(100.0, raw_total - penalty_total))

    quality_score = round(quality_points / sum(QUALITY_WEIGHTS.values()) * 100, 2)
    entry_score = round(entry_points / sum(ENTRY_WEIGHTS.values()) * 100, 2)

    triggered = [k for k in RED_LINE_KEYS if bool(red_lines.get(k, False))]
    capped = len(triggered) > 0
    verdict = CAPPED_VERDICT if capped else verdict_for(final_score)

    return {
        "ticker": data.get("ticker", ""),
        "company": data.get("company", ""),
        "raw_factor_points": round(raw_total, 2),
        "penalty_points": round(penalty_total, 2),
        "final_score": round(final_score, 2),
        "quality_score": quality_score,
        "entry_score": entry_score,
        "verdict": verdict,
        "capped_by_red_line": capped,
        "triggered_red_lines": triggered,
        "factor_details": factor_details,
        "penalty_details": penalty_details,
        "what_could_weaken_view": data.get("what_could_weaken_view", []),
        "evidence": data.get("evidence", []),
    }


def to_markdown(result):
    title = result.get("ticker") or "Unknown"
    if result.get("company"):
        title += f" ({result['company']})"
    lines = [
        f"# 成长股评分卡：{title}",
        "",
        f"结论：**{result['verdict']}**",
        f"总分：**{result['final_score']} / 100**　｜　质量分：**{result['quality_score']}**　｜　买点分：**{result['entry_score']}**",
        f"原始因子分：{result['raw_factor_points']}　｜　惩罚扣分：{result['penalty_points']}",
    ]
    if result["capped_by_red_line"]:
        lines.append(f"⚠️ 红线封顶：{', '.join(result['triggered_red_lines'])}")
    lines += ["", "## 因子", "| 因子 | 评分(0-5) | 权重 | 得分 |", "|---|---:|---:|---:|"]
    for key, d in result["factor_details"].items():
        lines.append(f"| {key} | {d['rating']} | {d['weight']} | {d['points']} |")
    lines += ["", "## 惩罚项 (×2)", "| 惩罚 | 评分(0-5) | 扣分 |", "|---|---:|---:|"]
    for key, d in result["penalty_details"].items():
        lines.append(f"| {key} | {d['rating']} | {d['points']} |")
    weak = [str(x).strip() for x in result.get("what_could_weaken_view", []) if str(x).strip()]
    if weak:
        lines += ["", "## 什么情况说明判断错了"]
        lines += [f"- {x}" for x in weak]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Score a growth-stock judgment")
    parser.add_argument("input", nargs="?", help="JSON file, or '-' for stdin")
    parser.add_argument("--template", action="store_true", help="Print a JSON template")
    parser.add_argument("--format", choices=["json", "md", "both"], default="json")
    args = parser.parse_args()

    if args.template:
        print(json.dumps(TEMPLATE, ensure_ascii=False, indent=2))
        return
    if not args.input:
        parser.error("input is required unless --template is used")

    result = score(load_input(args.input))
    if args.format in ("json", "both"):
        print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.format == "both":
        print("\n---\n")
    if args.format in ("md", "both"):
        print(to_markdown(result))


if __name__ == "__main__":
    main()
