# Release Bar and product-success protocol

## Contents

1. Three different decisions
2. Candidate Release Bar
3. Required evidence coverage
4. Defect severity
5. Release assessment
6. Product-success targets
7. Claim boundary

## 1. Three different decisions

Do not collapse these decisions into one percentage:

1. **Promotion:** a scope node reaches the project-local score threshold, normally
   95, and must descend until required depth is complete.
2. **Release:** one candidate passes every declared terminal node, hard gate,
   evidence-coverage gate, and change-control gate.
3. **Product validation:** a cohort meets the four commercial success targets.

A score of 95 is not “95% chance of top-tier design.” A 90% cohort release rate
is not a score of 90. Blind preference is measured separately from both.

## 2. Candidate Release Bar

A candidate meets the Release Bar only when all conditions are true:

- the recursive score report is `release_candidate`;
- visual, interaction, responsive, accessibility, and functional checks cover
  the declared release scope and contain direct evidence;
- every declared viewport, primary flow, required state, and accessibility
  method has passing evidence;
- no unresolved `blocker` or `severe` defect remains, including one marked
  `accepted_risk`;
- the change stays within authority;
- relevant tests pass;
- blast radius was reviewed;
- rollback is ready.

These are weakest-link gates. Do not average them. A beautiful desktop capture
cannot compensate for a broken mobile flow; a passing axe report cannot
compensate for unusable keyboard order.

## 3. Required evidence coverage

Declare coverage before implementation in `RELEASE_MANIFEST.json`.

Minimum web coverage normally includes:

- viewports: stable desktop and mobile, plus any breakpoint where composition
  changes materially;
- flows: the primary user task and every modified critical flow;
- states: default, focus, error, and success; add loading, empty, partial,
  destructive confirmation, and offline states where relevant;
- accessibility: automated semantics/contrast checks and keyboard replay; add a
  screen-reader method for critical application flows;
- responsive: no clipping, accidental overflow, unreachable controls, broken
  reading order, or unusable text resizing at declared viewports;
- functional: assertions for outcomes, not merely successful clicks;
- visual and interaction: current browser evidence for the candidate, not only
  source inspection.

Each check needs an evidence path or URL. A check without evidence fails the
Release Bar.

## 4. Defect severity

Use user effect, not visual drama:

| Severity | Definition | Release effect |
|---|---|---|
| `blocker` | primary task, safety, truth, or access is impossible | always blocks |
| `severe` | common task or required viewport is materially broken or misleading | always blocks |
| `moderate` | localized degradation with a viable path around it | may release only if recorded and within policy |
| `minor` | craft defect with low task impact | record; does not independently block |

Examples of `severe` defects include clipped primary actions on mobile,
keyboard traps, unreadable required content, missing error recovery, a control
that appears enabled but does nothing, or a major layout failure across a
required viewport.

Fixing a defect changes its status to `fixed`; preserve the record and before/after
evidence. Do not delete failed evidence from the run.

## 5. Release assessment

After scoring and deterministic/browser QA, run:

```bash
python <skill-dir>/scripts/assess_release.py \
  <project-root>/.top1-design/runs/<run-id>/RELEASE_MANIFEST.json \
  --output <project-root>/.top1-design/runs/<run-id>/release-report.json
```

Exit codes:

- `0`: Release Bar met;
- `2`: valid evidence, but not releasable;
- `1`: invalid or unreadable evidence.

The assessor verifies evidence records; it does not run the browser tests. Use
Playwright, axe, Storybook, Lighthouse, platform tools, and manual assistive
technology checks to create truthful records.

## 6. Product-success targets

Evaluate a matched pilot cohort with:

```bash
python <skill-dir>/scripts/assess_product_metrics.py \
  <project-root>/.top1-design/PRODUCT_METRICS.json
```

The product is commercially validated only when all four targets pass:

| Metric | Target | Exact definition |
|---|---:|---|
| severe-defect-free rate | ≥95% | eligible audited units with no unresolved blocker/severe visual or interaction defect ÷ all eligible audited units |
| Release Bar rate | ≥90% | eligible projects meeting the declared Release Bar ÷ all eligible projects |
| blind preference | ≥70% | Taste Engine wins ÷ all valid blinded comparisons, with ties retained in the denominator |
| human edit-time reduction | ≥50% | `1 − total Taste Engine human minutes ÷ total matched baseline human minutes` |

Freeze eligibility, audited-unit granularity, task, content, device matrix,
release budget, and time-accounting rules before the pilot. Exclude a project
only by a predeclared rule, never because it failed.

Report sample sizes beside every rate. Passing a tiny pilot is directional
evidence, not a universal market claim.

## 7. Claim boundary

Permitted when supported by the cohort:

- “95% of audited units had no severe visual or interaction defect.”
- “90% of eligible projects reached the declared Release Bar.”
- “The Taste Engine version won 70% of blinded comparisons.”
- “Matched human edit time fell by 50%.”

Not permitted:

- “95% of generated sites are top-tier design.”
- “The system objectively measures beauty.”
- “Any code repository can be safely redesigned automatically.”
