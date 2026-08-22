# R Reproducibility Guide

Load this file only for statistical replication, R implementation, analysis planning, or analysis-ready experiment logging.

## 1. Start from a Data Contract

Before code, define unit of analysis and keys:

| Table | Typical key | One row means |
|---|---|---|
| participant | `participant_id` | one participant |
| trial | `participant_id + study_id + trial_id` | one task event |
| group/round | `group_id + round_id` | one interaction round |
| item response | `participant_id + item_id + wave` | one questionnaire response |

Never average to participant level before preserving raw trial/item data. Keep a mapping from program variable names to analysis names.

## 2. Model Mapping

| Research structure | Chinese model name | Common R route | Notes |
|---|---|---|---|
| Continuous DV, independent rows | 普通最小二乘线性回归 | `stats::lm()` | Check residual form and influential cases |
| Binary DV | 二项逻辑回归 | `stats::glm(family = binomial)` | Report odds/probability-scale interpretation |
| Count DV | 泊松/负二项回归 | `glm(..., poisson)` / `MASS::glm.nb()` | Check overdispersion |
| Repeated continuous trials | 线性混合效应模型 | `lme4::lmer()` | State random-effects rationale |
| Repeated binary/count trials | 广义线性混合效应模型 | `lme4::glmer()` | Match family/link to outcome |
| Factorial repeated measures | 重复测量 ANOVA 或混合模型 | `afex::aov_ez()` / `lmer()` | Prefer mixed models when missing/unbalanced |
| Latent constructs/path model | 验证性因子/结构方程模型 | `lavaan::cfa()` / `lavaan::sem()` | Define estimator and missing-data method |
| Indirect effect | 中介分析 | `lavaan` or bootstrap workflow | Do not imply causality from cross-sectional mediation |
| Bayesian hierarchical model | 贝叶斯层级模型 | `brms::brm()` | Preserve priors and convergence diagnostics |

Match the original analysis unless there is a stated correction or sensitivity analysis. Do not replace an unfamiliar model merely because another package is easier.

## 3. Minimal Annotated Skeleton

Use only the blocks relevant to the paper. Replace uppercase placeholders explicitly.

```r
library(readr)
library(dplyr)
library(ggplot2)

set.seed(20260807) # （固定随机过程，方便重复结果）

raw <- read_csv("PATH/TO/trial_data.csv", show_col_types = FALSE) # （读取程序导出的试次数据）

required <- c("participant_id", "condition", "trial_id", "response_value")
stopifnot(all(required %in% names(raw))) # （先检查关键变量是否存在）

analysis_df <- raw |>
  mutate(
    exclusion_flag = FALSE # （替换为论文或预注册中的真实排除规则）
  ) |>
  filter(!exclusion_flag) # （生成实际进入分析的数据）

model <- lm(response_value ~ condition, data = analysis_df) # （示例：检验条件对连续因变量的影响）
summary(model)

write_csv(analysis_df, "outputs/analysis_dataset.csv") # （保存可审计的分析数据）
sessionInfo() # （记录 R 与软件包版本）
```

This is a scaffold, not original-author code. Replace `lm` with the source model and add participant/item random effects when the design requires them.

## 4. Reproduction Pipeline

### Import and validation

- Verify encoding, delimiters, duplicate keys, condition values, trial counts, impossible RTs, missingness, and program version.
- Keep raw files read-only; write cleaned/derived data to a new path.

### Exclusions

- Encode every exclusion as a named Boolean flag.
- Provide counts before/after and reasons by condition.
- Distinguish participant, trial, item, group, and session exclusions.

### Derived variables

- Put scoring direction, reverse coding, aggregation level, winsorization/transformation, and composite construction in one auditable script.
- Never silently overwrite raw variables.

### Models and contrasts

- Reproduce the reported model first.
- Define factor reference levels and planned contrasts explicitly.
- Add robustness/sensitivity models only after the primary reproduction.
- Link model output to the paper's table/figure/result block.

### Figures and tables

- Build figures from analysis data, not manually entered summary values.
- State whether uncertainty bands are SD, SE, CI, bootstrap intervals, or posterior intervals.

## 5. Reproducible Project Layout

```text
analysis/
  00_setup.R
  01_import_validate.R
  02_clean_score.R
  03_models.R
  04_figures_tables.R
data/
  raw/        # never modify
  derived/
outputs/
README_analysis.md
renv.lock     # when a stable package environment is needed
```

Use `here` for paths and `renv` for package-version capture when the user will rerun or share the project. Use `targets` only when the pipeline is large enough to justify it.

## 6. Program-to-R Bridge

Ask the experimental program to export UTF-8 CSV/TSV plus a codebook. Save raw response and derived score separately. Include timestamps and software/material version when timing or iterative deployment matters.

For multiple computers or external devices, add a shared synchronization key such as `session_id`, `group_id`, `round_id`, and an event timestamp. Test merges before data collection.

## 7. Verification Checklist

- Row counts match expected participants x trials or documented deviations.
- Randomization/condition balance matches the design.
- Scale scoring reproduces expected ranges and reliability method.
- Exclusion counts match the report or are explained.
- Primary coefficients/contrasts point in the reported direction.
- Tables/figures are generated from code.
- `sessionInfo()` and package environment are saved.
- Deviations from the paper are listed, not hidden.
