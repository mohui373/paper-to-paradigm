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

## 2. A: Paper Reconstruction Target and Evidence

Include: research question; theory; study map; bilingual variables; raw-response-to-index path; exclusions; statistical model; result/figure mapping; exact replication target.

For complex tasks, first provide a plain-language task conceptualization. For each Study state whether it will be directly replicated, conceptually replicated, or only summarized, and why.

For model-bearing theories, inspect the focal paper's in-text citations and distinguish the foundational theory, the source directly used by the paper, supplementary explanations, and empirical support. State which model path each source justifies. Check the original construct wording and measure before translating; do not collapse similarly named constructs such as `efficacy/effectance` and `self-efficacy`.

## 3. B: Participant-View Flow

Begin with `B0. 任务关系图`. Show Study, scenario, block, trial, round, role, practice, condition, and backend logic as serial, crossed, nested, repeated, or parallel. Use Mermaid for reusable structure.

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

## 5. D: Materials, Data, and Analysis Reproduction

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

Anchor ideas in at least two sources: paradigm structure, stated limitation, detected limitation, theory, adjacent research, or user direction. User fit is optional, not the default generator.

For papers older than three years, browse and return about five representative later sources covering reviews, replications, variants, method improvements, contradictory evidence, or open materials. Mark ideas as `已检索确认`, `部分支持`, or `待检索确认`. Do not claim a publishable gap from a superficial search.

## 7. Feedback and Project Iteration

End with the five-dimension 25-point feedback table. Do not create an F or G report section. Project-level lessons are written to the private upgrade log only after the user scores the output.
