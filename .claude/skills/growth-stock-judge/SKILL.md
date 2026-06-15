---
name: growth-stock-judge
description: Judge whether a specific US stock is worth investing in, through a growth-investing lens, and return a verdict-first report (worth investing / watch / avoid) backed by a multi-agent research workflow, a quantitative scorecard, a latest-earnings deep-read, and a risk/利空 module (lockups, offerings, insider selling, downgrades, options-market read). Use this skill whenever the user gives a US ticker or company and asks if it is worth buying/investing, e.g. "NVDA 值得投资吗", "帮我分析特斯拉现在能不能买", "判断这只美股值不值得投", "should I buy NVDA", "is TSLA worth investing", "analyze this US stock" — even if they don't say "analyze". For multi-stock theme/supply-chain screening, defer to serenity-skill instead.
license: MIT
compatibility: Best with web/search tools for live filings, transcripts, prices, and estimates. Multi-agent dispatch is an accelerator; single-agent sequential execution is a supported fallback. Bundled script is local-only Python 3 (stdlib).
metadata:
  version: "1.0.0"
  short-description: US growth-stock single-name investment judgment
---

# growth-stock-judge

Give one US ticker, get one verdict. This skill takes a single US stock and returns a **verdict-first growth-investing judgment** — 值得投资 / 观望 / 回避 — for *this name, at this price, right now*. The verdict carries two axes at once: how good the business is (质量) and whether the current entry is cheap or expensive (买点). Behind the verdict sit a multi-agent research workflow, a quantitative scorecard with a red-line kill-switch, a deep read of the latest earnings, and a risk/利空 module that covers lockups, offerings, insider selling, downgrades, and an options-market read. Lead with the call; back every claim with sourced evidence; say plainly which facts still need checking.

## 何时用 / 何时让位

- **用本 skill**：用户给一个具体美股代码或公司，问"现在该不该投 / 值不值得买 / 能不能买"。这是单股深度判断，输出一个结论。
- **让位给 serenity-skill**：用户问的是赛道/主题/供应链层面"哪几家最值得研究"、要做多股筛选与排名（如"美股 AI 半导体哪几家最值得看"）。那是 *where in the chain*，不是 *is this one name worth it now* — 交给 `serenity-skill`，或先反问用户具体要判断哪一只。
- 介于两者之间（给了一篮子股票要对比）时：可逐只用本 skill 的评分卡，但若用户其实想要赛道排名，引导到 serenity。

Why: 两个 skill 是搭档。serenity 找"哪一层卡脖子、谁离稀缺层最近"；本 skill 判"这只票现在该不该投"。强行用单股评分卡去裁决整个赛道会得到误导性结论。

## 执行模式（多 agent 编排）

执行模式是 **fan-out → synthesize**：编排者并行分派 7 个研究子代理，每个只负责一个模块、独立联网取证、回传统一结构的结论；最后由综合代理 barrier 汇总、跑评分卡、写报告。

- 7 个研究子代理：`company-profiler` / `earnings-analyst` / `growth-analyst` / `moat-economics-analyst` / `valuation-analyst` / `risk-analyst` / `positioning-options-analyst`。
- 综合代理：`judge-synthesizer`（汇总 → 运行 `scripts/growth_scorecard.py` → 红线判定 → 写"结论先行"报告）。
- 统一回传结构见 `assets/agent-findings-schema.json`。
- 分派/并行/barrier/失败处理与 I/O 契约的细节读 `references/orchestration.md`；每个子代理的 mission、负责的因子/惩罚/红线 key、取证要求读 `references/agent-roster.md`。

**单 agent 兜底**：若当前环境没有多 agent 能力，按 `references/growth-analysis-workflow.md` 的 10 步**顺序**自己跑一遍，逐模块联网取证，再汇总打分。多 agent 只是加速器，不是前置条件。Why: 保证无论宿主有没有并行分派能力，skill 都能完整出结论。

## 研究工作流

给定一个美股代码后，按这 10 步研究（多 agent 模式下各模块由对应子代理并行承担；单 agent 模式下顺序执行）。每一步要回答的具体问题、要读哪个 reference，见 `references/growth-analysis-workflow.md`。

1. **锁定公司** — 业务、收入结构、所处赛道与产业链位置。
2. **最近一次财报深读** — 最新鲜最硬的证据，靠前做。逐项 checklist 读 `references/earnings-readthrough.md`。
3. **增长引擎** — 收入增速及趋势、驱动因素、增长可持续性。
4. **市场空间** — TAM、渗透率、还有多长跑道。
5. **护城河 / 产业链位置** — 借 serenity 的"稀缺层/卡点"思路判竞争壁垒。
6. **单位经济性 / 盈利路径** — 毛利、经营杠杆、FCF 趋势、未来能不能赚钱。
7. **估值与买点** — P/S、PEG 类、对比历史/同业、隐含预期；现价合不合理。方法读 `references/valuation-and-entry.md`。
8. **风险与利空扫描** — 结构性风险读 `references/risk-and-bear-case.md`；资金面（解禁/增发/内部人卖出/降评级）+ 期权市场解读读 `references/positioning-and-options.md`。
9. **证据分级 + 反方** — 每个关键结论标 强/中/弱/待核实；列"什么情况说明判断错了"。
10. **打分出结论** — 跑评分卡（见下节）。

铁律：现价、现状、最新财报**必须联网查证，不靠记忆**；**有明确源路径（10-Q/10-K/8-K、IR 等）的项必须去查、查到就写进正文**，"待核实"只留给真正取不到的（实时期权 IV、未来才发生的事、非公开数据）——报告里的"待核实"清单应当很短。Why: 把记忆当事实、或把能查到的数据当 TODO 甩出去，是这类判断最常见也最危险的错误。

## 评分与结论

评分卡（`scripts/growth_scorecard.py`）：8 个因子各 0-5 分 × 权重（合计 100），减惩罚项（×2 倍率），再红线封顶。

**因子与权重**（前 6 项 = 质量分共 80，后 2 项 = 买点分共 20）：

| 因子 key | 权重 | 轴 |
|---|---:|---|
| `revenue_growth_durability` 收入增速与持续性 | 18 | 质量 |
| `tam_penetration` 市场空间 / 渗透率 | 14 | 质量 |
| `moat_chain_position` 护城河 / 产业链位置 | 14 | 质量 |
| `unit_economics_profit_path` 单位经济性 / 盈利路径 | 14 | 质量 |
| `product_customer_momentum` 产品与客户势能 | 12 | 质量 |
| `management_capital_allocation` 管理层与资本配置 | 8 | 质量 |
| `valuation_growth_match` 估值与增长匹配度 | 12 | 买点 |
| `entry_expectations` 买点 / 预期面 | 8 | 买点 |

- **双轴**：质量分（前 6 项）+ 买点分（后 2 项）。于是能给出"好公司但偏贵 → 观望/分批"这类细腻判断。买点占 20 分：价格能影响结论，但不会单凭"贵"就否掉一家好公司。
- **惩罚项**（×2）：`dilution_financing` / `customer_concentration` / `accounting_quality` / `governance` / `competition_disruption` / `regulation_geopolitics` / `liquidity_bubble` / `lockup_insider_supply`。
- **红线（kill-switch）封顶**：`accounting_fraud_suspicion` / `core_customer_loss` / `growth_engine_broken` 任一触发 → 结论封顶为"回避 / 观望（红线封顶）"，无论原始分多高。Why: 不让高分掩盖致命问题。
- **结论分档**：≥85 强信心值得投资；70-84 值得投资；55-69 观望 / 建仓试探；<55 暂不值得 / 回避。

跑法：把各模块判分填进 `assets/scorecard-input.json`（key 与脚本一一对应），运行
`python scripts/growth_scorecard.py assets/scorecard-input.json --format both`
得到总分、质量分、买点分、红线状态。每个因子/惩罚/红线 0-5 分的判分锚点读 `references/growth-scoring-rubric.md`。

## 输出契约

用 `assets/stock-verdict-template.md` 的固定 11 节结构出报告，**结论先行**：

1. 结论框（一句话结论 + 信心 + 双轴 + 总分）2. 评分卡表 3. 投资逻辑 4. 增长引擎+市场空间 5. 📊 最近财报重点 6. 护城河/产业链位置 7. 单位经济性/盈利路径 8. 估值与买点 9. ⚠️ 风险与利空（结构性 → 资金面 → 期权市场怎么看 → 下行情景 → kill-switch 清单）10. 结论复述+下一步要核实+催化/日历 11. 证据与来源。

- 每条关键结论标证据等级：**强 / 中 / 弱 / 待核实**；**第 11 节证据与来源尽量给可点击超链接** `[来源名](URL)`（SEC 文件、公司 IR、原始报道），便于用户一键核查与拓展阅读。
- **第 10 节催化 / 日历要排密**：按时间列出所有适用事件类型（下次财报 / 产品发布量产 / 行业大会·投资者日 / 解禁·增发·回购 / 大客户与上下游 capex 指引 / 监管·政策 / 竞品 / 分析师评级 / 指数纳入 / 宏观 / 重大合同·投票），每条标日期或"待核实"，别只写"下次财报"。事件类型清单见 `references/earnings-readthrough.md` 末尾。
- 结论框示例（双轴口径）：*"好公司，但当前偏贵 → 观望 / 分批；质量 82 / 买点 48 / 总分 71"*。
- 用用户的语言作答（默认中文；英文提问就用英文）；大白话，少术语。

## 证据与合规

- **研究判断，不替用户下单**：结论是研究信心（值得投 / 观望 / 回避），交易决定在用户手里。不用"保证收益 / 必涨"措辞。
- **绝不编造**价格、财报数字、来源；现价/现状/最新财报必须联网查，不靠记忆；拿不到的数据标"待核实"并给查证路径。
- **证据分级与合规边界**复用 serenity 的 evidence-ladder 与 risk-and-compliance 文档（在 serenity-skill 的 references 目录下，按需引用，不复制）。若 serenity 不在场，用下面的兜底。

**精简证据分级（兜底）**：强 = 一手 SEC 文件 / 财报 transcript / 业绩 PPT / 官方公告；中 = 可信媒体、行业报告、卖方分析、期权/筹码面情绪信号；弱 = 社媒/KOL/传闻（仅作 lead）；待核实 = 当前未联网取证。期权与资金面属情绪/持仓面，定为中/弱证据，辅助买点与风险，不作核心结论主驱动。

**精简合规（兜底）**：只做公开材料的研究与推理；不下买卖指令、不承诺收益、不基于传闻推荐、不使用任何非公开重大信息。最终责任在用户。

## 兜底

- **无 serenity references**：用上一节内联的精简证据分级与合规说明；护城河/产业链判断按 `references/growth-analysis-workflow.md` 第 5 步内的稀缺层说明走。
- **无 web/search 工具**：把所有依赖现价/现状/最新数据的结论标"待核实"，并在报告里给出确切查证路径（EDGAR 10-Q/10-K、财报 transcript、Form 4/S-3、交易所解禁日历、期权数据源），不要用记忆里的旧数字冒充事实。
- **无多 agent 能力**：单 agent 按 10 步工作流顺序自跑（见上文"执行模式"），照样跑评分卡出结论。
- **某模块数据不足/子代理失败**：在报告中把该模块标"待核实"，不阻塞整体结论；若该模块命中红线，按红线封顶。
