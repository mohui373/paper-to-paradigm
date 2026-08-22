# 为 paper-to-paradigm 做贡献 / Contributing

感谢你帮助改进 `paper-to-paradigm`。本项目面向所有读者，专长是实验与行为研究；贡献应让论文证据、参与者体验、研究实现、数据和分析之间的对应关系更清晰。

Thank you for improving `paper-to-paradigm`. Contributions should strengthen the connection between paper evidence, participant experience, research implementation, data, and analysis.

## 谁可以贡献，谁决定合并 / Who can contribute and who approves

任何人都可以 Fork 仓库、提交 Issue 或发起 Pull Request（PR），不需要预先获得许可。但是，提交 PR 不代表改动会自动进入正式版本：合并到 `main` 前，必须由项目维护者审查，并通过适用的自动校验。维护者可以批准、要求修改、暂缓或拒绝贡献。只有被明确授予仓库写入权限的协作者才能直接操作相应 GitHub 权限；即使如此，也应通过 PR 进入 `main`。

Anyone may fork the repository, open an issue, or submit a pull request without prior permission. A pull request does not automatically change the official release: changes must be reviewed by the maintainer and pass the applicable automated checks before merging into `main`. The maintainer may approve, request changes, defer, or decline a contribution. Direct repository permissions are limited to explicitly authorized collaborators, and changes to `main` should still go through pull requests.

## 可以贡献什么 / What to contribute

- 修正论文解剖或重组复现协议中的方法错误；
- 改进中英文触发语、研究类型路由、平台路由或证据边界；
- 改进 PDF 定位、输出校验、语义一致性审计或 eval；
- 增加原创、可合法再分发的平台实现资产、日志模式或分析接口；
- 修正文档、链接、术语和可访问性问题。

- Correct methodological errors in paper anatomy or reconstruction protocols.
- Improve bilingual triggers, study-type routing, platform routing, or evidence boundaries.
- Improve PDF grounding, output validation, semantic auditing, or evals.
- Add original, lawfully redistributable implementation assets, log schemas, or analysis interfaces.
- Fix documentation, links, terminology, or accessibility issues.

## 提交问题前 / Before opening an issue

请先确认问题来自当前 `main` 版本，并说明：

1. 使用的是 `paper-anatomy` 还是 `paper-reconstruction`；
2. 可用输入是全文、摘要、Supplement、OSF、数据、代码还是其他材料；
3. 预期行为与实际行为；
4. 能否在不公开论文全文、真实参与者数据或受限材料的情况下提供最小复现步骤；
5. 涉及平台实现时，提供平台名称与完整版本、结构概要、运行状态和失败阶段。

Confirm the issue against the current `main` branch. Report the Skill, available source scope, expected and actual behavior, a lawful minimal reproduction, and—when relevant—the platform and exact version, structure, runtime state, and failure stage.

## 修改规则 / Change rules

- 保持两个 Skill 的职责边界，不把阅读输出与复现输出混成同一契约。
- 修改 `SKILL.md` 触发描述时，同时覆盖中文与英文表达。
- 新增可选章节时，中英文文档保持相同顺序和含义。
- 行为变化必须更新或增加 `evals/evals.json`。
- 新增或修改产物字段时，同步更新输出契约、相关参考、校验器和测试。
- 平台专属规则只放在对应平台参考或实现资产中，不写成所有贡献都必须满足的通用规则。
- 不提交论文全文、整页渲染、真实参与者数据、私有仓库链接、API key、密码或其他受限信息。
- 不提交第三方运行时、商业软件组件或无权再分发的样例；只提交自己创建或获准公开的材料。

- Preserve the boundary between reading and replication contracts.
- Keep `SKILL.md` trigger descriptions bilingual.
- Keep optional Chinese and English documentation sections aligned in order and meaning.
- Update or add `evals/evals.json` cases for behavioral changes.
- Keep output contracts, relevant references, validators, and tests synchronized when artifacts change.
- Keep platform-specific rules in the corresponding platform reference or implementation assets rather than making them universal contribution rules.
- Do not commit full papers, rendered pages, participant data, private repository links, credentials, or restricted information.
- Do not redistribute third-party runtimes, commercial software components, or samples you lack permission to share.

## 完整 Skill 贡献要求 / Complete Skill contribution requirements

新增 Skill 或对现有 Skill 做结构性扩展时，不能只提交一段 prompt 或一个孤立的 `SKILL.md`。请提供与功能相匹配的完整结构：

- `SKILL.md`：名称、明确的中英文触发描述、工作流、边界和质量门；
- `agents/openai.yaml`：展示信息与默认调用提示；
- `README.md` 及对应英文文档：定位、适用场景、典型请求、输入、产出、边界和相关技能，并保持章节同步；
- `references/`：承载运行时必须读取的协议、输出契约和方法来源；
- `scripts/`：只有在需要确定性处理或校验时加入，并提供清楚的命令接口；
- `assets/`：只有在确有复用价值且有权公开时加入，注明来源、许可和运行状态；
- `evals/evals.json`：覆盖正常输入、材料不足、冲突证据和新增行为的失败边界；
- 校验器或测试：证明触发、结构、跨文件语义和产物契约没有被破坏；
- 依赖、隐私、许可、已知限制和验证范围说明。

不是每个 Skill 都必须拥有所有可选目录；但任何被 `SKILL.md`、README 或输出契约依赖的文件都必须随贡献完整提供，路径、名称和字段要能通过集合校验。

For a new Skill or a structural extension, do not submit only a prompt fragment or an isolated `SKILL.md`. Provide the complete set required by the feature: bilingual triggers and boundaries, agent metadata, synchronized user documentation, necessary references, deterministic scripts when warranted, lawfully redistributable assets, evals, validators or tests, and dependency/privacy/license/limitation notes. Optional directories are not mandatory, but every referenced dependency must be included and pass collection validation.

## 贡献许可 / Contribution license

提交贡献即表示你确认自己有权提交相关内容，并同意该贡献按照本仓库的 Apache License 2.0 公开。第三方论文、量表、刺激、图片、程序或数据仍受各自许可约束；请提供来源与许可信息，无法确认再分发权时只提交引用、获取说明或不含受限内容的自建替代。

By submitting a contribution, you confirm that you have the right to provide it and agree that it may be distributed under this repository's Apache License 2.0. Third-party papers, scales, stimuli, images, programs, and data retain their own terms; document their source and license, and submit only citations, acquisition instructions, or unrestricted original replacements when redistribution rights are unclear.

## 本地检查 / Local checks

在仓库根目录运行：

```bash
python -m pip install -r requirements-test.txt
python scripts/validate_collection.py
python skills/paper-reconstruction/scripts/audit_replication_bundle.py skills/paper-reconstruction/assets/eprime-starter
python -m unittest discover -s tests -p "test_*.py"
```

修改输出契约后，再对一份实际 Markdown 输出运行对应的 `validate_output.py`。涉及特定平台时，还要运行 `validate_platform_plan.py` 或该平台参考中规定的验证；不能把设计稿或可构建脚手架写成已经真实运行。GitHub Actions 会在 push 和 pull request 时重复集合、PDF fixture、平台、语义和引用文件检查。

After changing an output contract, run its `validate_output.py` against a real Markdown output. For platform-specific implementations, also run `validate_platform_plan.py` or the validation required by that platform reference; do not represent a design or buildable scaffold as runtime-verified. GitHub Actions repeats collection, PDF-fixture, platform, semantic, and citation checks on pushes and pull requests.

## Pull Request 内容与审查 / Pull request contents and review

请在 PR 中简要说明：解决的问题、改动范围、证据或方法来源、运行过的检查、已知限制，以及是否改变输出契约、平台路由或运行状态。一个 PR 尽量只解决一个清晰问题。自动检查通过只是进入人工审查的必要条件，不代表自动批准；最终合并决定由维护者作出。

In the pull request, summarize the problem, scope, evidence or method source, checks run, known limitations, and any change to an output contract, platform route, or runtime state. Keep each pull request focused on one clear problem. Passing automated checks is necessary for review but is not automatic approval; the maintainer makes the final merge decision.
