<h1 align="center">paper-to-paradigm</h1>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/blob/main/README.md">简体中文</a> ·
  <a href="https://github.com/mohui373/paper-to-paradigm/blob/main/README_EN.md">English</a> ·
  <a href="#what">🧰 Skill Index</a>
</p>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/actions/workflows/validate.yml"><img src="https://github.com/mohui373/paper-to-paradigm/actions/workflows/validate.yml/badge.svg" alt="Validate Skills"></a>
  <img src="https://img.shields.io/badge/version-0.1.0-7C3AED?style=flat-square" alt="Version 0.1.0">
  <img src="https://img.shields.io/badge/skills-2-0EA5E9?style=flat-square" alt="2 Skills">
  <a href="https://github.com/mohui373/paper-to-paradigm/stargazers"><img src="https://img.shields.io/github/stars/mohui373/paper-to-paradigm?style=flat-square&amp;logo=github&amp;label=stars&amp;color=F5B700" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-22C55E?style=flat-square" alt="Apache-2.0 License"></a>
  <img src="https://img.shields.io/badge/focus-experimental_%26_behavioral-F97316?style=flat-square" alt="Experimental and behavioral research">
</p>

<p align="center"><strong>paper-to-paradigm</strong> is a two-armed paper-surgery robot for every reader, with a specialty in experimental and behavioral research: <strong>paper-anatomy</strong> dissects theory, variables, evidence, and participant experience, while <strong>paper-reconstruction</strong> stitches sources, procedures, materials, data, and analyses back into a reproducible study. The patient is the paper; informed consent is still your responsibility.</p>

---

<a id="contents"></a>

## 🧭 Contents

- [💡 Why: Why build these Skills?](#why)
- [⏰ When: When should you use them?](#when)
- [👥 Who: Who and what research are they for?](#who)
- [🧰 What: What can they do now?](#what)
- [📦 Where: How do you install them in different Agents?](#where)
- [🚀 How: How do you invoke them, what do you provide, and what do you receive?](#how)
- [📚 References](#references)
- [⭐ Star History](#star-history)

---

<a id="why"></a>

## 💡 Why: Why build these Skills?

I am currently a graduate student in basic psychology, with an undergraduate background in human resource management. I focus primarily on behavioral experiments, with research interests in social and experimental psychology, organizational behavior, moral behavior, and decision-making. This project did not begin as another paper summarizer. It grew out of a set of recurring problems I encountered while reading papers, conducting research, and designing experiments.

Many excellent literature-search and paper-reading prompts and Skills already exist. They can help us find papers quickly and summarize background, methods, results, and conclusions. Consensus, for example, uses keyword and semantic search over titles and abstracts, then offers features such as Study Snapshot, Ask Paper, Pro Analysis, and Consensus Meter for single-paper and multi-paper synthesis ([Consensus, 2025](https://consensus.app/home/blog/how-consensus-works/)). These tools are good at answering “what should I find?” and “roughly what does the literature say?” Yet once the purpose of reading shifts from awareness to research, a gap may remain: **we know the conclusion, but we still cannot see clearly how it was produced by the research design.**

The parts of a paper that matter most for research quality are rarely concentrated in the abstract. How was an independent variable operationalized? What did participants perceive, and how was their response recorded? Where do mediators, moderators, and controls enter the model? How do raw responses become final indices? How do multiple studies progressively rule out alternative explanations? These details are scattered across the introduction, methods, results, figures, tables, appendices, and supplementary materials. Without a stable analysis route, readers repeatedly ask follow-up questions, flip between pages, and reconstruct context across multiple conversations—often ending with disconnected theory summaries, statistical notes, and method fragments.

Research quality also depends on whether the introduction and discussion tell a coherent “good story.” This does not mean dramatizing results. It means forming a testable chain from research question to theoretical gap, hypothesis, evidence, and conclusion. The introduction should explain why the problem matters, where existing explanations break down, and why each study is necessary. The discussion should return to the original question, state which explanations were supported, preserve the alternatives that remain, and define how far the conclusion can travel. Reading only methods and significance tests may miss the paper's theoretical advance; accepting a fluent narrative may mistake “plausible” for “well supported.” The Skills therefore reconstruct how the authors open and close the research story while checking whether each turn is supported by design, data, and citation.

The problem becomes even clearer in experimental design. Researchers enter an experiment already knowing the theory, hypotheses, and variables. Participants see only instructions, stimuli, choices, feedback, and rewards. A task that seems obvious to the researcher may mean something else to a participant. A manipulation intended to change one psychological process may instead create confusion, reveal the research purpose, or induce a strategy driven by the payoff structure. Unless we temporarily set aside our own theoretical knowledge and walk through the study from the participant's perspective, it is difficult to judge:

- what participants think the task is asking them to do;
- whether the instructions and materials create the intended understanding;
- whether a manipulation changes the focal construct or task difficulty, emotion, demand characteristics, or something else;
- whether each participant experience maps to a variable, event log, analysis index, and theoretical interpretation;
- whether a seemingly novel paradigm adds theoretical value or merely changes surface materials.

This matters not only for understanding papers but also for checking, reproducing, and extending research. Large-scale replication work has kept psychology's reproducibility problems in view ([Open Science Collaboration, 2015](https://doi.org/10.1126/science.aac4716)), while open-science frameworks such as the TOP Guidelines emphasize transparency in design, materials, data, analysis, and replication ([Nosek et al., 2015](https://doi.org/10.1126/science.aab2374)). `paper-to-paradigm` cannot solve reproducibility by itself, but it can separate “what the authors said,” “where the evidence is,” “what is still missing for implementation,” and “what is inference” at the reading stage, leaving cleaner interfaces for verification, preregistration, material preparation, and analysis.

The collection therefore aims to do three things:

1. **Close reading gaps:** connect theory, variables, participant experience, data, and discussion instead of merely summarizing conclusions; expose breaks, confounds, and evidence boundaries.
2. **Improve research efficiency:** answer in one stable structure what would otherwise require repeated follow-up, so notes can move directly into proposals, reviews, presentations, study design, and analysis.
3. **Help research keep growing:** extract transferable design parameters while respecting the original evidence; identify what can be replicated, what must be rebuilt, and what new ideas deserve a pilot, manipulation check, or follow-up study.

As experience accumulates, recurring strengths, risks, and implementation limits of the same design family can be retained. Reading then becomes more than one-time conclusion retrieval: it becomes a starting point for study design, cross-domain adaptation, and methodological improvement. This project does not replace the original paper, domain experts, or researcher judgment. It aims to make that judgment more complete, transparent, and attentive to what participants actually experience.

---

<a id="when"></a>

## ⏰ When: When should you use them?

### 🎓 1. Academic and research work

These Skills primarily support tasks closely connected to papers. Here, “learning” means more than memorizing conclusions: it means becoming able to ask questions, select theory, understand methods, design studies, and evaluate evidence.

| Use case | Common difficulty | What the Skills provide |
|---|---|---|
| Proposal and topic selection | Many papers have been read, but the theoretical origin and reality of the gap remain unclear | Organize theoretical sources, propositions, evidence, disputes, and unresolved questions |
| Literature review | The review becomes a list of paper summaries rather than an argument | Organize sources by claim, design, method, and conclusion boundary; build claim-source-evidence matrices |
| Theoretical support | A similarly named theory is found, but it may not support the proposed path | Trace the paper's direct sources and distinguish foundational theory, later integration, auxiliary explanation, and adjacent evidence |
| Journal club or presentation | The paper can be retold, but the reason for each Study is unclear | Reconstruct narrative, participant flow, variables, statistical evidence, and cross-Study progression |
| Learning an experimental paradigm | The paradigm name is familiar, but the participant experience and key parameters are not | Walk through the task from the participant's perspective; unpack manipulation, stimuli, feedback, scoring, timing, and comprehensibility |
| Experimental design and pilot | The researcher-side logic is complete, but the task may be unclear to participants | Check instructions, roles, demand characteristics, confounds, logs, manipulation checks, and implementation risks |
| Replication and platform migration | Original materials, programs, or field details are incomplete | Define the replication level and rebuild materials, protocols, data dictionaries, analyses, and validation steps |
| Personalized research extension | A new idea exists, but it may add complexity rather than theoretical value | Separate theoretical invariants from adjustable parameters and evaluate increment, boundary, measurement, cost, and untested assumptions |

The Skills can therefore support both the front end of research—proposals, reviews, theory selection, and study conception—and later stages such as experimental design, material preparation, data structure, statistical reproduction, and extension. A structured reading can feed the next stage instead of forcing the same paper to be understood again from scratch.

### 🛡️ 2. Everyday information verification

More health, exercise, psychology, education, and management communicators now attach references to popular-science claims. This is a positive development: readers at least have a route back to the source rather than having to trust an untraceable statement.

But “a paper is attached” does not guarantee that the statement matches the paper. In attention-driven environments, complex findings can be compressed into stronger headlines: correlation becomes causation, a narrow sample becomes “everyone,” statistical significance becomes a large practical benefit, and limitations disappear. Research on health-science communication has found that exaggeration in news is strongly associated with exaggeration in academic press releases, including causal claims from correlational work, unsupported advice, and direct generalization from animals to humans ([Sumner et al., 2014](https://doi.org/10.1136/bmj.g7015)). A large Twitter study found that false news traveled farther, faster, deeper, and more broadly than true news ([Vosoughi et al., 2018](https://doi.org/10.1126/science.aap9559)). These findings do not show that every communicator exaggerates intentionally, but they do show why striking and absolute wording may gain an advantage.

Health misinformation spans vaccines, diet, drugs, disease, and medical interventions across multiple social platforms, with prevalence varying by topic, platform, and method ([Suarez-Lledo & Alvarez-Galvez, 2021](https://pmc.ncbi.nlm.nih.gov/articles/PMC7857950/)). Misleading information may also continue to influence reasoning after correction—the continued influence effect ([Lewandowsky et al., 2012](https://doi.org/10.1177/1529100612451018)). It is therefore safer to retain a verification step when first receiving a claim than to wait until a stable impression must be corrected.

When the reader does not understand a field's measures, models, or effect sizes, `paper-anatomy` can compare “what the creator said” with “what the paper supports”:

1. record the original wording, citation, and communication context;
2. obtain the full paper and necessary supplementary materials;
3. explain the design, sample, variables, measures, effect sizes, and uncertainty in plain language;
4. classify the public claim as aligned, partly aligned, overstated, unsupported, or currently unverifiable;
5. check causal inflation, population overgeneralization, omitted boundaries, single-study overreach, and quote-mining;
6. calibrate high-impact conclusions against reviews, meta-analyses, guidelines, and later studies.

The goal is not merely to catch errors. It is to turn passive input into active understanding: readers learn not only whether a statement is credible, but also what the measure means, what the design can answer, and why the conclusion has boundaries. This is not universal fact-checking and does not replace diagnosis, clinical guidelines, or professional advice. It provides a route from an online claim back to paper-level evidence and independent judgment.

---

<a id="who"></a>

## 👥 Who: Who and what research are they for?

The collection is **for all readers, with a specialty in experimental and behavioral research**. It serves graduate and undergraduate students, researchers, teachers, research assistants, and non-specialist readers who want to verify paper-based claims. It is not restricted to one discipline or study type. Given a paper or another traceable source, it selects an anatomy or reconstruction route based on the research question, evidence-production process, and intended use, with greater depth in paradigms, participant experience, behavioral measurement, and implementation chains.

### 🧩 Different fields, different emphases

| Field or task | Adaptive focus | Example question |
|---|---|---|
| Experimental psychology | Paradigm, theory-manipulation link, participant experience, task stages, measurement sensitivity | Does a Stroop variant change inhibitory control, task difficulty, or both? |
| Social psychology | Social context, identity, interaction authenticity, demand characteristics, manipulation checks | Are the “other players” real-time humans, delayed matches, or generated feedback? |
| Organizational behavior and management | Organizational realism, level of analysis, behavior versus intention, generalizability across organizations | Can laboratory leader feedback represent organizational interaction? Can an individual-level conclusion be lifted to teams? |
| Behavioral decision-making and economics | Incentive compatibility, payoffs, risk, role information, decision process | Is third-party punishment a moral response or a product of rewards and social desirability? |
| Health and exercise research | Design, control group, measure meaning, surrogate endpoints, effect size, population | Does a statistically improved indicator imply a meaningful health benefit? |
| Education, communication, and HCI | Task ecology, learning/use context, behavioral logs, short- and long-term outcomes | Does a laboratory click represent sustained real-world platform use? |

### 🔬 Different designs, different judgment routes

| Study type | What to reconstruct | What to guard against |
|---|---|---|
| Experiment and quasi-experiment | Participant flow, manipulation, randomization, measurement, exclusion, result-hypothesis map | Confounding, demand characteristics, alternatives, excessive causal language |
| Cross-sectional survey | Constructs, scale sources, item coverage, reliability/validity, variable relations, model paths | Common-method bias, incomplete short scales, correlation-as-causation |
| Longitudinal and multiwave research | Waves, spacing, attrition, temporal order, lags, within-/between-person effects | Invariance problems, selective attrition, directional overclaiming |
| Qualitative research | Sampling, material generation, coding, researcher position, theme-material link | Untraceable themes, interpretation beyond material, missing reflexivity |
| Theoretical or conceptual paper | Central claims, theoretical origins, construct boundaries, testable paths | Near-name construct confusion, missing pivotal citations, invented empirical flow |
| Systematic review and meta-analysis | Search, eligibility, coding, effect construction, heterogeneity, bias | Letting a pooled effect hide evidence quality, heterogeneity, and causal limits |
| Delphi, consensus, and guideline | Expert selection, rounds, feedback, thresholds, recommendation formation | Treating expert agreement as an effect size or high-certainty evidence |

> [!NOTE]
> When a paper is not experimental, the Skill does not invent a participant screen flow. It reconstructs the evidence-production process appropriate to that study type.

---

<a id="what"></a>

## 🧰 What: What can they do now?

### 🤖 Two core Skills

<p align="center">
  <a href="skills/paper-anatomy/README_EN.md"><img src="https://img.shields.io/badge/paper--anatomy-Read_%26_Audit-7C3AED?style=for-the-badge" alt="paper-anatomy: Read and Audit"></a>
  <a href="skills/paper-reconstruction/README_EN.md"><img src="https://img.shields.io/badge/paper--reconstruction-Reconstruct_%26_Replicate-0EA5E9?style=for-the-badge" alt="paper-reconstruction: Reconstruct and Replicate"></a>
</p>

| Skill | Position | Main tasks | Boundary | Default output |
|---|---|---|---|---|
| [`paper-anatomy`](skills/paper-anatomy/README_EN.md) | Dissect a paper through both the researcher evidence chain and participant experience | Theoretical origins, variables and measures, Study flow, statistics, page/figure/table locators, conclusions, limitations, later evidence | Does not turn the study into a program | ABC anatomy report plus source-location sidecar |
| [`paper-reconstruction`](skills/paper-reconstruction/README_EN.md) | Reassemble a paper from participant experience to backend implementation | DOI/appendix/Supplement/OSF ledger, survey/longitudinal flow, platform-native structures, materials, logs, data dictionary, target-software analysis, validation, research development | Does not replace reading whose goal is understanding and critique | Minimum sufficient artifacts or an ABCDE package |

`paper-reconstruction` now treats E-Prime as its first deep implementation path. It defines Session/Block/Trial Procedures, the Lists that call them, object order, and whether trials are serial, serially repeated, interleaved, nested, conditional, or truly parallel through an external synchronization contract. A structured bundle connects the event log, data dictionary, and analysis contract, while semantic auditing prevents conditions and fields from being renamed, omitted, or disconnected across artifacts. Runtime status is not marked as verified until the `.es3 → .ebs3 → E-Run smoke test → log audit` chain is complete.

Non-E-Prime routes are not cosmetic renamings. PsychoPy, MATLAB/Psychtoolbox, jsPsych, Qualtrics/SoSci, oTree, Inquisit, Gorilla, and field protocols use native components, files, logs, and validation structures. Survey and longitudinal routes separately handle item IDs, display logic, anonymous matching, waves, reminders, attrition, cross-wave versions, paradata, and missingness. A cross-platform validator checks phases, native components, output fields, analysis interfaces, and runtime evidence.

### 🌱 Personalized innovation from existing research

When users have new ideas, `paper-reconstruction` can extend the original study with a new population, context, mechanism, variable, material, interaction, measure, or platform rather than copying it mechanically. It will:

1. distinguish theoretical invariants from adjustable parameters;
2. examine theoretical increment and participant comprehensibility;
3. audit confounds, measurement-analysis fit, and implementation cost;
4. separate original-paper support, later evidence, user hypotheses, and untested components;
5. avoid calling an idea “first,” “novel,” or a “research gap” before a current literature search.

> [!IMPORTANT]
> Personalized innovation is not arbitrary decoration. It is the process of turning an idea into a traceable, bounded, and testable study design.

### 🎛️ Task-specific questions and tool adaptation

Personalization does not mean a long onboarding questionnaire. The Skills first identify the requested artifact and ask only questions that change delivery. Implementation software is requested only for program replication or platform migration; R, Python, SPSS, Mplus, MATLAB, Stata, SAS, JASP/Jamovi, or another analysis environment is requested only for statistical reproduction, analysis code, or an analysis interface. Known information is not requested again, and unanswered questions do not block platform-neutral work.

The same paper can therefore produce different but semantically aligned artifacts: Proc/List and E-Run for E-Prime, Routine/Loop/conditions for PsychoPy, phase functions/Screen/event structures for MATLAB, Blocks/logic/waves/anonymous matching for surveys, and native SPSS or Python analysis artifacts rather than a forced R conversion.

---

<a id="where"></a>

## 📦 Where: How do you install them in different Agents?

> [!IMPORTANT]
> This repository uses multiple Skill directories in one collection. Keep each Skill directory intact during installation rather than copying only `SKILL.md`.

### 🟢 Option 1: install with `npx skills`

Node.js 18 or later is required. List available Skills first:

```bash
npx skills add mohui373/paper-to-paradigm --list
```

Install both Skills globally for Codex:

```bash
npx skills add mohui373/paper-to-paradigm --global --agent codex --skill '*' --yes --copy
```

Install for all CLI-supported Agents:

```bash
npx skills add mohui373/paper-to-paradigm --all
```

Update globally installed Skills:

```bash
npx skills update --global --yes
```

The following manual methods share one stable clone:

```bash
git clone https://github.com/mohui373/paper-to-paradigm.git
cd paper-to-paradigm
```

### 🟠 Option 2: Claude Code

Keep each entire Skill directory; copying only `SKILL.md` is not sufficient.

macOS / Linux:

```bash
mkdir -p ~/.claude/skills
cp -R ./skills/paper-anatomy ~/.claude/skills/
cp -R ./skills/paper-reconstruction ~/.claude/skills/
```

Windows PowerShell:

```powershell
$claudeSkills = Join-Path $env:USERPROFILE ".claude\skills"
New-Item -ItemType Directory -Force -Path $claudeSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\paper-anatomy" $claudeSkills
Copy-Item -Recurse -Force ".\skills\paper-reconstruction" $claudeSkills
```

Start a new Claude Code session, then invoke the Skills with natural language or by explicitly naming `paper-anatomy` or `paper-reconstruction`.

### 🔵 Option 3: Codex

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R ./skills/paper-anatomy ~/.codex/skills/
cp -R ./skills/paper-reconstruction ~/.codex/skills/
```

Windows PowerShell:

```powershell
$codexSkills = Join-Path $env:USERPROFILE ".codex\skills"
New-Item -ItemType Directory -Force -Path $codexSkills | Out-Null
Copy-Item -Recurse -Force ".\skills\paper-anatomy" $codexSkills
Copy-Item -Recurse -Force ".\skills\paper-reconstruction" $codexSkills
```

Restart Codex or open a new task so the Skills are discovered again. If a directory with the same name already exists, back it up and check versions first to avoid mixing old and new files.

### ⚪ Option 4: other Agents

For Agents that support `SKILL.md`, custom prompts, subagents, or slash commands:

1. keep one stable, complete clone of the repository;
2. copy or link `skills/paper-anatomy/` and `skills/paper-reconstruction/` as complete units;
3. if the Agent cannot discover Skills automatically, create a lightweight wrapper that first reads the relevant `SKILL.md`, then loads its `references/` and `scripts/` as needed;
4. do not copy only `SKILL.md`, and do not mix the two output contracts;
5. make only the minimum frontmatter adaptation required by the target Agent.

---

<a id="how"></a>

## 🚀 How: How do you invoke them, what do you provide, and what do you receive?

### 🗺️ Skill index

| Goal | Use | Recommended input | Main output |
|---|---|---|---|
| Understand or audit a paper | `paper-anatomy` | Full text or link, supplementary materials, question, output language | ABC: theory and narrative, design and evidence, conclusions with PDF page/figure pointers and field position |
| Verify an online popular-science claim | `paper-anatomy` | Original wording, cited paper, exact claim to verify | Public claim → paper result → evidence boundary → later evidence |
| Reconstruct an experiment, survey, or longitudinal study | `paper-reconstruction` | DOI, appendix/Supplement/OSF, replication level; implementation platform, analysis software, and limits when relevant | source ledger, participant/respondent flow, native implementation, materials/data, target-software analysis, validation, development |
| Develop a new study from a paper | `paper-reconstruction` | Original paper, your idea, target population/context, available resources | Theoretical invariants, adjustable parameters, novelty status, design, and validation plan |

### ⚡ Automatic and explicit invocation

After installation, describe the task in Chinese or English. To avoid routing ambiguity, name the Skill explicitly:

```text
$paper-anatomy Dissect this paper, focusing on variables, participant experience,
statistical results, exact PDF locations, and conclusion boundaries.
```

```text
$paper-reconstruction Reconstruct this paper as an executable PsychoPy experiment
and evaluate my proposal to add a moderator.
```

> [!TIP]
> If one request asks for both interpretation and replication, `paper-reconstruction` leads the delivery and performs the minimum paper anatomy required for implementation.

### 🔎 Input/output example 1: verify an online claim

Input:

```text
$paper-anatomy
A creator cites this study and claims: “Doing this exercise every day will definitely
improve mental health in all adults.” Check the original paper, explain the design,
sample, intervention, outcome variables, effect sizes, and boundaries, and decide
whether the claim is overstated.
Attachment: paper.pdf
```

Output index:

```text
A. What the paper proposes: theory, question, sample, and variables
B. How evidence is produced: design, measures, indices, statistics, effect sizes,
   and exact PDF page/figure/table locations
C. What the paper actually supports: source-grounded conclusions, limitations,
   applicable population, and later evidence

Claim verification:
Creator claim → paper evidence → aligned / partly aligned / overstated / unsupported
→ reasoned judgment
```

### 🧪 Input/output example 2: replicate and extend a study

Input:

```text
$paper-reconstruction
Reconstruct this third-party punishment experiment in PsychoPy. Real-time multiplayer
connection is not available, and we normally analyze in Python. I also want to add organizational identification as a
moderator. Evaluate theoretical increment, participant comprehensibility, measurement
placement, possible confounds, and the analysis plan.
Attachments: paper.pdf, supplement.pdf
```

Output index:

```text
A. DOI/Supplement/OSF source ledger, reconstruction target, and evidence boundary
B. Participant-perspective flow and task relationships
C. Original platform, PsychoPy blueprint, and no-server fallback
D. Materials, event log, data dictionary, Python analysis contract, and validation
E. Theoretical invariants, adjustable parameters, moderator extension,
   novelty status, and pilot plan
```

---

<a id="references"></a>

## 📚 References

Consensus. (2025, June 23). *How it works & Consensus FAQ’s*. https://consensus.app/home/blog/how-consensus-works/

Lewandowsky, S., Ecker, U. K. H., Seifert, C. M., Schwarz, N., & Cook, J. (2012). Misinformation and its correction: Continued influence and successful debiasing. *Psychological Science in the Public Interest, 13*(3), 106–131. https://doi.org/10.1177/1529100612451018

Nosek, B. A., Alter, G., Banks, G. C., Borsboom, D., Bowman, S. D., Breckler, S. J., Buck, S., Chambers, C. D., Chin, G., Christensen, G., Contestabile, M., Dafoe, A., Eich, E., Freese, J., Glennerster, R., Goroff, D., Green, D. P., Hesse, B., Humphreys, M., … Yarkoni, T. (2015). Promoting an open research culture. *Science, 348*(6242), 1422–1425. https://doi.org/10.1126/science.aab2374

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science, 349*(6251), Article aac4716. https://doi.org/10.1126/science.aac4716

Suarez-Lledo, V., & Alvarez-Galvez, J. (2021). Prevalence of health misinformation on social media: Systematic review. *Journal of Medical Internet Research, 23*(1), Article e17187. https://doi.org/10.2196/17187

Sumner, P., Vivian-Griffiths, S., Boivin, J., Williams, A., Venetis, C. A., Davies, A., Ogden, J., Whelan, L., Hughes, B., Dalton, B., Boy, F., & Chambers, C. D. (2014). The association between exaggeration in health related science news and academic press releases: Retrospective observational study. *BMJ, 349*, Article g7015. https://doi.org/10.1136/bmj.g7015

Vosoughi, S., Roy, D., & Aral, S. (2018). The spread of true and false news online. *Science, 359*(6380), 1146–1151. https://doi.org/10.1126/science.aap9559

---

<a id="star-history"></a>

## ⭐ Star History

<p align="center">
  <a href="https://www.star-history.com/#mohui373/paper-to-paradigm&amp;Date"><img src="https://api.star-history.com/svg?repos=mohui373/paper-to-paradigm&amp;type=Date" alt="paper-to-paradigm Star History Chart"></a>
</p>

<p align="center">
  <a href="https://github.com/mohui373/paper-to-paradigm/stargazers"><img src="https://img.shields.io/github/stars/mohui373/paper-to-paradigm?style=for-the-badge&amp;logo=github&amp;label=GitHub%20Stars&amp;color=F5B700" alt="GitHub stars"></a>
</p>

<p align="center">The badge tracks the current Star count, while the chart shows cumulative growth by date. A new repository may not show a curve until its first data points have been collected and synchronized.</p>
