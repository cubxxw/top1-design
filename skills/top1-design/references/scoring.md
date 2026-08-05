# Scoring protocol

## Contents

1. What the score means
2. Metrics and mode weights
3. Anchors
4. Confidence cap
5. Hard gates
6. Node status
7. Evidence requirements
8. Calibration

## 1. What the score means

The 0–100 number is a project-local, evidence-backed quality index. It helps order work and detect regression. It is not a universal measurement of beauty.

Use pairwise preference to choose among design directions. Use absolute scores to determine what to repair and whether a required leaf may advance.

## 2. Metrics and mode weights

All metric values are 0–100. Weights sum to 100.

| Metric | Persuade | Operate | Read | Experience |
|---|---:|---:|---:|---:|
| `goal_fit` | 18 | 15 | 16 | 12 |
| `specificity` | 12 | 10 | 10 | 18 |
| `hierarchy` | 15 | 12 | 17 | 14 |
| `typography` | 10 | 9 | 15 | 10 |
| `layout` | 10 | 12 | 13 | 10 |
| `color_material` | 8 | 6 | 5 | 12 |
| `interaction_states` | 10 | 18 | 8 | 8 |
| `motion` | 6 | 8 | 2 | 12 |
| `copy` | 11 | 10 | 14 | 4 |

Metric intent:

- `goal_fit`: makes the target user’s next valuable action easier.
- `specificity`: belongs to this product and could not be relabeled for an unrelated category.
- `hierarchy`: makes sequence, priority, grouping, and focal point obvious.
- `typography`: creates legible, coherent, expressive type hierarchy.
- `layout`: controls rhythm, alignment, density, whitespace, and responsive composition.
- `color_material`: uses palette, contrast, depth, border, shadow, imagery, and surface treatment coherently.
- `interaction_states`: supports task flow, feedback, affordance, error recovery, and complete states.
- `motion`: explains causality, spatial continuity, feedback, or emotion without distraction.
- `copy`: is concise, specific, truthful, useful, and appropriate to the user’s vocabulary.

## 3. Anchors

Score against observable anchors:

| Score | Meaning |
|---:|---|
| 0 | absent, broken, deceptive, or unusable |
| 40 | major intent is recognizable but task or composition regularly fails |
| 60 | functional baseline; generic, inconsistent, or incomplete |
| 75 | solid production work with visible weaknesses and missing states |
| 85 | strong, coherent, product-specific work; several refinements remain |
| 90 | excellent; defects are localized and do not dominate the experience |
| 95 | exceptional and evidence-backed at this scope; promote to deeper scope |
| 100 | reference-defining for the stated goal, context, state, and viewport |

Never assign 100 because no defect is immediately visible. Require a positive reason that the work establishes a new reference standard.

Score reasons must answer:

1. What is directly visible or measured?
2. Why does it help or hurt the goal?
3. Which anchor does that observation match?
4. What evidence would change the score?

## 4. Confidence cap

Confidence is 0–1 and reflects evidence coverage, not certainty theater.

The scoring script applies:

```text
confidence_cap = 80 + 20 × confidence
effective_score = min(weighted_score, confidence_cap)
```

Consequences:

- confidence 0.50 caps a node at 90;
- confidence 0.75 caps a node at 95;
- confidence 1.00 permits 100.

Increase confidence with:

- stable screenshots at required viewports;
- flow replay rather than a static hero;
- code or DOM inspection;
- deterministic a11y/performance tests;
- reversed pairwise comparisons;
- human or approved-baseline calibration.

Do not increase confidence because multiple agents repeat the same unsupported opinion.

## 5. Hard gates

The evaluation declares `required_hard_gates`. Every terminal node must include a boolean value for each required gate.

Canonical gates:

| Gate | Pass condition |
|---|---|
| `functional` | primary task and controls work |
| `truth` | product claims, proof, and data are accurate |
| `accessibility` | chosen WCAG/platform requirements pass |
| `responsive` | required viewports and text sizes work |
| `states` | relevant loading, empty, error, success, and destructive states exist |
| `motion_safety` | reduced-motion and comfort requirements pass |
| `performance` | declared performance budget passes |
| `seo` | applicable crawlability, metadata, usefulness, and structured data checks pass |

Set non-applicable gates outside `required_hard_gates`; do not mark them `true` without testing.

A failed or missing required gate makes the node `blocked` regardless of weighted score.

## 6. Node status

The script emits:

- `blocked`: a required hard gate failed or is missing;
- `repair`: effective score is below threshold;
- `promote`: threshold reached, but required depth remains;
- `pass`: threshold reached at or beyond required depth with gates passing.

The whole report is `release_candidate` only when every required terminal node is `pass`.

If a parent has children, child status controls release. Do not infer a pass from the parent.

## 7. Evidence requirements

Each node needs a non-empty `evidence` list. Each item should identify:

- artifact path or URL;
- viewport and state;
- capture time;
- commit or build identifier when applicable;
- browser/device environment;
- whether the artifact is current target, candidate, reference, or baseline.

Scores without evidence may be recorded as hypotheses, but confidence should keep them below promotion.

## 8. Calibration

Maintain an approved calibration set:

- three examples around 75;
- three around 85;
- three around 95;
- at least one known failure for every hard gate.

Monthly:

1. blind candidate names;
2. rerun pairwise comparisons;
3. compare ordering with the approved set;
4. identify judge drift and position bias;
5. update anchors only with user approval;
6. record the rubric version in every new evaluation.

Never silently change weights to make the current design pass.
