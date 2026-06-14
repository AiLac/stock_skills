# 示例：SPCX 成长股投资判断（worked example）

> **形态演示 / illustrative shape — 数字仅示意，非真实结论。** SPCX（SpaceX）于 2026-06-12 在纳斯达克挂牌，本例撰写时仅上市数日、尚无以上市公司身份披露的季度财报，活动报价/IV 等盘中数据随时变动。下文**引用的结构性事实（S-1 财务、Starlink 规模、解禁安排）来自公开来源并标注证据强度**；而**各因子打分、买点判断与任何前瞻数字均为示意**，用于演示本 skill 的输出形态，**不构成投资建议**。判一只真实股票时，请用联网工具拉取当下数据，把拿不到的项标“待核实”。
>
> 本例特意演示**双轴结论形态**：优质/激动人心的生意（质量分高）＋ 极贵的买点（买点分低）＝ 总分被拉低到“回避”。

本文件演示从 `assets/stock-verdict-template.md` 端到端填出一份判断报告：①填好的评分卡 JSON → ②`scripts/growth_scorecard.py` 的运行输出 → ③完整 11 段报告。三者内部一致（脚本算出的 verdict 与报告“结论”一致）。

---

## 1. 评分卡输入 JSON（喂给 `growth_scorecard.py`）

把下面这段保存为 `spcx-scorecard.json`：

```json
{
  "ticker": "SPCX",
  "company": "Space Exploration Technologies (SpaceX)",
  "factors": {
    "revenue_growth_durability": 4,
    "tam_penetration": 5,
    "moat_chain_position": 5,
    "unit_economics_profit_path": 2,
    "product_customer_momentum": 4,
    "management_capital_allocation": 3,
    "valuation_growth_match": 1,
    "entry_expectations": 1
  },
  "penalties": {
    "dilution_financing": 1,
    "customer_concentration": 1,
    "accounting_quality": 0,
    "governance": 2,
    "competition_disruption": 1,
    "regulation_geopolitics": 2,
    "liquidity_bubble": 3,
    "lockup_insider_supply": 3
  },
  "red_lines": {
    "accounting_fraud_suspicion": false,
    "core_customer_loss": false,
    "growth_engine_broken": false
  },
  "evidence": [
    {"claim": "FY2025 consolidated revenue", "value": "$18.674B (op loss $2.589B; adj EBITDA $6.584B)", "source": "SpaceX S-1 prospectus (2026-05-20)", "strength": "strong"},
    {"claim": "Q1 2026 revenue", "value": "$4.694B; annualizes ~$18.8B", "source": "SpaceX S-1 / Q1 2026 figures", "strength": "strong"},
    {"claim": "Implied price-to-sales at IPO", "value": "~112x sales at $1.75T valuation", "source": "S-1 valuation vs annualized Q1 revenue", "strength": "medium"},
    {"claim": "Starlink scale", "value": ">9,600 satellites, 10.3M subscribers (end-Mar 2026)", "source": "SpaceX S-1 prospectus", "strength": "strong"},
    {"claim": "Staggered insider lockup with early-release tranches", "value": "20%+ unlock after Apr-Jun results; 5 tranches at 70/90/105/120/135 days; full release ~Dec 2026; Musk 366-day", "source": "Yahoo Finance / CNBC / Motley Fool (2026-05)", "strength": "medium"}
  ],
  "what_could_weaken_view": [
    "Starship reaches reliable, high-cadence commercial operation and turns the Space segment EBITDA-positive, justifying the multiple",
    "Starlink ARPU + subscriber growth re-accelerate and consolidated operating losses narrow faster than the S-1 trajectory",
    "Post-IPO trading establishes a much lower price-to-sales that restores a reasonable entry"
  ]
}
```

## 2. 运行评分脚本

```bash
python scripts/growth_scorecard.py spcx-scorecard.json --format md
```

输出（关键行）：

```text
# 成长股评分卡：SPCX (Space Exploration Technologies (SpaceX))

结论：**暂不值得 / 回避**
总分：**40.4 / 100**　｜　质量分：**78.0**　｜　买点分：**20.0**
原始因子分：66.4　｜　惩罚扣分：26.0
```

脚本算出的 verdict = **暂不值得 / 回避**，与下方报告“结论”一致（双轴：质量 78 / 买点 20，惩罚扣 26 分把总分压到 40.4）。

---

## 3. 完整报告（按 `assets/stock-verdict-template.md`）

# SPCX（Space Exploration Technologies / SpaceX）成长股投资判断

## 结论
**暂不值得 / 回避（当前买点）**　｜　信心：中（生意强、买点贵的判断信心高；具体打分为示意）
质量分 78.0 / 买点分 20.0 / 总分 40.4
一句话：生意极强、想象空间极大，但 IPO 给到约 112x 销售额、且上市后数月有大量内部人解禁排队，**现价是“好公司、坏买点”的典型形态——观察名单，等估值与供给消化，而非现在追。**

## 评分卡
| 因子 | 评分(0-5) | 权重 | 得分 |
|---|---:|---:|---:|
| revenue_growth_durability | 4 | 18 | 14.4 |
| tam_penetration | 5 | 14 | 14.0 |
| moat_chain_position | 5 | 14 | 14.0 |
| unit_economics_profit_path | 2 | 14 | 5.6 |
| product_customer_momentum | 4 | 12 | 9.6 |
| management_capital_allocation | 3 | 8 | 4.8 |
| valuation_growth_match | 1 | 12 | 2.4 |
| entry_expectations | 1 | 8 | 1.6 |

惩罚项（×2）：governance 4.0、regulation_geopolitics 4.0、liquidity_bubble 6.0、lockup_insider_supply 6.0、dilution_financing 2.0、customer_concentration 2.0、competition_disruption 2.0、accounting_quality 0.0　→ 合计 26.0

红线状态：未触发（accounting_fraud_suspicion / core_customer_loss / growth_engine_broken 均为 false）

## 投资逻辑
SpaceX 是稀缺的“同时握住运力与天基连接两层”的资产：可复用火箭把发射成本压到难以复制的水平（强），Starlink 在此之上把这种运力变现成全球宽带订阅（强）。多头逻辑＝Starlink 现金牛持续扩张 + Starship 打开下一段更大的运力 TAM。**问题不在生意，在价格**：IPO 估值约 112x 销售额（示意性结论），把未来很多年的成功提前 price-in，安全边际极薄。

## 增长引擎 + 市场空间
- 引擎一 Starlink（连接段）：Q1 2026 营收 $3.257B、经营利润 $1.188B、adj EBITDA $2.087B；期末 >9,600 颗卫星、1030 万订户（强，来源 S-1）。这是目前**唯一盈利**的板块，是整个公司的现金支撑。
- 引擎二 发射/Starship（太空段）：Q1 2026 营收 $619M，但经营亏损 $662M、adj EBITDA 亏 $351M（强，来源 S-1）——是“期权价值”，尚未盈利。
- 市场空间：天基宽带 + 可复用重型运力的合并 TAM 巨大（tam_penetration=5，示意）；但变现节奏与 Starship 商业化时点是最大未知。

## 📊 最近财报重点
> 注：SPCX 上市仅数日，**尚无以上市公司身份披露的季度财报**；以下读数来自 IPO 招股书（S-1）的最新区间数据，作为“最近一期”的代用。下一份真正的上市后季报（Apr–Jun 季）将是首个验证点。
- 增长实绩：FY2025 合并营收 $18.674B；Q1 2026 营收 $4.694B（年化约 $18.8B）。增长在、但合并层面仍**经营亏损**（FY25 op loss $2.589B；Q1’26 op loss $1.943B）。（强，S-1）
- 指引：S-1 未给传统“季度指引”；上市后首份季报的连接段 ARPU/订户与太空段亏损收窄速度，是判断 revenue_growth_durability 是否该加分、还是触发 growth_engine_broken 红线的关键。
- 单位经济性：连接段已盈利、太空段烧钱，混合后 adj EBITDA 正（FY25 $6.584B）但 GAAP 经营仍亏——unit_economics_profit_path 只能给 2（路径可见、未兑现）。
- 客户与势能：订户 1030 万、政府/商业发射订单充足，势能强（product_customer_momentum=4）。
- 财报后反应：上市首日报道收涨约 +19%（中，来源 TradingKey）——情绪热，进一步说明“买点贵”。

## 护城河 / 产业链位置
护城河强（moat_chain_position=5，示意）：可复用火箭带来的成本与发射频次优势短期内无可比对手；Starlink 的卫星星座 + 频谱 + 地面网络构成规模壁垒。在“运力 → 连接”的产业链里，SpaceX 同时占据上游运力与下游变现两个稀缺层（参考 serenity 的“稀缺层/卡点”思路：这里卡点恰恰被它自己握住）。风险是壁垒被竞争对手（其他低轨星座、可复用火箭追赶者）逐步侵蚀——competition_disruption 给轻度惩罚。

## 单位经济性 / 盈利路径
- 连接段：已盈利，是单位经济性的亮点（Q1’26 段 EBITDA margin 高）。
- 太空段：仍亏，盈利路径取决于 Starship 复用成熟度与发射单价。
- 合并：adj EBITDA 正、GAAP 经营亏——盈利路径“看得见、未走完”，故 unit_economics_profit_path=2。

## 估值与买点
- 估值：约 112x 当期销售额（$1.75T 估值 ÷ 年化约 $18.8B 营收，中等证据，由 S-1 数据推算）。即便对超高增长龙头，这也处于历史与同业极端区间——valuation_growth_match=1。
- 买点/预期面：上市数日、首日大涨，市场已把“成功”充分 price-in，预期门槛极高、安全边际极薄——entry_expectations=1。
- 映射：两个买点因子拉满低分，叠加 liquidity_bubble 惩罚，是本例总分被压到 40.4 的核心原因。**好公司，坏买点。**

## ⚠️ 风险与利空
### 结构性风险
- 太空段长期亏损、Starship 商业化时点不确定（competition_disruption / 执行风险）。
- 监管与地缘：发射许可、频谱、出口管制、与政府合同的政治敏感性（regulation_geopolitics 惩罚=2）。
### 资金面（解禁/增发/内部人卖出/降评级）
- **解禁日历（利空，date window 关键）**：本次 IPO 采用**非典型分批早解禁**结构（中，来源 Yahoo/CNBC/Motley Fool 2026-05）——
  - 公布 Apr–Jun 季报后，最多 **20%** 合格内部人股份解锁；若股价较发行价涨 ≥30% 再加 **10%**；
  - 上市后 **70 / 90 / 105 / 120 / 135 天** 各释放约 **7%**；
  - 公布 Jul–Sep 季报后再解 **28%**；
  - **180 天（约 2026-12）** 余量全部解锁；Musk 为 **366 天**（约 2027-06）。
  - 含义：未来数月几乎**每个里程碑都对应一波潜在抛压**，是压制 entry/买点的实打实供给——lockup_insider_supply 惩罚=3。
- 增发/稀释：作为新上市公司，后续二次发行/激励稀释需跟踪（dilution_financing=1）。
- 评级/13F：上市太新，卖方评级与机构持仓尚未稳定——**待核实**（见下）。
### 期权市场怎么看
- **待核实**：上市仅数日，期权链/IV/IV percentile/expected move 尚未稳定或尚未充分挂牌；本例不冻结任何 IV 数字。查证路径：券商期权链、IV 数据源（上市满数周后再读）。这属于中/弱证据（情绪面），不作为核心判断驱动。
### 下行情景
- 逻辑：若 Starship 商业化延后、连接段增速放缓，市场对 112x 销售额的容忍度会迅速收缩；叠加解禁抛压，估值可能向“可比高增长龙头上沿”均值回归。
- 估值地板（示意）：把销售倍数从约 112x 压到更“正常”的高增长区间，价格存在数量级的下修空间——这是“坏买点”风险的量化直觉，非精确目标价。
### 什么情况说明判断错了（kill-switch）
- Starship 实现可靠、高频次的商业运营，太空段转 EBITDA 为正，从而**坐实**当前倍数 → 多头成立。
- Starlink ARPU + 订户重新加速，合并经营亏损收窄快于 S-1 轨迹 → 质量分上修。
- 上市后交易把销售倍数打到明显更低的水平 → 买点修复，结论可从“回避”转“观望/建仓试探”。

## 结论复述 + 下一步要核实 + 催化/日历
- 复述：**生意极强（质量 78）＋ 买点极贵（买点 20）＋ 供给悬顶（解禁惩罚）＝ 现价回避，进观察名单。**
- 下一步要核实（待核实清单）：① 上市后**首份季报（Apr–Jun）**的连接段 ARPU/订户与太空段亏损收窄；② 稳定后的**期权 IV / expected move**；③ 卖方**首批评级**与机构 13F；④ 实际**解禁日各批次量**与是否触发 30% 涨幅附加解锁。
- 催化/日历：Apr–Jun 季报（首份上市后财报，触发首批解禁）；70/90/105/120/135 天时间解禁；Jul–Sep 季报（再解 28%）；约 2026-12 全量解禁；约 2027-06 Musk 解禁。

## 证据与来源
- FY2025 合并营收 $18.674B（op loss $2.589B；adj EBITDA $6.584B）— SpaceX S-1 招股书（2026-05-20）— **强**
- Q1 2026 营收 $4.694B（年化约 $18.8B）；连接段 $3.257B、太空段 $619M — S-1 — **强**
- Starlink >9,600 颗卫星、1030 万订户（截至 2026-03）— S-1 — **强**
- 估值约 $1.75T、约 112x 销售额 — 由 S-1 估值与年化营收推算 — **中**
- 上市首日收涨约 +19% — TradingKey（2026-06）— **中**
- 分批/早解禁结构（20%+ / 5×7% / 28% / 180天 / Musk 366天）— Yahoo Finance、CNBC、The Motley Fool（2026-05）— **中**
- 期权 IV / expected move、卖方评级、机构 13F — **待核实**（上市过新，数据未稳定）

> 复用与合规：本判断只提供研究层面的取舍，不构成交易建议，是否买入由用户自行决定。各因子打分为示意，真实判断请联网核实当下价格、最新财报与解禁实际执行。
