# Reading Protocol

## 1. Evidence Discipline

Use this order: article text; figures/tables/appendices; supplied supplements; linked repositories; external scholarly literature; labeled inference.

Tag uncertainty with plain labels when needed:

- `原文明确`
- `补充材料`
- `外部文献`
- `合理推断`
- `未能核实`

Never manufacture statistics, sample details, scale items, causal claims, URLs, or novelty.

## 2. Paper-Type Routing

先依据摘要与方法判断一个主要类型；混合论文可再标一个次要类型。类型判断必须改变 A、B、C 的分析重点，不能只改标题。理论、综述、元分析、文献计量、Delphi/共识或指南的详细路线见 `special-routes.md`。

| Type | B section treatment |
|---|---|
| Laboratory/online/field experiment | Participant flow, manipulation, measure, analysis, evidence |
| Multi-study empirical paper | Every Study gets at least a compact flow and result role |
| Survey/SEM/archival/modeling paper | Measurement and data-production flow; do not invent trials |
| Qualitative/mixed-method paper | Sampling, elicitation, coding, integration, evidential limits |
| Theory/review/conceptual paper | Empirical evidence base and 3-6 concrete empirical-study entries |
| Meta-analysis | Search/inclusion, effect construction, model, heterogeneity, publication-bias checks |
| Bibliometric/science-mapping paper | Database/query, cleaning, unit, network method, parameter, cluster interpretation |
| Delphi/consensus/guideline | Evidence base, panel composition, rounds, anonymity, threshold, disagreement, recommendation strength |

## 3. A: Research Narrative and Theory

Answer in this order:

1. Plain-language one-paragraph answer: what problem and what was found.
2. Research question and why it matters.
3. Theoretical lineage: key constructs and competing explanations.
4. Literature-review logic: known -> unresolved -> proposed answer.
5. Hypotheses or conceptual model.
6. Study architecture: what each Study contributes to the overall argument.

Separate the author's stated gap from a gap inferred by this skill.

### 3.1 Theory-source audit

For every theory or construct that carries a hypothesis, mediator, moderator, or discussion-level mechanism, inspect the article's in-text citation and reference entry. When accessible, read at least the abstract or relevant passage of the cited source rather than relying on the theory label alone.

Report compactly:

```text
theory/construct used
-> source directly cited by the focal paper
-> original proposition borrowed
-> path or claim it supports here
-> source role: foundational / integrative / supplementary / empirical / statistical
```

Distinguish the original theorist from the source through which the focal article imports the theory. If the direct source itself traces an older root, label the levels explicitly rather than replacing the focal article's citation.

Perform a construct-name check before translation. Similar terms are not interchangeable. For example, `efficacy and effectance` in psychological-ownership theory is not automatically Bandura's `self-efficacy`; verify the original wording, named theorist, measure, and model role. If a theory label is used without a clear foundational citation, say so and list the empirical sources the author actually provides.

Prioritize model-bearing citations. Do not turn A into an exhaustive bibliography of every introductory reference.

For theory, conceptual, and narrative-review papers, also perform a compact reference-integrity check on those model-bearing citations:

```text
in-text author/year
-> matching reference-list entry exists?
-> author/year/title are consistent?
-> cited source actually supports the borrowed proposition?
```

Report missing entries, year mismatches, or source substitutions as traceability limitations. Do not treat a bibliography error alone as disproof of the model, and do not audit every citation when it does not carry theoretical weight.

### 3.2 Claim-source map for reviews

For theory, review, meta-analysis, consensus, and guideline papers, state the overall thesis and split it into 3-7 checkable claims. For each claim, identify the theory or literature carrying it, source role, evidence type, consistency, contrary evidence, and boundary. Do not treat citation count as evidential strength or list theories without explaining what proposition is borrowed.

## 4. B: Design, Measurement, and Evidence

### 4.1 Task conceptualization

Before technical details, explain what participants actually see, know, decide, report, or learn. For cognitive/neuroscience/computational papers, translate abstract states, arms, values, replay, model parameters, or neural measures into observable task events.

For social-interaction, deception, simulated-agent, vignette, identity, exclusion, cooperation, or relationship-induction experiments, inspect the supplied materials for the exact context-building chain: cover story, role and identity assignment, social-presence cues, group labels, shared history, interaction contingency, instructions that induce imagination or closeness, event wording, persistence of the manipulation, and debriefing. Explain how these elements make the participant experience a relationship or social situation; do not reduce the manipulation to a condition label such as “member leaves.” Distinguish real partners from computer-controlled or pre-scripted partners.

### 4.2 Study coverage

For each Study report: sample; assignment; participant-visible sequence; manipulation/conditions; measures; exclusions; analysis; result; role in the paper. Use a Mermaid relation map when phases or branches are nontrivial.

### 4.3 Variables and analysis

Use bilingual labels where useful. Explain the analysis in concise Chinese before model syntax, for example:

- 普通最小二乘线性回归（ordinary least squares regression; `lm`）
- 二项逻辑回归（binomial logistic regression; `glm(..., family = binomial)`）
- 线性混合效应模型（linear mixed-effects model; `lmer`）
- 广义线性混合效应模型（generalized linear mixed-effects model; `glmer`）
- 结构方程模型（structural equation modeling; `lavaan`）

Do not turn the reading output into a statistics textbook. State that the user can ask for a deeper model explanation when needed.

### 4.4 Result-to-claim table

Prefer a table with:

```text
Study/result block | comparison or model | key statistic/trend | supports what | does not establish | figure/table
```

Distinguish manipulation checks, primary tests, secondary/exploratory results, mediation, robustness, and null findings.

For meta-analyses, add `k`, N, effect metric and direction, estimate, confidence interval, heterogeneity, prediction interval when reported, bias/robustness checks, and practical meaning. For Delphi or consensus papers, distinguish agreement percentage, effect magnitude, evidence certainty, and recommendation strength.

## 5. C: Evidence-to-Discussion Closure

Build a claim ladder:

```text
observed result
-> supported empirical claim
-> author's theoretical interpretation
-> discussion-level generalization
-> boundary condition / alternative explanation
```

Identify the strongest contribution, unresolved inconsistency, external-validity boundary, measurement boundary, and causal boundary. Practical implications must be proportional to the design.

## 6. Current-Literature Check

For papers older than three years, browse by default and conduct an extended check yielding about five representative sources. Search in this order when accessible:

1. Reviews/meta-analyses and direct replications.
2. Later empirical variants addressing the original limitation.
3. Paradigm or measurement improvements.
4. Open materials/data/code useful for follow-up.
5. Strong contradictory or boundary-condition evidence.

Try Google Scholar and APA PsycNet when accessible, but never claim access if blocked. Use publisher pages, Crossref, Semantic Scholar, PubMed, OSF, repositories, and cited references as fallbacks. Record brief query logic and give clickable DOI/publisher/repository links.

For recent papers, browse when the user asks about current status, when novelty is evaluated, or when external literature is needed to interpret the claim.

## 7. Concision

Use tables for cross-Study comparisons and result mappings. Avoid repeating the same finding in A, B, and C:

- A states the proposed answer.
- B shows the evidence.
- C explains what that evidence changes and where it stops.
