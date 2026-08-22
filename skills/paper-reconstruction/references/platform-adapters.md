# 非 E-Prime 平台原生结构与交付契约

在程序复现、直接复制或跨平台迁移且目标不是 E-Prime 时读取本文件。先保留论文中的条件、材料、时序、随机化、反应和日志语义，再映射到平台原生对象；不要把其他平台强行写成 Proc/List。

## 共同交付骨架

每个平台都交付：原平台证据、目标平台与版本、选择来源、参与者流程、原生组件图、条件/随机化、材料清单、原始事件、稳定 ID、数据字典、分析接口、运行状态、验证测试与迁移差异。结构化计划可用 `scripts/validate_platform_plan.py` 校验。

## PsychoPy

- 结构：Experiment → Routine → Component；Loop/TrialHandler 调用 conditions 文件，Code Component 只承担 Builder 无法表达的逻辑。
- 文件：`.psyexp`、必要的 `.py`、conditions `.csv/.xlsx`、刺激、资源清单与启动说明。
- 数据：participant/session/study/block/trial/stimulus/condition/response/accuracy/RT/status；区分 wide、trials、log 输出。
- 验证：Routine/Loop 引用存在，条件列与代码/日志同名，帧率和 dropped frames 有记录，随机种子与设备键位可追踪。

## MATLAB + Psychtoolbox

- 结构：主入口 + 参数配置 + 阶段函数或显式状态机 + 刺激呈现 + 输入/触发 + 保存 + 异常清理。
- 文件：`.m`/`.mlx`、配置文件、材料、数据结构说明和运行入口；使用 `onCleanup`/`try-catch` 恢复屏幕与输入状态。
- 数据：统一事件结构与时间戳，区分计划 onset、实际 flip、响应和设备触发；记录 MATLAB、Psychtoolbox 与操作系统版本。
- 验证：`Screen('Flip')` 时序、键盘队列、随机数流、刷新率、同步测试结果和异常退出均有记录。

## jsPsych

- 结构：初始化 → consent/instructions → timeline/timeline variables → plugin trials → debrief/finish；复杂条件使用显式 timeline 路由。
- 文件：HTML/JavaScript 或构建工程、依赖锁文件、插件版本、刺激清单、部署与本地运行说明。
- 数据：为每个 trial 增加稳定 study/phase/block/trial/condition/stimulus 字段；说明浏览器、本地/服务器保存、失败重试和重复提交。
- 验证：浏览器/设备矩阵、资源预加载、全屏/焦点丢失、计时精度、网络中断、数据接收确认和隐私边界。

## Qualtrics / SoSci Survey

- 结构：Block/页面、Survey Flow、Randomizer、Branch/Display/Skip Logic、Embedded Data、计分与结束状态。
- 文件：可导出的问卷定义或逐页构建说明、题项字典、显示逻辑表、随机化表、嵌入字段、联系人/提醒协议与导出代码本。
- 数据：respondent/participant key、wave、item ID、原始响应、显示状态、完成状态、开始/结束时间、时长、设备和质控标记。
- 验证：逐路径预览、随机化频数、必答/验证、回退行为、手机端、匿名性、测试记录与导出字段一致性。

## oTree

- 结构：Subsession/Group/Player 模型，Page/WaitPage 流程，分组、超时、互动、支付和 session config。
- 文件：app、配置、模板、静态资源、rooms/session 说明和启动命令。
- 数据：session/participant/group/round/player、行为、等待、超时、断线、支付、角色和匹配历史。
- 验证：多人并发、等待页、重新连接、组别/轮次状态、支付边界、bot tests 与导出数据。

## Inquisit、Gorilla 与其他平台

- Inquisit：按 script、values、expressions、list、trial、block、data 映射，并记录版本与计时/设备约束。
- Gorilla：按 project/task/tree/node、spreadsheet、zone、branch、randomisation 和 metrics 映射，并记录部署版本。
- 其他程序：使用平台原生组件名称；若不了解其运行语义，先输出平台中立组件契约和待验证项，不伪造可运行代码。

## 运行状态

所有平台统一使用 `design-only`、`buildable`、`generated`、`runtime-verified`。最后一档至少需要：源文件、可启动产物、精确环境版本、无真实被试的烟雾测试、日志核对、已知差异和产物哈希。平台仅有文字蓝图时不得高于 `design-only`。
