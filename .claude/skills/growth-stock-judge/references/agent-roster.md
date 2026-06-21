# 子代理名册（agent roster）

8 个并行研究子代理 + 1 个综合代理。每个研究子代理只负责一个模块、独立联网取证、按 `assets/agent-findings-schema.json` 回传，并只填**自己拥有的因子/惩罚/红线键**（其余留 `null`/`false`）。证据分级沿用 serenity 的 `references/evidence-ladder.md`；不在场时用 SKILL.md 内精简分级表兜底。各键定义以 `scripts/growth_scorecard.py` 为准。

> **重叠键说明**：少数键由多个代理共同关注——`product_customer_momentum`（`earnings-analyst` 与 `growth-analyst` 都给）、`entry_expectations`（`valuation-analyst` 与 `positioning-options-analyst` 都给）、`management_capital_allocation`（`earnings-analyst` 与 `management-analyst` 都给）。这些重叠键不在子代理层裁决，由 `judge-synthesizer` 用**证据更强**的一方调和（见 `references/orchestration.md` 的 I/O 契约）。

## company-profiler

- **Mission**：锁定这是一家什么公司，为其余代理提供共同上下文。
- **拥有的模块 / 流程步骤**：锁定公司（流程 1）。
- **取证重点**：主营业务、收入结构（分业务线/产品/地区）、所处赛道与产业链位置、商业模式。
- **回传字段**：仅 context（不拥有任何因子/惩罚/红线键，`suggested_*` 全留 `null`/`false`）；产出供其他代理与综合代理引用的 `findings[]` 与 `summary`。
- **证据要求**：以 10-K/10-Q 业务描述、公司官网/IR、招股书为强证据来源。

## earnings-analyst

- **Mission**：深读最近一次财报，拿最新鲜最硬的证据（见 `references/earnings-readthrough.md`）。
- **拥有的模块 / 流程步骤**：最近财报深读（流程 2，第 6 节）。
- **取证重点**：增速实绩（beat/miss、加速/放缓）、指引（上调/维持/下修）、核心产品与研发进展、盈利与单位经济性、客户与势能、资本配置、电话会弦外之音与红旗、财报后反应。
- **回传字段**：
  - 因子键：`product_customer_momentum`、`management_capital_allocation`。
  - 惩罚键：`accounting_quality`。
  - 红线键：`growth_engine_broken`（指引大幅下修 / 增长引擎失效时触发）。
- **证据要求**：最新 10-Q/10-K + 财报电话会 transcript + 业绩 PPT（强证据）。

## growth-analyst

- **Mission**：判断增长引擎能不能持续、跑道还有多长。
- **拥有的模块 / 流程步骤**：增长引擎 + 市场空间（流程 3-4）。
- **取证重点**：收入增速及趋势、增长驱动因素与可持续性、TAM 与渗透率、客户/产品势能（NRR/NDR、订单、指引上调）。
- **回传字段**：
  - 因子键：`revenue_growth_durability`、`tam_penetration`、`product_customer_momentum`（与 `earnings-analyst` 重叠，由综合代理调和）。
  - 惩罚键：—。
  - 红线键：—。
- **证据要求**：财报与电话会强证据为主；第三方行业 TAM 测算属中证据，需注明假设。

## moat-economics-analyst

- **Mission**：判断竞争壁垒强不强、未来能不能赚钱。
- **拥有的模块 / 流程步骤**：护城河 + 单位经济性（流程 5（护城河）+ 6（单位经济性））。
- **取证重点**：护城河/产业链位置（借 serenity 的稀缺层/卡点思路）、毛利率、经营杠杆、FCF 趋势、盈利路径、相对竞品定位。
- **回传字段**：
  - 因子键：`moat_chain_position`、`unit_economics_profit_path`。
  - 惩罚键：`competition_disruption`。
  - 红线键：—。
- **证据要求**：财报财务数据为强证据；竞争格局判断用中证据（行业/专业研究）并交叉验证。

## valuation-analyst

- **Mission**：判断现价贵不贵、市场已 price-in 了多少（见 `references/valuation-and-entry.md`）。
- **拥有的模块 / 流程步骤**：估值与买点（流程 7）。
- **取证重点**：P/S vs 增速、PEG 类、EV/Sales、Rule-of-40、对比历史/同业、隐含预期/反向 DCF 直觉、距一致预期的位置、预期门槛；**基本面 vs 股价背离 / 市场在边际上重估什么**——若基本面亮眼但股价滞涨/回调（距高点回撤震荡），反推远期一致预期/隐含假设被如何下修，市场在重估的是增长持续性、利润率可防御性、需求天花板还是大客户议价权（见 `references/valuation-and-entry.md`「股价行为 vs 基本面」节）。
- **回传字段**：
  - 因子键：`valuation_growth_match`、`entry_expectations`（与 `positioning-options-analyst` 重叠，由综合代理调和）。
  - 惩罚键：`liquidity_bubble`。
  - 红线键：—。
- **证据要求**：现价/估值倍数**必须联网查证**，拿不到标"待核实"并给查证路径。

## risk-analyst

- **Mission**：扫描结构性风险与利空，识别致命问题（见 `references/risk-and-bear-case.md`）。
- **拥有的模块 / 流程步骤**：风险与利空（流程 8，第 7 节）。
- **取证重点**：客户流失/集中度、治理红旗、监管/地缘/政策、会计治理嫌疑、增长引擎是否受损、核心客户是否流失。
- **回传字段**：
  - 因子键：—。
  - 惩罚键：`customer_concentration`、`governance`、`regulation_geopolitics`。
  - 红线键：`accounting_fraud_suspicion`、`core_customer_loss`。
- **证据要求**：红线判定需强证据（监管文件、官方公告、确凿披露）；仅凭弱证据不得封顶，但应标"待核实"提示。

## positioning-options-analyst

- **Mission**：读资金面/筹码面与期权市场，辅助买点与风险（见 `references/positioning-and-options.md`）。
- **拥有的模块 / 流程步骤**：资金面 + 期权（流程 8，第 7 节）。
- **取证重点**：解禁日（日期/规模/谁）、增发/ATM/S-3、内部人卖出（Form 4、10b5-1、集体减持）、机构降评级/13F 减持、回购 vs 稀释净额；IV/IV 百分位、财报隐含波动、put/call、skew、OI/max pain、异常活动、期限结构；**把价格行为（距 52 周高的回撤、震荡、动量、财报后涨跌与 beat/miss 是否匹配）读作远期预期的信号**——不止情绪，而是"市场是否在重估远期假设"的线索，供 `entry_expectations` 背离读数（仍属中/弱证据，不作核心驱动，不机械按涨跌打分）。
- **回传字段**：
  - 因子键：`entry_expectations`（价格/预期面上下文，与 `valuation-analyst` 重叠，由综合代理调和）。
  - 惩罚键：`dilution_financing`、`lockup_insider_supply`。
  - 红线键：—。
- **证据要求**：期权/筹码面属**中/弱证据**（情绪/持仓面），不作核心结论主驱动；EDGAR Form 4/S-3 为强证据，期权数据拿不到标"待核实"并给数据源。

## management-analyst

- **Mission**：从"人"的维度判断公司发展潜力，独立联网取证，回传**定性**结论（不打分）。详见 `references/management-analysis.md`。
- **拥有的模块 / 流程步骤**：管理层 / 领导力（研究工作流"护城河"之后那一步）。（注：本代理**不拥有任何因子键**，产出为纯定性叙述，故"拥有"指报告节归属，而非评分卡因子所有权。）
- **取证重点**：四维度——① 创始人/CEO 背景与往绩 ② 愿景与战略执行力（said-vs-done）③ 利益绑定（内部人持股/薪酬对齐）④ 团队稳定性/关键人物风险。
- **证据来源**：DEF 14A 代理声明、10-K/20-F、Form 4、财报电话会 transcript、管理层访谈；Glassdoor 等仅弱证据。每条标 强/中/弱/待核实；本模块**不出因子分**，判断写进报告「👤 管理层 / 领导力」节。
- **回传字段（联动现有键，不新增因子）**：定性叙述进 `summary`/`findings[]`；可贡献 `suggested_factor_scores.management_capital_allocation`（与 `earnings-analyst` 重叠 → 综合代理择优调和）、`suggested_penalties.governance`、以及命中诚信/造假时 `suggested_red_lines.accounting_fraud_suspicion`、关键人物出走作 `growth_engine_broken` 风险输入。

## judge-synthesizer

- **Mission**：综合所有研究代理产出，出分与结论，写报告。
- **拥有的模块 / 流程步骤**：综合（synthesis lane，barrier 之后）。
- **取证重点**：调和重叠的 `suggested_factor_scores`（取证据更强的一方）；合并 `flags[]`、`needs_checking[]`；按 `assets/agent-findings-schema.json` 读取，组装评分卡输入。
- **闭环核实（出报告前必做）**：汇总所有 `needs_checking[]` 与取证失败项，按 SKILL.md「🔁 闭环核实协议」分流并**再发一轮定向核实子代理**补齐——(A) 有源路径的去查、(B) fetch 失败的换路再取、(C) 真正不可得的才保留。能查到的写进正文，不甩给用户；这步在打分/写报告之前完成。
- **预期再定价合成（出报告前必做）**：把 earnings-analyst 的「财报后反应 + 远期一致预期修正方向」、valuation-analyst 的「隐含预期 / 背离」、positioning-options-analyst 的「价格行为」**合成为一个**「市场在边际上重估什么 / 基本面 vs 股价背离是否合理」读数，**强制写进报告第 8 节的「市场在重估什么 / 基本面 vs 股价背离」子块**，并据此校准（连同解释）`entry_expectations`。护栏：价格属中/弱证据，解释背离、不按涨跌机械打分；存在背离时第 1 节 one-liner 须点名。
- **回传字段**：不新拥有键——**调和全部因子/惩罚/红线键**，以 `assets/scorecard-input.json` 为模板复制临时文件填分（勿覆盖模板）后运行 `scripts/growth_scorecard.py`（含双轴、惩罚、红线封顶），按 `assets/stock-verdict-template.md` 写"结论先行"的 12 节报告。
- **证据要求**：每条结论标 强/中/弱/待核实；红线命中则封顶，不让高分掩盖致命问题。
