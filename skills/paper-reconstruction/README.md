# paper-reconstruction｜把论文重新缝成可运行的研究

简体中文 · [English](README_EN.md)

> **一句话定位：** 面向所有读者、专长是实验与行为研究，把论文从“作者写了什么”重组为“参与者经历什么、选定平台怎样执行、数据怎样记录、研究团队怎样分析”的可执行蓝图；负责重建、迁移、验证与基于证据的发展，不替代单纯的论文阅读。

这里的“重组”始终围绕论文证据展开：先保留理论与设计不变量，再把材料、参数、平台、数据和分析映射到研究者真正使用的工具，而不是脱离原文自由拼装。

## 什么时候该把研究送进“重组室”

当问题从“这篇论文说了什么”推进到“怎样把它真正做出来”时，使用 `paper-reconstruction`：

- **实验与行为任务**：重建条件、角色、步骤、随机化、刺激、反应、反馈、计分和排除。
- **参与者体验到后台实现**：逐屏或逐事件说明参与者看见、理解和完成什么，程序或主试同时记录什么。
- **问卷与纵向研究**：重建招募、同意、题项逻辑、匿名匹配、波次、提醒、流失、数据结构和纵向分析接口。
- **多平台迁移**：使用 E-Prime、PsychoPy、MATLAB/Psychtoolbox、jsPsych、Qualtrics/SoSci、oTree、Inquisit、Gorilla 或现场协议的原生结构。
- **统计复现**：连接原始数据、排除、指标、模型、对比和图表，并适配 R、Python、SPSS、Mplus、MATLAB、Stata、SAS、JASP/Jamovi 或其他环境。
- **研究发展**：在原研究基础上加入新群体、情境、机制、变量或平台，同时检查理论增量、被试可理解性、混淆、成本和证据边界。

| 复现层级 | 目标 |
|---|---|
| 概念复现 | 保留理论或因果逻辑，重新构造材料与情境 |
| 程序复现 | 重建指导语、刺激、随机化、界面、时序、日志和运行文件 |
| 统计复现 | 从已有数据重建排除、指标、模型、对比和表图 |
| 直接复制 | 使用获准使用的原程序、材料、参数和分析包尽可能原样运行 |

## 个性化适配：只在任务需要时提问

Skill 不会在第一次安装时要求填写偏好问卷，也不会每次机械追问。它先识别所需产物，再补问真正影响交付的问题：

- 只读懂论文：转交 `paper-anatomy`，不询问程序或分析软件。
- 程序复现、直接复制或平台迁移：用户未说明时，询问研究团队使用的实施平台。
- 统计复现、分析代码或分析接口：用户未说明时，询问研究团队使用的分析软件。
- 已经从上下文得到答案：直接采用，不重复询问。
- 用户未回答：继续完成平台中立部分，不让问题无限阻塞。

计算机化行为实验在无偏好时可明确默认 E-Prime 3.0；问卷、纵向、现场和纯统计任务不会被强行套用 E-Prime。分析环境未回答时提供平台中立分析契约，不默认 R。

## 平台适配：使用原生结构，不做名称替换

| 平台 | 主要结构 | 重点验证 |
|---|---|---|
| **E-Prime 3.0** | Session/Block/Trial Proc、List、对象、E-Basic、串联/交错/嵌套关系 | `.es3/.ebs3`、E-Run、日志、版本、哈希 |
| **PsychoPy** | Experiment、Routine、Loop/TrialHandler、Conditions、Component、Code Component | 条件列、Routine/Loop 引用、帧率、dropped frames、wide/trials/log 输出 |
| **MATLAB + Psychtoolbox** | 主入口、阶段函数/状态机、Screen、输入队列、触发与事件结构 | flip 时序、刷新率、同步测试、随机数流、异常清理 |
| **jsPsych** | init、timeline、plugin、timeline variables、路由与部署 | 预加载、浏览器/设备、焦点、网络中断、trial data 接收确认 |
| **Qualtrics / SoSci** | Block/页面、Survey Flow、Randomizer、Branch/Display Logic、Embedded Data | 逐路径预览、匿名性、手机端、随机化频数、导出字段 |
| **oTree** | Subsession、Group、Player、Page、WaitPage、支付和互动状态 | 并发、等待、重连、组别/轮次、bot tests、支付与导出 |
| **Inquisit / Gorilla** | script/trial/block/data，或 task/tree/node/spreadsheet/zone | 版本、随机化、计时/浏览器、数据字段和部署状态 |
| **现场或其他程序** | 平台原生组件或主试协议，不强行使用 Proc/List | 同步、人工步骤、稳定 ID、事件记录和分析接口 |

所有平台统一声明 `design-only`、`buildable`、`generated` 或 `runtime-verified`。非 E-Prime 结构化计划可由 [`validate_platform_plan.py`](scripts/validate_platform_plan.py) 检查组件、阶段、字段、分析接口和运行证据。E-Prime 仍是当前第一条深度构建路径；其他平台已经具备原生结构契约与机器校验，但尚不宣称都拥有完整可运行模板。

## 问卷与纵向研究：从题项显示走到跨波分析

横断问卷会重建招募、资格、同意、Block/页面、稳定题项 ID、量表版本与许可、随机化、分支、质控、完成状态、paradata、导出和值标签。

纵向研究进一步要求：

- wave ID、时间窗、目标间隔、实际间隔与版本变化；
- 与联系方式分离的匿名 `participant_key`；
- 邀请、提醒、退订、无效地址、拒绝、完成和失访状态；
- 每波样本流、题项/量尺/语言/平台稳定性和跨波差异；
- `participant_key`、`wave_id`、`item_id`、`response_raw`、`invitation_status`、`completion_status` 等数据字段；
- 宽表/长表、time 变量、缺失机制、流失偏差与纵向模型接口。

未指定问卷平台时会询问一次；未回答则给平台中立蓝图，不默认 E-Prime。组织研究还会分离组织、团队、主管、员工和 dyad ID，并说明聚合、跨层链接、权限和隐私边界。

## 分析适配：先确认研究团队真正使用的环境

只有任务需要分析产物且用户尚未说明时，Skill 才会询问：

> 你或研究团队通常使用什么软件分析数据？可以选择 R、Python、SPSS、Mplus、MATLAB、Stata、SAS、JASP/Jamovi，或说明其他工具；暂时不确定时，我会先给平台中立分析契约。

无论软件为何，产出都保持同一条逻辑链：

```text
导入 → 字段与值标签检查 → 排除 → 派生指标 → 描述
→ 主模型 → 对比/效应量/不确定性 → 表图 → 导出 → 环境与运行记录
```

R 路线提供脚本/Quarto、`renv` 与 `sessionInfo()`；Python 提供脚本/notebook、依赖锁与测试；SPSS 提供可保存的 `.sps` 而不只给菜单点击；Mplus 提供 `.inp`、变量顺序、缺失编码与 `.out` 核对；其他环境使用对应的原生产物。迁移分析软件时保留原分析契约与目标实现差异。

## 工作方式：从论文证据走到可执行复现包

1. 确认论文版本、目标 Study 和概念/程序/统计/直接复制层级。
2. 建立 DOI、正文、附录、Supplement、OSF、预注册、数据、代码和材料来源账本。
3. 完成实现所需的最小论文解剖，查清理论、变量、原始反应、指标、模型和表图关系。
4. 判断实验、问卷、纵向、互动或现场路线，建立参与者/受访者流程。
5. 仅在需要实施时选择平台，分别给出原平台证据、目标平台原生组件和迁移差异。
6. 仅在需要分析产物时选择分析环境；未选择则交付平台中立契约。
7. 连接材料、事件/问卷日志、稳定 ID、数据字典、分析字段和验证测试。
8. 对 E-Prime bundle 或跨平台计划运行相应语义校验。
9. 用户提出新想法时，区分原文、后续证据、用户构想与待验证部分。
10. 按适用的 ABCDE 部分和最小充分产物交付，并说明真实运行状态。

## 可以这样发出“重组任务”

```text
$paper-reconstruction 请把这篇反应时论文重组到 MATLAB + Psychtoolbox。
我们用 Python 分析，请给出阶段函数、flip/响应日志、数据字典、分析接口和烟雾测试。
```

```text
$paper-reconstruction 请把这篇三波员工问卷重建到 Qualtrics。
我们用 SPSS，请设计匿名匹配、提醒与流失状态、导出字段和可保存的 .sps 分析路线。
```

```text
$paper-reconstruction 请重组这篇第三方惩罚实验到单机 PsychoPy。
无法实时联网，请给预生成反馈方案，并区分论文事实、迁移决定和需要 pilot 的部分。
```

## 开始重组前，请尽量提供

| 信息 | 最低要求 | 提供后会更好 |
|---|---|---|
| 研究来源 | PDF、DOI、链接或设计说明之一 | Supplement、OSF/GitHub、预注册、数据、程序和材料 |
| 复现目标 | 想处理哪项研究 | 指定复现层级和 Study |
| 实施环境 | 仅在程序落地时需要，可暂时未知 | 平台/版本、系统、设备、实验室/线上/现场、联网和多人同步 |
| 分析环境 | 仅在需要分析产物时需要，可暂时未知 | R/Python/SPSS/Mplus 等版本、原代码、需要对应的表图 |
| 问卷/纵向 | 仅对应任务需要 | 波次、间隔、匿名匹配、联系提醒、平台与样本流 |
| 现实限制 | 没有限制也可以说明 | 时间、预算、样本、支付、设备、伦理、隐私和许可 |
| 新研究想法 | 仅扩展任务需要 | 新群体、情境、机制、变量、材料和理论价值 |
| 输出偏好 | 默认中文和最小充分产物 | 是否需要完整 ABCDE、代码、结构化 JSON、行动顺序或 Markdown |

材料不完整不会让任务停在“无法复现”。Skill 会区分 `原文明确`、`补充材料`、`外部材料`、`合理推断` 与 `复现建议`，说明今天可以自建什么、怎样验证，以及牺牲了哪一种复现层级。

## 你会收到怎样的 ABCDE 复现包

| 部分 | 核心问题 | 主要内容 |
|---|---|---|
| **A. 目标与证据** | 复现什么，来源是否齐全？ | DOI/Supplement/OSF/数据/代码账本、理论、Study、变量、指标、模型和表图映射 |
| **B. 参与者/受访者流程** | 实际经历什么？ | 任务关系、逐屏/逐步流程、后台动作、波次、匿名匹配和保存数据 |
| **C. 程序与现场协议** | 怎样运行？ | 原平台、目标平台原生组件、问卷逻辑、互动真实性、同步、降级和事件日志 |
| **D. 材料、数据与分析复现** | 怎样从材料走到分析？ | 材料清单、数据字典、目标软件分析管线、代码/设置与验证 |
| **E. 参数沉淀与研究发展** | 哪些结构可迁移？ | 参数卡、理论锚点、后续证据、新问题、创新状态和 pilot |

## 运行和依赖：核心 Skill 轻量，目标环境按需准备

- Skill 本身不要求 API key、MCP 或固定平台，也不会自动安装商业软件。
- Markdown、平台计划和 E-Prime bundle 校验器使用 Python 3 与标准库。
- 目标程序和分析软件由用户自行合法准备；Skill 记录版本、依赖、运行日志和产物状态。
- E-Prime 深度路径以 3.0 为目标；仓库不分发 PST 运行时或自带样例。
- 检查后续研究、创新状态或外部材料时，需要 Agent 具备联网检索能力。

## 内置参考：从路由到验证的重组工具箱

| 内置内容 | 使用场景 |
|---|---|
| [`reconstruction-protocol.md`](references/reconstruction-protocol.md) | 每次重组使用的主协议 |
| [`replication-source-ledger.md`](references/replication-source-ledger.md) | DOI、附录、Supplement、OSF、数据、代码与材料账本 |
| [`replication-deliverables.md`](references/replication-deliverables.md) | 选择最小充分复现产物 |
| [`platform-selection.md`](references/platform-selection.md) | 程序复现、直接复制或平台迁移时选择平台 |
| [`platform-adapters.md`](references/platform-adapters.md) | 非 E-Prime 平台的原生组件、文件、日志和验证 |
| [`survey-longitudinal-path.md`](references/survey-longitudinal-path.md) | 横断问卷、纵向、多波和组织链接研究 |
| [`analysis-environment.md`](references/analysis-environment.md) | 选择分析软件并生成对应产物 |
| [`domain-adaptation.md`](references/domain-adaptation.md) | 领域、研究设计和创新适配 |
| [`eprime-execution-path.md`](references/eprime-execution-path.md) | E-Prime Proc/List、重复关系与运行状态 |
| [`r-reproducibility-guide.md`](references/r-reproducibility-guide.md) | 只有选择 R 时读取 |
| [`output-contract.md`](references/output-contract.md) | 完整 ABCDE 正式报告字段 |
| [`validate_output.py`](scripts/validate_output.py) | 校验正式 ABCDE Markdown 的结构与来源状态字段 |
| [`validate_platform_plan.py`](scripts/validate_platform_plan.py) | 校验非 E-Prime 平台计划、问卷/纵向和分析字段 |
| [`audit_replication_bundle.py`](scripts/audit_replication_bundle.py) | 校验 E-Prime Proc/List、日志、字典与分析语义 |
| [`evals.json`](evals/evals.json) | 材料边界、平台适配、纵向与分析环境回归用例 |

## 重组不能越过哪些证据边界

- 不把缺失的程序、材料、题项、参数或字段冒充作者原件。
- 不把设计稿、伪代码或可构建脚手架描述为已经真实运行。
- 不把其他平台强行写成 E-Prime Proc/List，也不把所有分析固定成 R。
- 不默认社会互动中的其他参与者是真人。
- 不让界面先于数据：稳定 ID、原始反应、派生指标、时间和排除必须进入分析接口。
- 不把未响应自动当成随机缺失，也不把邮箱、工号等身份信息写入公开数据。
- 不把用户新想法写成原文结论；未经检索不声称“首次创新”。
- 不绕过欺骗、知情同意、支付、隐私、许可、事后告知和伦理要求。

## 与 paper-anatomy 的关系：先解剖，还是直接重组

[`paper-anatomy`](../paper-anatomy/README.md) 负责查清理论、设计、结果和结论边界；`paper-reconstruction` 把证据继续接到参与者流程、平台、材料、数据和分析。

- 只需要读懂或审查：使用 `paper-anatomy`。
- 需要搭建、迁移、统计复现或发展研究：使用 `paper-reconstruction`。
- 两者都需要：由 `paper-reconstruction` 统领交付，并完成实现所需的最小论文解剖。
- 理论、综述、Meta 或共识论文默认使用 `paper-anatomy`；只有复现检索、筛选、编码或共识流程时才进入重组。

运行规则见 [`SKILL.md`](SKILL.md)，完整字段见 [`output-contract.md`](references/output-contract.md)，项目总览见 [`paper-to-paradigm`](../../README.md)。
