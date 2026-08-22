# 实验实施平台选择与产物路由

本参考只在程序复现、直接复制或平台迁移时读取。平台选择面向研究者或研究团队，而不是被试：被试体验研究界面，研究者决定使用什么工具实现、运行和维护研究。

## 先问一次，再继续工作

如果用户已经明确目标平台，直接采用，不重复询问。否则按研究类型问一次：

> 你或研究团队通常使用什么软件实施这项研究？计算机化行为实验可以选择 E-Prime 3.0、PsychoPy、MATLAB + Psychtoolbox、jsPsych、Inquisit 或 Gorilla；问卷/纵向研究可以选择 Qualtrics、SoSci Survey 或其他调查平台；互动研究也可以选择 oTree。请说明其他平台或现场协议。

不要让这一问题无限阻塞任务。计算机化行为实验未回答或无偏好时，采用 `E-Prime 3.0（默认）` 并披露假设；问卷、纵向、现场或其他非行为程序任务未回答时，输出平台中立蓝图，不强行使用 E-Prime。用户稍后指定平台时重新映射实现层，不改变已经确认的论文证据。

## 平台与端到端产物

| 选择 | 实现结构 | 必须连接的数据产物 |
|---|---|---|
| E-Prime 3.0 | Session/Block/Trial Proc、调用它们的 List、对象顺序、属性、E-Basic 与串联/重复关系 | E-DataAid/E-Run 输出、事件日志、稳定 ID、数据字典、分析字段 |
| PsychoPy | Experiment、Routine、Loop、Conditions、Component 与必要的 Code Component | `.psyexp`/脚本、日志、宽表/长表数据、数据字典与分析字段 |
| MATLAB + Psychtoolbox | 主入口、阶段函数或状态机、刺激呈现、时间控制、输入设备、随机化与异常处理 | 原始事件结构、时间戳、保存文件、数据字典与分析字段 |
| jsPsych | timeline、plugin、timeline variables、条件路由、浏览器与设备约束 | 浏览器事件、trial data、会话/被试 ID、导出与分析字段 |
| Qualtrics / SoSci Survey | Block、题项、Randomizer、Display/Skip Logic、Embedded Data 与提交规则 | 响应导出、匿名匹配、波次字段、流失/完成状态与代码本 |
| oTree | Subsession、Group、Player、Page、WaitPage、支付和互动状态 | 房间/组别/玩家 ID、行为与支付日志、超时/断线状态、分析字段 |
| Inquisit / Gorilla | script/trial/block/data，或 task/tree/node/spreadsheet/zone | 条件、试次、设备/浏览器状态、稳定 ID、导出与分析字段 |
| 其他或现场协议 | 将论文步骤映射到该平台的原生组件或主试操作，不强行套用 E-Prime 名称 | 稳定 ID、事件日志或现场记录、数据字典、分析接口与验证记录 |

## 路由规则

1. 先保留论文的理论、条件、刺激、时序、随机化、反应与排除规则，再把它们映射到所选平台。
2. 原论文平台与研究者目标平台不同时，同时记录“原平台蓝图”和“目标平台实现”，并说明迁移造成的时间精度、交互、设备或数据差异。
3. E-Prime 3.0 只是在未指定的计算机化行为实验中的缺省平台和当前第一条深度路径，不是问卷、纵向、现场或统计任务的强制平台。
4. `assets/eprime-starter/` 只是中性结构脚手架，不是论文复现案例，也不能作为实证依据。
5. 第一份标记为 `runtime-verified` 的可运行案例必须从一篇明确指定、合法取得材料的真实论文出发，逐项记录论文版本、DOI、Supplement/OSF、实现差异、运行环境、烟雾测试和产物哈希。
6. 无论平台为何，最终都要闭合“论文证据 → 被试流程 → 实现组件 → 原始事件 → 数据字典 → 分析字段 → 验证测试”。
