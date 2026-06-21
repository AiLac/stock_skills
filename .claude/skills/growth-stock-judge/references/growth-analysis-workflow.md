# 单股深度研究工作流（11 步）

给定一个美股代码，按此 11 步研究一只成长股，最后用评分卡出结论。多 agent 模式下，第 1-8 步由 `references/agent-roster.md` 的 8 个研究子代理**并行**承担，第 9-10 步由 `judge-synthesizer` 综合（编排见 `references/orchestration.md`）；单 agent 兜底时同一个 agent 按本顺序逐步跑。

> **铁律（贯穿全程）**：现价、现状、最新财报、估值倍数、解禁日、内部人交易等**必须联网查证，不靠记忆**。拿不到的数据标"待核实"并给查证路径（在哪个文件/数据源能查到），**绝不编造数字**。证据分级沿用 serenity 的 `references/evidence-ladder.md`（强/中/弱/待核实）；不在场时用 SKILL.md 内精简分级表兜底。各评分键名以 `scripts/growth_scorecard.py` 为准。

## 1. 锁定公司

先搞清这是一家什么公司，给后续步骤提供共同上下文。

- 主营业务是什么？怎么赚钱（商业模式）？
- 收入结构：分业务线 / 产品 / 地区，哪块是大头、哪块在增长？
- 所处赛道与产业链位置（上游/中游/下游、卖铲子还是卖应用）？
- 谁是客户、谁是竞争对手？

**接下来读**：拿到业务基本盘后，直接进第 2 步财报深读。

## 2. 最近一次财报深读

放在最靠前，因为这是**最新鲜、最硬**的证据。逐项 checklist 见 `references/earnings-readthrough.md`（8 个 block）。

- 实际收入 vs 一致预期（beat/miss 多少）？YoY/QoQ 增速在加速还是放缓？
- 指引：下季度 / 全年指引相对预期是上调、维持还是下修？
- 核心产品与研发进展、盈利与单位经济性、客户与势能、资本配置如何？
- 电话会有没有弦外之音 / 红旗？财报后股价与分析师预期怎么反应？

**接下来读**：`references/earnings-readthrough.md` 逐项填，再进第 3 步。

## 3. 增长引擎

判断增长是真的、可持续的，还是一次性的。

- 收入增速及趋势：当前增速多少、几个季度的轨迹（加速/放缓）？
- 增长驱动因素是什么（新品放量、提价、新市场、客户扩张）？
- 增长可持续性：驱动因素能延续吗，还是已经透支（pull-forward）？
- 客户/产品势能：净留存（NRR/NDR）、订单/RPO/backlog、指引是否上调？

**评分键**：`revenue_growth_durability`、`product_customer_momentum`。锚点见 `references/growth-scoring-rubric.md`。

## 4. 市场空间

判断跑道还有多长。

- TAM 有多大、用什么口径测算（自上而下还是自下而上）？测算假设是否可信？
- 当前渗透率多少？离天花板还有多远？
- 市场本身在扩张还是已成熟？公司能否扩大自己的份额？

**评分键**：`tam_penetration`。第三方 TAM 测算属**中证据**，须注明假设。锚点见 `references/growth-scoring-rubric.md`。

## 5. 护城河 + 产业链位置

判断竞争壁垒强不强。借 serenity 的"卡点 / 稀缺层"思路：**离稀缺层越近、越难被替代，壁垒越硬**——别人扩产/迭代绕不过它、供应商少、认证慢，就是强护城河。

- 壁垒来自哪里（技术/规模/网络效应/转换成本/牌照/生态）？
- 在产业链里卡不卡位？是"卖铲子"的稀缺层，还是容易被替代的一环？
- 相对竞品的定位在变强还是变弱？

> **serenity 复用**：稀缺层/卡点判断借用 `serenity-skill/references/public-profile-and-evaluation.md` 与 `deep-research-workflow.md` 的思路。**兜底**：serenity 不在场时，按本步骤的壁垒来源清单自行判断，不阻塞。

**评分键**：`moat_chain_position`。锚点见 `references/growth-scoring-rubric.md`。

## 5b. 管理层 / 领导力（定性，不打分）

从"人"的维度判发展潜力。详细四维度 checklist 见 `references/management-analysis.md`。

- 创始人/CEO 背景与往绩；是否 founder-led。
- 愿景与战略执行力：承诺兑现率（said-vs-done）、战略连贯性。
- 利益绑定：内部人持股、薪酬是否对齐长期（DEF 14A / Form 4）。
- 团队稳定性 / 关键人物风险：高管流失、key-person 依赖、接班深度。

**不新增因子**：本步定性，写进报告「👤 管理层 / 领导力」节；可定性联动现有键 `management_capital_allocation`（与第 6 步资本配置重叠，综合代理择优）、`governance` 惩罚、诚信红线 `accounting_fraud_suspicion`、关键人物出走作 `growth_engine_broken` 输入。

## 6. 单位经济性

成长股看"未来能不能赚钱"，不是现在赚不赚。

- 毛利率水平与趋势（在扩张还是被侵蚀）？
- 经营杠杆：收入增长时费用率是否下降、营业利润率是否改善？
- FCF 趋势、现金跑道；盈利路径清不清晰（什么时候转正 / 已转正）？
- SBC 占收比是否过高（变相稀释）？

**评分键**：`unit_economics_profit_path`。锚点见 `references/growth-scoring-rubric.md`。

## 7. 估值与买点

判断现价贵不贵、市场已经 price-in 了多少。方法与映射见 `references/valuation-and-entry.md`。

- P/S vs 增速、PEG 类、EV/Sales、Rule-of-40；对比自身历史与同业。
- 隐含预期 / 反向 DCF 直觉：现价隐含了多高的增长假设？
- 距一致预期的位置、预期门槛是否已经很高（容易 miss）？
- **股价行为 vs 基本面对齐度（必做）**：现价是顺着基本面动能（beat / 指引上调 / TAM 扩张）走，还是背离（基本面强、股价滞涨/回调/距高点回撤震荡）？若背离，**市场在边际上重估什么**（增长持续性 / 利润率可防御性 / 需求天花板 / 大客户议价权），背离合不合理、何时收敛。这层须强制写进报告第 9 节「市场在重估什么 / 基本面 vs 股价背离」子块。护栏：价格属中/弱证据，解释背离、不按涨跌机械打分。

**评分键**：`valuation_growth_match`、`entry_expectations`。现价/估值倍数**必须联网查**，拿不到标"待核实"。锚点见 `references/growth-scoring-rubric.md`。

## 8. 风险与利空扫描

区分**风险**（结构性、长期隐患）与**利空**（近期可能落地的坏消息/负面催化）。清单见 `references/risk-and-bear-case.md`；资金面/筹码面 + 期权见 `references/positioning-and-options.md`。

- 结构性风险：竞争颠覆、客户集中度、监管/地缘、会计治理红旗、宏观/流动性。**这些不只是静态清单——同时把它们当作买点轴的「边际再定价催化剂」**：哪一条是市场当下正在重估的、压制股价的边际利空（如自研替代蚕食推理份额、地缘市场被砍、大客户既是金主又在自研），与第 7 节的背离读数联动。
- 业绩/估值利空：增速放缓、指引下修、杀估值。
- 资金面/筹码面：解禁日（日期/规模/谁）、增发/ATM/S-3、内部人卖出（Form 4）、机构降评级/13F 减持。
- 期权市场怎么看：IV/IV 百分位、财报隐含波动、put/call、skew、OI/max pain。
- **红线判定**：有没有命中 `accounting_fraud_suspicion` / `core_customer_loss` / `growth_engine_broken`？命中则封顶。

**评分键**：惩罚项 `dilution_financing`、`customer_concentration`、`accounting_quality`、`governance`、`competition_disruption`、`regulation_geopolitics`、`liquidity_bubble`、`lockup_insider_supply`；红线 `accounting_fraud_suspicion`、`core_customer_loss`、`growth_engine_broken`。锚点见 `references/growth-scoring-rubric.md`。

## 9. 证据分级 + 反方

为结论上"防伪标签"，并主动找自己判断的破绽。

- 每个关键结论标 **强/中/弱/待核实**（依据 serenity `evidence-ladder.md`，兜底用 SKILL.md 精简表），并尽量记下**来源 URL**（SEC 文件页、公司 IR、原始报道），供报告第 11 节给可点击链接。
- 列"**什么情况说明判断错了**"（kill-switch / 反方清单）：哪些数据一旦出现，就推翻当前结论？
- **"待核实"是最后手段，不是偷懒出口（出报告前先闭环核实）**：凡是有明确源路径、能联网查到的（10-Q/10-K/8-K 里的 SBC 净稀释、客户集中度、出口管制最新细节、下代产品时间线、Q+1 共识是否已消化指引等），**先去查、查到就写进上文对应章节**。**取证失败（fetch 403/超时/被挡）≠ 不可得——必须换路再取**：SEC 文件走 **shell/curl 带正常 User-Agent 抓主文档原始页（WebFetch 403 时最有效）** → EDGAR 全文检索(efts) → data.sec.gov API → 镜像(bamsec/last10k/stocktitan) → exhibits → 公司 IR；现价/倍数换多个数据源交叉；合同/事件查原始公告 + 政府采购/交易所登记。换遍仍拿不到才留"待核实"，并注明**试过哪些路**。只有真正取不到的（实时期权 IV、未来才发生的事件、非公开数据）才进"待核实"。报告第 11 节这张清单应当**很短**，关键项全部闭环时写"无 — 关键项均已闭环核实"。多 agent 模式下，这一轮补查由 `judge-synthesizer` 在 barrier 后**再发一轮定向核实子代理**完成（见 `references/orchestration.md` 第 5 步与 SKILL.md「🔁 闭环核实协议」）。

**接下来读**：把分级好的证据与反方喂给第 10 步打分。

## 10. 打分出结论

用评分卡把上面的研究压成一个可复核的结论。机制见 `references/growth-scoring-rubric.md`，代码见 `scripts/growth_scorecard.py`。

- 以 `assets/scorecard-input.json` 为**模板复制一份临时文件**（如 `/tmp/<ticker>-scorecard.json`，**别改动模板本身**），在临时文件里填 8 个因子（0-5）、8 个惩罚项（0-5）、3 个红线（true/false）。
- 运行 `python scripts/growth_scorecard.py /tmp/<ticker>-scorecard.json --format both`，得到**总分**、**质量分**、**买点分**、**结论分档**与**红线封顶状态**。
- 结论分档：≥85 强信心值得投资；70-84 值得投资；55-69 观望 / 建仓试探；<55 暂不值得 / 回避；**命中红线封顶为"回避 / 观望"**（无论原始分多高）。
- 按 `assets/stock-verdict-template.md` 写"结论先行"的 12 节报告，结论同时给出**双轴**（好公司但偏贵 → 观望/分批 这类细腻判断）。
- 报告第 11 节的**催化 / 日历**要排密、别只写"下次财报"：按时间列出所有适用的事件类型，每条标日期或"待核实"。完整事件类型清单见 `references/earnings-readthrough.md` 末尾「催化 / 日历事件类型」。
- 报告第 12 节**证据与来源**尽量给**可点击链接**（[来源名](URL)），方便用户核查与拓展阅读。
