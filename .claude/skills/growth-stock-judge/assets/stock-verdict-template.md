# {{TICKER}}（{{COMPANY}}）成长股投资判断

## 结论
**{{VERDICT}}**　｜　信心：{{CONVICTION}}
质量分 {{QUALITY_SCORE}} / 买点分 {{ENTRY_SCORE}} / 总分 {{FINAL_SCORE}}
一句话：{{ONE_LINER}}

## 评分卡

### 因子（前 6 项＝质量分共 80，后 2 项＝买点分共 20）
| 因子 | 评分(0-5) | 权重 | 得分 | 轴 |
|---|---:|---:|---:|---|
{{FACTOR_ROWS}}

总分 **{{FINAL_SCORE}}**　｜　质量分 **{{QUALITY_SCORE}}**　｜　买点分 **{{ENTRY_SCORE}}**　｜　原始因子分 {{RAW_FACTOR_POINTS}}

### 惩罚项（×2 倍率，合计扣 {{PENALTY_TOTAL}} 分）
| 惩罚项 | 评分(0-5) | 扣分 | 理由 |
|---|---:|---:|---|
{{PENALTY_ROWS}}

> 每个惩罚项都要在「理由」列写清**为什么给这个分**（具体证据，一句话），不要只给数字。

### 红线（kill-switch）
| 红线 | 状态 | 说明 |
|---|:--:|---|
| accounting_fraud_suspicion | {{RL1}} | {{RL1_NOTE}} |
| core_customer_loss | {{RL2}} | {{RL2_NOTE}} |
| growth_engine_broken | {{RL3}} | {{RL3_NOTE}} |

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

### 结论复述
{{RECAP}}（一两句把"质量 vs 买点 vs 风险"的取舍和最终结论再说清一遍）

### 下一步要核实
> 只列**真正查不到**的（实时期权 IV/skew、未来才发生的事、非公开数据）。有明确源路径能查到的（10-Q/10-K/8-K 里的 SBC、客户集中度、监管细节、共识预期等）应已在上文正文，不堆这里——这张表应当很短。

| # | 待核实项 | 为什么没查到 | 查证路径 |
|---|---|---|---|
{{OPEN_ITEM_ROWS}}

### 催化 / 日历
> 按时间先后排，每条标**日期或日期窗口**，未知标"待核实"。逐类覆盖适用者（别只写"下次财报"）：下次财报/业绩预告 · 产品发布/量产/上市 · 行业大会·投资者日(GTC/CES/WWDC/Computex/Analyst Day) · 解禁/增发/回购 · **大客户与上下游 capex 指引**(如算力链看 MSFT/GOOGL/AMZN/META) · 监管·政策(出口管制/反垄断/FDA/关税) · 竞品发布/价格战 · 分析师评级/目标价 · 指数纳入剔除 · 宏观(FOMC/CPI/利率) · 重大合同·股东投票。

| 日期 / 窗口 | 事件 | 类型 | 强度 |
|---|---|---|:--:|
{{CATALYST_ROWS}}

## 证据与来源
逐条列出，每条格式：**结论/数据 — [来源名称](URL) — 强 / 中 / 弱 / 待核实**。尽量给**可点击的具体链接**（SEC 文件页、公司 IR / 新闻稿、财报 transcript、原始报道），方便用户一键核查与拓展阅读；确实没有公开 URL 的，写清来源名称与定位（如"NVDA 10-Q FY2026 Q1，合并现金流量表"）。
{{EVIDENCE_LIST}}
