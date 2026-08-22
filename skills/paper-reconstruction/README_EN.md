# paper-reconstruction | Reassemble a paper into a runnable study

[简体中文](README.md) · English

> **In one sentence:** For all readers, with a specialty in experimental and behavioral research, this Skill turns “what the authors wrote” into an executable blueprint of participant experience, platform-native implementation, recorded data, and the research team's actual analysis environment; it reconstructs, migrates, validates, and extends studies without replacing paper reading.

Reconstruction remains evidence-bound. It preserves theoretical and design invariants before mapping materials, parameters, platforms, data, and analysis to the tools the researcher actually uses.

## When to send a study to the reconstruction room

Use `paper-reconstruction` when the question moves from “what does this paper say?” to “how can I implement it?” It supports experiments and behavioral tasks, participant-to-backend mapping, surveys and longitudinal studies, platform migration, statistical reproduction, and evidence-bounded study development.

| Replication level | Goal |
|---|---|
| Conceptual | Preserve theory or causal logic while rebuilding materials and context |
| Program | Rebuild instructions, stimuli, randomization, interface, timing, logs, and runnable artifacts |
| Statistical | Recreate exclusions, indices, models, contrasts, tables, and figures from data |
| Direct copy | Run authorized original programs, materials, parameters, and analysis packages as closely as possible |

## Personalized adaptation: ask only when the task requires it

The Skill does not present an onboarding questionnaire. It identifies the requested artifact first, then asks only questions that change delivery. Reading routes to `paper-anatomy`; implementation questions appear only for program/direct replication or migration; analysis-software questions appear only for statistical or analysis artifacts. Known answers are not requested again, and an unanswered question does not block platform-neutral work.

An unspecified computerized behavioral experiment may explicitly default to E-Prime 3.0. Surveys, longitudinal studies, field protocols, and purely statistical tasks are not forced into E-Prime. An unspecified analysis environment receives a platform-neutral contract rather than an automatic R pipeline.

## Platform adaptation: use native structures, not renamed E-Prime objects

| Platform | Primary structure | Key validation |
|---|---|---|
| **E-Prime 3.0** | Session/Block/Trial Procs, Lists, objects, E-Basic, serial/interleaved/nested relations | `.es3/.ebs3`, E-Run, logs, versions, hashes |
| **PsychoPy** | Experiment, Routine, Loop/TrialHandler, Conditions, Components, Code Components | references, condition columns, frame rate, dropped frames, wide/trials/log outputs |
| **MATLAB + Psychtoolbox** | entry point, phase functions/state machine, Screen, input queues, triggers, event structures | flip timing, refresh rate, sync tests, random streams, cleanup |
| **jsPsych** | initialization, timeline, plugins, timeline variables, routing, deployment | preload, browser/device matrix, focus, network failure, data receipt |
| **Qualtrics / SoSci** | Blocks/pages, Survey Flow, Randomizer, branch/display logic, Embedded Data | path previews, anonymity, mobile layout, randomization counts, exports |
| **oTree** | Subsession, Group, Player, Page, WaitPage, payment and interaction state | concurrency, waits, reconnects, groups/rounds, bots, payments, exports |
| **Inquisit / Gorilla** | script/trial/block/data or task/tree/node/spreadsheet/zone | versions, randomization, timing/browser state, fields, deployment |
| **Field or other** | native components or an experimenter protocol, never forced Proc/List terminology | synchronization, manual steps, stable IDs, event records, analysis interface |

All platforms use `design-only`, `buildable`, `generated`, or `runtime-verified`. [`validate_platform_plan.py`](scripts/validate_platform_plan.py) checks non-E-Prime components, phases, fields, analysis interfaces, and runtime evidence. E-Prime remains the first deep build path; other platforms now have native contracts and machine validation, but the project does not claim that all have complete runnable templates.

## Surveys and longitudinal studies: from item display to cross-wave analysis

A cross-sectional survey reconstructs recruitment, eligibility, consent, pages/Blocks, stable item IDs, scale version and license, randomization, branching, quality control, completion states, paradata, exports, and value labels.

A longitudinal study additionally requires wave IDs and windows, anonymous participant keys separated from contact information, invitation/reminder/opt-out/refusal/completion/attrition states, cross-wave version differences, timing data, and interfaces for wide/long transformations, missingness, attrition, and longitudinal models. Required fields include `participant_key`, `wave_id`, `item_id`, `response_raw`, `invitation_status`, and `completion_status`.

If the survey platform is unspecified, the Skill asks once; if unanswered, it produces a platform-neutral survey blueprint rather than defaulting to E-Prime. Organizational research also separates organization, team, supervisor, employee, and dyad IDs, with explicit aggregation, linking, access, and privacy boundaries.

## Analysis adaptation: confirm the team's actual environment

Only when analysis artifacts are required and the environment is unknown, the Skill asks:

> Which software does your team normally use for analysis? Choose R, Python, SPSS, Mplus, MATLAB, Stata, SAS, JASP/Jamovi, or another tool. If you are unsure, I will first provide a platform-neutral analysis contract.

Every route preserves:

```text
import -> validate fields and labels -> exclude -> derive -> describe
-> model -> contrasts/effect sizes/uncertainty -> tables/figures -> export
-> environment and run record
```

R receives scripts/Quarto, `renv`, and `sessionInfo()`; Python receives scripts/notebooks, an environment lock, and tests; SPSS receives saved `.sps` syntax rather than menu-only instructions; Mplus receives `.inp`, variable order, missing-value coding, and `.out` checks. Migration preserves both the original analysis contract and target-software differences.

## Workflow: from paper evidence to an executable package

1. Confirm the paper version, target Study, and conceptual/program/statistical/direct-copy level.
2. Build a DOI, article, appendix, Supplement, OSF, preregistration, data, code, and material ledger.
3. Perform the minimum paper anatomy needed to connect theory, variables, raw responses, indices, models, and figures.
4. Route experiments, surveys, longitudinal, interactive, and field studies to their actual participant/respondent flow.
5. Select an implementation platform only when implementation is required; preserve original-platform evidence and migration differences.
6. Select an analysis environment only when analysis artifacts are required; otherwise keep the contract platform-neutral.
7. Connect materials, event/survey logs, stable IDs, data dictionaries, analysis fields, and validation tests.
8. Run the E-Prime bundle auditor or cross-platform plan validator.
9. Separate paper evidence, later evidence, user ideas, and untested decisions when extending a study.
10. Deliver applicable ABCDE sections and minimum sufficient artifacts with an honest runtime state.

## Typical requests

```text
$paper-reconstruction Rebuild this reaction-time paper in MATLAB + Psychtoolbox.
We use Python for analysis. Provide phase functions, flip/response logging,
a data dictionary, an analysis interface, and smoke tests.
```

```text
$paper-reconstruction Rebuild this three-wave employee survey in Qualtrics.
We use SPSS. Design anonymous matching, reminders, attrition states, export fields,
and a saved .sps analysis route.
```

## What to provide

| Information | Minimum | Helpful additions |
|---|---|---|
| Research source | PDF, DOI, link, or design description | Supplement, OSF/GitHub, preregistration, data, programs, materials |
| Replication target | Study to address | replication level and exact Study |
| Implementation environment | only for program delivery; may be unknown | platform/version, OS, devices, lab/online/field, networking, synchronization |
| Analysis environment | only for analysis artifacts; may be unknown | R/Python/SPSS/Mplus version, original code, target tables/figures |
| Survey/longitudinal context | only for relevant tasks | waves, intervals, anonymous matching, contact/reminders, platform, sample flow |
| Constraints | may be none | time, budget, sample, payments, devices, ethics, privacy, licenses |
| Output preference | Chinese and minimum sufficient artifacts by default | full ABCDE, code, structured JSON, action order, Markdown |

Missing material does not end the task. The Skill labels paper-explicit, supplement, external material, reasonable inference, and replicator decision, then explains what can be rebuilt today, how to validate it, and which replication level is lost.

## What the ABCDE package contains

| Part | Core question | Main contents |
|---|---|---|
| **A. Target and evidence** | What is being replicated, and are sources complete? | ledger, theory, Studies, variables, indices, models, table/figure mapping |
| **B. Participant/respondent flow** | What is actually experienced? | task relationships, screens/steps, backend actions, waves, matching, saved data |
| **C. Program and field protocol** | How does it run? | original and target native components, survey logic, social reality, synchronization, fallbacks, logs |
| **D. Materials, data, and analysis reproduction** | How do materials reach analysis? | material ledger, data dictionary, target-software pipeline, code/settings, validation |
| **E. Parameter transfer and development** | What can be extended? | parameter cards, theory anchors, later evidence, new questions, novelty status, pilots |

## Runtime and dependencies

- The core Skill requires no API key, MCP, fixed platform, or automatic commercial-software installation.
- Markdown, platform-plan, and E-Prime bundle validators use Python 3 and the standard library.
- Users lawfully provide target implementation and analysis environments; the Skill records versions, dependencies, logs, and runtime state.
- The E-Prime deep path targets 3.0; the repository does not redistribute PST runtimes or installed samples.
- Later-evidence and novelty checks require internet-enabled literature discovery.

## Built-in references

| Resource | Use |
|---|---|
| [`reconstruction-protocol.md`](references/reconstruction-protocol.md) | core protocol |
| [`replication-source-ledger.md`](references/replication-source-ledger.md) | source ledger |
| [`replication-deliverables.md`](references/replication-deliverables.md) | minimum sufficient artifacts |
| [`platform-selection.md`](references/platform-selection.md) | conditional implementation-platform selection |
| [`platform-adapters.md`](references/platform-adapters.md) | non-E-Prime native structures and validation |
| [`survey-longitudinal-path.md`](references/survey-longitudinal-path.md) | survey, multi-wave, and organizational linking |
| [`analysis-environment.md`](references/analysis-environment.md) | analysis-software selection and native artifacts |
| [`domain-adaptation.md`](references/domain-adaptation.md) | domain, design, and extension routing |
| [`eprime-execution-path.md`](references/eprime-execution-path.md) | E-Prime Proc/List and runtime state |
| [`r-reproducibility-guide.md`](references/r-reproducibility-guide.md) | loaded only for R |
| [`output-contract.md`](references/output-contract.md) | full ABCDE fields |
| [`validate_output.py`](scripts/validate_output.py) | formal ABCDE Markdown structure and source-status validation |
| [`validate_platform_plan.py`](scripts/validate_platform_plan.py) | cross-platform, longitudinal, and analysis validation |
| [`audit_replication_bundle.py`](scripts/audit_replication_bundle.py) | E-Prime semantic audit |
| [`evals.json`](evals/evals.json) | source, platform, longitudinal, and analysis cases |

## Boundaries

- Never present missing programs, materials, items, parameters, or fields as author originals.
- Never describe a design, pseudocode, or buildable scaffold as runtime-verified.
- Do not force other platforms into Proc/List terminology or every analysis into R.
- Do not assume that interaction partners are real humans.
- Do not let interface design precede stable IDs, raw responses, derived fields, timing, exclusions, and analysis interfaces.
- Do not treat nonresponse as automatically missing at random or expose direct identifiers in public data.
- Do not present a user extension as the paper's conclusion or claim novelty without a current search.
- Do not bypass consent, deception, payment, privacy, licensing, debriefing, or ethics requirements.

## Relationship with paper-anatomy

[`paper-anatomy`](../paper-anatomy/README_EN.md) establishes theory, design, result, and conclusion boundaries. `paper-reconstruction` carries that evidence into participant flow, platforms, materials, data, and analysis.

- Understanding or critique only: use `paper-anatomy`.
- Implementation, migration, statistical reproduction, or extension: use `paper-reconstruction`.
- Both: `paper-reconstruction` leads and performs the minimum anatomy required for implementation.
- Theory, review, meta-analysis, and consensus papers default to `paper-anatomy` unless reproducing search, screening, coding, or consensus procedures.

See [`SKILL.md`](SKILL.md), [`output-contract.md`](references/output-contract.md), and the [project overview](../../README_EN.md).
