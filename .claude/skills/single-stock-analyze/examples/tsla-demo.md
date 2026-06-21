# 示例：TSLA（Tesla, Inc.）成长股投资判断（worked example）

> **本示例由真实 8-agent 联网重跑生成，数据截至 2026-06-21。**
> 由 single-stock-analyze 的 **8-agent 完整 fan-out**（`company-profiler` + `earnings-analyst` + `growth-analyst` + `moat-economics-analyst` + `valuation-analyst` + `risk-analyst` + `positioning-options-analyst` + `management-analyst`）联网取证后，`judge-synthesizer` 综合出分并按 13 节模板成文。展示本 skill 的标准输出形态：**结论先行 + 评分卡 + 13 节报告**，每条结论标证据等级（强 / 中 / 弱 / 待核实）、来源给可点击超链接、催化日历排密。价格与数据随时变动，**研究用途，不构成投资建议**。

本文件从 `assets/stock-verdict-template.md` 端到端填出，内部一致：第 2 节「评分卡」嵌入的 JSON 经 `scripts/growth_scorecard.py` 算出的 verdict（`暂不值得 / 回避`，总分 23.6）与第 1 节「结论」一致。

---

# TSLA（Tesla, Inc.）成长股投资判断

## 结论
**暂不值得 / 回避（当前价位）**　｜　信心：中高
质量分 65.0 / 买点分 28.0 / 总分 23.6
一句话：Tesla 是一家真实的、护城河多重的好公司（质量分 65），但市场正在**边际上重估它最核心的两件事——增长持续性与治理可信度**：汽车主业 2025 年首次年度负增长、欧洲/中国品牌结构性受损，而 ~$1.50 万亿市值（[前瞻 P/S ~14×、Rule-of-40 仅 ~12](https://stockanalysis.com/stocks/tsla/statistics/)）几乎全部押在尚未变现的 Robotaxi/Optimus 期权上——叠加治理（$1 万亿薪酬 + $5.73 亿关联交易 + $2B xAI→SpaceX 转换）与监管（四项 NHTSA 调查 + DOJ/SEC FSD 欺诈调查）双 4 分惩罚，把总分从 57.6 的原始因子分压到 23.6。**好公司，但市场正在重估增长持续性与治理可信度、且现价已透支期权价值 → 现价回避，等期权变现或估值 reset。**

> 这与卖方共识基本一致：[27 位分析师"持有"、均值目标价 ~$395–420（≈ 现价）](https://stockanalysis.com/stocks/tsla/ratings/)，目标价区间却横跨 [$25（GLJ）到 $600+（Wedbush）](https://www.benzinga.com/quote/TSLA/analyst-ratings)——市场对"如何给期权定价"毫无共识。本 skill 把"期权值不值这个价 + 治理/监管风险负荷"算进结论，给"回避"。**红线未触发**，但 DOJ/SEC FSD 调查若升级即可能触发 `accounting_fraud_suspicion`（见第 11 节「⚠️ 风险与利空」）。

## 评分卡

### 评分卡输入 JSON（喂给 `scripts/growth_scorecard.py`）

```json
{
  "ticker": "TSLA",
  "company": "Tesla, Inc.",
  "factors": {
    "revenue_growth_durability": 3,
    "tam_penetration": 4,
    "moat_chain_position": 4,
    "unit_economics_profit_path": 3,
    "product_customer_momentum": 3,
    "management_capital_allocation": 2,
    "valuation_growth_match": 1,
    "entry_expectations": 2
  },
  "penalties": {
    "dilution_financing": 2,
    "customer_concentration": 1,
    "accounting_quality": 1,
    "governance": 4,
    "competition_disruption": 1,
    "regulation_geopolitics": 4,
    "liquidity_bubble": 3,
    "lockup_insider_supply": 1
  },
  "red_lines": {
    "accounting_fraud_suspicion": false,
    "core_customer_loss": false,
    "growth_engine_broken": false
  },
  "what_could_weaken_view": [
    "Cybercab/Robotaxi 2026 内提前放量并贡献可见收入（管理层指引 2027 才 material），把期权价值兑现，推翻'故事尚未变现'的判断",
    "DOJ/SEC FSD 营销欺诈调查若升级为正式起诉或处罚，accounting_fraud_suspicion 红线可能被触发，结论从'回避'转为'红线封顶'",
    "汽车毛利率剔除一次性后回到 17-18% 并继续走低、Q2 交付再 miss，则 unit_economics 与 revenue_growth_durability 应下调"
  ]
}
```

脚本输出（关键行）：`结论：暂不值得 / 回避｜总分 23.6｜质量分 65.0｜买点分 28.0｜原始因子分 57.6｜惩罚扣分 34.0｜红线：未触发`

### 因子（前 6 项＝质量分共 80，后 2 项＝买点分共 20）
| 因子 | 评分(0-5) | 权重 | 得分 | 轴 |
|---|---:|---:|---:|---|
| revenue_growth_durability | 3 | 18 | 10.8 | 质量 |
| tam_penetration | 4 | 14 | 11.2 | 质量 |
| moat_chain_position | 4 | 14 | 11.2 | 质量 |
| unit_economics_profit_path | 3 | 14 | 8.4 | 质量 |
| product_customer_momentum | 3 | 12 | 7.2 | 质量 |
| management_capital_allocation | 2 | 8 | 3.2 | 质量 |
| valuation_growth_match | 1 | 12 | 2.4 | 买点 |
| entry_expectations | 2 | 8 | 3.2 | 买点 |

总分 **23.6**　｜　质量分 **65.0**　｜　买点分 **28.0**　｜　原始因子分 57.6

### 惩罚项（×2 倍率，合计扣 34.0 分）
| 惩罚项 | 评分(0-5) | 扣分 | 理由 |
|---|---:|---:|---|
| dilution_financing | 2 | 4.0 | SBC Q1 2026 飙至 $10.3 亿（+80% YoY）、年化 ~$44 亿且无回购对冲；2025 CEO 薪酬方案 4.237 亿股（占已发行股本 ~12%）为多年稀释悬顶——但近期无 ATM/S-3 增发，$447 亿现金无被动稀释压力 [中]。 |
| customer_concentration | 1 | 2.0 | 个人/B 端客户高度分散，无单一客户达营收 10%；惩罚低分仅来自地理集中（美国 49% + 中国 22% ≈ 71%），但该项主要计入 regulation_geopolitics [强]。 |
| accounting_quality | 1 | 2.0 | 现金流与利润大体匹配（OCF $39.4 亿 vs GAAP 净利 $4.77 亿，差异为 SBC/折旧合理项）；红旗在于 Q1 毛利含 ~$4.8 亿一次性（关税退款 + 质保拨回）粉饰、且公司不单项披露金额，使"干净经常性毛利"不可验证 [中]。 |
| governance | 4 | 8.0 | 严重治理问题：董事会主席 Denholm 自 2014 累计获 $6.82 亿薪酬、独立性受特拉华法院质疑；2025 年 $1 万亿薪酬方案在 Musk 公开威胁离职下强行通过（ISS/Glass Lewis 均反对）；$5.73 亿关联交易网络；$2B xAI 投资未经再批准即转为 SpaceX 股权——多条 [强] 证据。 |
| competition_disruption | 1 | 2.0 | 竞争加剧但护城河尚未被实质击穿：全球 BEV 销量被 BYD 超越（2025 年 BYD 226 万 vs Tesla 164 万）、美国份额从 49%→46%、欧洲 13 个月连降；但 Tesla 仍保 FSD 数据飞轮 + 充电网络 + 美国 EV 利润领先，Q1 2026 还短暂夺回纯电季度销冠 [中]。 |
| regulation_geopolitics | 4 | 8.0 | 监管/地缘风险密集：四项并行 NHTSA 调查（FSD 涉 290 万辆、Autopilot、门把手、低能见度）、DOJ（刑事）+ SEC（民事）FSD 营销欺诈调查、$7,500 美国 EV 税收抵免 2025 年 7 月取消、欧洲连降 + 中国零售同比 -45%、关税与 TSMC 芯片地缘敞口——多条 [强] 证据。 |
| liquidity_bubble | 3 | 6.0 | 估值泡沫化但流动性极好：P/S 15.3×、EV/EBITDA 133×、前瞻 P/E ~194×、PEG ~8×，全部远超纯汽车可比（BYD ~1×、Rivian ~4×），溢价全押 AI/Robotaxi 期权；高估值对利率/风险偏好高度敏感，但日均成交 4,480 万股、机构持股 66%，无流动性枯竭 [强/中]。 |
| lockup_insider_supply | 1 | 2.0 | 近期筹码面供给压力低：Musk 2026 年 6 月行权 3.04 亿份期权但**零公开市场卖出**，新股锁定至 2028 年 1 月 + 5 年限售（到 2033）；董事级减持温和（12 个月共 ~$1.64 亿，多为例行）；空头仅 2.56% 流通盘、1.7 天回补 [强/中]。 |

> 红线虽未触发，但 governance(4) + regulation_geopolitics(4) 两项满载惩罚 = 扣 16 分，是把"质量 65 的好公司"打到"总分 23.6 回避"的主因。

### 红线（kill-switch）
| 红线 | 状态 | 说明 |
|---|:--:|---|
| accounting_fraud_suspicion | 未触发 | DOJ/SEC 就 FSD 营销欺诈展开刑事/民事调查，但仍处**信息收集阶段**，无正式起诉、无审计师辞任/非标意见、无财报重述——未达红线证据门槛。**这是最接近触发的一条**，若升级为正式指控即可能封顶 [中]。 |
| core_customer_loss | 未触发 | 零售消费者业务高度分散，无核心大客户可"流失"；不适用 [强]。 |
| growth_engine_broken | 未触发 | 2025 年首次年营收 -3% 一度逼近，但 Q1 2026 重回 +16% 增长、能源 FY2025 +27%、FSD 订阅 +51%——增长引擎放缓但未失效 [强]。 |

## 🏢 公司介绍 / 核心产品
> **结构化优先** — 表格驱动；每条标证据级（强/中/弱/待核实）+ 来源链接。本节为**描述性事实**；竞争壁垒能否持续的判断在第 7 节「护城河 / 产业链位置」。

### 一句话画像 + 商业模式
Tesla 是一家深度垂直整合的电动汽车与清洁能源公司，正从整车制造商向 **AI 自动驾驶 / 机器人 / 能源平台**转型，以 Model Y/3 为基石，以 FSD 订阅、Megapack 储能、Robotaxi 和 Optimus 为增长引擎 [强]。

**商业模式**：硬件主导 + 软件/服务快速增长的混合模式。变现方式：(1) **汽车销售**（一次性，Q1 2026 占 72.5% 收入）——直销无经销商；(2) **FSD 自动驾驶订阅**（经常性，2026 年 2 月起转纯订阅 $99/月，Q1 2026 活跃 128 万、年化 ARR ~$5.46 亿）；(3) **Megapack/Powerwall 储能**（项目制，毛利率 28–40%）；(4) **服务与其他**（充电、保险、二手车、碳积分——经常性成分上升）；(5) **Robotaxi 按里程抽佣**（导入期，Austin 已商业运营）；(6) **Optimus 人形机器人**（尚无商业收入）。整体经常性收入占比在提升但仍 <20% [强]。碳积分 FY2025 收入 $1.99B（[政策敏感、同比 -28%](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026003952/tsla-20251231.htm)）[强]。

### 业务分部与收入拆分
| 分部 | 收入 | 占比% | YoY | 毛利特征 |
|---|---:|---:|---:|---|
| 汽车（Automotive） | FY2025 $69.53B / Q1'26 $16.23B | FY25 73.3% / Q1'26 72.5% | FY25 **-9.8%** / Q1'26 **+16%** | Q1'26 含碳积分 21.1%、剔除 19.2%（vs Q4'25 17.9%），近 8 季最高；含 ~$4.8 亿一次性（关税退款+质保拨回）粉饰 [强] |
| 能源发电与储存（Energy） | FY2025 $12.77B / Q1'26 $2.41B | FY25 13.5% / Q1'26 10.8% | FY25 **+26.6%** / Q1'26 **-12%** | Q1'26 毛利率 39.5%（含 ~$2.5 亿一次性关税收益），基准 ~28.7%；FY2025 部署 46.7 GWh（+49%），最高增速分部 [强/中] |
| 服务与其他（Services & Other） | FY2025 $12.53B / Q1'26 $3.75B | FY25 13.2% / Q1'26 16.7% | FY25 **+19.0%** / Q1'26 **+42%** | Q1'26 毛利率 9.2%（偏低，被二手车/碰撞维修拖累）；增长引擎为 Supercharger/FSD/保险，最快增长分部 [强] |

来源：[evwire Q1 2026 财报](https://evwire.com/p/tesla-tsla-q1-2026-earnings-results)（强）、[Yahoo FY2025 营收](https://finance.yahoo.com/news/tesla-revenue-slips-2025-energy-163645200.html)（强）、[bullfincher 分部历史](https://bullfincher.io/companies/tesla/revenue-by-segment)（强）。**FY2025 总收入 $94.83B（-3% YoY），为 Tesla 上市以来首次年度收入下滑** [强]。

### 核心产品 / 服务
| 产品/服务 | 是什么 | 卖给谁 | 变现/定价 | 收入占比 | 生命周期阶段 |
|---|---|---|---|---:|---|
| Model Y（Juniper 刷新版） | 中型 SUV，2025 全面刷新，续航升至 447 英里 | 全球 C 端 + B 端车队 | 整车直销 + FSD $99/月 | Model 3/Y 合占 Q1'26 交付 95.5%、汽车分部 ~75%+ | 成熟期（刷新后重新放量） |
| Model 3（Highland 刷新版） | 紧凑型轿车，欧洲占比高 | 全球 C 端 | 整车直销 + FSD + 服务 | 与 Model Y 合并报告（全年交付 97%） | 成熟期 |
| Cybertruck | 不锈钢全尺寸电动皮卡 | 北美 C 端 + 工程/农业 | 整车直销（高 ASP $80K–120K） | Q1'26 "Other" 16,130 辆（4.5%）；收入估 5–8% | 放量期（产能爬坡） |
| Tesla Semi | 纯电动重卡，续航 ~500 英里 | 大型物流/食饮企业 B2B | 整车销售（估 $150K+） | 量极小，待核实 | 导入期 |
| Megapack | 集装箱式电网级储能（~3.9 MWh/台） | 公用事业/IPP/工业 B2B | 按系统销售（项目制） | 能源分部主力（FY25 $12.77B 大部分） | 放量期（上海'25 投产、休斯顿'26 启动） |
| Powerwall / 太阳能屋顶 | 住宅电池储能（13.5 kWh）+ 光伏 | 住宅业主 C 端 | 硬件销售 + 安装 | 能源分部次要，待核实 | 成熟期 |
| FSD 订阅 | 完全自动驾驶软件（监督级，OTA 升级） | Tesla 车主 B/C 端 | 月订阅 $99/月（经常性） | 归入汽车/服务，ARR ~$5.46 亿（年化收入 ~2.4%） | 放量期（订阅 +51% YoY） |
| Supercharger 网络 | 自有快充网络（8,182 站/77,682 接头） | Tesla + 第三方 EV C 端 | 按 kWh 计费 | 服务收入主驱动之一，独立占比待核实 | 放量期（NACS 成北美标准） |
| Tesla Insurance | 实时驾驶行为定价车险（美国 ~12 州） | Tesla 车主 C 端 | 月保费（经常性） | 含于服务，待核实 | 放量期（覆盖州数快增） |
| Cybercab Robotaxi | 无方向盘双座自动驾驶出租车 | 普通消费者 C 端（替代 Uber/Lyft） | 按里程/时间抽佣（平台模式） | 收入极小（导入期） | 导入期（Austin 已商业运营） |
| Optimus 人形机器人 | 自研人形机器人，内部物料搬运 | 制造业 B2B（长期全行业） | 硬件销售 + 可能 RaaS | 尚无外部商业收入 | 导入期（2027 起对外） |

来源：[evwire Q1 2026](https://evwire.com/p/tesla-tsla-q1-2026-earnings-results)（强）、[FSD 订阅破 128 万](https://www.basenor.com/blogs/news/tesla-fsd-hits-1-28m-subscribers-in-q1-2026-record-growth)（强）、[Cybercab 4 月量产](https://www.basenor.com/blogs/news/tesla-cybercab-production-starts-april-2026-the-autonomous-era-begins)（中）、[Optimus/Model S/X 转产](https://carboncredits.com/tesla-shifts-from-evs-to-ai-musk-says-robots-will-be-80-of-company-value/)（中）。

### 客户
主要客户为**全球消费者个人（C 端）** 和工商业主体（B 端），高度分散，无单一客户集中度风险。三类：(1) **汽车端（73% 收入）**——终端消费者直购为主，无经销商；大客户含租车公司（Hertz 曾批量采购后部分退订）、企业车队、政府采购。(2) **能源端（14% 收入）**——Megapack 面向公用事业/IPP/工业，单项目数百万至数千万美元但客户分散，无单客户超 10% 营收公开披露；Powerwall 面向住宅。(3) **服务端（13% 收入）**——Supercharger 以 Tesla 车主为核心（2023 后开放非 Tesla EV）、保险以车主为主，FSD 订阅达 128 万（12% 车主渗透率）。**地理集中度**：[美国 48.9% + 中国 22.1%（FY2025）合计 71%](https://metricshour.com/blog/tesla-revenue-by-country-how-exposed-is-tsla-to-china-and-europe/)，中国市场地缘敞口显著 [强]。
> 客户集中度的**扣分**见第 11 节「⚠️ 风险与利空」（`customer_concentration`=1，主因地理而非单客户），此处只描述。

### 竞品分析
| 对手 | 产品/定位 | 相对规模/市占 | 与本公司正面交锋点 |
|---|---|---|---|
| **BYD（比亚迪）** | 全球销量第一纯电+插混，中低到中高端，电池/半导体自研 | FY2025 全球 BEV ~226 万 vs Tesla ~164 万；全球纯电份额 ~17% vs ~9%；2025 总营收已超 Tesla | 中国正面竞争（Model 3/Y vs 汉/海豹/海鸥）、欧洲快速渗透（Tesla 欧洲'25 前 11 月 -40%）、储能亦有竞品；不入 Robotaxi/FSD 赛道 |
| **GM（Chevy/Cadillac/GMC）** | 传统巨头转型 EV，Ultium 平台，美国品牌认知强 | 美国 EV 份额 ~13–15%（美国第二）；全球远小于 BYD/Tesla | 美国中型 SUV/皮卡（Model Y vs Equinox EV；Cybertruck vs Silverado EV）；依赖联邦补贴（已取消承压） |
| **Waymo（Alphabet）** | Robotaxi 商业运营领导者，激光雷达+HD 地图（对立纯视觉） | FY2025 完成 1,400 万次全自动行程、收入 ~$2.86 亿；估值 ~$450 亿 | Robotaxi 直接竞争（Austin vs Austin）；技术路线之争（纯视觉 vs 多传感器融合） |
| **Rivian** | 美国纯电皮卡/SUV 初创，R2/R3 剑指 Model Y 价格带 | 2025 交付 ~5.1 万辆，美国份额 ~2%，市值 ~$150 亿 | Model Y vs R2、Cybertruck vs R1T；与 Uber 合作 Robotaxi 中期竞争 |
| **现代/起亚** | 韩系 IONIQ/EV 系列，美国第四大 EV 品牌，建 Metaplant Georgia | 美国 EV 份额 ~5%；2025 美国销量 ~9 万辆 | 中型 EV（Model Y vs IONIQ 5/EV6）；IONIQ 5 N vs Model 3 Performance |
| **CATL（电池供应竞争）** | 全球最大第三方动力电池厂 | 全球动力电池份额 ~37%（2025）；Tesla 仍采购部分 LFP | Tesla 4680 自研内制化（目标 2026 全自供）以降低成本并减少对 CATL 依赖 |

来源：[BYD 夺全球 BEV 冠](https://electrek.co/2026/01/02/byd-crushes-tesla-all-electric-sales-for-2025-secures-global-bev-crown/)（强）、[美国 EV 份额](https://cleantechnica.com/2026/02/04/tesla-had-46-of-us-ev-market-in-2025-down-from-49-in-2024-gm-13-ford-7/)（强）、[Waymo vs Tesla](https://www.programming-helper.com/tech/waymo-tesla-robotaxi-race-autonomous-vehicle-market-2026)（中）、[BYD 产能对比](https://evboosters.com/ev-charging-news/tesla-vs-byd-a-battle-of-global-production-capacity/)（中）。

### 竞争力分析
**强项（事实层）**：① **超级充电网络壁垒**——全球 8,182 站/77,682 接头，行业最大自有快充网络，NACS 已成北美标准（Ford/GM/Hyundai/Rivian/BMW/Toyota 全采纳）[中]；② **垂直整合深度**——锂精炼→正极→4680 电芯→整车→销售→保险→充电全链自研，4680 已成最低成本内制电芯 [中]；③ **FSD 数据飞轮**——10.05 亿累计自动驾驶英里（42× Waymo）、128 万付费订阅，数据资产无对手匹敌 [中]；④ **直销 + 软件 OTA**——无经销商、迭代快 [强]；⑤ **美国品牌定位**——[美国 EV 份额 ~46–59%](https://cleantechnica.com/2026/02/04/tesla-had-46-of-us-ev-market-in-2025-down-from-49-in-2024-gm-13-ford-7/)、车主忠诚度高 [强]；⑥ **能源规模化**——上海+休斯顿 Megafactory 规划 90 GWh，高毛利且增速快 [强]。

**弱项（事实层）**：① **全球份额被 BYD 超越**（BYD 2025 BEV 226 万 vs Tesla 164 万）、欧洲'25 前 11 月 -40% [强]；② **产品线集中**——Model 3/Y 占交付 97%，单车型依赖高 [强]；③ **自动驾驶商业化落后 Waymo**（后者已 1,400 万次行程有营收）[中]；④ **Musk 精力分散**（同领 SpaceX/xAI/X/DOGE）[中]；⑤ **关税与供应链**——部分车型仍依赖 CATL LFP、4680 国产化爬坡中 [中]；⑥ **FY2025 首次年营收下滑** -3% [强]。
> 本节只列事实层强弱；壁垒**能否持续**见第 7 节「护城河 / 产业链位置」。

### 产业链位置
Tesla 在电动汽车价值链中占据**高度垂直整合的中下游整车+软件+能源一体化**位置 [强]：
- **上游**：部分自产（4680 电芯、正极内制、Robstown 锂精炼），仍从 CATL/Panasonic 采购部分电芯；
- **中游**：自有 Gigafactory 制造（Fremont/上海/柏林/Texas）+ 自研软件（FSD/Autopilot/OS/Dojo）；
- **下游**：直销→交付→服务（Supercharger/保险/维修/OTA）→数据回流训练 FSD；
- **能源链**：Megapack 制造→电网侧储能集成/运营，扮演 EPC 类角色；
- **Robotaxi**：既是整车制造商（Cybercab）又是出行平台运营者（Tesla Network），近似 Uber+Tesla 合一。

**议价权**：对消费者较强（直销无中间商）；对上游核心矿材（锂/镍/钴）仍有依赖，通过长期锁价+自建精炼减少敞口；对公用事业 Megapack 客户中等议价权（CATL/BYD 在争夺）[中]。

### 公司沿革与规模
**关键里程碑**：2003 创立 → 2008 Roadster 交付、Musk 任 CEO → 2010 NASDAQ IPO（$17/股）→ 2012 Model S → 2017 Model 3 大众化 + FSD 预购确认 → 2020 Model Y + 上海投产 + 纳入 S&P 500 → 2021 首次年度盈利（$5.52B）→ 2023 Cybertruck 量产 + FY 收入 $96.77B 历史新高 + Supercharger 开放 → 2024 交付 178.9 万（-1%）、价格战压毛利、Musk 转向 DOGE → **2025 FY 收入 $94.83B（-3%，首次年降）、交付 163.6 万（-8.6%）、BYD 超越成全球最大 BEV、能源 +27% 创新高、Robotaxi 软启动** → **2026（截至研究日）Q1 收入 $22.39B（+16%）、毛利率 21.1%（8 季最高）、Cybercab 量产+运营、FSD 转纯订阅、宣布 $25B+ 资本支出、入股 SpaceX $20 亿** [强/中]。

**规模指标（2025 年底/2026 年初）**：员工 [100,883 人](https://sqmagazine.co.uk/how-many-people-work-at-tesla/)（+2.8% YoY）[中]；6 座 Gigafactory（Fremont/Austin/Reno/上海/柏林/Buffalo）+ 上海/休斯顿 Megafactory；汽车年产能 ~235 万辆；[股价 ~$400、市值 ~$1.50 万亿、流通股 ~37.6 亿](https://capital.com/en-int/market-updates/tesla-stock-forecast-03-06-2026)（中）；收入地理 [美国 $47.73B（48.9%）/ 中国 $20.96B（22.1%）/ 其他 $26.24B（27.7%）](https://metricshour.com/blog/tesla-revenue-by-country-how-exposed-is-tsla-to-china-and-europe/)（强）。

## 投资逻辑
**多头逻辑（why own）**：Tesla 是**两个故事的叠加**——(1) 一家正在企稳的好汽车+能源公司：Q1 2026 重回 +16% 增长、毛利率 21.1%（8 季最高）、能源 FY2025 +27%、FSD 订阅 +51% 至 128 万、Q1 短暂夺回纯电季度销冠 [强]；(2) 一个尚未变现的 **AI/Robotaxi/Optimus 期权**：TAM 跨 EV+自动驾驶+储能+人形机器人四条曲线、合计数万亿美元，Tesla 在其中两条（EV、储能）已是龙头，护城河多重（充电网络、数据飞轮、垂直整合）[中/弱]。

**空头逻辑（why avoid now）**：当前 ~$1.50 万亿市值几乎**全部押在第二个故事上**，而管理层自己指引 [Robotaxi 2026 内不 material、2027 才放量](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap)、Optimus 2027 才对外销售 [强]。第一个故事的基本面在**结构性走弱**：2025 首次年营收负增长、欧洲 13 个月连降、中国零售 -45%、美国份额从 49%→46% [强]。叠加治理（$1 万亿薪酬 + $5.73 亿关联交易）与监管（四项 NHTSA + DOJ/SEC FSD 调查）双重 4 分惩罚 [强]。

**净判断**：好公司（质量 65），但**市场正在重估增长持续性与治理可信度**、且现价已透支期权价值（买点 28）——惩罚把总分压到 23.6，**现价回避**。要么等期权变现（Cybercab/Optimus 见到收入），要么等估值 reset。

## 增长引擎 + 市场空间
**近期增长引擎（已变现）**：① **汽车复苏**——Q1 2026 +16% YoY 至 $16.23B，但交付 +6% 显著弱于生产 +13%，[产销缺口 5 万辆、库存天数 15→27 天](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-earnings-results/)，需求信号偏软 [强]；② **FSD 订阅飞轮**——128 万付费（+51% YoY），ARR ~$5.46 亿，2026 年 2 月转纯订阅扩大漏斗 [中]；③ **能源储能**——FY2025 +27% 至 $12.8B、~30% 毛利（最高分部），但 Q1 2026 部署 8.8 GWh（环比 -38%、同比 -15%，低于 12–14 GWh 预期，管理层称项目时点）[强]；④ **服务**——Q1 +42%（最快），Supercharger/保险/FSD 驱动 [强]。

**高期权增长引擎（尚未变现，2027+）**：⑤ **Cybercab/Robotaxi**——2026 年 4 月量产、Austin 等 3 城已对公众收费，[Musk 指引 2026 不 material、2027 才显著](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap) [强]；⑥ **Optimus**——零外部收入，[Musk 称"史上最大产品"、2027 对外](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap) [强]。

**市场空间（TAM）**：EV（[全球 EV 渗透率 ~19.8%、美国 BEV 仅 5.5%](https://recharged.com/articles/ev-sales-statistics-2026) [中]）+ 电网储能（[IEA 2030 需扩 35×](https://www.iea.org/energy-system/electricity/grid-scale-storage) [中]）+ Robotaxi（[$147B by 2033，但测算高度投机](https://www.nasdaq.com/articles/one-analyst-thinks-teslas-robotaxi-revenue-could-soar-250-billion-2035-here-are-3-things) [弱]）+ 人形机器人（[$38B by 2035 [弱]](https://www.adamasintel.com/tesla-could-capture-half-the-humanoid-robot-market-in-the-us-by-2027/)）。TAM 真实巨大、Tesla 在两条曲线领先，但**最大的两条曲线（Robotaxi/Optimus）当前几乎 pre-revenue**——`revenue_growth_durability`=3（复苏真实但中速、2025 暴露脆弱性）、`tam_penetration`=4（TAM 巨大、份额领先，但大曲线变现要 1–2 年）、`product_customer_momentum`=3（FSD/Robotaxi 催化真实，但交付 miss + 库存堆积 + 储能 GWh 下滑引入不确定）。2026 全年收入共识 [~$102–105B（隐含 ~8% 增速）](https://stockanalysis.com/stocks/tsla/forecast/) [中]。

## 📊 最近财报重点
**Q1 2026（截至 2026-03-31，4 月 22 日发布）质量上行、叙事承压**：
- **营收 $22.387B（+15.8% YoY），beat 共识 ~$4.6 亿**；[毛利率 21.1%（+478bp YoY，5 季最高）](https://evwire.com/p/tesla-tsla-q1-2026-earnings-results)；调整后 EPS $0.41（+52% YoY，beat ~14%）[强]。
- **盈利质量喜忧参半**：经营利润 $941M（+91% YoY，营业利润率 4.2%）；GAAP 净利仅 $477M（被 $10.3 亿 SBC + 比特币减值压制），non-GAAP $1.45B [强]。
- **现金流**：[OCF $3.94B（+83%）、资本支出 $2.49B、FCF $1.44B（+117%）、现金及短投 $44.74B](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative)（+21% YoY）[强]。
- **电话会震撼弹**：[全年资本支出指引上调 $5B 至"超 $25B"（前 $20B），CFO 确认 Q2–Q4 2026 FCF 转负，全年 FCF 预计 ~-$8.5B](https://www.foreignpolicyjournal.com/2026/04/24/tesla-tsla-earnings-call-reveals-25-billion-capex-plan-for-ai-optimus-robots-and-cybercab-as-stock-retreats/)，覆盖六工厂+AI 算力+半导体 Fab+Optimus [强]。
- **红旗（财报质量）**：① [产销缺口 5 万辆、成品库存环比 +$20 亿至 $68.4 亿、库存天数 15→27 天](https://www.stocktitan.net/sec-filings/TSLA/10-q-tesla-inc-quarterly-earnings-report-7f5462f3d917.html)——需求弱于供给 [强]；② [碳积分环比 -30% 至 $380M](https://www.cnbc.com/2026/04/22/tesla-tsla-q1-2026-earnings-report.html)——结构性下滑 [强]；③ 毛利含 ~$4.8 亿一次性（关税退款+质保拨回），公司不单项披露 [中]；④ [SBC $1.03B（+80% YoY），未确认 CEO 奖励 $99.7 亿在前](https://www.stocktitan.net/sec-filings/TSLA/10-q-tesla-inc-quarterly-earnings-report-7f5462f3d917.html) [强]；⑤ [HW3 永久无缘无监督 FSD](https://www.shacknews.com/article/148805/tesla-tsla-q1-2026-earnings-call-transcript)，需以旧换新升级，贬损存量车队 [中]。
- **财报后反应**：[盘后初涨 4% 后回吐，次日（4/23）收 -3.56%（$373.60）](https://www.tikr.com/blog/tesla-q1-2026-earnings-beat-so-why-did-the-stock-fall-3-56)，资本支出意外是回吐主因 [中]。
- **综合（earnings-analyst 读数）**：当季在质量轴改善（利润率、经营杠杆），但远期叙事要求 $25B+ 的信任押在 Cybercab/Optimus/FSD 如期兑现——高方差赌注，市场只部分定价。对应 `product_customer_momentum`=3、`management_capital_allocation`=2、`accounting_quality` 惩罚=1、`growth_engine_broken` 红线=未触发。

## 护城河 / 产业链位置
**护城河结构（moat-economics-analyst 判断）**：Tesla 是一组**强度不均**的多层壁垒，软件/服务护城河在拓宽、汽车硬件护城河在收窄。
- **硬护城河（结构性、难复制）**：① **Supercharger 网络**——[~79,900 接头、NACS 成北美标准、30–40% 毛利、$20B 长期收入潜力](https://www.teslarati.com/tesla-tsla-20b-revenue-access-supercharger-nacs-deal-dan-ives/)（弱/中）；② **数据飞轮**——[10.05 亿 FSD 英里、42× Waymo、128 万付费](https://www.notateslaapp.com/news/4042/tesla-hits-546-million-in-annual-recurring-revenue-from-fsd-subscriptions)（中）；③ **垂直整合**——[4680 干电极成最低成本电芯、单车 COGS 一度 <$35K](https://www.nextbigfuture.com/2026/03/tesla-making-lower-cost-batteries-and-cars-late-in-2026-and-in-2027.html)（中）。
- **高质量毛利池**：[能源 39.5% 毛利](https://www.teslaacessories.com/blogs/news/tesla-energy-q1-2026-update-megapack-deployments-surge-to-record-highs-as-utility-scale-storage-transforms-the-grid)（中，含一次性）+ 服务 +42% 增长，部分对冲汽车周期压力。
- **护城河威胁**：① [BYD 垂直整合+规模（2024 交付 4.27M vs Tesla 1.79M）+ 电池专利 1,117 vs 97](https://driveauthority.com/tesla-vs-byd-the-real-battle-for-ev-dominance/)（中）；② [美国份额 49%→46%、GM 近翻倍至 13.2%](https://cleantechnica.com/2026/02/04/tesla-had-46-of-us-ev-market-in-2025-down-from-49-in-2024-gm-13-ford-7/)（强）；③ [$25B+ 资本支出、Q2–Q4 FCF 转负](https://news.alphastreet.com/tesla-tsla-posts-margin-rebound-in-q1-2026-but-25b-capex-surge-raises-stakes/)——护城河投资周期尚未证明（中）。
- **单位经济性/盈利路径**：[剔除碳积分汽车毛利 19.2%（vs Q1'25 12.5%）](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)（强）大幅恢复，但约 $4.8 亿是一次性；FCF Q1 转正但全年转负。**净判断**：`moat_chain_position`=4（强但非不可破——硬件护城河收窄、软件护城河拓宽）、`unit_economics_profit_path`=3（恢复中但杠杆于一次性项 + 重资本支出周期）、`competition_disruption` 惩罚=1（真实但未结构性致命，因美国地位+定价溢价仍在）。

## 👤 管理层 / 领导力
> **定性，不打分**——从"人"的维度判发展潜力。每条标证据级并给来源链接。

### 创始人 / CEO 背景与往绩
Elon Musk 自 [2008 年 10 月任 CEO、2004 年 4 月入董事会](https://ir.tesla.com/corporate/elon-musk)，18 年不间断任期 [强]。长弧产品押注（Model 3、能源、FSD 平台）的往绩非凡，但被**系统性的时间表跳票**所拖累：[L5 自动驾驶承诺 2019、百万 Robotaxi 承诺 2020、无监督 FSD 承诺 2025 年底，现指引"约 Q4 2026"，电话会原话"我只是在猜"](https://en.wikipedia.org/wiki/List_of_predictions_for_autonomous_Tesla_vehicles_by_Elon_Musk) [强]。

### 愿景与战略执行力（said-vs-done）
愿景宏大且兑现过几次（量产化 Model 3、能源做到最高毛利分部），但**最重要的增长论点 FSD/Robotaxi 已跳票 7+ 年**：[Austin Robotaxi 2025 年 6 月启动时仅 ~36 辆且仍有安全员](https://insideevs.com/news/785220/tesla-robotaxi-austin-no-safety-monitor/)，与"车内无人"承诺相悖 [中]；[HW3 被确认永久无法实现无监督 FSD](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap)，逆转了对老车主的多年隐性承诺 [强]。Q1 2026 把资本支出从 $20B 上调至 $25B 并披露 $2B SpaceX 投资 [强]。

### 利益绑定（skin in the game）
Musk 持股 [~15.3–16%](https://capital.com/en-int/analysis/tesla-shareholder-who-owns-the-most-tsla-stock)（全部行权后可至 ~25%），利益绑定深 [强]——这是真实的锚。但 2025 年 [$1 万亿里程碑薪酬方案（4.237 亿股，ISS/Glass Lewis 均反对，75%+ 通过）](https://www.cnbc.com/2025/11/06/tesla-shareholders-musk-pay.html) 在他公开威胁离职背景下通过，绑定与勒索的边界模糊 [强]。

### 团队稳定性 / 关键人物风险
关键人物风险**极端**——战略/路线图/投资论点单点依赖 Musk 一人，且他同时领导 SpaceX/xAI/X/Neuralink/Boring/DOGE [强]。[2024 年 4 月高管出走潮（18 年老将 SVP Baglino + 3 位 VP）是 Tesla 史上最大资深流失](https://www.bloomberg.com/news/articles/2024-04-15/tesla-executive-baglino-leaves-as-musk-loses-another-top-deputy) [强]；CFO Taneja 自 2023 年 8 月稳定 [中]。[Tesla-SpaceX 合并讨论活跃（Wedbush 估 80% 概率）](https://www.cnbc.com/2026/05/26/spacex-tesla-merger-chatter-reignites-as-musk-rocket-company-nears-ipo.html)将是 Musk 第四笔十亿级自我交易，治理风险在升级 [中]。

### 对发展潜力的净判断
管理层**轻度净负面**：Musk 的愿景与持股是真实锚点，但治理质量、精力分散与连环跳票实质拖累评估。本判断**联动**了 `management_capital_allocation`=2（resource diversion + 自我交易拉低资本配置纪律，management-analyst 与 earnings-analyst 同给 2）与 `governance` 惩罚=4（risk-analyst 强证据：$6.82 亿主席薪酬 + $5.73 亿关联交易 + $2B xAI→SpaceX 转换，证据强于 management-analyst 的 1，由 judge-synthesizer 择优取 4）；诚信红线 `accounting_fraud_suspicion` 经评估**未触发**（DOJ/SEC FSD 调查仍信息收集阶段）。结论框信心"中高"已反映这一拖累。

## 单位经济性 / 盈利路径
- **毛利**：Q1 2026 总毛利率 21.1%（+478bp YoY）；[剔除碳积分汽车毛利 19.2%（vs Q1'25 12.5%、Q4'25 17.9%）](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)（强）——真实恢复，但约 $4.8 亿是一次性（关税退款+质保拨回），剔除后经常性 ~17–18% [中]。
- **经营杠杆**：经营利润 $941M、营业利润率 4.2%（+214bp YoY）但环比 Q4'25 的 5.7% 下滑；R&D +38%、SG&A +47%，opex 增速快于收入 [强]。
- **FCF/盈利路径**：Q1 FCF +$1.44B（+117%），但 [CFO 指引 Q2–Q4 转负、全年 ~-$8.5B](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative)（强），因 $25B+ 资本支出（~3× 2025 的 $8.5B）。
- **SBC 拖累**：[Q1 SBC $1.03B（+80% YoY），$9.97B 未确认 CEO 奖励在前](https://www.stocktitan.net/sec-filings/TSLA/10-q-tesla-inc-quarterly-earnings-report-7f5462f3d917.html)（强）——多年 GAAP EPS 逆风。
- **净判断**：`unit_economics_profit_path`=3——毛利健康且恢复、$44.7B 现金充裕，但杠杆于一次性项 + 重资本支出周期使全年自我造血转负，盈利路径清晰但"投资周期回报尚未证明"。

## 估值与买点
- **现价/市值**：[~$396–400（2026-06-21）、市值 ~$1.50 万亿、净现金 $28.85B、EV ~$1,471B](https://stockanalysis.com/stocks/tsla/statistics/)（强）。[Live MCP：收盘 $396.38、52 周区间 $288.77–$498.83、YTD -11.86%、年化 IV 41.4%](#)（强，IBKR contract 76792991）。
- **估值倍数（全面扩张）**：[TTM P/S 15.3×、前瞻 P/S（2026E $105B）~14.3×、EV/EBITDA 133×、前瞻 P/E ~194×、PEG ~8×](https://stockanalysis.com/stocks/tsla/statistics/)（强）；[Rule-of-40 仅 ~12（增速 8% + 营业利润率 4.2%）](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative)，远低于 40 健康门槛（中）。
- **历史/同业对比**：[历史 2022 年同等更高增速（51%）时 P/S 仅 4.77×](https://companiesmarketcap.com/tesla/ps-ratio/)，今天增速 8% 却给 15.3×（中）；[纯汽车同业 BYD ~1×、Rivian ~4×](https://247wallst.com/investing/2026/03/27/tesla-vs-byd-the-better-ev-stock-for-2026/)，溢价全来自 AI/Robotaxi 期权（中）。
- **反向 DCF 直觉**：[12% 折现 + 2.5% 终值增速下，须 15 年内 FCF CAGR ~38–40% 才能桥接当前 EV](https://www.tradingkey.com/analysis/stocks/us-stocks/261732341-tesla-2026-stock-analysis-ai-robotaxi-valuation-tradingkey)（弱）——完全依赖 Robotaxi+Optimus 在 10–15 年产生 $100B+ FCF。
- **共识/目标价**：[27 位分析师"持有"、均值目标 ~$395–420（≈ 现价，几无上行）](https://stockanalysis.com/stocks/tsla/ratings/)，区间 [$25（GLJ）至 $600+（Wedbush）](https://www.benzinga.com/quote/TSLA/analyst-ratings)——分歧极大（中）。
- **净判断**：`valuation_growth_match`=1（增速 8% 给 P/S 15×，纯汽车赛道无同业支撑，严重不匹配，但 Robotaxi 期权价值暂不封顶至 0）；`entry_expectations`=2（距高点 ~20% 回撤给了一点再定价空间，但远期假设仍极激进、SpaceX 并购传言添不确定）；`liquidity_bubble` 惩罚=3（流动性极好但估值泡沫化、高利率敏感）。

### 市场在重估什么 / 基本面 vs 股价背离
> **必填子块**（"好公司 ≠ 当前价位的好股票"）。

**① 现价已 price-in 的隐含假设**：P/S 15.3×、PEG ~8×、反向 DCF 隐含 38–40% FCF CAGR——现价隐含 Robotaxi+Optimus **大规模商业化成功且如期**，把 Tesla 重估为 AI/机器人平台而非汽车公司 [强/弱]。

**② 基本面动能 vs 股价动能是否背离**：当季 Q1 2026 **beat（EPS +52%、毛利率 8 季最高）但股价次日 -3.56%、YTD -11.86%、距 52 周高 $498 回撤 ~20% 后震荡**——典型"利好出尽 + 远期预期被下修"的负向背离 [中]。期权市场中性偏谨慎：[ATM IV ~40–41.7%、IV Rank ~32–38%（非恐慌）、put/call OI ~0.9（略高于均值 0.8）、$400 call wall 压制](https://flashalpha.com/stock/tsla)（中）。

**③ 市场在边际上重估什么**：不是当季业绩，而是 **(a) 增长持续性**——2025 首次年降 + 欧洲 13 月连降 + 中国零售 -45% 让市场质疑汽车主业能否撑到期权变现；**(b) 治理可信度**——$1 万亿薪酬 + $2B xAI→SpaceX 转换 + 合并传言让市场给治理折价；**(c) 自由现金流**——$25B+ 资本支出使全年 FCF 转负，"投资周期回报"被打问号 [强]。把这三项结构性利空当**再定价催化剂**读。

**④ 背离是否合理、何时收敛**：**合理**——完美预期已透支，而支撑预期的两大支柱（增长持续性、治理）正被削弱。收敛需要：Cybercab/Optimus 见到可见收入（2027 才指引 material）、或汽车主业在欧洲/中国止跌、或治理事件落地（DOJ/SEC 调查结果、合并投票）——均列入第 12 节「结论复述 + 下一步要核实 + 催化/日历」。**护栏**：价格/期权属中/弱证据，此处用于解释背离、不追涨杀跌；正向看，若错杀（基本面未坏而过度悲观）则买点变好，当前判断是"完美透支 → 买点变差"。

## ⚠️ 风险与利空
### 结构性风险
- **治理（governance=4，扣 8 分）**：[董事会独立性被特拉华法院判定"严重瑕疵"](https://www.thecorporategovernanceinstitute.com/insights/news-analysis/teslas-governance-nightmare/)（中）；[主席 Denholm 自 2014 累计 $6.82 亿薪酬、董事会含 Musk 之弟 Kimbal、分类董事会无视多数股东票](https://www.sec.gov/Archives/edgar/data/0001318605/000121465925015361/o1027253px14a6g.htm)（强）；[$5.73 亿关联交易网络（xAI $430.1M Megapack + SpaceX $143.3M）+ $2B xAI 投资未经再批准转 SpaceX](https://electrek.co/2026/05/01/tesla-tsla-web-transactions-musk-companies-spacex-xai-10ka-2025/)（强）；[最高 $145 亿未决诉讼](https://electrek.co/2026/04/16/tesla-facing-up-to-14-billion-lawsuits-deep-dive/)（中）。
- **监管/地缘（regulation_geopolitics=4，扣 8 分）**：[NHTSA FSD 调查涉 290 万辆、6 起伤人事故](https://mlq.ai/news/nhtsa-launches-federal-probe-into-teslas-full-self-driving-for-traffic-violations/)（强）+ [门把手调查](https://finance.yahoo.com/news/tesla-faces-investigation-over-door-140001111.html)（中）；[DOJ 刑事 + SEC 民事 FSD 营销欺诈调查](https://automotive-transportation.news-articles.net/content/2026/05/05/tesla-faces-federal-probes-over-potential-fsd-fraud.html)（中）；[$7,500 美国 EV 税收抵免 2025 年 7 月取消](https://www.investing.com/news/stock-market-news/teslas-firstquarter-deliveries-miss-estimates-as-tax-credit-expiry-weighs-4595678)（强）；[欧洲 1 月 -17%（13 个月连降）](https://www.cnbc.com/2026/02/24/tesla-car-sales-elon-musk-europe-autos-trump-evs.html)（中）+ [中国零售 -45%](https://electrek.co/2026/02/12/tesla-tsla-sales-in-china-crash-45-to-lowest-level-in-over-three-years/)（中）；[台海冲突情景或致芯片断供、营收 -25%](https://seekingalpha.com/article/4773550-tesla-will-survive-a-trade-war-but-a-taiwan-conflict-would-be-perilous)（弱，尾部）。
- **竞争（competition_disruption=1，扣 2 分）**：[BYD 全球 BEV 超越 + 电池专利 1,117 vs 97](https://driveauthority.com/tesla-vs-byd-the-real-battle-for-ev-dominance/)（中）+ [美国份额 49%→46%](https://cleantechnica.com/2026/02/04/tesla-had-46-of-us-ev-market-in-2025-down-from-49-in-2024-gm-13-ford-7/)（强）——加剧但未结构性致命。
- **客户集中（customer_concentration=1，扣 2 分）**：[无单一客户达营收门槛，主要是地理集中（美中合计 71%）](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)（强）。
- **会计质量（accounting_quality=1，扣 2 分）**：现金流与利润大体匹配，但 [Q1 毛利含 ~$4.8 亿一次性且不单项披露](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-one-time-benefits-warranty-tariff-refunds-margins/)（中）+ [SBC 激增 $1.03B](https://www.stocktitan.net/sec-filings/TSLA/10-q-tesla-inc-quarterly-earnings-report-7f5462f3d917.html)（强）。

### 资金面（解禁/增发/内部人卖出/降评级）
- **稀释（dilution_financing=2，扣 4 分）**：[SBC Q1 飙至 $1.09B（年化 ~$44 亿）、无回购对冲、$0 回购 vs $44.7B 现金](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm)（强）；[2025 CEO 奖励 4.237 亿股（占股本 ~12%）10 年归属](https://www.sec.gov/Archives/edgar/data/0001318605/000110465925108507/tm2530590d1_ex10-2.htm)（强）为多年稀释悬顶；但 [无 S-3/ATM/shelf 增发](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001318605&type=S-3&dateb=&owner=include&count=40)（待核实），无被动稀释。
- **内部人/解禁（lockup_insider_supply=1，扣 2 分）**：[Musk 2026 年 6 月行权 3.04 亿份期权但零公开市场卖出，锁定至 2028 年 1 月 + 5 年限售至 2033](https://www.stocktitan.net/sec-filings/TSLA/form-4-tesla-inc-insider-trading-activity-7416f9cbe52a.html)（强）；[董事级 12 个月共减持 ~$1.64 亿、多为例行/缴税](https://www.marketbeat.com/stocks/NASDAQ/TSLA/insider-trades/)（中）。
- **机构/评级**：[机构持股 66.2%、12 个月净流入 +$56 亿（买家 3,427 vs 卖家 2,224）](https://www.marketbeat.com/stocks/NASDAQ/TSLA/institutional-ownership/)（中）——净买入；[共识"持有"、JPMorgan 6/5 上调目标至 $475](https://stockanalysis.com/stocks/tsla/ratings/)（中），但 [JPMorgan 另有 $145 极熊目标](https://electrek.co/2026/04/08/tesla-jpmorgan-145-price-target-60-percent-downside/)（中）。

### 期权市场怎么看
[ATM IV ~40–41.7%、IV Rank ~32–38%（中段，非恐慌）、20 日 HV ~46–48%（HV > IV，IV 未被吹高）](https://flashalpha.com/stock/tsla)（中）；[put/call OI ~0.9（略高于 52 周均值 0.8，温和对冲）](https://www.barchart.com/stocks/quotes/TSLA/put-call-ratios)（中）；[gamma 正区间（dealer 多 gamma、价格被抑制），$400 call wall 阻力、$390–395 put wall 支撑、gamma flip $394](https://flashalpha.com/stock/tsla)（中）——被钉在 $400 call wall 下方。[财报前仅隐含 ~5% 波动、实际资本支出冲击超出隐含区间](https://www.insiderfinance.io/news/tesla-q1-2026-earnings-margins-and-inventory-risk)（弱）——期权市场系统性低估执行风险。

### 下行情景
若 Cybercab/Optimus 2027 仍不放量、汽车主业欧洲/中国持续失血、$25B 资本支出回报落空，则估值锚从"AI 平台"塌回"汽车公司"——[纯汽车同业 P/S ~1–4×](https://247wallst.com/investing/2026/03/27/tesla-vs-byd-the-better-ev-stock-for-2026/) 意味着深度回撤空间（[极熊目标 $25–145](https://www.benzinga.com/quote/TSLA/analyst-ratings)，中/弱）。叠加 DOJ/SEC FSD 调查升级或合并自我交易实锤，是尾部加速器。

### 什么情况说明判断错了（kill-switch）
- **正向证伪（判断太保守）**：Cybercab/Robotaxi 2026 内提前放量并贡献可见收入（管理层指引 2027 才 material），把期权价值兑现 → 推翻"故事尚未变现"。
- **负向证伪（判断太乐观）**：DOJ/SEC FSD 营销欺诈调查升级为正式起诉/处罚 → 可能触发 `accounting_fraud_suspicion` 红线，结论从"回避"转为"红线封顶"。
- **基本面证伪**：汽车毛利剔除一次性后回到 17–18% 并继续走低、Q2 交付再 miss → `unit_economics_profit_path` 与 `revenue_growth_durability` 应下调。

## 结论复述 + 下一步要核实 + 催化/日历

### 结论复述
Tesla 是一家**护城河多重的好公司（质量分 65）**，但在三件事上同时承压：① **买点差（28）**——~$1.50 万亿市值、P/S 15×、PEG 8× 几乎全押尚未变现（2027 才指引 material）的 Robotaxi/Optimus 期权；② **治理与监管双 4 分惩罚**——$1 万亿薪酬 + $5.73 亿关联交易 + 四项 NHTSA + DOJ/SEC FSD 调查，合计扣 16 分把总分压到 23.6；③ **基本面 vs 股价负向背离**——当季 beat 但股价 YTD -11.86%、距高点回撤震荡，市场在重估增长持续性与治理可信度。红线未触发但 `accounting_fraud_suspicion` 最接近。**质量好、买点差、风险重 → 现价回避**，等期权变现或估值 reset 再评估。

### 下一步要核实（仅限闭环后仍真正不可得项）
| # | 仍不可得项 | 为什么不可得（已试过的取证路） | 何时 / 怎样才能拿到 |
|---|---|---|---|
| 1 | Q1 2026 完整 10-Q 分部毛利明细（剔除 ~$4.8 亿一次性后的干净经常性汽车毛利） | SEC EDGAR 直取 403 被挡；二手报道仅给合并数，公司不单项披露一次性金额 | Q2 2026 10-Q 发布（约 7 月底）后比对分部毛利环比；或等卖方拆解模型 |
| 2 | DOJ/SEC FSD 欺诈调查是否升级（正式起诉/大陪审团传票） | 现仅信息收集阶段，DOJ/SEC 不预披露在途调查 | 查 DOJ 新闻稿 + SEC EDGAR 执法页；若升级即为 `accounting_fraud_suspicion` 红线触发信号 |
| 3 | 实时期权 IV 百分位精确值、max pain | flashalpha 仅给 ~32–38% 区间、未返回数值 max pain | optioncharts.io / Market Chameleon / maximum-pain.com 实时查询（中/弱证据，随时变） |
| 4 | $25B 资本支出按类别拆分（AI 算力 vs 工厂 vs Cybercab vs Optimus） | 总额确认但分配未公开 | 等 Q2 电话会补充材料或 10-Q 附注 |
| 5 | Tesla-SpaceX 合并是否正式推进/付诸股东投票 | 仅媒体传言（Wedbush 估 80%），无正式公告 | 查 Tesla 8-K / DEF 14A；若成案即第四笔十亿级自我交易，治理风险升级 |
| 6 | Q2 2026 交付与中国/欧洲零售（需求复苏是否兑现） | 未来事件，尚未发生 | Q2 交付报告（约 7 月初）；Goldman 估 420K vs 共识 400K |

### 催化 / 日历
| 日期 / 窗口 | 事件 | 类型 | 强度 |
|---|---|---|:--:|
| 2026 年 7 月初 | Q2 2026 交付报告（Goldman 420K vs 共识 400K，欧洲 +85–90% 抵消美国弱） | 业绩预告/交付 | 强 |
| 约 2026-07-22（待核实） | Q2 2026 财报 + 电话会（资本支出分配/FCF/Robotaxi 进度） | 财报 | 强 |
| 2026 年夏（7 月底–8 月） | Optimus V3 demo + Fremont 量产启动 | 产品/量产 | 中 |
| 2026 H2 | Cybercab 全面上线 + Robotaxi 扩至"约十几个州" | 产品/服务扩张 | 中 |
| 进行中 | DOJ/SEC FSD 欺诈调查、四项 NHTSA 调查进展 | 监管 | 强 |
| 进行中 | Tesla-SpaceX 合并讨论（Wedbush 估 80% 概率）/ SpaceX IPO | 重大交易/治理 | 中 |
| 2028-01 / 2033 | Musk 行权股解禁（2028 锁定到期）+ 5 年限售到期 | 解禁/筹码面 | 中 |
| 进行中 | 美国 EV 税收抵免取消后需求 + 关税/中国地缘 | 政策/地缘 | 强 |
| 进行中 | BYD/GM/Rivian/Waymo 竞品发布与价格战 | 竞品 | 中 |

## 证据与来源
- Q1 2026 总营收 $22.387B（+15.8% YoY）、毛利率 21.1%（5 季最高）、调整后 EPS $0.41（+52%）— [evwire Q1 2026 财报](https://evwire.com/p/tesla-tsla-q1-2026-earnings-results) / [teslarati](https://www.teslarati.com/tesla-tsla-q1-2026-earnings-results/) — 强
- FY2025 总收入 $94.83B（-3% YoY，上市以来首次年降）— [Yahoo Finance](https://finance.yahoo.com/news/tesla-revenue-slips-2025-energy-163645200.html) — 强
- FY2025 分部：汽车 $69.53B（-9.8%）/ 能源 $12.77B（+26.6%）/ 服务 $12.53B（+19.0%）— [bullfincher](https://bullfincher.io/companies/tesla/revenue-by-segment) — 强
- Q1 2026 交付 358,023（+6%）、生产 408,386（+13%）、产销缺口 5 万辆、库存天数 15→27 — [electrek 交付](https://electrek.co/2026/04/02/tesla-tsla-q1-2026-delivery-results-misses-expectations/) / [stocktitan 10-Q](https://www.stocktitan.net/sec-filings/TSLA/10-q-tesla-inc-quarterly-earnings-report-7f5462f3d917.html) — 强
- FY2025 交付 163.6 万（-8.6%）、BYD 全球 BEV 226 万超越 — [electrek BYD 夺冠](https://electrek.co/2026/01/02/byd-crushes-tesla-all-electric-sales-for-2025-secures-global-bev-crown/) — 强
- FSD 活跃订阅 128 万（+51%）、ARR ~$5.46 亿、2026-02 转纯订阅 $99/月 — [basenor](https://www.basenor.com/blogs/news/tesla-fsd-hits-1-28m-subscribers-in-q1-2026-record-growth) / [notateslaapp ARR](https://www.notateslaapp.com/news/4042/tesla-hits-546-million-in-annual-recurring-revenue-from-fsd-subscriptions) — 中
- 资本支出指引上调至"超 $25B"、Q2–Q4 FCF 转负、全年 FCF ~-$8.5B — [Foreign Policy Journal 电话会](https://www.foreignpolicyjournal.com/2026/04/24/tesla-tsla-earnings-call-reveals-25-billion-capex-plan-for-ai-optimus-robots-and-cybercab-as-stock-retreats/) / [tikr FCF](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative) — 强
- 剔除碳积分汽车毛利 19.2%（vs Q1'25 12.5%）、碳积分 $380M（-30% QoQ）、SBC $1.03B、$9.97B 未确认 CEO 奖励 — [SEC 10-Q（CIK 1318605）](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026026673/tsla-20260331.htm) / [CNBC](https://www.cnbc.com/2026/04/22/tesla-tsla-q1-2026-earnings-report.html) — 强
- Q1 毛利含 ~$4.8 亿一次性（关税退款 + 质保拨回）— [electrek 一次性项](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-one-time-benefits-warranty-tariff-refunds-margins/) — 中
- 能源 Q1'26 部署 8.8 GWh（环比 -38%、同比 -15%）、毛利率 39.5%（含一次性）— [electrek 财务](https://electrek.co/2026/04/22/tesla-tsla-q1-2026-financial-results/) / [teslaacessories 能源](https://www.teslaacessories.com/blogs/news/tesla-energy-q1-2026-update-megapack-deployments-surge-to-record-highs-as-utility-scale-storage-transforms-the-grid) — 强/中
- Musk 指引 Robotaxi 2026 不 material、2027 才显著；HW3 永久无缘无监督 FSD — [notateslaapp 电话会](https://www.notateslaapp.com/news/4031/everything-tesla-announced-during-its-q1-2026-earnings-call-summaryrecap) / [shacknews transcript](https://www.shacknews.com/article/148805/tesla-tsla-q1-2026-earnings-call-transcript) — 强
- Cybercab 2026-04 量产、Austin 等城商业运营 — [basenor Cybercab](https://www.basenor.com/blogs/news/tesla-cybercab-production-starts-april-2026-the-autonomous-era-begins) — 中
- 估值倍数：P/S 15.3×、EV/EBITDA 133×、前瞻 P/E ~194×、PEG ~8×、净现金 $28.85B、EV $1,471B — [stockanalysis 统计](https://stockanalysis.com/stocks/tsla/statistics/) / [gurufocus mktcap](https://www.gurufocus.com/term/mktcap/TSLA) — 强
- Rule-of-40 ~12、2026 收入共识 ~$102–105B（~8% 增速）— [tikr](https://www.tikr.com/blog/tesla-q1-2026-earnings-revenue-up-16-eps-up-52-but-free-cash-flow-turns-negative) / [stockanalysis 预测](https://stockanalysis.com/stocks/tsla/forecast/) — 中
- 历史 P/S：2022 年增速 51% 时仅 4.77× vs 今天 8% 增速给 15.3× — [companiesmarketcap](https://companiesmarketcap.com/tesla/ps-ratio/) — 中
- 同业 P/S：BYD ~1×、Rivian ~4× — [247wallst](https://247wallst.com/investing/2026/03/27/tesla-vs-byd-the-better-ev-stock-for-2026/) — 中
- 反向 DCF：须 15 年 FCF CAGR ~38–40% 桥接当前 EV — [tradingkey 估值](https://www.tradingkey.com/analysis/stocks/us-stocks/261732341-tesla-2026-stock-analysis-ai-robotaxi-valuation-tradingkey) — 弱
- 共识"持有"、均值目标 ~$395–420、区间 $25–$600 — [stockanalysis 评级](https://stockanalysis.com/stocks/tsla/ratings/) / [Benzinga](https://www.benzinga.com/quote/TSLA/analyst-ratings) — 中
- 股价 ~$400、52 周 $288.77–$498.83、距高点回撤 ~20% — [capital.com](https://capital.com/en-int/market-updates/tesla-stock-forecast-03-06-2026) — 中
- 治理：董事会"严重瑕疵"、主席 $6.82 亿薪酬、$5.73 亿关联交易、$2B xAI→SpaceX、$1 万亿薪酬方案、$145 亿诉讼 — [Corp Gov Institute](https://www.thecorporategovernanceinstitute.com/insights/news-analysis/teslas-governance-nightmare/) / [electrek 关联交易](https://electrek.co/2026/05/01/tesla-tsla-web-transactions-musk-companies-spacex-xai-10ka-2025/) / [SEC PX14A6G](https://www.sec.gov/Archives/edgar/data/0001318605/000121465925015361/o1027253px14a6g.htm) / [CNBC 薪酬](https://www.cnbc.com/2025/11/06/tesla-shareholders-musk-pay.html) / [electrek 诉讼](https://electrek.co/2026/04/16/tesla-facing-up-to-14-billion-lawsuits-deep-dive/) — 强/中
- 监管：NHTSA FSD 涉 290 万辆、门把手调查、DOJ/SEC FSD 欺诈调查、$7,500 抵免取消、欧洲 -17%、中国 -45% — [mlq.ai NHTSA](https://mlq.ai/news/nhtsa-launches-federal-probe-into-teslas-full-self-driving-for-traffic-violations/) / [Yahoo 门把手](https://finance.yahoo.com/news/tesla-faces-investigation-over-door-140001111.html) / [news-articles DOJ/SEC](https://automotive-transportation.news-articles.net/content/2026/05/05/tesla-faces-federal-probes-over-potential-fsd-fraud.html) / [investing 抵免](https://www.investing.com/news/stock-market-news/teslas-firstquarter-deliveries-miss-estimates-as-tax-credit-expiry-weighs-4595678) / [CNBC 欧洲](https://www.cnbc.com/2026/02/24/tesla-car-sales-elon-musk-europe-autos-trump-evs.html) / [electrek 中国](https://electrek.co/2026/02/12/tesla-tsla-sales-in-china-crash-45-to-lowest-level-in-over-three-years/) — 强/中
- 美国 EV 份额 49%→46%、GM 13.2% — [cleantechnica](https://cleantechnica.com/2026/02/04/tesla-had-46-of-us-ev-market-in-2025-down-from-49-in-2024-gm-13-ford-7/) — 强
- BYD 4.27M（2024）/ 2.26M BEV（2025）、电池专利 1,117 vs 97、产能 5.82M vs 2.5M — [driveauthority](https://driveauthority.com/tesla-vs-byd-the-real-battle-for-ev-dominance/) / [evboosters 产能](https://evboosters.com/ev-charging-news/tesla-vs-byd-a-battle-of-global-production-capacity/) — 中
- Waymo 1,400 万次全自动行程、收入 $2.86 亿 — [programming-helper](https://www.programming-helper.com/tech/waymo-tesla-robotaxi-race-autonomous-vehicle-market-2026) — 中
- 4680 干电极成最低成本电芯、单车 COGS <$35K — [nextbigfuture](https://www.nextbigfuture.com/2026/03/tesla-making-lower-cost-batteries-and-cars-late-in-2026-and-in-2027.html) — 中
- Supercharger NACS $20B 长期收入潜力、~79,900 接头 — [teslarati NACS](https://www.teslarati.com/tesla-tsla-20b-revenue-access-supercharger-nacs-deal-dan-ives/) / [teslaacessories 充电](https://www.teslaacessories.com/blogs/news/supercharging-in-2026-how-tesla%E2%80%99s-network-is-reshaping-ev-ownership-in-the-us-and-europe) — 弱/中
- 收入地理：美国 48.9% / 中国 22.1% / 其他 27.7% — [metricshour](https://metricshour.com/blog/tesla-revenue-by-country-how-exposed-is-tsla-to-china-and-europe/) — 强
- Musk 任职 2008（CEO）/2004（董事会）、持股 ~15.3–16% — [Tesla IR](https://ir.tesla.com/corporate/elon-musk) / [capital.com 持股](https://capital.com/en-int/analysis/tesla-shareholder-who-owns-the-most-tsla-stock) — 强
- FSD/Robotaxi 时间表连环跳票（L5 2019、百万 Robotaxi 2020、无监督 FSD 2025）— [Wikipedia 预测清单](https://en.wikipedia.org/wiki/List_of_predictions_for_autonomous_Tesla_vehicles_by_Elon_Musk) — 强
- Austin Robotaxi 启动仅 ~36 辆且有安全员 — [insideevs](https://insideevs.com/news/785220/tesla-robotaxi-austin-no-safety-monitor/) — 中
- 2025 CEO 薪酬方案 $1 万亿/4.237 亿股（ISS/GL 反对）— [SEC 薪酬协议附件](https://www.sec.gov/Archives/edgar/data/0001318605/000110465925108507/tm2530590d1_ex10-2.htm) / [CNBC](https://www.cnbc.com/2025/11/06/tesla-shareholders-musk-pay.html) — 强
- 2024-04 高管出走潮（SVP Baglino + 3 VP）— [Bloomberg](https://www.bloomberg.com/news/articles/2024-04-15/tesla-executive-baglino-leaves-as-musk-loses-another-top-deputy) — 强
- Tesla-SpaceX 合并讨论（Wedbush 估 80%）— [CNBC 合并](https://www.cnbc.com/2026/05/26/spacex-tesla-merger-chatter-reignites-as-musk-rocket-company-nears-ipo.html) — 中
- Musk 2026-06 行权 3.04 亿份期权零卖出、锁定至 2028/2033 — [stocktitan Form 4](https://www.stocktitan.net/sec-filings/TSLA/form-4-tesla-inc-insider-trading-activity-7416f9cbe52a.html) — 强
- 董事级减持 ~$1.64 亿（多例行）、空头 2.56% 流通盘 — [marketbeat 内部交易](https://www.marketbeat.com/stocks/NASDAQ/TSLA/insider-trades/) / [marketbeat 空头](https://www.marketbeat.com/stocks/NASDAQ/TSLA/short-interest/) — 中
- 机构持股 66.2%、12 个月净流入 +$56 亿；JPMorgan $145 极熊目标 — [marketbeat 机构](https://www.marketbeat.com/stocks/NASDAQ/TSLA/institutional-ownership/) / [electrek JPM](https://electrek.co/2026/04/08/tesla-jpmorgan-145-price-target-60-percent-downside/) — 中
- 期权：ATM IV ~40–41.7%、IV Rank ~32–38%、put/call OI ~0.9、$400 call wall — [flashalpha](https://flashalpha.com/stock/tsla) / [barchart put/call](https://www.barchart.com/stocks/quotes/TSLA/put-call-ratios) / [insiderfinance 隐含波动](https://www.insiderfinance.io/news/tesla-q1-2026-earnings-margins-and-inventory-risk) — 中/弱
- 员工 100,883 — [sqmagazine](https://sqmagazine.co.uk/how-many-people-work-at-tesla/) — 中
- 全球 EV 渗透率 ~19.8%、美国 BEV 5.5% — [recharged](https://recharged.com/articles/ev-sales-statistics-2026) — 中
- IEA 电网储能 2030 需扩 35× — [IEA](https://www.iea.org/energy-system/electricity/grid-scale-storage) — 中
- Robotaxi/人形机器人 TAM（投机）— [nasdaq Robotaxi](https://www.nasdaq.com/articles/one-analyst-thinks-teslas-robotaxi-revenue-could-soar-250-billion-2035-here-are-3-things) / [adamasintel 人形](https://www.adamasintel.com/tesla-could-capture-half-the-humanoid-robot-market-in-the-us-by-2027/) — 弱
- 台海冲突尾部情景（营收 -25%）— [Seeking Alpha](https://seekingalpha.com/article/4773550-tesla-will-survive-a-trade-war-but-a-taiwan-conflict-would-be-perilous) — 弱
- 财报后反应：盘后 +4% 回吐、次日 -3.56% — [tikr 股价](https://www.tikr.com/blog/tesla-q1-2026-earnings-beat-so-why-did-the-stock-fall-3-56) — 中
- 碳积分 FY2025 $1.99B（-28% YoY）— [SEC 10-K（CIK 1318605）](https://www.sec.gov/Archives/edgar/data/0001318605/000162828026003952/tsla-20251231.htm) — 强
- Live MCP 价格快照（收盘 $396.38、52 周 $288.77–$498.83、YTD -11.86%、IV 41.4%）— Live MCP price snapshot（IBKR contract 76792991, NASDAQ）— 强
