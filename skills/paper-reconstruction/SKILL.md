---
name: paper-reconstruction
description: "For all readers, with a specialty in experimental and behavioral research: reconstruct, replicate, adapt, and extend paper-grounded studies / 面向所有读者、专长是实验与行为研究：根据论文重组、复现、改造并发展研究。Use when a user asks in English or Chinese to reconstruct, reproduce, implement, program, audit, adapt, or extend an experiment, survey, longitudinal study, interactive task, organizational or field protocol; migrate E-Prime, PsychoPy, MATLAB/Psychtoolbox, jsPsych, Qualtrics/SoSci, oTree, Inquisit, Gorilla, or another platform; define materials, event logs, wave plans, data dictionaries, and analysis contracts for R, Python, SPSS, Mplus, MATLAB, Stata, SAS, JASP/Jamovi, or other tools；中文触发包括论文重组复现、复现实验、问卷或纵向流程重建、研究创新、搭实验、写程序、被试流程、材料重建、平台迁移、数据字典与统计复现。"
---

# 论文重组复现 / Paper Reconstruction

> **一句话定位：** 面向所有读者、专长是实验与行为研究，把论文中的研究从参与者体验到后台实现重组为可执行复现包，主要覆盖来源、流程、材料、程序、数据与分析，但不替代仅以理解和评议为目标的论文阅读。

这里的“重组”始终以论文证据为对象，不是脱离原文的泛化范式创作。

## 任务边界

- 用于从论文或研究设计重建实验对象、被试流程、程序/现场协议、材料、日志、数据和分析。
- 问卷或纵向研究可重建招募、波次、匿名匹配、量表呈现、流失管理、数据结构与分析；纯理论、综述、Meta 或共识阅读优先转用 `paper-anatomy`。
- 用于把用户的新想法建立在原研究之上：区分理论不变量与可调参数，并检查理论增量、被试可理解性、混淆、测量、实施和当前文献位置。
- 若用户只想读懂理论、结果或讨论，不要求落地复现，转用 `paper-anatomy`。
- 同时要求解读与复现时，先完成支撑实现的最小论文解剖，再输出统一的重组复现包。
- 发表文章优先，补充材料校准，开放程序和材料增强；任何缺失都必须标成缺失、假设或待验证项。

## 按需加载

1. 每次读取 `references/reconstruction-protocol.md`。
2. 每次读取 `references/replication-source-ledger.md`，逐项检查 DOI、附录、Supplement、OSF、预注册、数据、代码、材料及更正信息。
3. 每次读取 `references/replication-deliverables.md`，先确定概念/程序/统计/直接复制层级并选择最小充分产物。
4. 需要程序复现、直接复制或平台迁移时，读取 `references/platform-selection.md`；目标不是 E-Prime 时再读取 `references/platform-adapters.md`。
5. 横断问卷、纵向/多波、组织档案链接或问卷平台任务，读取 `references/survey-longitudinal-path.md` 和 `references/domain-adaptation.md`。
6. 需要统计复现、分析代码或分析接口时，读取 `references/analysis-environment.md`；只有用户选择 R 时才读取 `references/r-reproducibility-guide.md`。
7. 涉及组织行为、社会互动、行为决策、健康/运动、教育/HCI、现场研究或跨领域迁移时，读取 `references/domain-adaptation.md`。
8. 目标平台为 E-Prime，或需要判断 Proc/List、串联/交错/嵌套重复与运行状态时，读取 `references/eprime-execution-path.md`，并复制 `assets/eprime-starter/` 作为结构起点。
9. 正式报告或保存 Markdown 时，读取 `references/output-contract.md`。

## 工作流

1. 确认论文版本、目标 Study 和复现层级：概念、程序、统计或直接复制；不要为无关产物询问平台。
2. 建立复现来源账本：规范化 DOI，逐项记录正文、附录、Supplement、OSF、预注册、数据、代码与材料的链接、版本、访问状态和读取范围。
3. 提取研究问题、理论来源、核心发现、变量、指标、模型和图表对应关系；若已有 `paper-anatomy` 的 `source_bundle.json`，复用其页码与链接候选。
4. 判定实验、问卷、纵向、互动或现场研究类型；为每个 Study 建立参与者/受访者流程，纵向研究增加波次、匿名匹配、提醒和流失状态。
5. 只有需要程序复现、直接复制或迁移时才解析目标实施平台：用户已说明则采用；否则按研究类型询问一次。计算机化行为实验未回答时声明默认 E-Prime 3.0；问卷/纵向未回答时保持平台中立。
6. 识别原平台或现场协议，按目标平台输出原生组件、文件、随机化、设备/同步、日志、运行状态和迁移差异；社会互动要明确真人、延迟、主试控制、预生成或虚构。
7. 只有需要分析代码、统计复现或分析接口时才解析分析环境：已说明则采用；否则询问一次。未回答时输出平台中立分析契约，不默认 R。
8. 在确有实施需求时重建材料清单；随后闭合事件/问卷日志、稳定 ID、数据字段、**原文分析路线**与验证测试。不要为了填充模板生成泛化的“自建材料包”；来源冲突必须进入验证计划。
9. 对 E-Prime bundle 运行 `scripts/audit_replication_bundle.py`；对其他平台的结构化计划运行 `scripts/validate_platform_plan.py`，保持组件、流程、字段和分析语义统一。
10. 用户提出新想法时，先写出“原文限制或范式结构 → 理论/相邻文献 → 可检验问题”，再给设计；每个优先 idea 至少有两个可追溯支点（如原文限制 + 后续文献，或理论 + 相邻实证），并标为 `已检索确认`、`部分支持` 或 `待检索确认`。不得把未检索的灵感写成领域空白。
11. 按适用的 ABCDE 部分交付；最小交付优先，保存为正式 Markdown 或结构化包时运行对应校验器。

## ABCDE 输出契约

```text
A. 论文重组复现目标与文献证据
B. 被试视角流程
C. 程序与现场协议蓝图
D. 材料、数据与分析复现
E. 实验参数沉淀与研究发展
```

完整字段、行动顺序和反馈表见 `references/output-contract.md`。不得在 ABCDE 之外增加互相竞争的顶级输出结构。

## 不可妥协规则

1. 多 Study 均有完整或精简流程，或明确说明不展开的证据理由。
2. 原平台必须明示；现场流程本身也是一种运行平台。
3. 社会互动必须说明真假、同步方式、角色状态、支付和日志边界。
4. 伪代码说明用途，关键行配简短中文括注；不能把概念建议冒充原作者代码。
5. 数据结构可直接进入分析：稳定 ID、条件、试次、原始反应、派生指标和排除标记齐全。
6. 未知列名使用显式占位符；只有模型、变量与目标分析环境足够确定时才给可运行代码骨架。
7. 缺少原程序不自动等于严重缺口；必须说明今天如何自建、验证及牺牲的复现层级。
8. E-Prime 不得把“并行”作为未定义关系；必须写成 `serial`、`serial-repeat`、`interleaved-repeat`、`nested-repeat`、`conditional` 或带同步契约的 `parallel-external`。
9. 没有 `.es3`、生成的 `.ebs3`、烟雾运行记录和产物哈希时，不得把状态写成 `runtime-verified`。
10. 中性 starter 只能作为结构脚手架；第一份真正标记为 `runtime-verified` 的程序案例必须对应一篇明确论文，并保留 DOI、材料来源、实现差异和运行证据。

## 校验

保存为 Markdown 后运行：

```bash
python scripts/validate_output.py OUTPUT.md
```

校验器检查 A0 来源账本、ABCDE、关键实现字段、行动顺序和反馈表；链接是否真的可访问、版本是否正确、实现是否符合论文仍需人工核查。

生成结构化复现包后运行：

```bash
python scripts/audit_replication_bundle.py BUNDLE_DIRECTORY
```

语义审计器检查跨文件命名和依赖；E-Prime/E-Run 是否真实运行仍由运行状态门和烟雾测试证明。

## 质量门

- A0 明确 DOI、附录、Supplement、OSF、数据、代码和材料的真实访问状态；A 的理论、变量、分析和图表均能回到论文证据。
- B/C 能让实现者逐屏或逐现场事件重建实验，并知道后台状态变化。
- C0 同时记录原论文平台、研究者目标平台及选择来源：用户明确、团队惯用、论文原平台、E-Prime 3.0 行为实验默认或平台中立。
- E-Prime 的 Proc/List 或其他平台的原生组件、调用关系、条件、日志责任和运行状态明确；问卷/纵向同时闭合题项、逻辑、波次、匹配、流失和导出字段。
- C5 以原文真实的统计方法、模型、对比和分析软件为中心；不要用试次字段表或默认 R 管线取代原分析路线。
- D 依次连接来源/材料状态、最小数据字段和验证差异处理；跨文件名称通过语义审计。只有真正需要实施时，才另列自建材料。
- 正文、Supplement、OSF、数据或代码矛盾时保留版本差异，并把消解测试加入 D3。
- E 只沉淀从论文复现得到的参数与经文献校准的发展方向；每个优先 idea 显式写出证据起点、理论依据、可检验设计与证据状态，不把用户想法冒充证据。
