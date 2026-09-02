# paper-anatomy | Put a paper on the evidence dissection table

[简体中文](README.md) · English

> **In one sentence:** For all readers, with a specialty in experimental and behavioral research, this Skill performs a non-destructive academic anatomy of a paper's story, theory, variables, participant experience, data, and discussion; it reads, audits, and verifies evidence without building a replication program.

## When to put a paper on the anatomy table

Use `paper-anatomy` when a normal abstract no longer answers the question. It can:

- reconstruct how the introduction establishes a problem, the literature motivates a gap, Studies support conclusions, and the discussion returns evidence to theory;
- explain how independent, dependent, mediating, moderating, and control variables are operationalized and how raw responses become indices;
- replay what participants see, understand, and do, including task difficulty, demand characteristics, manipulations, and alternatives;
- map models, comparisons, and figures to hypotheses and separate significance, proposition support, and generalizability;
- route experiments, surveys, longitudinal and qualitative studies, theory papers, reviews, meta-analysis, bibliometrics, Delphi, consensus, and guidelines differently;
- compare an online claim with its cited paper and classify it as aligned, partly aligned, overstated, unsupported, or unresolved;
- always complete C4, the field-position check: recent papers receive 3–5 focused scholarly anchors, while older papers receive an extended check of about five or more sources covering development, replication, correction, or controversy.

## Workflow: from research story to evidence boundary

1. Confirm the paper version, main text, supplementary material, and the user's actual question.
2. Generate a separate PDF source bundle containing file pages, sections, figures, tables, images, links, and inspected material scope.
3. Classify the document type so unlike studies are not forced into one template.
4. Reconstruct prior work -> gap/dispute -> theoretical explanation -> hypothesis/proposition, and check whether the introduction earns the question.
5. Rebuild each Study or evidence-production stage, connecting participants/materials, measures, variables, processing, models, and results.
6. Map statistical evidence -> supported proposition -> conclusions that cannot be inferred.
7. Audit how the discussion closes the story, separating interpretation, contribution, generalization, and alternatives.
8. Complete the mandatory C4 field-position check with clickable scholarly links, then deliver an ABC report with compact source pointers; a recent paper never skips C4.

## Typical requests

```text
$paper-anatomy Dissect this multi-Study paper. Explain how the introduction motivates
the question, what alternative each Study addresses, and whether the discussion exceeds the data.
```

```text
$paper-anatomy Replay this social-exclusion experiment from the participant perspective.
What did participants see, did they believe other players were real, and did the manipulation
also change difficulty or demand characteristics?
```

```text
$paper-anatomy Analyze this longitudinal survey paper without rewriting it as an experiment.
Check waves, attrition, measurement, lagged models, and causal language.
```

## What to provide

| Information | Minimum | Helpful additions |
|---|---|---|
| Paper | PDF, DOI, webpage, or readable text | final published version and exact title |
| Additional materials | optional; gaps will be disclosed | Supplement, appendix, open data, preregistration, repository |
| Focus | “help me understand it” is enough | theory, variable, Study, figure, model, dispute, or public claim |
| Claim source | only for verification | exact wording, screenshot/link, cited paper, publication date |
| Output preference | Chinese by default | length, statistical depth, table detail, Markdown output |

## What the anatomy report contains

| Part | Core question | Main contents |
|---|---|---|
| **A. Research narrative and theoretical position** | What problem is the paper trying to solve? | one-sentence answer, story line, theory sources, literature chain, gap/dispute, hypotheses, Study map |
| **B. Research design, measurement, and evidence** | How was evidence produced? | participant flow, variables, measures, raw-to-index path, models, results, figures, result-to-conclusion chain |
| **C. Conclusions, discussion, contribution, and field position** | What does the paper actually support? | grounded conclusions, discussion closure, contribution, limitations, alternatives, generalization, mandatory C4 field anchors, and judgment |

For a PDF, the Skill first builds a two-level index: it separates a standalone paper from individual papers in proceedings or another collection, then locates each paper's **abstract, introduction and theory, research design, results and data analysis, and discussion and value**. A user-specified paper is selected by ordinal, DOI, or a unique title phrase; if none is specified, all detected papers are read by default. Key claims in B4, C1, and the final judgment point to exact locations such as `[Paper: PDF p. 7, Fig. 2]`. The full index remains in `source_bundle.json` so it does not crowd out interpretation.

## Runtime and dependencies

- Reading requires access to paper text or PDF. C4 is mandatory for every paper: recent papers use 3–5 focused scholarly anchors, while older papers receive an extended check of about five or more development, replication, correction, or controversy sources. Each anchor has a clickable scholarly link; if browsing is genuinely unavailable, C4 remains and explicitly reports that limitation rather than claiming a current field conclusion.
- PDF source preparation requires Python 3 and `pypdf`; `pdfplumber` adds caption and image coordinates; `--render-pages` also requires `pdftoppm`.
- The repository includes a programmatically generated synthetic PDF with no real paper or participant data. CI exercises pages, sections, Figure/Table captions, DOI, links, embedded images, and `--no-text` output.
- Output-contract validation uses only the Python standard library.
- No R, PsychoPy, E-Prime, or other implementation platform is required because this Skill does not build experiments.

## Built-in references

| Resource | Use |
|---|---|
| [`anatomy-protocol.md`](references/anatomy-protocol.md) | core narrative, theory, variable, participant, result, and discussion protocol |
| [`source-grounding.md`](references/source-grounding.md) | PDF pages, figures, tables, images, Supplement/OSF scope, locator rules |
| [`special-routes.md`](references/special-routes.md) | theory, reviews, meta-analysis, bibliometrics, Delphi, consensus, guidelines |
| [`claim-verification.md`](references/claim-verification.md) | public claim -> paper evidence -> generalization boundary -> judgment |
| [`output-contract.md`](references/output-contract.md) | full ABC report fields |
| [`scoring-rubric.md`](references/scoring-rubric.md) | quality scoring and revision feedback |
| [`prepare_paper.py`](scripts/prepare_paper.py) | standalone/collection detection, per-paper boundaries, five-part reading index, figures, tables, links, and material scope |
| [`synthetic_paper.pdf`](../../tests/fixtures/synthetic_paper.pdf) | copyright-free synthetic source-grounding fixture |
| [`validate_output.py`](scripts/validate_output.py) | ABC structure and PDF-locator validation |
| [`evals.json`](evals/evals.json) | full paper, abstract-only, missing Supplement, contradictory evidence cases |

## Boundaries

- Do not generate experiment programs, platform projects, full stimulus packages, trial logs, or executable bundles.
- Do not turn association into causality or statistical significance into practical importance.
- Do not invent samples, scales, statistics, links, author views, or unavailable supplementary material.
- Do not accept a fluent story as sufficient evidence or dismiss all value because limitations exist.
- When verifying public communication, judge claim-evidence alignment without inferring the communicator's motives.
- In medical, health, and other high-stakes domains, do not replace diagnosis, clinical guidance, or domain expertise.
- If the goal becomes implementation, migration, or replication, use `paper-reconstruction`.

## Relationship with paper-reconstruction

`paper-anatomy` is the evidence-dissection arm of the paper surgery robot. [`paper-reconstruction`](../paper-reconstruction/README_EN.md) reconnects established evidence to flows, materials, programs, data, and analysis.

- Understanding, critique, or verification only: use `paper-anatomy`.
- Implementation, replication, migration, or adaptation: use `paper-reconstruction`.
- Both: `paper-reconstruction` leads and performs the minimum anatomy needed for implementation.

See [`SKILL.md`](SKILL.md), [`output-contract.md`](references/output-contract.md), and the [project overview](../../README_EN.md).
