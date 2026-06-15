# 示例：TSLA（Tesla）成长股投资判断（worked example）

> **真实走查示例**，由 growth-stock-judge 的多 agent 流程联网生成，数据截至 **2026-06-16**。展示本 skill 的标准输出形态：结论先行 + 评分卡 + 11 节报告，**每条结论标证据等级、来源给可点击超链接、能查的查进正文、催化日历排密**。价格与数据随时变动，**研究用途，不构成投资建议**。

本文件从 `assets/stock-verdict-template.md` 端到端填出，内部一致：下方评分卡 JSON 经 `scripts/growth_scorecard.py` 算出的 verdict 与报告"结论"一致。

---

## 评分卡输入 JSON（喂给 `growth_scorecard.py`）

```json
{
  "ticker": "TSLA",
  "company": "Tesla, Inc.",
  "factors": {
    "revenue_growth_durability": 2.5, "tam_penetration": 3, "moat_chain_position": 3,
    "unit_economics_profit_path": 2.5, "product_customer_momentum": 3, "management_capital_allocation": 2,
    "valuation_growth_match": 1, "entry_expectations": 1
  },
  "penalties": {
    "dilution_financing": 1, "customer_concentration": 2, "accounting_quality": 2, "governance": 4,
    "competition_disruption": 3.5, "regulation_geopolitics": 3.5, "liquidity_bubble": 3, "lockup_insider_supply": 2
  },
  "red_lines": {"accounting_fraud_suspicion": false, "core_customer_loss": false, "growth_engine_broken": false}
}
```
脚本输出（关键行）：`结论：暂不值得 / 回避｜总分 5.2｜质量分 54.0｜买点分 20.0｜原始因子分 47.2｜惩罚扣分 42.0`

---

# TSLA（Tesla, Inc.）成长股投资判断

## 结论
**暂不值得 / 回避（当前买点）**　｜　信心：中高
**质量分 54.0 / 买点分 20.0 / 总分 5.2**　｜　红线：未触发（但 core_customer_loss 接近，见下）
一句话：一个真实的 AI/自动驾驶**期权**，被钉在一个汽车业务处于利润低谷、品牌在核心市场流失的躯壳上，却按 [~190x 前瞻市盈率](https://stockanalysis.com/stocks/tsla/statistics/) 定价。生意本身只算中等（质量 54），但**治理、监管、竞争、品牌**四重风险叠加把总分几乎打到地板——**好故事、坏价格、重风险 → 现价回避**。

> 这与卖方"持有、目标价≈$420（仅 +2%）"基本一致；多数 DCF（[GF Value $287](https://www.gurufocus.com/term/forward-pe-ratio/TSLA)、[Alpha Spread $16](https://www.alphaspread.com/security/nasdaq/tsla/dcf-valuation/base-case)）显示深度高估。本 skill 把"AI 期权值不值这个价 + 风险负荷"算进结论，所以给"回避"。

## 评分卡
| 因子 | 评分(0-5) | 权重 | 得分 | 轴 |
|---|---:|---:|---:|---|
| revenue_growth_durability | 2.5 | 18 | 9.0 | 质量 |
| tam_penetration | 3.0 | 14 | 8.4 | 质量 |
| moat_chain_position | 3.0 | 14 | 8.4 | 质量 |
| unit_economics_profit_path | 2.5 | 14 | 7.0 | 质量 |
| product_customer_momentum | 3.0 | 12 | 7.2 | 质量 |
| management_capital_allocation | 2.0 | 8 | 3.2 | 质量 |
| valuation_growth_match | 1.0 | 12 | 2.4 | 买点 |
| entry_expectations | 1.0 | 8 | 1.6 | 买点 |

### 惩罚项（×2 倍率，合计扣 42.0 分）
| 惩罚项 | 评分(0-5) | 扣分 | 理由 |
|---|---:|---:|---|
| governance | 4 | 8.0 | 董事会被实质俘获、覆盖法院裁决批 $56B 薪酬、未约束 Musk 跨 5 家公司分心（Harvard Law / 公司治理研究所均点名） |
| competition_disruption | 3.5 | 7.0 | 三重夹击：Waymo 实景 L4 领先、BYD+华为 ADS 蚕食中国、撑利润的监管积分面临立法取消 |
| regulation_geopolitics | 3.5 | 7.0 | NHTSA 对 320 万辆 FSD 升级工程分析（recall 前一步）；Robotaxi 全国部署无联邦批准；加州仍需人类驾驶 |
| liquidity_bubble | 3 | 6.0 | 散户/meme 资金集中、约 $300+/股纯期权溢价、ATH 三周回撤 25% 的泡沫式波动 |
| customer_concentration | 2 | 4.0 | 无单一大客户，但高度依赖美/中两大承压市场，欧洲塌方削弱分散度 |
| accounting_quality | 2 | 4.0 | 一次性保修/关税项美化毛利且拒绝拆分；FSD 订阅数含历史购买者、口径偏松 |
| lockup_insider_supply | 2 | 4.0 | 董事会成员（Denholm/Kimbal/Wilson-Thompson）持续 10b5-1 减持；Musk 本人无公开市场卖出 |
| dilution_financing | 1 | 2.0 | 304M+424M 股薪酬期权锁定至 2028-2033，近期流通盘稀释低，仅 $9.97B SBC 入表拖累 |

### 红线（kill-switch）
| 红线 | 状态 | 说明 |
|---|:--:|---|
| accounting_fraud_suspicion | 未触发 | 一次性项与监管积分是披露质量问题、非造假；无 SEC 立案，报表 GAAP 合规 |
| core_customer_loss | 未触发（接近） | 风险代理标 TRUE（[欧洲 -44%](https://electrek.co/2026/02/02/tesla-tsla-cant-find-bottom-europe-2026-brutal-decline/)、美国 8 年低份额、创始客群流失）；综合代理判为**严重惩罚级**而非硬红线——Tesla 仍[夺回全球纯电第一](https://carboncredits.com/tesla-reclaims-ev-crown-from-byd-in-q1-2026-tsla-stock/)、中国一季度回暖；**若美/欧份额继续下滑则升级为红线封顶** |
| growth_engine_broken | 未触发 | 营收重新加速 +16%、毛利从低谷回升；但"下一代引擎"(Robotaxi/Optimus) 商业化≈0，二元性极大 |

## 投资逻辑
多头逻辑几乎全押在"自动驾驶 + 人形机器人"两个期权：可复用的 FSD 数据飞轮（[10B+ 累计英里、29M/天](https://electrek.co/2026/05/03/tesla-fsd-10-billion-miles-no-magical-milestone-autonomy/)）、Supercharger/NACS 充电标准、储能（Megapack）高增长。问题是：**今天的生意支撑不了今天的估值**——汽车在利润低谷、品牌在核心市场流失，而 Robotaxi/Optimus 的商业化要到 2027+ 才有意义。$1.53T 市值里约 $300+/股是纯期权溢价，安全边际几乎为零。

## 增长引擎 + 市场空间
- **收入重新加速但底子虚**：Q1 2026 营收 [$22.39B（+15.8% YoY）](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative)，但是从 2025 低谷反弹——[FY2025 交付 1.636M（-8.6%）](https://teslanorth.com/2026/01/02/tesla-q4-2025-deliveries-418227-vehicles/)，仍低于 2024 峰值 1.79M。
- **结构在变**：Services & Other [$3.75B（+42%）](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-financial-results/) 最快；储能是高margin 引擎但 [Q1 仅 8.8 GWh（-38% QoQ、不及预期）](https://www.ess-news.com/2026/04/23/elon-musk-says-teslas-energy-storage-business-very-strong-actual-forecast-for-2026-is-weak/)。
- **FSD 渗透在走**：[订阅数 1.28M、车队渗透 14%](https://www.notateslaapp.com/news/4030/tesla-fsd-adoption-hits-14-as-subscriptions-soar-in-q1)（2 月起改为纯订阅）。
- **TAM 巨大但渗透≈0**：Robotaxi（[ARK 估 2030 全球 $10T](https://www.ark-invest.com/articles/analyst-research/tesla-launched-its-robotaxi-now-what)）、Optimus、能源——但管理层明说 [Robotaxi 2026 收入"不重要"](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap)。→ revenue_growth_durability 2.5 / tam 3。

## 📊 最近财报重点（Q1 2026，4/22 报告）
- **营收小超 + EPS beat**：[$22.39B vs ~$22.28B 预期](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-financial-results/)；non-GAAP EPS [$0.41 vs $0.36（+14% beat、YoY +52%）](https://www.investing.com/news/transcripts/earnings-call-transcript-tesla-beats-q1-2026-eps-forecasts-stock-rises-93CH-4631008)。
- **交付不及 + 库存堆积**：[交付 358,023（差 ~7,600）](https://www.cnbc.com/2026/04/02/tesla-tsla-q1-2026-vehicle-delivery-production.html)，产量比交付多 50,363 辆（约 $2B 收入递延、Q2 margin 风险）。
- **毛利被一次性项美化**：GAAP GM 21.1%、汽车 ex-credits 19.2%，但管理层承认 [~$230M 保修 + ~$250M 关税退款一次性、拒绝拆分](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-one-time-benefits-warranty-tariff-refunds-margins/)——净化后核心更弱。
- **指引**：未给传统全年指引；[2026 capex >$25B、全年 FCF 约 -$8.5B](https://techcrunch.com/2026/04/22/tesla-just-increased-its-capex-to-25b-heres-where-the-money-is-going/)；现金 $44.7B。
- **产品里程碑**：[Optimus V3 7 月底/8 月发布、放量"很慢"](https://electrek.co/2026/04/22/tesla-optimus-production-fremont-model-sx-line/)；Robotaxi 仍 ~20-42 辆。
- **财报后**：[股价 -3.6% 至 ~$373](https://fortune.com/2026/04/23/tesla-stock-price-earnings-call-outlook/)；全年 EPS 共识从 ~$1.89 砍到 ~$1.37。

## 护城河 / 产业链位置
- **真护城河**：[Supercharger/NACS 占美国 52% 快充口、几乎全行业采用](https://usevchargingstations.info/guides/nacs-transition/)——基础设施壁垒，越多非 Tesla 车加入越强；FSD 真实数据规模领先。
- **在被侵蚀**：实景 Robotaxi 运营 [Waymo 远超（TX ~577 vs Tesla ~42 辆）](https://www.techtimes.com/articles/318160/20260610/tesla-robotaxi-trails-waymo-42-577-texasaustin-map-masks-20-car-fleet-until-fsd-v15-rewrite.htm)；中国端 [BYD + 华为 ADS 从品牌和技术两头夹](https://www.teslaacessories.com/blogs/news/fsd-vs-competitors-can-tesla-outperform-byd-and-huawei-in-autonomous-driving-technology-)。→ moat 3。

## 单位经济性 / 盈利路径
- 汽车 ex-credits GM 19.2%（含一次性，真实可能 17-18%）；储能 GM 高（[2025 全年 29.8%](https://www.energy-storage.news/tesla-energy-storage-deployments-jumped-in-crucial-ai-transformation-year-company-expects-margin-compression-in-2026/)，2026 指引压缩）。
- **盈利路径远**：经营利润率仅 4.2%，[2026 FCF 约 -$8.5B](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative)；[$2.76B 监管积分（近 100% 毛利）面临立法取消威胁](https://www.notateslaapp.com/news/2885/tesla-to-face-billions-in-lost-profit-as-big-beautiful-bill-kills-ev-credits)。→ unit_economics 2.5。

## 估值与买点
- **极贵**：[前瞻 P/E ~188-208x、P/S 15.8x、EV/EBITDA 136x、PEG 4.12、净利率 3.95%](https://stockanalysis.com/stocks/tsla/statistics/)；[市值超过其余所有车企总和](https://cleantechnica.com/2026/02/19/tesla-market-cap-more-than-market-cap-of-toyota-byd-gm-ford-hyundai-kia-mercedes-benz-stellantis-geely-ferrari-bmw-volkswagen-group-honda-nissan-renault-xpeng-and-nio-combined/)。
- **买点贵到没缓冲**：现价 ~$406 ≈ [47 位分析师均价目标 $419.94（+2.3%）](https://stockanalysis.com/stocks/tsla/forecast/)，目标价分歧极大（$25–$600）。反向读：现价隐含 Robotaxi + Optimus **同时**大规模成功。→ valuation/entry 各 1。

## ⚠️ 风险与利空
### 结构性风险
- **创始客群流失（#1）**：[欧洲 1 月注册 -44% YoY、连跌三年](https://electrek.co/2026/02/02/tesla-tsla-cant-find-bottom-europe-2026-brutal-decline/)；[美国份额 8 年新低、Musk 政治引发抵制](https://www.usnews.com/news/business/articles/2026-04-02/tesla-sales-rise-after-brutal-year-of-musk-boycotts-but-still-fall-short-of-expectations)；[中国 4 月跌出前十（-53% MoM）](https://cnevpost.com/2026/05/13/automakers-share-china-nev-market-apr-2026/)。
- **监管/自动驾驶**：[NHTSA 对 320 万辆 FSD 升级到工程分析（recall 前一步）](https://www.insurancejournal.com/news/national/2026/03/20/862650.htm)；[Robotaxi 17 起事故、约人类 4 倍](https://www.cbsnews.com/news/tesla-robotaxi-austin-14-crashes-nhtsa/)。
- **监管积分**：[Q1 $380M（-36% YoY），2027 可能归零](https://carboncredits.com/tesla-q1-2026-hits-22-38b-revenue-but-do-weak-deliveries-and-falling-credits-expose-a-fragile-growth/)。

### 资金面（解禁/增发/内部人卖出/降评级）
- **稀释**：[2018 年 304M 股奖励已 S-8 注册](https://www.sec.gov/Archives/edgar/data/1318605/000162828026026551/tsla-20260422.htm)，但**锁定至约 2033**；[2025 年 $1T 奖励 424M 股期权](https://www.cnbc.com/2025/11/06/tesla-shareholders-musk-pay.html)按 7.5-10 年里程碑解锁——近期流通盘稀释**低**（dilution 1），主要拖累是 $9.97B SBC 费用入表。
- **内部人**：[董事会成员持续 10b5-1 减持](https://finance.yahoo.com/news/tesla-insider-sales-increase-ahead-233118428.html)（Denholm ~$117M、Kimbal ~$31M、Wilson-Thompson ~$10.6M）；Musk 无公开市场卖出。→ lockup_insider_supply 2。
- **评级**：[共识"持有"（47 家：18 强买/18 持有/6 卖）](https://stockanalysis.com/stocks/tsla/ratings/)，[JPM 6/5 从 $145 大幅上调至 $475](https://www.gurufocus.com/news/8903458/jpmorgan-upgrades-tesla-tsla-outlook-after-analyst-change)（深空头投降），[GLJ 维持 $25 极空](https://stockanalysis.com/stocks/tsla/ratings/)。

### 期权市场怎么看（中证据）
[30 天 IV ~48%、IV 百分位仅 ~33-38（不贵）](https://www.alphaquery.com/stock/TSLA/volatility-option-statistics/30-day/iv-mean)、[P/C 0.64（偏多）](https://fintel.io/sopt/us/tsla)。期权没在恐慌定价，Q2 财报前 straddle 不算贵。**skew 与财报隐含跳空待核实**（查 optioncharts.io/options/TSLA/volatility-skew、Market Chameleon 财报页）。

### 下行情景
若 Robotaxi/Cybercab 监管/放量低于预期 + 监管积分归零 + 欧洲结构性流失，市值向"汽车 only"回归——多家估值框架指向 [$100-150（约 -63%~-75%）甚至更低](https://www.tradingkey.com/analysis/stocks/us-stocks/261732341-tesla-2026-stock-analysis-ai-robotaxi-valuation-tradingkey)。

### 什么情况说明判断错了（kill-switch）
1. **Robotaxi 现金收入迟迟不放量**：年底前 Cybercab 部署 <1 万辆、Austin 单位经济跑不通 → 占市值约 $1T 的非汽车估值无近期盈利锚。
2. **汽车毛利跌回 18% 以下**：Q2 清库存被迫降价 + 积分 <$300M/季 → "毛利复苏"叙事破。
3. **Musk 把主要精力转向 xAI/X**：若 Q3 披露其投入 Tesla <50% 工作时间 → $56B 薪酬的人力资本理由崩，机构可能逼宫治理重整。
4. **美/欧份额继续下滑** → `core_customer_loss` 从"严重惩罚"升级为**红线封顶**。

## 结论复述 + 下一步要核实 + 催化/日历

### 结论复述
中等的生意（质量 54）+ 几乎完美的定价（买点 20）+ 治理/监管/竞争/品牌四重风险（惩罚 −42）＝ **现价回避**。等估值大幅回落、或 Robotaxi 真正放量验证单位经济，再重新评估——现在这个价＋这些风险不值得追。

### 下一步要核实
| # | 待核实项 | 为什么没查到 | 查证路径 |
|---|---|---|---|
| 1 | 期权 skew / 25-delta 风险反转、财报隐含跳空 | 需实时期权终端，公开页未稳定 | optioncharts.io/options/TSLA/volatility-skew；Market Chameleon TSLA 财报页 |
| 2 | Q2 2026 财报确切日期 | 两源冲突（7/22 vs 7/29） | ir.tesla.com 财报日历 |
| 3 | NHTSA 320 万辆 FSD 工程分析结论 | 调查进行中，尚无结果 | nhtsa.gov 调查页 + Tesla 8-K |
| 4 | Robotaxi 扩城实际进度与车队规模 | 公司仅给目标城市、无确认日期 | Tesla IR / 各州监管批文 |
| 5 | 净化一次性项后的真实汽车毛利 | Q1 含未拆分的保修/关税一次性项 | 待 Q2 财报（~7 月）干净季度 |

### 催化 / 日历
| 日期 / 窗口 | 事件 | 类型 | 强度 |
|---|---|---|:--:|
| **2026-06-16/17** | [FOMC 议息](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)（高估值成长股对利率敏感） | 宏观 | 强 |
| **~2026-07-02** | Q2 交付与产量报告（库存悬念验证点） | 业绩节奏 | 中 |
| **~2026-07** | FSD v15 重写推送（Robotaxi 放量前提） | 产品/技术 | 中 |
| **~2026-07-22/29** | Q2 2026 财报（日期待核实） | 业绩节奏 | 强 |
| **2026-07-28/29** | [FOMC 议息](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) | 宏观 | 强 |
| **2026 7 月底/8 月** | [Optimus V3 发布/产线启动](https://electrek.co/2026/04/22/tesla-optimus-production-fremont-model-sx-line/) | 产品/技术 | 中 |
| **~2026 年中后** | Robotaxi 扩城（Phoenix/Miami/Vegas 等，可能滑期） | 产品/监管 | 中/弱 |
| **2026 H2** | 年度股东大会（日期 TBD）；NHTSA 工程分析结论 | 治理/监管 | 中 |
| **~2028 / ~2033** | 2018 薪酬期权可行权 / 股份可卖出 | 筹码面 | 弱 |

## 证据与来源（强/中/弱）
- Q1 2026 业绩（$22.39B、EPS $0.41、GM 21.1%）— [Electrek](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-financial-results/) / [TIKR](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative) — **强**
- 交付 358K/库存 50K — [CNBC](https://www.cnbc.com/2026/04/02/tesla-tsla-q1-2026-vehicle-delivery-production.html) — **强**
- 一次性保修/关税项 — [Electrek](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-one-time-benefits-warranty-tariff-refunds-margins/) — **中**
- 估值（P/E、P/S、PEG、目标价）— [StockAnalysis 统计](https://stockanalysis.com/stocks/tsla/statistics/) / [预测](https://stockanalysis.com/stocks/tsla/forecast/) — **强**
- 欧洲 -44% / 美国份额新低 — [Electrek](https://electrek.co/2026/02/02/tesla-tsla-cant-find-bottom-europe-2026-brutal-decline/) / [US News](https://www.usnews.com/news/business/articles/2026-04-02/tesla-sales-rise-after-brutal-year-of-musk-boycotts-but-still-fall-short-of-expectations) — **强**
- NHTSA 320 万辆工程分析 — [Insurance Journal](https://www.insurancejournal.com/news/national/2026/03/20/862650.htm) — **强**
- $25B capex / -$8.5B FCF — [TechCrunch](https://techcrunch.com/2026/04/22/tesla-just-increased-its-capex-to-25b-heres-where-the-money-is-going/) — **强**
- $56B/2018 奖励 S-8 与锁定 — [Electrek](https://electrek.co/2026/04/27/tesla-files-deliver-elon-musk-56-billion-pay-package-shares/) / [SEC S-8](https://www.sec.gov/Archives/edgar/data/1318605/000162828026026551/tsla-20260422.htm) — **强**
- DCF/GF Value 深度高估 — [Alpha Spread](https://www.alphaspread.com/security/nasdaq/tsla/dcf-valuation/base-case) / [GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/TSLA) — **中**
- 期权 IV/PC — [AlphaQuery](https://www.alphaquery.com/stock/TSLA/volatility-option-statistics/30-day/iv-mean) — **中/弱**
- skew / 财报隐含跳空 / Q2 确切日期 — **待核实**

> 研究判断，不构成交易建议；是否买入由你决定。各因子打分基于上述联网取证，价格/数据随时变动，关键项请在下单前自行复核。
