# Paper Reconstruction and Replication Protocol / 论文重组复现协议

## 1. Evidence and Scope

Use evidence in this order: article; figures/tables/appendices; supplements; OSF/GitHub/preregistration/data repositories; program materials; labeled inference; replicator decision.

At the top state what materials were actually inspected. Mark claims as `原文明确`, `补充材料`, `外部材料`, `合理推断`, or `复现建议` when ambiguity matters.

Replication levels:

| Level | Meaning |
|---|---|
| Conceptual | Preserve causal/design logic with newly built materials |
| Program | Recreate instructions, stimuli, randomization, screens, timing, and logging |
| Statistical | Recreate exclusions, variables, models, contrasts, and figures from data |
| Direct copy | Use original program, stimuli, settings, randomization, and analysis package |

### PDF index gate

For every PDF, run the shared `../paper-anatomy/scripts/prepare_paper.py` before reconstruction. Use `document_index` to separate a standalone paper from papers in proceedings or another collection, select the requested paper by ordinal, `paper_id`, DOI, or unique title phrase, and then locate its abstract, introduction/theory, research design, results/analysis, and discussion/value ranges. If the user does not specify a paper in a multi-paper document, process all detected papers by default. Never guess an ambiguous selection.

Treat `source_bundle.json` as a local navigation sidecar, not a report section or replication deliverable. Bring only the selected page ranges into working context. In the ABCDE output, retain the selected-paper scope and compact page/figure/table pointers needed to support claims; do not paste `document_index`, page inventories, or page text.

## 2. A: Paper Reconstruction Target and Evidence

Include: research question; theory; study map; bilingual variables; raw-response-to-index path; exclusions; statistical model; result/figure mapping; exact replication target.

For complex tasks, first provide a plain-language task conceptualization. For each Study state whether it will be directly replicated, conceptually replicated, or only summarized, and why.

For model-bearing theories, inspect the focal paper's in-text citations and distinguish the foundational theory, the source directly used by the paper, supplementary explanations, and empirical support. State which model path each source justifies. Check the original construct wording and measure before translating; do not collapse similarly named constructs such as `efficacy/effectance` and `self-efficacy`.

## 3. B: Participant-View Flow

Begin with `B0. 任务关系图`. Show Study, scenario, block, trial, round, role, practice, condition, and backend logic as serial, crossed, nested, repeated, or parallel. Use Mermaid for reusable structure.

When a paper has multiple task versions, cohorts, arms, or control samples, mark **sample assignment** separately from **within-person repetition**. State the expected number of blocks, trials, or waves per version when the design makes it recoverable. Never call two independently recruited versions “within-subject” merely because each version contains repeated conditions.

For each screen or protocol step report:

```text
participant sees | participant does | backend/experimenter action | saved data | research logic
```

Multi-role designs must identify the current role. Give every Study at least a compact flow or a concrete reason for omission.

## 4. C: Program and Protocol Blueprint

### 4.1 Identify the original and target platforms conditionally

Ask about a target implementation platform only for program replication, direct copy, or migration. Recognize E-Prime, PsychoPy, MATLAB/Psychtoolbox, jsPsych, Qualtrics, SoSci Survey, oTree, Inquisit, Gorilla, custom code, field/paper/oral/cash protocol, hybrid apparatus, or unspecified. Do not infer the original platform from task style alone. Use `platform-adapters.md` for non-E-Prime native structures and `survey-longitudinal-path.md` for survey or longitudinal workflows.

### 4.2 Original-platform blueprint

Map screens/steps to native structures:

- E-Prime: List / Proc / Slide / TextDisplay / ImageDisplay / FeedbackDisplay / Inline.
- PsychoPy: routines / loops / conditions / components / code.
- MATLAB/Psychtoolbox: entry point / phase functions or state machine / Screen / input queue / event structure.
- jsPsych: timeline / plugin / timeline variables / data properties.
- Qualtrics/SoSci: blocks / display logic / randomizer / embedded data / scoring.
- oTree: subsession / group / player / pages / WaitPage / payoff.
- Field protocol: role cards / spoken script / comprehension / decision sheets / matching / payment / experimenter log.

### 4.3 Local implementation and downgrade

Always give an operable local route when direct implementation is unsuitable. Consider:

- single-computer simulated interaction;
- face-to-face dual-computer operation;
- LAN/shared-folder/CSV handoff;
- experimenter-mediated synchronization;
- prerecorded or pregenerated partner feedback;
- confederate script;
- external timer, microphone, camera, eye tracker, EEG/fNIRS trigger, button box;
- offline protocol plus later data entry.

State what stays automated, what becomes manual, how synchronization works, and what must be logged.

For E-Prime, distinguish `serial`, `serial-repeat`, `interleaved-repeat`, `nested-repeat`, `conditional`, and `parallel-external`. A Procedure is a sequential event timeline and is normally launched by a List; do not describe several Trial types as truly parallel when they are actually interleaved or nested. Read `eprime-execution-path.md` for the full build and runtime-state contract.

### 4.4 Reality check for social interaction

Classify partners as real simultaneous humans, delayed real responses, experimenter-controlled, prerecorded/pregenerated, or simulated agents. Preserve deception and debriefing requirements.

### 4.5 Pseudocode

Label code as executable or conceptual. Explain purpose in one sentence and use inline Chinese parenthetical comments, for example:

```text
if trial.partner_type == "simulated":      # （读取虚构玩家条件）
    shown_choice = schedule[trial_index]    # （按预设序列显示对方选择）
save(trial_index, raw_rt, shown_choice)     # （保存试次级原始数据）
```

### 4.6 Analysis-ready logging

Before programming ends, define a tidy event log that the selected analysis environment can read. At minimum consider:

```text
participant_id, session_id, study_id, condition, role, block_id, trial_id,
stimulus_id, response_raw, response_value, rt_ms, outcome, timestamp,
attention_check, exclusion_flag, software_version
```

Only include fields relevant to the study.

Before delivery, cross-check that every field logged by the program exists in the data dictionary and every field required by the analysis is either logged or has a declared derivation. For structured bundles, run `scripts/audit_replication_bundle.py`.

## 5. C5 and D: Analysis, Materials, Data, and Verification

Put the paper's **actual analysis route** in C5: analysis environment, model family, outcome, predictors, random/repeated structure, estimand or contrasts, correction, and the table/figure it should reproduce. Do not replace this with a generic event-log table or silently substitute a preferred method such as R, regression, or mediation.

Use D for the handoff after analysis has been specified:

```text
D1 source/material status and what it can support
-> D2 minimum data fields / dictionary needed to run the stated analysis
-> D3 validation, source-conflict resolution, and runtime/analysis difference handling
```

Only add a standalone self-built materials package when the user requests implementation artifacts or it is necessary to close a documented material gap. Do not generate a generic list of invented files merely to occupy D2.

Turn gaps into actions:

| Item | Available evidence | Can copy | Must rebuild/customize | Validation |
|---|---|---|---|---|

Prioritize instructions, stimuli, randomization, manipulation checks, scoring, exclusion rules, code, data dictionary, analysis code, preregistration, and platform settings.

If original materials are unavailable, specify what can be rebuilt today, which invariants must be preserved, and which pilot/comprehension/manipulation checks are required.

If analysis artifacts are needed and the user has not named an environment, ask once which software the team uses. If unanswered, provide a platform-neutral data and analysis contract rather than defaulting to R. Preserve this pipeline across software:

```text
import -> validate -> exclude -> derive -> describe -> model -> contrasts -> figure/table -> export -> session record
```

Read `analysis-environment.md` whenever analysis artifacts are needed. Read `r-reproducibility-guide.md` only when R is selected.

## 6. E: Experimental Parameters and Research Development

Extract manipulable paradigm parameters: information, role, agency, timing, social reality, stakes, feedback, observability, response, and outcome.

Build each priority idea as an evidence chain, not an inspiration list:

```text
paper limitation or reusable paradigm structure
-> named theory and/or later scholarly evidence
-> remaining uncertainty
-> falsifiable research question and compact design
-> evidence status and boundary
```

Each idea needs at least two traceable anchors. A strong minimum is one paper-specific anchor plus one named theory or later scholarly source with a clickable link; user direction can refine relevance but does not replace evidence. State whether the support is `已检索确认`, `部分支持`, or `待检索确认`. Treat cross-sectional mediation, adjacent tasks, and review claims as bounded evidence rather than proof of the focal paper's mechanism.

For papers older than three years, browse and return about five representative later sources covering reviews, replications, variants, method improvements, contradictory evidence, or open materials. Mark ideas as `已检索确认`, `部分支持`, or `待检索确认`. Do not claim a publishable gap from a superficial search.

## 7. Feedback and Project Iteration

End with the five-dimension 25-point feedback table. Do not create an F or G report section. Project-level lessons are written to the private upgrade log only after the user scores the output.
