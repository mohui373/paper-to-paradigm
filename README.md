<h1 align="center">paper-to-paradigm</h1>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/blob/main/README.md">简体中文</a> ·
  <a href="https://github.com/mohui373/paper-to-paradigm/blob/main/README_EN.md">English</a> ·
  <a href="#what">🧰 技能索引</a>
</p>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/actions/workflows/validate.yml"><img src="https://github.com/mohui373/paper-to-paradigm/actions/workflows/validate.yml/badge.svg" alt="Validate Skills"></a>
  <img src="https://img.shields.io/badge/version-0.1.0-7C3AED?style=flat-square" alt="Version 0.1.0">
  <img src="https://img.shields.io/badge/skills-2-0EA5E9?style=flat-square" alt="2 Skills">
  <a href="https://github.com/mohui373/paper-to-paradigm/stargazers"><img src="https://img.shields.io/github/stars/mohui373/paper-to-paradigm?style=flat-square&amp;logo=github&amp;label=stars&amp;color=F5B700" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-22C55E?style=flat-square" alt="Apache-2.0 License"></a>
  <img src="https://img.shields.io/badge/focus-experimental_%26_behavioral-F97316?style=flat-square" alt="Experimental and behavioral research">
</p>

<p align="center"><strong>paper-to-paradigm</strong> 像一台专长实验与行为研究、但面向所有读者的“双臂论文手术机器人”——<strong>paper-anatomy</strong> 负责把理论、变量和参与者体验层层剖开，<strong>paper-reconstruction</strong> 负责按证据把来源、流程、材料与分析重新缝合；手术对象是论文，知情同意由你负责。</p>

---

<a id="contents"></a>

## 🧭 目录

- [💡 Why：为什么建立这套 Skills](#why)
- [⏰ When：什么时候使用](#when)
- [👥 Who：适用于哪些研究与使用者](#who)
- [🧰 What：目前有哪些功能](#what)
- [📦 Where：如何安装到不同 Agent](#where)
- [🚀 How：如何调用、输入什么、得到什么](#how)
- [📚 参考文献](#references)
- [⭐ Star 历史](#star-history)

---

<a id="why"></a>

## 💡 Why：为什么建立这套 Skills

我目前是基础心理学研究生，本科阶段学习人力资源管理，主要专注于行为实验，研究兴趣包括社会与实验心理学、组织行为、道德行为与决策。这个项目最初并不是为了再做一个“论文摘要器”，而是来自我在阅读论文、开展研究和设计实验时反复遇到的一组真实问题。

现在已经有很多优秀的文献检索、阅读 Prompt 和 Skill。它们能够帮助我们快速找到论文，概括背景、方法、结果与结论。例如 Consensus 会先通过标题和摘要进行关键词与语义检索，再使用 Study Snapshot、Ask Paper、Pro Analysis 和 Consensus Meter 分析单篇或综合多篇论文（[Consensus, 2025](https://consensus.app/home/blog/how-consensus-works/)）。这些工具很好地解决了“找到什么”和“论文大致说了什么”，但当阅读目标从了解转向研究时，仍可能留下一个缺口：**我们知道了结论，却还没有真正看清结论是怎样从研究设计中产生的。**

一篇论文中最影响研究质量的内容，往往并不集中在摘要里。自变量如何操作化、因变量如何被感知和记录、中介与调节变量放在什么位置、控制变量为何需要进入模型、原始反应如何变成最终指标、多个 Study 又如何逐步排除替代解释——这些信息经常分散在引言、方法、结果、图表、附录和补充材料中。如果没有一条固定的分析路线，阅读者就需要不断补问、反复翻页，并在多轮对话中重新建立上下文；最后得到的仍可能是彼此分离的理论摘要、统计结果和方法笔记。

研究质量也体现在引言与讨论能否共同讲清一个“好故事”。这里的故事不是把结果包装得更戏剧化，而是让研究问题、理论缺口、假设、证据与结论形成可检验的逻辑链：引言需要说明为什么这个问题值得研究、已有解释在哪里断开，以及每个 Study 为什么必须这样安排；讨论则需要把结果放回原问题，交代哪些解释得到支持、哪些替代解释仍然存在、结论可以推广到哪里。只看方法和显著性，可能错过一篇论文真正的理论推进；只接受流畅的叙事，又可能把“讲得通”误当成“证据足够”。因此，Skill 既要还原作者怎样建立并闭合研究故事，也要检查故事的每个转折是否有设计、数据和引用支撑。

更明显的问题出现在实验设计中。研究者进入实验时已经知道理论、假设和变量，被试却只看得到指导语、刺激、选项、反馈和奖励。研究者认为清楚的任务，被试可能理解成另一件事；研究者希望操纵某个心理过程，被试却可能只是感到困惑、猜到研究目的，或根据奖励结构采取了另一套策略。如果不暂时放下已有理论，从被试视角把实验重新走一遍，就很难判断：

- 被试认为自己正在完成什么任务；
- 指导语和材料是否足以形成目标理解；
- 操纵改变的是目标构念，还是任务难度、情绪、需求特征或其他因素；
- 被试的每一步体验能否与变量、事件日志、分析指标和最后的理论解释对应；
- 一个看起来新颖的实验范式究竟具有理论增量，还是只更换了材料表面。

这不仅关系到读懂论文，也关系到研究是否能够被检查、复现和继续发展。心理学的大规模重复研究使可重复性问题受到持续关注（[Open Science Collaboration, 2015](https://doi.org/10.1126/science.aac4716)）；TOP Guidelines 等开放科学工作则强调设计、材料、数据、分析与复现过程的透明性（[Nosek et al., 2015](https://doi.org/10.1126/science.aab2374)）。`paper-to-paradigm` 无法单独解决整个可重复性问题，但它可以在阅读阶段就把“作者说了什么、证据来自哪里、实现还缺什么、哪些部分属于推断”分开，为之后的复核、预注册、材料准备和分析保留更清楚的接口。

因此，这套 Skills 希望同时做三件事：

1. **补足阅读漏洞**：不止概括结论，还要连接理论、变量、被试体验、数据和讨论，暴露断裂、混淆与证据边界。
2. **提高研究效率**：用稳定的结构一次性回答原本需要多轮追问的问题，让论文笔记可以继续进入开题、综述、汇报、实验设计和分析，而不是读完后重新整理一次。
3. **帮助研究继续生长**：在尊重原论文证据的基础上，提炼可迁移的设计参数，判断哪些内容可以复现、哪些需要重建、哪些新想法值得通过 pilot、操纵检验或后续研究继续验证。

随着案例逐渐积累，同一种研究设计的成功经验、失败风险和实现边界也可以被保留下来。这样，阅读不再只是一次性的“获取结论”，而能够成为后续研究设计、跨领域迁移和方法改进的起点。这个项目不替代原文、领域专家或研究者的判断；它希望让判断建立在更完整、更透明、也更接近被试实际体验的证据之上。

---

<a id="when"></a>

## ⏰ When：什么时候使用

### 🎓 第一类：学术工作与研究需要

这套 Skills 首先服务于与论文高度相关的学习和研究任务。这里的“学习”不是停留在记住作者结论，而是为了能够提出问题、选择理论、理解方法、设计研究和评价证据。

| 使用场景 | 常见困难 | Skills 可以提供什么 |
|---|---|---|
| 开题与研究选题 | 读了很多文献，却难以说明理论从哪里来、缺口是否真实 | 整理理论源头、关键命题、已有证据、争议与尚未闭合的研究问题 |
| 文献综述 | 文献容易变成逐篇摘要，难以形成观点和证据链 | 按命题、研究类型、方法和结论边界组织文献，建立观点—来源—证据矩阵 |
| 理论支持 | 找到名称相近的理论，却不确定是否真正支持模型路径 | 回到作者引用的一层来源，区分奠基理论、后续整合、辅助解释和相邻实证 |
| 文献汇报与组会 | 能复述论文，但讲不清各 Study 为什么这样安排 | 还原研究叙事、被试流程、变量、统计证据与跨 Study 推进逻辑 |
| 学习实验范式 | 知道范式名称，却不知道被试实际看到什么、关键参数是什么 | 从被试视角重走任务，拆解操纵、刺激、反馈、计分、时序与可理解性 |
| 实验设计与 pilot | 研究者视角完整，但任务可能对被试不清楚 | 检查指导语、角色、需求特征、混淆、日志、操纵检验和实施风险 |
| 复现与平台迁移 | 原材料、程序或现场细节不完整 | 明确复现层级，重建材料、程序/现场协议、数据字典、分析和验证步骤 |
| 个性化研究创新 | 有新想法，却不确定是在增加理论价值还是只增加复杂度 | 区分理论不变量与可调参数，评估增量、边界、测量、成本与待验证假设 |

因此，它既可以出现在研究的前端——开题、综述、理论选择和研究构思，也可以进入中后端——实验设计、材料准备、数据结构、分析复现与后续扩展。一次结构化阅读的结果可以继续被下一阶段使用，而不是每换一个任务就从零开始理解同一篇论文。

### 🛡️ 第二类：日常生活中的信息核验

现在越来越多健康、运动、心理、教育和管理领域的科普创作者会主动附上参考文献。这是一个值得肯定的变化：读者至少有机会返回来源，而不是只能相信一句无法追踪的结论。

但“附有论文”并不自动等于“表述与论文完全一致”。在信息竞争激烈的平台环境中，复杂结论可能被压缩成更有传播力的标题，例如把相关关系说成因果关系、把特定样本外推到所有人、把统计显著说成效果巨大，或省略原论文的限制与不确定性。针对健康科学传播的研究也观察到，新闻中的夸大与学术新闻稿中的夸大高度相关，其中常见形式就包括从相关推到因果、给出论文并未支持的行为建议，以及把动物结果直接推广到人类（[Sumner et al., 2014](https://doi.org/10.1136/bmj.g7015)）。一项大规模 Twitter 研究发现，虚假新闻比真实新闻传播得更远、更快、更深入和更广（[Vosoughi et al., 2018](https://doi.org/10.1126/science.aap9559)）。这些结果不能证明每位博主都在故意夸大，却说明更醒目、更绝对的表达确实可能在传播环境中获得优势。

健康错误信息也横跨疫苗、饮食、药物、疾病和医疗干预等主题，并出现在多种社交平台；其比例随主题、平台和研究方法而变化（[Suarez-Lledo & Alvarez-Galvez, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7857950/)）。而错误信息在被纠正后仍可能继续影响推理，即持续影响效应（continued influence effect）（[Lewandowsky et al., 2012](https://doi.org/10.1177/1529100612451018)）。与其等到形成稳定印象后再纠正，更稳妥的做法是在接收结论时就保留一次主动核验。

当我们不熟悉某个领域的指标、模型或效应大小时，`paper-anatomy` 可以把“博主说了什么”与“论文实际支持什么”逐项对照：

1. 记录原始表述、引用与传播情境；
2. 找到论文全文和必要的补充材料；
3. 用通俗语言解释研究类型、样本、变量、指标、效应大小和不确定性；
4. 判断传播主张是与原文一致、部分一致、过度概括、不受支持，还是目前无法判断；
5. 检查是否存在因果夸大、对象外推、边界遗漏、单篇研究代表全部证据或断章取义；
6. 在结论影响较大时，再用系统综述、Meta-analysis、指南和后续研究校准。

这种核验的意义不只是“抓错”，而是把一次被动的信息输入变成主动理解：读者不仅知道某句话可不可信，也能顺便学会论文中的指标代表什么、研究设计能够回答什么、结论为什么有边界。它不是万能事实核查，也不代替医学诊断、临床指南或专业意见；它提供的是一条从网络主张返回论文证据、再形成自主判断的路径。

---

<a id="who"></a>

## 👥 Who：适用于哪些研究与使用者

这套 Skills **面向所有读者，专长是实验与行为研究**：既包括研究生、本科生、研究者、教师和研究助理，也包括希望主动核验论文证据的普通读者。它不以学科或研究类型设限；只要能够提供论文或其他可追溯证据，就会根据研究问题、证据生产方式和使用目标选择相应的解剖或重组路线，并在实验范式、参与者体验、行为测量和实现链条上提供更细的分析。

### 🧩 不同领域会关注不同问题

| 领域或任务 | 自适应关注点 | 示例问题 |
|---|---|---|
| 实验心理学 | 实验范式、理论—操纵链接、被试体验、任务阶段、测量敏感性 | Stroop 变式究竟改变了抑制控制，还是同时改变了任务难度？ |
| 社会心理学 | 社会情境、身份、互动真实性、需求特征、操纵检验 | 排斥范式中的“其他玩家”是真人、延迟匹配还是预生成反馈？ |
| 组织行为与管理学 | 组织情境真实性、分析层级、实际行为与意向、跨组织普适性 | 实验中的领导反馈能否代表真实组织互动？个体结论能否上推到团队？ |
| 行为决策与行为经济学 | 激励相容、收益结构、风险、角色信息和决策过程 | 第三方惩罚是道德反应，还是奖励结构和社会期许造成的？ |
| 健康与运动研究 | 研究设计、对照组、指标含义、替代终点、效应大小和适用人群 | “显著改善某指标”是否等于对健康结果具有实际意义？ |
| 教育、传播与 HCI | 任务生态、学习/使用情境、行为日志、短期与长期结果 | 实验室点击行为能否代表真实平台中的持续使用？ |

### 🔬 不同研究设计会采用不同判断路线

| 研究类型 | 重点还原什么 | 重点防止什么 |
|---|---|---|
| 实验与准实验 | 被试流程、操纵、随机化、测量、排除与结果—假设映射 | 混淆、需求特征、替代解释和过度因果化 |
| 横断问卷 | 构念、量表来源、题项覆盖、信效度、变量关系和模型路径 | 共同方法偏差、短量表缺失和“相关等于因果” |
| 纵向与多波研究 | 时间点、间隔、流失、时间顺序、滞后和个体内/个体间效应 | 时间等值性不足、选择性流失和错误方向推断 |
| 定性研究 | 抽样、材料生成、编码、研究者位置和主题—材料对应 | 主题不可追溯、解释超出材料和反身性缺失 |
| 理论与概念论文 | 中心命题、理论源头、概念边界和可检验路径 | 近名构念混用、关键引文缺失和虚构实证流程 |
| 系统综述与 Meta-analysis | 检索、纳排、编码、效应构造、异质性与偏倚 | 用汇总效应掩盖证据质量、异质性和因果边界 |
| Delphi、共识与指南 | 专家选择、轮次、反馈、阈值和推荐形成 | 把专家赞同率当作效应量或高确定性证据 |

> [!NOTE]
> 当论文不是实验研究时，Skill 不会虚构被试 Screen Flow，而会改为还原该研究类型真实的证据生产过程。

---

<a id="what"></a>

## 🧰 What：目前有哪些功能

### 🤖 两个核心 Skill

<p align="center">
  <a href="skills/paper-anatomy/README.md"><img src="https://img.shields.io/badge/paper--anatomy-Read_%26_Audit-7C3AED?style=for-the-badge" alt="paper-anatomy: Read and Audit"></a>
  <a href="skills/paper-reconstruction/README.md"><img src="https://img.shields.io/badge/paper--reconstruction-Reconstruct_%26_Replicate-0EA5E9?style=for-the-badge" alt="paper-reconstruction: Reconstruct and Replicate"></a>
</p>

| Skill | 一句话定位 | 主要任务 | 使用边界 | 默认输出 |
|---|---|---|---|---|
| [`paper-anatomy`](skills/paper-anatomy/README.md) | 从研究者证据链与参与者体验两条视角解剖论文 | 理论源头、变量与测量、Study 流程、统计结果、页码/图表定位、结论、限制和后续证据 | 不负责把实验落地为程序 | ABC 论文解剖报告 + 来源定位清单 |
| [`paper-reconstruction`](skills/paper-reconstruction/README.md) | 把论文从参与者体验到后台实现重组为复现包 | DOI/附录/Supplement/OSF 来源账本、问卷/纵向流程、平台原生结构、材料、日志、数据字典、目标软件分析管线、验证与研究发展 | 不替代以理解和评议为目标的阅读 | 最小充分产物或 ABCDE 复现包 |

`paper-reconstruction` 目前把 E-Prime 作为第一条深度实现路径：逐个定义 Session/Block/Trial Proc、调用它们的 List、对象顺序，以及 Trial 的串联、连续重复、交错重复、嵌套重复、条件路由或外部并行关系。结构化复现包会继续连接事件日志、数据字典和分析契约，并通过语义审计防止同一条件或字段在不同文件中改名、漏记或失去对应。只有完成 `.es3 → .ebs3 → E-Run 烟雾测试 → 日志核对` 后，才会把运行状态标为“已经验证”。

非 E-Prime 路线不会只做名称替换：PsychoPy、MATLAB/Psychtoolbox、jsPsych、Qualtrics/SoSci、oTree、Inquisit、Gorilla 和现场协议分别使用原生组件、文件、日志与验证结构。问卷与纵向研究还会单独处理题项 ID、显示逻辑、匿名匹配、波次、提醒、流失、跨波版本、paradata 和缺失机制。结构化跨平台计划可由校验器检查阶段、组件、输出字段、分析接口与运行证据。

### 🌱 基于已有研究的个性化创新

当用户产生新想法时，`paper-reconstruction` 可以在原研究基础上发展新的群体、情境、机制、变量、材料、互动方式、测量和平台，而不是机械复制。它会：

1. 区分原研究的理论不变量与可调整参数；
2. 检查新想法的理论增量和被试可理解性；
3. 审查潜在混淆、测量—分析匹配与实施成本；
4. 区分原文支持、后续证据支持、用户推测和待验证部分；
5. 未检索当前文献时，不把想法直接称为“首次”“创新”或“研究空白”。

> [!IMPORTANT]
> 个性化创新不是随意给别人的研究“加料”，而是把自己的想法变成有来源、有边界、可检验的新研究设计。

### 🎛️ 根据任务进行个性化提问与工具适配

个性化不等于第一次安装时填写一长串偏好。Skills 会先判断用户真正需要的产物，再只询问会改变结果的问题：程序复现或平台迁移才询问研究团队使用的实施软件；统计复现、分析代码或分析接口才询问使用 R、Python、SPSS、Mplus、MATLAB、Stata、SAS、JASP/Jamovi 还是其他环境。上下文已经说明时不会重复询问，未回答时也会继续完成平台中立部分。

因此，同一篇论文可以得到不同但语义一致的交付：E-Prime 用户获得 Proc/List 与 E-Run 路径，PsychoPy 用户获得 Routine/Loop/conditions，MATLAB 用户获得阶段函数、Screen 和事件结构，问卷研究者获得 Block/逻辑/波次/匿名匹配，SPSS 或 Python 用户则获得对应的原生分析产物，而不是统一被转换成 R。

---

<a id="where"></a>

## 📦 Where：如何安装到不同 Agent

> [!IMPORTANT]
> 本项目采用单仓库、多 Skill 目录结构；安装时请保留两个 Skill 各自的完整目录，不要只复制 `SKILL.md`。

### 🟢 方式一：`npx skills` 安装

需要 Node.js 18 或更高版本。先查看仓库中的可安装 Skill：

```bash
npx skills add mohui373/paper-to-paradigm --list
```

将两个 Skill 全局安装到 Codex：

```bash
npx skills add mohui373/paper-to-paradigm --global --agent codex --skill '*' --yes --copy
```

安装到 CLI 支持的所有 Agent：

```bash
npx skills add mohui373/paper-to-paradigm --all
```

更新已安装 Skill：

```bash
npx skills update --global --yes
```

下面三种手动安装方式共用同一个稳定仓库副本，先执行一次：

```bash
git clone https://github.com/mohui373/paper-to-paradigm.git
cd paper-to-paradigm
```

### 🟠 方式二：Claude Code

保留完整 Skill 目录，不能只复制 `SKILL.md`。

macOS / Linux：

```bash
mkdir -p ~/.claude/skills
cp -R ./skills/paper-anatomy ~/.claude/skills/
cp -R ./skills/paper-reconstruction ~/.claude/skills/
```

Windows PowerShell：

```powershell
$claudeSkills = Join-Path $env:USERPROFILE ".claude\skills"
New-Item -ItemType Directory -Force -Path $claudeSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\paper-anatomy" $claudeSkills
Copy-Item -Recurse -Force ".\skills\paper-reconstruction" $claudeSkills
```

重新开启 Claude Code 会话后，用自然语言触发，或明确要求使用 `paper-anatomy` / `paper-reconstruction`。

### 🔵 方式三：Codex

macOS / Linux：

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/paper-anatomy ~/.codex/skills/
cp -R ./skills/paper-reconstruction ~/.codex/skills/
```

Windows PowerShell：

```powershell
$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $codexSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\paper-anatomy" $codexSkills
Copy-Item -Recurse -Force ".\skills\paper-reconstruction" $codexSkills
```

重新启动 Codex 或新建任务，以便重新发现 Skill。若已存在同名目录，请先备份并确认版本，避免新旧文件混合。

### ⚪ 方式四：其他 Agent

对于支持 `SKILL.md` 或自定义 prompt / subagent / slash command 的 Agent：

1. 保留一个稳定的完整仓库 clone；
2. 将 `skills/paper-anatomy/` 和 `skills/paper-reconstruction/` 作为完整单元复制或链接到目标 Agent；
3. 若 Agent 不会自动发现 Skill，创建轻量 wrapper，先读取对应 `SKILL.md`，再按需读取同目录下的 `references/` 和 `scripts/`；
4. 不要只复制 `SKILL.md`，也不要混合两个 Skill 的输出契约；
5. 目标 Agent 若有自己的 frontmatter 规范，再做最小兼容调整。

---

<a id="how"></a>

## 🚀 How：如何调用、输入什么、得到什么

### 🗺️ Skill 索引

| 想做什么 | 使用 | 推荐输入 | 主要输出 |
|---|---|---|---|
| 读懂或审查论文 | `paper-anatomy` | 论文全文/链接、补充材料、关注问题、输出语言 | ABC：理论与叙事、设计与证据、带 PDF 页码/图表指针的结论与领域位置 |
| 核验网络科普引用 | `paper-anatomy` | 博主原话、引用论文、需要核验的具体结论 | “传播主张—原文结果—证据边界—后续证据”对照 |
| 重组与复现实验、问卷或纵向研究 | `paper-reconstruction` | 论文 DOI、附录/Supplement/OSF、复现层级；按需提供实施平台、分析软件和现实限制 | 来源账本、参与者/受访者流程、平台原生结构、材料/数据、目标软件分析、验证与研究发展 |
| 基于论文发展新研究 | `paper-reconstruction` | 原论文、你的想法、目标群体/情境、可用资源 | 理论不变量、可调参数、创新状态、设计方案与验证计划 |

### ⚡ 自动触发与显式调用

安装后可直接使用中文或英文描述任务；需要避免路由歧义时，显式指定 Skill：

```text
$paper-anatomy 请解剖这篇论文，重点检查变量、被试体验、统计结果和结论边界。
```

```text
$paper-reconstruction 请把这篇论文重组为可执行的 PsychoPy 实验，并评估我增加调节变量的想法。
```

> [!TIP]
> 如果一个请求同时要求解释与复现，以 `paper-reconstruction` 统领交付，并完成实现所需的论文解剖。

### 🔎 输入输出示例一：核验网络科普

输入：

```text
$paper-anatomy
某博主引用这篇研究声称：“每天进行这种运动一定能显著改善所有成年人的心理健康。”
请核对原论文，解释研究设计、样本、运动方案、因变量、效应量和结论边界，并判断博主是否过度概括。
附件：paper.pdf
```

输出索引：

```text
A. 论文提出了什么：理论、研究问题、样本与变量
B. 证据怎样产生：设计、测量、指标、统计结果、效应大小与 PDF 页码/图表定位
C. 论文真正支持什么：带来源指针的作者结论、限制、适用人群与后续证据

主张核验：
博主说法 → 原文证据 → 一致 / 部分一致 / 过度概括 / 不支持 → 判断理由
```

### 🧪 输入输出示例二：复现并发展新研究

输入：

```text
$paper-reconstruction
请重组复现这篇第三方惩罚实验。目标平台为 PsychoPy，无法实时多人连接。
我们通常使用 Python 分析。我还想加入“组织认同”作为调节变量，请评估其理论增量、被试可理解性、测量位置、潜在混淆和分析方案。
附件：paper.pdf、supplement.pdf
```

输出索引：

```text
A. DOI、Supplement、OSF 等来源账本、重组复现目标与证据边界
B. 被试视角流程与任务关系
C. 原平台、PsychoPy 蓝图和无服务器降级
D. 材料清单、事件日志、数据字典、Python 分析契约与验证
E. 理论不变量、可调参数、组织认同扩展、创新状态与 pilot 方案
```

---

<a id="references"></a>

## 📚 参考文献

Consensus. (2025, June 23). *How it works & Consensus FAQ’s*. https://consensus.app/home/blog/how-consensus-works/

Lewandowsky, S., Ecker, U. K. H., Seifert, C. M., Schwarz, N., & Cook, J. (2012). Misinformation and its correction: Continued influence and successful debiasing. *Psychological Science in the Public Interest, 13*(3), 106–131. https://doi.org/10.1177/1529100612451018

Nosek, B. A., Alter, G., Banks, G. C., Borsboom, D., Bowman, S. D., Breckler, S. J., Buck, S., Chambers, C. D., Chin, G., Christensen, G., Contestabile, M., Dafoe, A., Eich, E., Freese, J., Glennerster, R., Goroff, D., Green, D. P., Hesse, B., Humphreys, M., … Yarkoni, T. (2015). Promoting an open research culture. *Science, 348*(6242), 1422–1425. https://doi.org/10.1126/science.aab2374

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science, 349*(6251), Article aac4716. https://doi.org/10.1126/science.aac4716

Suarez-Lledo, V., & Alvarez-Galvez, J. (2021). Prevalence of health misinformation on social media: Systematic review. *Journal of Medical Internet Research, 23*(1), Article e17187. https://doi.org/10.2196/17187

Sumner, P., Vivian-Griffiths, S., Boivin, J., Williams, A., Venetis, C. A., Davies, A., Ogden, J., Whelan, L., Hughes, B., Dalton, B., Boy, F., & Chambers, C. D. (2014). The association between exaggeration in health related science news and academic press releases: Retrospective observational study. *BMJ, 349*, Article g7015. https://doi.org/10.1136/bmj.g7015

Vosoughi, S., Roy, D., & Aral, S. (2018). The spread of true and false news online. *Science, 359*(6380), 1146–1151. https://doi.org/10.1126/science.aap9559

---

<a id="star-history"></a>

## ⭐ Star 历史

<p align="center">
  <a href="https://www.star-history.com/#mohui373/paper-to-paradigm&amp;Date"><img src="https://api.star-history.com/svg?repos=mohui373/paper-to-paradigm&amp;type=Date" alt="paper-to-paradigm Star History Chart"></a>
</p>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/stargazers"><img src="https://img.shields.io/github/stars/mohui373/paper-to-paradigm?style=for-the-badge&amp;logo=github&amp;label=GitHub%20Stars&amp;color=F5B700" alt="GitHub stars"></a>
</p>

<p align="center">徽章实时显示当前 Star 数量，图表按日期展示累计变化；新仓库的曲线可能在产生并同步首批数据点后出现。</p>
