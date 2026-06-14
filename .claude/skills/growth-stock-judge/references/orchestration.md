# 多 agent 编排

本 skill 的执行模式是 **fan-out → synthesize**：编排者（lead）把一只美股的研究拆成 7 个互相独立的模块，**并行**分派给 7 个专职研究子代理；每个子代理只负责一个模块、独立联网取证、回传**统一结构的结论**（`assets/agent-findings-schema.json`）。所有研究代理返回后（barrier），由综合代理 `judge-synthesizer` 汇总、跑评分卡（含双轴、惩罚、红线封顶）、写"结论先行"报告。这样并行取证最快拿到最新证据，而打分与红线判定集中在一个地方，保证结论一致、可复核。各子代理的职责与回传字段见 `references/agent-roster.md`。

## 执行步骤

1. **解析代码（parse ticker）**：从用户输入解析出美股代码与公司名；含糊时先确认是哪一只，再开工。
2. **并行分派 7 个研究子代理（fan-out）**：`company-profiler`、`earnings-analyst`、`growth-analyst`、`moat-economics-analyst`、`valuation-analyst`、`risk-analyst`、`positioning-options-analyst` **同时**分派，互相独立、无共享状态，**各自联网做自己的研究**。不要串行等一个再发下一个——并行才能压缩耗时。
3. **统一回传结构**：每个子代理回传 `assets/agent-findings-schema.json` 定义的结构——`module`、`summary`、`findings[]`（含 `claim/value/source/strength`）、`flags[]`（红旗/利空）、`needs_checking[]`、`suggested_factor_scores`、`suggested_penalties`、`suggested_red_lines`。子代理只填自己负责的键，其余留 `null`/`false`。
4. **屏障等待（barrier）**：等**全部** 7 个研究子代理返回后，才进入综合阶段。任一代理未返回，按"子代理失败处理"标注，不无限等待。
5. **综合出结论（synthesize）**：`judge-synthesizer` 合并所有回传，按"I/O 契约"对冲突字段择优，组装 `assets/scorecard-input.json`，运行 `scripts/growth_scorecard.py` 出分与结论，再按 `assets/stock-verdict-template.md` 写 11 节报告。

## 子代理失败处理

- 某个子代理失败、超时，或拿到的数据太薄：在报告里把**该模块标"待核实"**，写明缺什么、怎么查（给查证路径），**不阻塞出结论**——其余模块照常打分，缺失模块的因子按保守/中性处理并标注。
- 但凡有子代理回传 `suggested_red_lines` 命中红线（`accounting_fraud_suspicion` / `core_customer_loss` / `growth_engine_broken`），即使其他模块缺失，也按评分卡**红线封顶**结论为"回避 / 观望"，红线优先于数据完整性。

## 可移植性与兜底

- **通用写法**：以通用的"分派并行子代理"能力描述（任意 Task/Agent 工具皆可）；本 skill 不硬依赖任何特定编排框架。
- **可选映射**：若处于 OMC 环境，可把研究/综合角色映射到 `oh-my-claudecode:explore`（锁定公司/取证）、`oh-my-claudecode:analyst`（汇总判断）、`oh-my-claudecode:quality-reviewer`（红旗/反方）等；若处于 superpowers 环境，对接 `dispatching-parallel-agents` 来并行分派。两者都是**可选加速器**。
- **兜底（fallback）**：当环境没有多 agent 能力时，**单 agent 顺序执行就是兜底**——同一个 agent 按 `references/agent-roster.md` 的角色顺序，一个模块一个模块地跑（先 7 个研究模块、再综合打分），产出同样的报告。无多 agent 能力不影响 skill 可用。

## I/O 契约

- 所有研究子代理与综合代理之间，**统一以 `assets/agent-findings-schema.json` 为接口**：研究代理按该结构回传，综合代理按该结构读取。
- **冲突对冲规则**：当多个子代理对同一个键给出建议（例如 `product_customer_momentum` 由 `earnings-analyst` 和 `growth-analyst` 都会给、`entry_expectations` 由 `valuation-analyst` 和 `positioning-options-analyst` 都会给），由 `judge-synthesizer` 调和——**优先采用证据更强的一方**（`strength` 越接近 `strong`、来源越硬的输入权重越高），弱证据仅作辅证。最终只有一份 `assets/scorecard-input.json` 喂给评分卡。
