# E-Prime 第一条可运行复现路径

## 定位

E-Prime 是 `paper-reconstruction` 的第一条深度实现路径。目标不是只画 E-Studio 对象树，而是让论文证据、参与者流程、Proc/List 结构、日志字段和分析变量保持同名、同义和可追踪。

## Proc、List 与重复关系

E-Prime 的 Procedure 定义顺序事件；Session、Block、Trial 等层级应使用不同 Proc 表达。Proc 通常不能直接放入另一个 Proc 的时间线，而由 List 的 `Procedure` 列调用。因此每个 Proc 都要回答：谁调用它、执行什么阶段、内部对象顺序、记录什么数据。

不得只写“重复若干 Trial”，必须选择以下关系之一：

| 关系 | 含义 | E-Prime 实现 |
|---|---|---|
| `serial` | A 完成后才进入 B | 同一 Proc 时间线从左到右，或两个 List 依次放置 |
| `serial-repeat` | 同一阶段连续重复 N 次 | List 行、Weight 或上层 BlockList 控制 |
| `interleaved-repeat` | 多类 Trial 在一个序列中交错抽取 | 同一 TrialList 中设置 `TrialKind`，再选 Sequential/Random 等 Order |
| `nested-repeat` | 上层条件选择下层刺激/试次集合 | Parent List → Proc → Nested/Child List |
| `conditional` | 根据属性、反应或状态进入不同路径 | 不同 Procedure 值、List 条件或显式 InLine/Jump；必须记录路由变量 |
| `parallel-external` | E-Prime 之外存在真正同时运行的设备、参与者或服务 | 显式同步协议、时钟、握手、超时和失败日志；不得用普通 List 冒充并行 |

E-Prime 的对象时间线默认仍是顺序执行；实验设计里俗称“并行重复”的多种 Trial，通常应落成 `interleaved-repeat` 或 `nested-repeat`。只有外部设备或多机真的同时运行时才使用 `parallel-external`。

## 复现包应包含的产物

| 产物 | 作用 |
|---|---|
| `bundle_manifest.json` | 全包唯一命名与状态源，声明 Study、条件、Proc、List、关系、来源和运行状态 |
| `procedure_map.csv` | 逐个 Proc 固定对象顺序、对象类型和日志责任 |
| `lists/*.tsv` | 固定 List 的行、Procedure、条件、TrialKind、Weight 与关键属性 |
| `eprime_build_spec.json` | 把可读契约转换为 E-Studio 创建步骤和属性设置 |
| `inline/*.ebs` | 只保存确有必要且可审计的 E-Basic 片段 |
| `event_log_schema.json` | 定义运行时必须记录的字段及其来源对象 |
| `data_dictionary.csv` | 解释字段含义、类型、取值、原始/派生状态和缺失规则 |
| `analysis_contract.json` | 声明分析真正使用的字段、派生变量和主模型接口 |
| `.es3` | E-Studio 中保存的用户实验源文件；没有它不能称为程序复现完成 |
| `.ebs3` | 由 E-Studio Generate 产生的运行脚本；没有它不能交给 E-Run |
| 烟雾测试记录 | 记录 E-Prime 版本、测试时间、Subject/Session、完成 Trial 数、异常和输出字段 |

## 四个运行状态

- `design-only`：只有概念与流程，不能声称可构建。
- `buildable`：结构、表和代码片段通过语义审计，但仍需在 E-Studio 组装。
- `generated`：已经产生 `.es3` 与 `.ebs3`，尚未完成端到端运行验证。
- `runtime-verified`：固定版本 E-Prime 中完成烟雾运行，日志字段与分析契约均通过，并记录文件哈希。

只有 `runtime-verified` 可以表述为“真正可以运行”。缺少许可证、E-Studio 或 E-Run 时，保持当前真实状态，不降格措辞掩盖最后一公里。

## 一致性检查

从 Skill 目录运行：

```bash
python scripts/audit_replication_bundle.py assets/eprime-starter
```

审计器至少检查：Proc/List 相互调用、时间线顺序、串联/交错/嵌套/外部并行关系、条件名称、List 行数、对象名称、稳定 ID、事件日志、数据字典、分析字段、来源 ID，以及运行状态是否拥有对应 `.es3`、`.ebs3` 和烟雾记录。

## 运行门

1. 先让语义审计通过。
2. 在 E-Studio 按构建规范创建或更新 `.es3`。
3. Generate 产生 `.ebs3`，记录 E-Prime 完整版本。
4. 用专用测试 Subject/Session 完成最小烟雾运行；不使用正式被试数据。
5. 检查 Trial 数、条件频数、顺序/随机化、正确答案、RT、退出与异常日志。
6. 导出测试数据，确认每个分析必需字段存在且类型一致。
7. 记录 `.es3`、`.ebs3` 和烟雾日志 SHA-256 后，才把状态改为 `runtime-verified`。

E-Prime 许可证允许用户分享自己创建的 `.es3`、`.ebs3` 等文件，但不能把 E-Prime 运行时本身放入仓库。论文刺激、量表和其他材料仍须单独核对版权与再分发许可。
