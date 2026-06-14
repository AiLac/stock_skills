# growth-stock-judge Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Claude skill `growth-stock-judge` that takes one US ticker and outputs a verdict-first growth-investing judgment (worth investing / watch / avoid), backed by a multi-agent research workflow and a quantitative scorecard.

**Architecture:** A SKILL.md orchestrates 7 parallel research sub-agents (fan-out) whose findings a synthesizer agent merges, scores via `growth_scorecard.py`, and renders into an 11-section report (synthesize). Reference docs hold the deep detail; the one real code unit is the scorecard. Reuses `serenity-skill` assets (evidence ladder, US source paths, risk/compliance) with built-in fallbacks. Built and validated per the `skill-creator` conventions.

**Tech Stack:** Markdown (SKILL.md + references), Python 3 stdlib (scorecard + unittest), JSON (templates/schema/evals). No third-party runtime deps.

**Spec:** `docs/superpowers/specs/2026-06-14-growth-stock-judge-design.md`

---

## File Structure (locked in)

All paths relative to repo root `C:/Users/Admin/Desktop/stock/`.

```
.claude/skills/growth-stock-judge/
├── SKILL.md                          # frontmatter + orchestration + workflow skeleton + scoring summary + output contract + fallback
├── agents/
│   └── openai.yaml                   # Agent Skills interface manifest (serenity format)
├── scripts/
│   ├── growth_scorecard.py           # REAL CODE: weighted scoring, penalties, dual-axis, red-line cap
│   └── test_growth_scorecard.py      # stdlib unittest, dependency-free
├── references/
│   ├── orchestration.md              # dispatch / parallel / barrier / sub-agent I/O contract
│   ├── agent-roster.md               # role definition per sub-agent (mission/inputs/output/evidence)
│   ├── growth-analysis-workflow.md   # detailed 10-step single-stock research workflow
│   ├── growth-scoring-rubric.md      # 0-5 anchors for each of the 8 factors + penalties + red lines
│   ├── earnings-readthrough.md       # latest-earnings deep-read checklist (8 blocks)
│   ├── valuation-and-entry.md        # growth-stock valuation + entry-point method
│   ├── risk-and-bear-case.md         # risk/利空 catalog + red-line (kill-switch) criteria
│   └── positioning-and-options.md    # 筹码面 + options-market signals, data sources, grading
├── assets/
│   ├── scorecard-input.json          # input template (mirrors scorecard TEMPLATE)
│   ├── agent-findings-schema.json    # unified sub-agent output structure
│   └── stock-verdict-template.md     # 11-section report template
├── examples/
│   └── spcx-demo.md                  # SPCX worked example
└── evals/
    ├── evals.json                    # runnable test set (prompts + assertions), skill-creator format
    └── test-cases.md                 # human-readable trigger/behavior/orchestration checklist
```

**Build order rationale:** scorecard first (real code, everything else references its keys), then assets (schema/templates that depend on scorecard keys), then references (detail), then SKILL.md (ties it together, must reference the now-existing files), then agents manifest, example, evals, finally validation.

---

## Task 1: Scaffold the skill directory

**Files:**
- Create: `.claude/skills/growth-stock-judge/` (directory)

- [ ] **Step 1: Create the directory tree**

Run:
```bash
mkdir -p ".claude/skills/growth-stock-judge/agents" \
         ".claude/skills/growth-stock-judge/scripts" \
         ".claude/skills/growth-stock-judge/references" \
         ".claude/skills/growth-stock-judge/assets" \
         ".claude/skills/growth-stock-judge/examples" \
         ".claude/skills/growth-stock-judge/evals"
```
Expected: directories created, no output.

- [ ] **Step 2: Verify**

Run: `ls -R ".claude/skills/growth-stock-judge"`
Expected: the six subdirectories listed, all empty.

(No commit yet — empty dirs aren't tracked by git. The first commit lands in Task 2.)

---

## Task 2: `growth_scorecard.py` (TDD — the core code unit)

This is the only real logic. Build it test-first. Tests use the stdlib `unittest` so they run anywhere with `python` (no pip install).

**Files:**
- Create: `.claude/skills/growth-stock-judge/scripts/test_growth_scorecard.py`
- Create: `.claude/skills/growth-stock-judge/scripts/growth_scorecard.py`

- [ ] **Step 1: Write the failing tests**

Create `.claude/skills/growth-stock-judge/scripts/test_growth_scorecard.py`:

```python
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import growth_scorecard as gs


def all_factors(rating):
    return {k: rating for k in gs.WEIGHTS}


class TestWeights(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(gs.WEIGHTS.values()), 100)

    def test_quality_entry_split(self):
        self.assertEqual(sum(gs.QUALITY_WEIGHTS.values()), 80)
        self.assertEqual(sum(gs.ENTRY_WEIGHTS.values()), 20)


class TestScoring(unittest.TestCase):
    def test_perfect_score(self):
        r = gs.score({"factors": all_factors(5)})
        self.assertEqual(r["final_score"], 100.0)
        self.assertEqual(r["quality_score"], 100.0)
        self.assertEqual(r["entry_score"], 100.0)
        self.assertEqual(r["verdict"], "强信心值得投资")
        self.assertFalse(r["capped_by_red_line"])

    def test_zero_score(self):
        r = gs.score({"factors": all_factors(0)})
        self.assertEqual(r["final_score"], 0.0)
        self.assertEqual(r["verdict"], "暂不值得 / 回避")

    def test_penalty_reduces_score(self):
        r = gs.score({"factors": all_factors(5),
                      "penalties": {"dilution_financing": 5}})
        # raw 100 - (5 * 2.0) = 90
        self.assertEqual(r["final_score"], 90.0)
        self.assertEqual(r["verdict"], "强信心值得投资")

    def test_dual_axis_good_company_expensive(self):
        # quality factors maxed, entry factors zero -> great biz, bad price
        factors = {k: (5 if k in gs.QUALITY_WEIGHTS else 0) for k in gs.WEIGHTS}
        r = gs.score({"factors": factors})
        self.assertEqual(r["quality_score"], 100.0)
        self.assertEqual(r["entry_score"], 0.0)
        self.assertEqual(r["final_score"], 80.0)  # raw quality points = 80
        self.assertEqual(r["verdict"], "值得投资")

    def test_red_line_caps_high_score(self):
        r = gs.score({"factors": all_factors(5),
                      "red_lines": {"accounting_fraud_suspicion": True}})
        self.assertTrue(r["capped_by_red_line"])
        self.assertEqual(r["verdict"], gs.CAPPED_VERDICT)
        self.assertIn("accounting_fraud_suspicion", r["triggered_red_lines"])

    def test_invalid_rating_raises(self):
        with self.assertRaises(ValueError):
            gs.score({"factors": {"revenue_growth_durability": 6}})


if __name__ == "__main__":
    unittest.main(verbosity=2)
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python ".claude/skills/growth-stock-judge/scripts/test_growth_scorecard.py"`
Expected: FAIL — `ModuleNotFoundError: No module named 'growth_scorecard'` (file not created yet).

- [ ] **Step 3: Write the implementation**

Create `.claude/skills/growth-stock-judge/scripts/growth_scorecard.py`:

```python
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
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python ".claude/skills/growth-stock-judge/scripts/test_growth_scorecard.py"`
Expected: `OK` — all 7 tests pass.

- [ ] **Step 5: Smoke-test the CLI**

Run: `python ".claude/skills/growth-stock-judge/scripts/growth_scorecard.py" --template`
Expected: JSON template printed with `factors`, `penalties`, `red_lines`, `evidence`, `what_could_weaken_view`.

- [ ] **Step 6: Commit**

```bash
git add ".claude/skills/growth-stock-judge/scripts/"
git commit -m "feat(growth-stock-judge): add scorecard with dual-axis and red-line cap"
```

---

## Task 3: Assets — input template, findings schema, report template

**Files:**
- Create: `.claude/skills/growth-stock-judge/assets/scorecard-input.json`
- Create: `.claude/skills/growth-stock-judge/assets/agent-findings-schema.json`
- Create: `.claude/skills/growth-stock-judge/assets/stock-verdict-template.md`

- [ ] **Step 1: Write `scorecard-input.json`** — must match the scorecard keys exactly (so it feeds `growth_scorecard.py` unchanged):

```json
{
  "ticker": "EXAMPLE",
  "company": "Example Co",
  "factors": {
    "revenue_growth_durability": 0,
    "tam_penetration": 0,
    "moat_chain_position": 0,
    "unit_economics_profit_path": 0,
    "product_customer_momentum": 0,
    "management_capital_allocation": 0,
    "valuation_growth_match": 0,
    "entry_expectations": 0
  },
  "penalties": {
    "dilution_financing": 0,
    "customer_concentration": 0,
    "accounting_quality": 0,
    "governance": 0,
    "competition_disruption": 0,
    "regulation_geopolitics": 0,
    "liquidity_bubble": 0,
    "lockup_insider_supply": 0
  },
  "red_lines": {
    "accounting_fraud_suspicion": false,
    "core_customer_loss": false,
    "growth_engine_broken": false
  },
  "evidence": [
    {"claim": "", "value": "", "source": "", "strength": "strong/medium/weak/needs_checking"}
  ],
  "what_could_weaken_view": ["", "", ""]
}
```

- [ ] **Step 2: Write `agent-findings-schema.json`** — the unified structure every research sub-agent returns to the synthesizer:

```json
{
  "module": "company_profile | earnings | growth | moat_economics | valuation | risk | positioning_options",
  "ticker": "",
  "summary": "one-line plain-language takeaway for this module",
  "findings": [
    {"claim": "", "value": "", "source": "", "strength": "strong | medium | weak | needs_checking"}
  ],
  "flags": [
    {"type": "red_flag | 利空", "detail": "", "severity": "low | medium | high | red_line", "date_window": ""}
  ],
  "needs_checking": [""],
  "suggested_factor_scores": {
    "revenue_growth_durability": null,
    "tam_penetration": null,
    "moat_chain_position": null,
    "unit_economics_profit_path": null,
    "product_customer_momentum": null,
    "management_capital_allocation": null,
    "valuation_growth_match": null,
    "entry_expectations": null
  },
  "suggested_penalties": {
    "dilution_financing": null,
    "customer_concentration": null,
    "accounting_quality": null,
    "governance": null,
    "competition_disruption": null,
    "regulation_geopolitics": null,
    "liquidity_bubble": null,
    "lockup_insider_supply": null
  },
  "suggested_red_lines": {
    "accounting_fraud_suspicion": false,
    "core_customer_loss": false,
    "growth_engine_broken": false
  }
}
```
(A sub-agent fills only the keys it owns; `null` means "not my module / no opinion".)

- [ ] **Step 3: Write `stock-verdict-template.md`** — the fixed 11-section report (spec §8). Use literal `{{placeholders}}` the synthesizer fills:

```markdown
# {{TICKER}}（{{COMPANY}}）成长股投资判断

## 结论
**{{VERDICT}}**　｜　信心：{{CONVICTION}}
质量分 {{QUALITY_SCORE}} / 买点分 {{ENTRY_SCORE}} / 总分 {{FINAL_SCORE}}
一句话：{{ONE_LINER}}

## 评分卡
{{SCORECARD_TABLE}}
红线状态：{{RED_LINE_STATUS}}

## 投资逻辑
{{THESIS}}

## 增长引擎 + 市场空间
{{GROWTH_AND_TAM}}

## 📊 最近财报重点
{{EARNINGS_READTHROUGH}}

## 护城河 / 产业链位置
{{MOAT}}

## 单位经济性 / 盈利路径
{{UNIT_ECONOMICS}}

## 估值与买点
{{VALUATION_ENTRY}}

## ⚠️ 风险与利空
### 结构性风险
{{STRUCTURAL_RISKS}}
### 资金面（解禁/增发/内部人卖出/降评级）
{{POSITIONING_RISKS}}
### 期权市场怎么看
{{OPTIONS_READ}}
### 下行情景
{{DOWNSIDE}}
### 什么情况说明判断错了（kill-switch）
{{KILL_SWITCHES}}

## 结论复述 + 下一步要核实 + 催化/日历
{{RECAP_AND_CALENDAR}}

## 证据与来源
{{EVIDENCE_LIST}}
```

- [ ] **Step 4: Validate the JSON files parse and match scorecard keys**

Run:
```bash
python -c "import json,sys; a=json.load(open('.claude/skills/growth-stock-judge/assets/scorecard-input.json',encoding='utf-8')); sys.path.insert(0,'.claude/skills/growth-stock-judge/scripts'); import growth_scorecard as gs; assert set(a['factors'])==set(gs.WEIGHTS); assert set(a['penalties'])==set(gs.PENALTY_KEYS); assert set(a['red_lines'])==set(gs.RED_LINE_KEYS); json.load(open('.claude/skills/growth-stock-judge/assets/agent-findings-schema.json',encoding='utf-8')); print('OK')"
```
Expected: `OK` (input template keys exactly match scorecard; both JSON files parse).

- [ ] **Step 5: Verify the template feeds the scorecard end-to-end**

Run: `python ".claude/skills/growth-stock-judge/scripts/growth_scorecard.py" ".claude/skills/growth-stock-judge/assets/scorecard-input.json" --format md`
Expected: a markdown scorecard with verdict `暂不值得 / 回避` (all-zero input).

- [ ] **Step 6: Commit**

```bash
git add ".claude/skills/growth-stock-judge/assets/"
git commit -m "feat(growth-stock-judge): add input template, findings schema, report template"
```

---

## Task 4: References — orchestration + agent roster

**Files:**
- Create: `.claude/skills/growth-stock-judge/references/orchestration.md`
- Create: `.claude/skills/growth-stock-judge/references/agent-roster.md`

- [ ] **Step 1: Write `orchestration.md`** (spec §4.1). Required sections, in order:
  1. `# 多 agent 编排` — one-paragraph overview of fan-out → synthesize.
  2. `## 执行步骤` — numbered: (a) parse ticker; (b) dispatch the 7 research sub-agents **in parallel**, independent, each does its own web research; (c) each returns the `assets/agent-findings-schema.json` structure; (d) **barrier** — wait for all; (e) `judge-synthesizer` merges, runs `growth_scorecard.py`, writes the report.
  3. `## 子代理失败处理` — if a sub-agent fails or data is thin, mark that module 待核实 in the report, do not block the verdict; if a red line is found, cap per scorecard.
  4. `## 可移植性与兜底` — generic Task/Agent dispatch; optional mapping to OMC (`oh-my-claudecode:explore/analyst/quality-reviewer`) or superpowers `dispatching-parallel-agents`; **single-agent sequential execution is the fallback** when no multi-agent capability exists.
  5. `## I/O 契约` — point to `assets/agent-findings-schema.json`; state that the synthesizer reconciles overlapping `suggested_factor_scores` by preferring stronger evidence.

- [ ] **Step 2: Write `agent-roster.md`**. One `##` block per agent. For each: **Mission**, **拥有的模块/流程步骤**, **取证重点**, **回传字段 (which factor/penalty/red_line keys it owns)**, **证据要求**. The 7 research agents + 1 synthesizer (mapping from spec §4.1 table):

| agent | owns factor keys | owns penalty/red-line keys |
|---|---|---|
| `company-profiler` | (context only) | — |
| `earnings-analyst` | product_customer_momentum, management_capital_allocation | accounting_quality; growth_engine_broken |
| `growth-analyst` | revenue_growth_durability, tam_penetration, product_customer_momentum | — |
| `moat-economics-analyst` | moat_chain_position, unit_economics_profit_path | competition_disruption |
| `valuation-analyst` | valuation_growth_match, entry_expectations | liquidity_bubble |
| `risk-analyst` | — | customer_concentration, governance, regulation_geopolitics; accounting_fraud_suspicion, core_customer_loss |
| `positioning-options-analyst` | entry_expectations (price/expectations context) | dilution_financing, lockup_insider_supply |
| `judge-synthesizer` | reconciles all, runs scorecard, writes report | — |

State explicitly: overlapping keys (e.g. `product_customer_momentum`, `entry_expectations`) are reconciled by the synthesizer using the higher-evidence input.

- [ ] **Step 3: Verify factor/penalty key references are valid**

Run:
```bash
python -c "import sys; sys.path.insert(0,'.claude/skills/growth-stock-judge/scripts'); import growth_scorecard as gs; t=open('.claude/skills/growth-stock-judge/references/agent-roster.md',encoding='utf-8').read(); missing=[k for k in list(gs.WEIGHTS)+gs.PENALTY_KEYS+gs.RED_LINE_KEYS if k not in t]; print('MISSING:',missing if missing else 'none — all keys referenced')"
```
Expected: `MISSING: none — all keys referenced` (every scorecard key is assigned to some agent).

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/references/orchestration.md" ".claude/skills/growth-stock-judge/references/agent-roster.md"
git commit -m "feat(growth-stock-judge): add orchestration and agent-roster references"
```

---

## Task 5: References — workflow + scoring rubric

**Files:**
- Create: `.claude/skills/growth-stock-judge/references/growth-analysis-workflow.md`
- Create: `.claude/skills/growth-stock-judge/references/growth-scoring-rubric.md`

- [ ] **Step 1: Write `growth-analysis-workflow.md`** — the detailed 10-step single-stock workflow (spec §4), one `##` per step (锁定公司 / 最近财报深读 / 增长引擎 / 市场空间 / 护城河+产业链 / 单位经济性 / 估值与买点 / 风险与利空扫描 / 证据分级+反方 / 打分出结论). Each step lists concrete questions to answer + which reference to read next. Include the rule: 现价/现状/最新财报必须联网查证，拿不到标"待核实"并给查证路径. For 护城河 step, point to serenity's scarce-layer thinking with fallback note.

- [ ] **Step 2: Write `growth-scoring-rubric.md`** — 0-5 anchors. Add a TOC at top (file will exceed 100 lines). For **each of the 8 factors**, give what a 0, 3, and 5 look like (concrete, growth-investing framed). Then a `## 惩罚项判分` section: for each of the 8 penalty keys, what rating 0 vs 3 vs 5 means. Then `## 红线 (kill-switch)` section: the exact condition that sets each of `accounting_fraud_suspicion`, `core_customer_loss`, `growth_engine_broken` to true. Factor/penalty/red-line key names must match `growth_scorecard.py` exactly.

- [ ] **Step 3: Verify rubric covers every scorecard key**

Run:
```bash
python -c "import sys; sys.path.insert(0,'.claude/skills/growth-stock-judge/scripts'); import growth_scorecard as gs; t=open('.claude/skills/growth-stock-judge/references/growth-scoring-rubric.md',encoding='utf-8').read(); missing=[k for k in list(gs.WEIGHTS)+gs.PENALTY_KEYS+gs.RED_LINE_KEYS if k not in t]; print('MISSING:',missing if missing else 'none')"
```
Expected: `MISSING: none`.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/references/growth-analysis-workflow.md" ".claude/skills/growth-stock-judge/references/growth-scoring-rubric.md"
git commit -m "feat(growth-stock-judge): add workflow and scoring-rubric references"
```

---

## Task 6: Reference — earnings read-through checklist

**Files:**
- Create: `.claude/skills/growth-stock-judge/references/earnings-readthrough.md`

- [ ] **Step 1: Write the file** — the 8-block latest-earnings checklist (spec §6), TOC at top, one `##` per block: ①增长实绩 ②指引 ③核心产品与研发进展 ④盈利与单位经济性 ⑤客户与势能 ⑥资本配置 ⑦电话会弦外之音与红旗 ⑧财报后反应. Each block = a bullet checklist of exactly what to extract. Include the scoring linkage note: 指引上调→revenue_growth_durability 加分; 指引下修→growth_engine_broken 红线判断 + penalty. Sources line: latest 10-Q/10-K + earnings call transcript + investor presentation (strong evidence).

- [ ] **Step 2: Verify structure**

Run: `grep -c "^## " ".claude/skills/growth-stock-judge/references/earnings-readthrough.md"`
Expected: `8` (eight blocks).

- [ ] **Step 3: Commit**

```bash
git add ".claude/skills/growth-stock-judge/references/earnings-readthrough.md"
git commit -m "feat(growth-stock-judge): add earnings read-through checklist"
```

---

## Task 7: Reference — valuation and entry

**Files:**
- Create: `.claude/skills/growth-stock-judge/references/valuation-and-entry.md`

- [ ] **Step 1: Write the file** (spec §4 step 7 + §5.1 entry factors). Sections:
  1. `## 估值方法（成长股）` — P/S vs growth, PEG-style, EV/Sales, Rule-of-40, vs own history, vs peers, implied-expectations / reverse-DCF intuition.
  2. `## 买点 / 预期面` — distance to consensus, expectations bar (是否已被 price-in), recent reset, what the market is paying for.
  3. `## 如何映射到评分` — how these map to `valuation_growth_match` and `entry_expectations` 0-5 (defer anchors to growth-scoring-rubric.md; cross-link).
  4. `## 数据获取` — where to find each metric online; mark hard-to-get as 待核实 with a source path.

- [ ] **Step 2: Verify it references both entry factor keys**

Run: `grep -E "valuation_growth_match|entry_expectations" ".claude/skills/growth-stock-judge/references/valuation-and-entry.md"`
Expected: both keys appear.

- [ ] **Step 3: Commit**

```bash
git add ".claude/skills/growth-stock-judge/references/valuation-and-entry.md"
git commit -m "feat(growth-stock-judge): add valuation-and-entry reference"
```

---

## Task 8: References — risk/bear-case + positioning/options

**Files:**
- Create: `.claude/skills/growth-stock-judge/references/risk-and-bear-case.md`
- Create: `.claude/skills/growth-stock-judge/references/positioning-and-options.md`

- [ ] **Step 1: Write `risk-and-bear-case.md`** (spec §7). Sections:
  1. `## 风险 vs 利空` — define both (structural vs near-term catalyst).
  2. `## 利空类别扫描` — 业绩/指引利空; 估值杀; 竞争与技术颠覆; 客户流失/集中度; 监管/地缘/政策; 会计与治理红旗; 宏观/流动性. Map each to a penalty key.
  3. `## 红线 (kill-switch) 标准` — exact triggers for `accounting_fraud_suspicion`, `core_customer_loss`, `growth_engine_broken`, and that any trigger caps the verdict.
  4. `## 下行情景` — how to sketch the downside (logic + valuation floor).
  5. Reuse note: 沿用 serenity `risk-and-compliance.md`; fallback = inline compliance summary.

- [ ] **Step 2: Write `positioning-and-options.md`** (spec §7.2–7.4). TOC at top. Sections:
  1. `## 供给与筹码面` — 解禁日 (date/size/who); 增发/ATM/S-3; 内部人卖出 (Form 4, 10b5-1, cluster); 机构降评级/13F 减持; 回购 vs 稀释净额. Map to `dilution_financing` + `lockup_insider_supply`.
  2. `## 期权市场解读` — IV + IV percentile; earnings expected move; put/call; skew; OI/max pain; unusual activity (lead only); term structure.
  3. `## 证据分级` — these are 中/弱 evidence (sentiment/positioning), not core-verdict drivers; if data unavailable, mark 待核实 with source path.
  4. `## 数据源` — EDGAR Form 4 / S-3, exchange lockup calendars, options data sources.

- [ ] **Step 3: Verify both files reference their penalty keys**

Run:
```bash
grep -E "dilution_financing|lockup_insider_supply" ".claude/skills/growth-stock-judge/references/positioning-and-options.md" && grep -E "accounting_fraud_suspicion|core_customer_loss|growth_engine_broken" ".claude/skills/growth-stock-judge/references/risk-and-bear-case.md"
```
Expected: matches in both files.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/references/risk-and-bear-case.md" ".claude/skills/growth-stock-judge/references/positioning-and-options.md"
git commit -m "feat(growth-stock-judge): add risk/bear-case and positioning/options references"
```

---

## Task 9: SKILL.md (frontmatter + body)

**Files:**
- Create: `.claude/skills/growth-stock-judge/SKILL.md`

- [ ] **Step 1: Write the frontmatter** (spec §12.1). The `description` must be "pushy" and cover Chinese + English triggers:

```markdown
---
name: growth-stock-judge
description: Judge whether a specific US stock is worth investing in, through a growth-investing lens, and return a verdict-first report (worth investing / watch / avoid) backed by a multi-agent research workflow, a quantitative scorecard, a latest-earnings deep-read, and a risk/利空 module (lockups, offerings, insider selling, downgrades, options-market read). Use this skill whenever the user gives a US ticker or company and asks if it is worth buying/investing, e.g. "NVDA 值得投资吗", "帮我分析特斯拉现在能不能买", "判断这只美股值不值得投", "should I buy NVDA", "is TSLA worth investing", "analyze this US stock" — even if they don't say "analyze". For multi-stock theme/supply-chain screening, defer to serenity-skill instead.
license: MIT
compatibility: Best with web/search tools for live filings, transcripts, prices, and estimates. Multi-agent dispatch is an accelerator; single-agent sequential execution is a supported fallback. Bundled script is local-only Python 3 (stdlib).
metadata:
  version: "1.0.0"
  short-description: US growth-stock single-name investment judgment
---
```

- [ ] **Step 2: Write the body** (keep total file < 500 lines; push detail to references). Required sections:
  1. `# growth-stock-judge` + one-paragraph promise (verdict-first growth judgment for one US ticker).
  2. `## 何时用 / 何时让位` — single-stock judgment here; theme screening → serenity.
  3. `## 执行模式（多 agent 编排）` — short summary; point to `references/orchestration.md` and `references/agent-roster.md`; state the single-agent fallback.
  4. `## 研究工作流` — the 10-step skeleton; point to `references/growth-analysis-workflow.md`; call out the latest-earnings deep-read (`references/earnings-readthrough.md`) and risk module (`references/risk-and-bear-case.md`, `references/positioning-and-options.md`).
  5. `## 评分与结论` — summarize the 8 factors + weights, dual-axis, penalties, red-line cap, verdict bands (spec §5); instruct to run `scripts/growth_scorecard.py` with `assets/scorecard-input.json`; point to `references/growth-scoring-rubric.md` for anchors.
  6. `## 输出契约` — use `assets/stock-verdict-template.md`, 结论先行; every claim labeled 强/中/弱/待核实; example one-liner from spec §8.
  7. `## 证据与合规` — never invent numbers; current facts must be searched, not recalled; research conviction only, trade decision is the user's; reuse serenity `evidence-ladder.md` / `risk-and-compliance.md` with inline fallback.
  8. `## 兜底` — what to do when serenity references are absent / no web tools / no multi-agent capability.

- [ ] **Step 3: Verify line count and that referenced files exist**

Run:
```bash
wc -l ".claude/skills/growth-stock-judge/SKILL.md"
```
Expected: under 500.

Run:
```bash
python -c "import re,os; b='.claude/skills/growth-stock-judge/'; t=open(b+'SKILL.md',encoding='utf-8').read(); refs=set(re.findall(r'(?:references|assets|scripts|examples|agents)/[A-Za-z0-9._-]+', t)); missing=[r for r in refs if not os.path.exists(b+r)]; print('MISSING:', missing if missing else 'none — all referenced files exist')"
```
Expected: `MISSING: none — all referenced files exist`.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/SKILL.md"
git commit -m "feat(growth-stock-judge): add SKILL.md"
```

---

## Task 10: agents/openai.yaml (interface manifest)

**Files:**
- Create: `.claude/skills/growth-stock-judge/agents/openai.yaml`

- [ ] **Step 1: Write the manifest** (mirror serenity's format):

```yaml
interface:
  display_name: "Growth Stock Judge"
  short_description: "Judges whether a specific US growth stock is worth investing in"
  brand_color: "#0B5FFF"
  default_prompt: "Use growth-stock-judge to analyze a US ticker through a growth-investing lens and return a verdict-first judgment: is it worth investing now, with a scorecard, latest-earnings read, and risk/利空 (lockups, offerings, insider selling, downgrades, options) section."
policy:
  allow_implicit_invocation: true
dependencies:
  tools: []
```

- [ ] **Step 2: Verify YAML parses**

Run: `python -c "import yaml; yaml.safe_load(open('.claude/skills/growth-stock-judge/agents/openai.yaml',encoding='utf-8')); print('OK')"`
Expected: `OK`. (If PyYAML is missing, instead run `python -c "print(open('.claude/skills/growth-stock-judge/agents/openai.yaml',encoding='utf-8').read())"` and eyeball the structure against serenity's.)

- [ ] **Step 3: Commit**

```bash
git add ".claude/skills/growth-stock-judge/agents/openai.yaml"
git commit -m "feat(growth-stock-judge): add Agent Skills interface manifest"
```

---

## Task 11: examples/spcx-demo.md (SPCX worked example)

**Files:**
- Create: `.claude/skills/growth-stock-judge/examples/spcx-demo.md`

- [ ] **Step 1: Resolve the ticker first.** The example must not present fabricated data as real (spec §3 note). Determine via web search what `SPCX` is and whether it is a tradeable US stock.
  - If `SPCX` is a live, tradeable US stock with public financials: build the example from real, sourced data, labeled with evidence strengths.
  - If `SPCX` is not tradeable / data is insufficient (e.g. maps to a private company like SpaceX): put a bold banner at the top — `> 形态演示 / illustrative shape — 数字仅示意，非真实结论` — and fill the template with clearly-illustrative values.

- [ ] **Step 2: Write the example** following `assets/stock-verdict-template.md` end to end: a filled scorecard JSON, the `growth_scorecard.py` output, and the full 11-section report. Show the dual-axis verdict pattern (e.g. good company / pricey entry) so it teaches the output shape. Include at least one 待核实 item and one risk/利空 entry with a date window.

- [ ] **Step 3: Verify the example's embedded scorecard JSON actually scores.** Extract the JSON block to a temp file and run it:

Run: `python ".claude/skills/growth-stock-judge/scripts/growth_scorecard.py" /tmp/spcx-scorecard.json --format md`
Expected: a scorecard whose verdict matches the verdict written in the example's 结论 section (internal consistency).

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/examples/spcx-demo.md"
git commit -m "docs(growth-stock-judge): add SPCX worked example"
```

---

## Task 12: evals (evals.json + test-cases.md)

**Files:**
- Create: `.claude/skills/growth-stock-judge/evals/evals.json`
- Create: `.claude/skills/growth-stock-judge/evals/test-cases.md`

- [ ] **Step 1: Write `evals.json`** (skill-creator format — prompts now, assertions included):

```json
{
  "skill_name": "growth-stock-judge",
  "evals": [
    {
      "id": 1,
      "prompt": "NVDA 现在还值得投资吗？帮我判断一下",
      "expected_output": "Verdict-first growth judgment for NVDA: a clear 值得投资/观望/回避 line, dual-axis quality/entry scores, a scorecard, a latest-earnings read, and a 风险与利空 section (incl. 资金面 + 期权). Claims labeled 强/中/弱/待核实.",
      "files": [],
      "assertions": [
        "Output leads with an explicit verdict (值得投资 / 观望 / 回避 or 强信心值得投资).",
        "Includes a scorecard with the 8 factors and a dual-axis (质量分 + 买点分).",
        "Has a 最近财报 section covering growth + guidance.",
        "Has a 风险与利空 section that includes 资金面 (解禁/增发/内部人卖出/降评级) and an 期权市场 read.",
        "Claims carry evidence labels (强/中/弱/待核实); no invented exact figures presented as fact."
      ]
    },
    {
      "id": 2,
      "prompt": "I'm thinking about buying Tesla. Is TSLA worth investing in right now?",
      "expected_output": "Same verdict-first growth report for TSLA, responding in the user's language (English here), with valuation/entry factored into the verdict.",
      "files": [],
      "assertions": [
        "Responds in English (matches user's language).",
        "Verdict reflects BOTH business quality AND current valuation/entry (dual-axis).",
        "Includes risk/利空 section and a kill-switch / what-would-change-my-mind list."
      ]
    },
    {
      "id": 3,
      "prompt": "美股 AI 半导体这个赛道，哪几家最值得研究？",
      "expected_output": "This is a multi-stock theme scan, NOT single-stock judgment — growth-stock-judge should defer to serenity-skill rather than produce a single-name verdict.",
      "files": [],
      "assertions": [
        "Does NOT force a single-stock scorecard verdict on a whole sector.",
        "Defers to / hands off to serenity-skill for theme screening, or asks which specific ticker to judge."
      ]
    }
  ]
}
```

- [ ] **Step 2: Write `test-cases.md`** — human-readable mirror: 触发测试, 行为测试, 编排测试 (spec §10). Bullet checklist form.

- [ ] **Step 3: Validate evals.json parses**

Run: `python -c "import json; d=json.load(open('.claude/skills/growth-stock-judge/evals/evals.json',encoding='utf-8')); assert len(d['evals'])>=3; print('OK', len(d['evals']),'evals')"`
Expected: `OK 3 evals`.

- [ ] **Step 4: Commit**

```bash
git add ".claude/skills/growth-stock-judge/evals/"
git commit -m "test(growth-stock-judge): add eval set and test-case checklist"
```

---

## Task 13: Whole-skill validation

**Files:**
- Modify: none (validation only)

- [ ] **Step 1: Run serenity's structural validator against the new skill (if present)**

Run: `python ".claude/skills/serenity-skill/scripts/validate_skill.py" ".claude/skills/growth-stock-judge"`
Expected: PASS, or a clear list of structural issues to fix. (If the validator hard-codes serenity paths and errors, skip and rely on Step 2.)

- [ ] **Step 2: Run the full validation sweep**

Run:
```bash
python - <<'PY'
import json, os, re, sys
b = ".claude/skills/growth-stock-judge/"
sys.path.insert(0, b + "scripts")
import growth_scorecard as gs

# scorecard tests
import subprocess
r = subprocess.run([sys.executable, b+"scripts/test_growth_scorecard.py"], capture_output=True, text=True)
assert r.returncode == 0, r.stderr

# JSON files parse + key alignment
inp = json.load(open(b+"assets/scorecard-input.json", encoding="utf-8"))
assert set(inp["factors"]) == set(gs.WEIGHTS)
assert set(inp["penalties"]) == set(gs.PENALTY_KEYS)
assert set(inp["red_lines"]) == set(gs.RED_LINE_KEYS)
json.load(open(b+"assets/agent-findings-schema.json", encoding="utf-8"))
ev = json.load(open(b+"evals/evals.json", encoding="utf-8"))
assert len(ev["evals"]) >= 3

# required files exist
required = ["SKILL.md","agents/openai.yaml","scripts/growth_scorecard.py",
    "references/orchestration.md","references/agent-roster.md",
    "references/growth-analysis-workflow.md","references/growth-scoring-rubric.md",
    "references/earnings-readthrough.md","references/valuation-and-entry.md",
    "references/risk-and-bear-case.md","references/positioning-and-options.md",
    "assets/scorecard-input.json","assets/agent-findings-schema.json",
    "assets/stock-verdict-template.md","examples/spcx-demo.md",
    "evals/evals.json","evals/test-cases.md"]
missing = [f for f in required if not os.path.exists(b+f)]
assert not missing, f"missing files: {missing}"

# SKILL.md under 500 lines and frontmatter present
skill = open(b+"SKILL.md", encoding="utf-8").read()
assert skill.startswith("---"), "SKILL.md missing frontmatter"
assert "name: growth-stock-judge" in skill
assert len(skill.splitlines()) < 500

# every scorecard key referenced somewhere in references
alltext = "".join(open(b+"references/"+f, encoding="utf-8").read() for f in os.listdir(b+"references"))
unref = [k for k in list(gs.WEIGHTS)+gs.PENALTY_KEYS+gs.RED_LINE_KEYS if k not in alltext]
assert not unref, f"keys not documented in references: {unref}"

print("ALL CHECKS PASSED")
PY
```
Expected: `ALL CHECKS PASSED`.

- [ ] **Step 3: Commit (if Step 1/2 required any fixes)**

```bash
git add ".claude/skills/growth-stock-judge/"
git commit -m "fix(growth-stock-judge): address validation findings"
```
(If nothing changed, skip this commit.)

---

## Task 14: skill-creator eval loop, description optimization, packaging (optional, deferred)

This task runs the `skill-creator` quality loop. It is **optional** and can be deferred until the static skill is reviewed by the user. Do not start it without confirming the user wants the full eval run (it spawns subagents and is token-heavy).

- [ ] **Step 1:** Re-enter the `skill-creator` skill and run the test cases from `evals/evals.json` (with-skill vs baseline), one subagent each, per skill-creator's "Running and evaluating test cases".
- [ ] **Step 2:** Generate the eval viewer with `eval-viewer/generate_review.py` and have the user review outputs + benchmark.
- [ ] **Step 3:** Iterate the skill on feedback; rerun.
- [ ] **Step 4:** Run description optimization (`scripts.run_loop`) using the current session's model id; apply `best_description` to SKILL.md frontmatter.
- [ ] **Step 5:** Package with `python -m scripts.package_skill ".claude/skills/growth-stock-judge"` and hand the `.skill` file to the user.

---

## Self-Review (completed by plan author)

**Spec coverage** — every spec section maps to a task:
- §1 目标/范围 → SKILL.md (Task 9), description (Task 9 Step 1)
- §2 与 serenity 分工 → SKILL.md §何时让位 (Task 9), reuse notes (Tasks 4/8/9)
- §3 文件结构 → Tasks 1–12 (every file)
- §4 研究流程 + §4.1 编排 → Tasks 4, 5, 9
- §5 评分卡（因子/权重/惩罚/红线/双轴/分档） → Task 2 (code + tests), Task 5 (rubric)
- §6 财报深读 → Task 6
- §7 风险与利空（含筹码面+期权） → Task 8
- §8 输出报告结构 → Task 3 (template), Task 9 (output contract)
- §9 合规与语言 → Task 9 §证据与合规
- §10 测试用例 → Task 12
- §11 复用 serenity 对接点 → Tasks 4/8/9 reuse notes + Task 13 validator
- §12 skill-creator 合规 → frontmatter (Task 9), evals.json (Task 12), Task 14

**Placeholder scan** — code steps (Task 2, Task 3 JSON) contain full content; doc tasks specify exact sections/headings + acceptance checks rather than vague "add content"; report template uses intentional `{{placeholders}}` filled at runtime (not plan placeholders).

**Type/key consistency** — factor keys, penalty keys, red-line keys are defined once in `growth_scorecard.py` (Task 2) and every later task that names them (assets Task 3, roster Task 4, rubric Task 5, references Tasks 6–8) is followed by a grep/python check that the names match the script exactly. Verdict-band strings ("强信心值得投资" / "值得投资" / "观望 / 建仓试探" / "暂不值得 / 回避" / CAPPED_VERDICT) are defined in the script and asserted in tests.
