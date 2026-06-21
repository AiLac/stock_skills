---
name: growth-stock-judge
description: Judge whether one specific US stock is worth investing in right now, through a growth-investing lens, returning a verdict-first report (值得投资 / 观望 / 回避 — worth / watch / avoid) backed by a multi-agent research workflow, a quantitative scorecard, a latest-earnings deep-read, and a risk/利空 module (lockups, offerings, insider selling, analyst downgrades, options-market read). Use it whenever the user names a US ticker or company and asks — in any phrasing — whether to buy, add, hold, or how to judge the 买点/entry — e.g. "NVDA 现在还值得买吗", "判断下 RKLB 能不能投/该不该建仓", "加仓 AMD 值不值得", "should I buy PLTR now or wait", "is TSLA worth owning", "start a position in SHOP?", "analyze this US stock" — even if they don't say "analyze" or "invest". NOT for multi-stock theme/sector or supply-chain screening (那是 serenity-skill), nor portfolio/ETF allocation, market/macro news, or translation/coding tasks that merely mention a ticker.
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

执行模式是 **fan-out → synthesize**：把这只股票的研究拆成 8 个互相独立的模块，**在同一条消息里一次性并行分派 8 个研究子代理**，每个只负责一个模块、独立联网取证、回传统一结构的结论；8 个全部返回后（barrier）再由综合代理汇总、跑评分卡、写报告。

### ⛓️ 并行分派协议（硬性 · 触发后第一个动作）

触发本 skill 后，**你的第一个动作（first turn）就是 fan-out**——不要先自己上网搜、不要先逐个读 reference、不要"先试一个看看"。照这 5 步走：

1. **一条消息 · 8 个调用 · 同时发出**：在**同一个回合（one assistant message / single turn）**里，用你的并行子代理工具——Claude Code 的 `Agent`/`Task` 工具（多个调用放进同一条消息即并行）；若有 `Workflow` 等编排工具，用它的 `parallel()` 一次拉起 8 个更稳——发出**全部 8 个**研究子代理调用。8 个子代理是：`company-profiler` / `earnings-analyst` / `growth-analyst` / `moat-economics-analyst` / `valuation-analyst` / `risk-analyst` / `positioning-options-analyst` / `management-analyst`。
2. **禁止串行 / 禁止挤牙膏**：❌ 不要"发 1 个 → 等它回 → 再发下一个"；❌ 不要先发 2-3 个、回头再补剩下的；❌ 不要自己顺序跑完几个模块再分派。任何"分批发"都会把这个 skill 退化成单线程，丧失它的全部价值。一次就把 8 个发齐。
3. **每个子代理自带完整任务包**：ticker、它负责的模块、取证重点、它拥有的因子/惩罚/红线 key、统一回传结构（`assets/agent-findings-schema.json`）、证据分级与"必须联网取证不靠记忆"的要求。子代理之间无共享状态，任务包必须让它能独立联网跑完。每个子代理的 mission 与负责字段见 `references/agent-roster.md`。
4. **barrier 等齐**：等 8 个**全部**返回再继续。某个失败/超时/数据太薄 → 先进下一步「闭环核实」抢救，补不齐才标"待核实"、按保守处理、不阻塞；**只要有子代理回传红线命中，仍按红线封顶**。
5. **闭环核实（出报告前必做）**：把 8 份回传里所有 `needs_checking[]` 与取证失败项汇总、分流、**再发一轮定向核实**补齐——细则见下方「🔁 闭环核实协议」。一句话原则：**能查到的不留给用户**。
6. **综合出结论**：综合代理 `judge-synthesizer` 合并回传 → 调和重叠 key（取证据更强一方）→ 以 `assets/scorecard-input.json` 为模板**复制出一份临时文件**（如 `/tmp/<ticker>-scorecard.json`，**不要覆盖这个空白模板**）填好分数 → 对该临时文件跑 `scripts/growth_scorecard.py`（双轴 + 惩罚 + 红线封顶）→ 按 `assets/stock-verdict-template.md` 写 12 节"结论先行"报告。

一次发齐的形状（伪代码示意，换成你实际的并行工具）：

```
# ✅ 同一条消息里同时发出 8 个（这才叫并行 fan-out）
dispatch(company-profiler,        ticker, 任务包)  ┐
dispatch(earnings-analyst,        ticker, 任务包)  │
dispatch(growth-analyst,          ticker, 任务包)  │  全部放进
dispatch(moat-economics-analyst,  ticker, 任务包)  ├─ 同一条消息
dispatch(valuation-analyst,       ticker, 任务包)  │  并行发出
dispatch(risk-analyst,            ticker, 任务包)  │
dispatch(positioning-options-analyst, ticker, 任务包) │
dispatch(management-analyst,      ticker, 任务包)  ┘
# → barrier：等 8 个全部返回 → judge-synthesizer 综合打分出报告

# ❌ 反例（别这么干）：dispatch 一个 → 等返回 → 再 dispatch 下一个 …… 串行 = 退化成单 agent
```

Why 必须并行、必须一次发齐：8 个模块各自要独立联网取证，串行会把 8 段调研叠加成约 8 倍墙钟时间；一次性并行分派 + barrier 汇总，正是这个 skill 又快、又能把打分集中在一处保证口径一致的根本原因。挤牙膏式分批发，等于既丢了速度又丢了结构。分派/失败处理/I-O 契约的更多细节见 `references/orchestration.md`。

### 🔁 闭环核实协议（verify-before-output · 出报告前必做）

报告**不该把能查到的问题甩给用户**。barrier 之后、写报告之前，综合代理必须对所有"待核实候选"做**一轮闭环核实**：

1. **汇总**：收齐 8 份回传里的 `needs_checking[]`，以及任何被标 `weak`/`needs_checking`、却影响因子/惩罚/红线判分的关键 finding。
2. **分流三类**：
   - **(A) 有明确源路径、只是没查** → 去查（10-Q/10-K/20-F/8-K/6-K、IR、Form 4/S-3、共识预期等）。
   - **(B) 取证失败（fetch 403 / 超时 / JS 墙 / 被挡）** → **换路再取，不许因为第一次失败就丢给用户**。
   - **(C) 真正不可得** → 实时期权 IV/skew、未来才发生的事件、管理层不披露的非公开数据。
3. **再发一轮定向核实**：对 (A)(B) 用并行子代理（或定向搜索）**一次性补齐**；和主 fan-out 一样，多个核实任务放进**同一条消息**并行发，别串行。这是**有界的一轮**——补齐即停，不无限循环。
4. **(B) 的换路清单**（取证失败必试，试过再说"拿不到"）：
   - SEC 文件（WebFetch 常被 403）：**优先用 shell/`curl` 带正常 User-Agent 直接抓 `sec.gov/Archives/...htm` 原始文件——绕过 403 最有效的一招** → EDGAR 全文检索（efts.sec.gov）→ `data.sec.gov` 提交 API（带正常 UA）→ 文件镜像（bamsec / last10k / stocktitan）→ 该文件的 exhibits → 公司 IR 同稿。
   - 现价 / 估值倍数：换多个行情·数据源交叉。
   - 合同 / 事件状态：原始公告 + 可信二手 + 政府采购·交易所登记。
5. **写报告**：闭环后，(A)(B) 查到的写进**正文**对应章节并标证据级；只有 (C) 才进第 11 节「下一步要核实」，且按"持续跟踪 / 盯盘"口吻写、注明**试过哪些路都没拿到**。关键项全部闭环时，那张表写"无 — 关键项均已闭环核实"。

Why: 用户要的是结论，不是 TODO 清单。取证失败 ≠ 不可得——第一次 fetch 被挡就把 SEC 里白纸黑字的数（股本、客户集中度、内控结论）当"待核实"甩出去，是把自己的活推给用户，也是这类报告最掉价的地方。换路再取、补进正文，报告才算闭环。

### 单 agent 兜底（仅当确无并行能力时）

只有当宿主**完全没有**并行子代理能力时才退回单 agent：同一个 agent 按 `references/growth-analysis-workflow.md` 的步骤**顺序**逐模块联网取证，再汇总打分，产出同样的 12 节报告（含「👤 管理层 / 领导力」节）。这是 fallback，不是默认路径——**只要有并行能力，就必须走上面的 fan-out**。Why: 保证无论宿主有没有并行能力，skill 都能完整出结论；但有能力却走单线程，是对这个 skill 的误用。

## 研究工作流

给定一个美股代码后，按这 11 步研究（多 agent 模式下各模块由对应子代理并行承担；单 agent 模式下顺序执行）。每一步要回答的具体问题、要读哪个 reference，见 `references/growth-analysis-workflow.md`。

1. **锁定公司** — 业务、收入结构、所处赛道与产业链位置。
2. **最近一次财报深读** — 最新鲜最硬的证据，靠前做。逐项 checklist 读 `references/earnings-readthrough.md`。
3. **增长引擎** — 收入增速及趋势、驱动因素、增长可持续性。
4. **市场空间** — TAM、渗透率、还有多长跑道。
5. **护城河 / 产业链位置** — 借 serenity 的"稀缺层/卡点"思路判竞争壁垒。
6. **管理层 / 领导力** — 从"人"的维度判发展潜力（定性，不打分）。四维度见 `references/management-analysis.md`。
7. **单位经济性 / 盈利路径** — 毛利、经营杠杆、FCF 趋势、未来能不能赚钱。
8. **估值与买点** — P/S、PEG 类、对比历史/同业、隐含预期；现价合不合理。方法读 `references/valuation-and-entry.md`。
9. **风险与利空扫描** — 结构性风险读 `references/risk-and-bear-case.md`；资金面（解禁/增发/内部人卖出/降评级）+ 期权市场解读读 `references/positioning-and-options.md`。
10. **证据分级 + 反方 + 闭环核实** — 每个关键结论标 强/中/弱/待核实；**出报告前对所有"待核实候选"按「🔁 闭环核实协议」换路再取、能查到的补进正文**；列"什么情况说明判断错了"。
11. **打分出结论** — 跑评分卡（见下节）。

铁律：现价、现状、最新财报**必须联网查证，不靠记忆**；**有明确源路径（10-Q/10-K/8-K、IR 等）的项必须去查、查到就写进正文**。**取证失败（403/超时/被挡）≠ 不可得——必须换路再取**（见「🔁 闭环核实协议」），换遍了还拿不到才算"待核实"。"待核实"只留给真正取不到的（实时期权 IV、未来才发生的事、非公开数据）——出报告前先跑闭环核实，把这张清单压到接近空。Why: 把记忆当事实、或把第一次没 fetch 到的数据当 TODO 甩给用户，是这类判断最常见也最掉价的错误。

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
- **核心原则：好公司 ≠ 当前价位的好股票**。基本面反映**过去与现在**，股价反映市场对**未来的预期**。当二者背离（基本面亮眼、股价却滞涨/回调/震荡）时，不能用"业绩好"草率收尾——**必须判断市场在边际上重估什么、这个背离合不合理**。这条「预期再定价 / 基本面与股价背离」主线由买点轴承载，方法见 `references/valuation-and-entry.md`，并须在报告第 9 节强制产出。**护栏**：价格/期权属中/弱证据，作用是**逼出对背离的解释与远期假设的检验**，不是按涨跌给分——解释背离，不追涨杀跌；与基本面冲突时仍以基本面为准。
- **惩罚项**（×2）：`dilution_financing` / `customer_concentration` / `accounting_quality` / `governance` / `competition_disruption` / `regulation_geopolitics` / `liquidity_bubble` / `lockup_insider_supply`。
- **红线（kill-switch）封顶**：`accounting_fraud_suspicion` / `core_customer_loss` / `growth_engine_broken` 任一触发 → 结论封顶为"回避 / 观望（红线封顶）"，无论原始分多高。Why: 不让高分掩盖致命问题。
- **结论分档**：≥85 强信心值得投资；70-84 值得投资；55-69 观望 / 建仓试探；<55 暂不值得 / 回避。

跑法：以 `assets/scorecard-input.json` 为模板**复制一份临时文件**（如 `/tmp/<ticker>-scorecard.json`），把各模块判分填进**临时文件**（key 与脚本一一对应，**不要改动模板本身**），运行
`python scripts/growth_scorecard.py /tmp/<ticker>-scorecard.json --format both`
得到总分、质量分、买点分、红线状态。每个因子/惩罚/红线 0-5 分的判分锚点读 `references/growth-scoring-rubric.md`。

## 输出契约

用 `assets/stock-verdict-template.md` 的固定 12 节结构出报告，**结论先行**：

1. 结论框（一句话结论 + 信心 + 双轴 + 总分）2. 评分卡（因子表 + **惩罚项表【每项含「理由」列】** + 红线表）3. 投资逻辑 4. 增长引擎+市场空间 5. 📊 最近财报重点 6. 护城河/产业链位置 7. 👤 管理层/领导力 8. 单位经济性/盈利路径 9. 估值与买点（**含强制子块「市场在重估什么 / 基本面 vs 股价背离」**）10. ⚠️ 风险与利空（结构性 → 资金面 → 期权市场怎么看 → 下行情景 → kill-switch 清单）11. 结论复述+下一步要核实+催化/日历 12. 证据与来源。

- **第 9 节必含「市场在重估什么 / 基本面 vs 股价背离」强制子块**：回答四问——① 现价已 price-in 的隐含假设；② 基本面动能 vs 股价动能是否背离（如 beat 但股价滞涨/回调/距高点回撤震荡）；③ 市场在边际上重估什么（增长持续性 / 利润率可防御性 / 需求天花板 / 大客户议价权）；④ 背离是否合理、要发生什么才会收敛。把结构性利空（如自研替代、地缘、客户集中）当作**边际再定价催化剂**来解读，而非孤立清单。价格属中/弱证据——解释背离，不追涨杀跌。当存在背离时，第 1 节 one-liner 须点名（例："好公司，但市场正在重估增长持续性 → …"）。

- **用 md 表格的地方必须用表格，别用流水句**：第 2 节**惩罚项**用表格列出，每项在「理由」列写清为什么给这个分（具体证据，一句话）；第 11 节的**「下一步要核实」**和**「催化/日历」**都各用一张 md 表格填满，不要留半截。
- **第 11 节「下一步要核实」出报告前必须先闭环核实**：凡有源路径、或仅因 fetch 失败没拿到的项，先按「🔁 闭环核实协议」换路查、查到写进正文，**不留给用户**；这张表最终只剩闭环后仍真正不可得的（实时期权 IV/skew、未来事件、非公开数据），按"持续跟踪/盯盘"口吻写、注明试过哪些路。关键项全部闭环时写"无 — 关键项均已闭环核实"。
- 每条关键结论标证据等级：**强 / 中 / 弱 / 待核实**；**第 12 节证据与来源尽量给可点击超链接** `[来源名](URL)`（SEC 文件、公司 IR、原始报道），便于用户一键核查与拓展阅读。
- **第 11 节催化 / 日历要排密**：按时间列出所有适用事件类型（下次财报 / 产品发布量产 / 行业大会·投资者日 / 解禁·增发·回购 / 大客户与上下游 capex 指引 / 监管·政策 / 竞品 / 分析师评级 / 指数纳入 / 宏观 / 重大合同·投票），每条标日期或"待核实"，别只写"下次财报"。事件类型清单见 `references/earnings-readthrough.md` 末尾。
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
- **无多 agent 能力**：单 agent 按 11 步工作流顺序自跑（见上文"执行模式"），照样跑评分卡出结论。
- **某模块数据不足/子代理失败**：在报告中把该模块标"待核实"，不阻塞整体结论；若该模块命中红线，按红线封顶。
