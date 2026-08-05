# Architecture and recursive control loop

## Contents

1. The two-tree model
2. Scope-tree construction
3. Quality-tree construction
4. Cell evaluation
5. Recursive decision algorithm
6. Candidate search
7. State and memory
8. Completion and escalation

## 1. The two-tree model

Separate **where** a defect exists from **what kind** of defect it is.

### Scope tree

The scope tree localizes the experience:

```text
experience
├── surface A
│   ├── region A1
│   │   ├── component A1a
│   │   └── component A1b
│   └── region A2
└── surface B
```

Canonical depth:

| Depth | Scope | Example |
|---:|---|---|
| 0 | experience | acquisition-to-activation journey |
| 1 | surface | marketing site or iOS app |
| 2 | page / screen | home, pricing, candidate detail |
| 3 | region / flow step | hero, proof, screenshot import |
| 4 | component | action card, contact panel, nav |
| 5 | element | title, border, icon, CTA |
| 6 | state / motion frame | hover, loading, error, confirmation |

The actual minimum depth belongs in `GOAL.md`. Do not descend to elements when the user only requested an information-architecture diagnosis. Do descend to states and frames for a release-candidate build.

### Quality tree

The quality tree names the judgment:

```text
quality
├── value
│   ├── comprehension
│   │   ├── goal fit
│   │   └── hierarchy and copy
│   └── credibility
│       ├── product truth and proof
│       └── design specificity
└── experience
    ├── perception
    │   ├── typography and layout
    │   └── color, material, and imagery
    └── operation
        ├── interaction, states, and motion
        └── accessibility, resilience, and performance
```

Production constraints such as truth, accessibility, and performance also appear as hard gates. This is deliberate: they influence craft, but cannot be averaged away.

## 2. Scope-tree construction

Keep the tree binary: each non-terminal node has one or two children.

Choose a split that explains user meaning:

- decision / proof;
- input / confirmation;
- discovery / detail;
- primary task / supporting task;
- rest state / active state;
- content / control;
- mobile / desktop when the composition meaningfully changes.

Avoid arbitrary equal-area or equal-DOM-count splits. The goal is diagnostic isolation, not a perfectly balanced data structure.

When a node is too broad, select the split that maximizes:

```text
expected information gain
= user impact × uncertainty × repair independence
```

A useful split makes it possible to repair one child without destabilizing the other.

## 3. Quality-tree construction

Use the fixed top-level quality tree so runs remain comparable. Add domain-specific leaves only beneath an existing branch.

Examples:

- a recruiting CRM can add `signal legibility` below comprehension;
- an iOS app can add `platform familiarity` below operation;
- a publishing surface can add `reading rhythm` below perception;
- a motion-heavy site can add `spatial continuity` below interaction and motion.

Do not add a leaf that merely restates a favored visual style.

## 4. Cell evaluation

A cell is:

```text
scope node × quality leaf × state × viewport
```

Example:

```text
candidate-detail/action-card × comprehension × proposed state × iPhone 15
```

Every scored cell needs:

- one or more direct evidence artifacts;
- a rubric anchor;
- a confidence value;
- a short causal explanation;
- reference IDs when a reference informed the judgment;
- a proposed repair if below threshold.

Aggregate scores are navigation aids. Repairs happen at cells.

## 5. Recursive decision algorithm

```text
evaluate(node):
    collect current browser evidence
    replay relevant user task
    score required quality leaves
    run hard gates

    if any hard gate fails:
        repair highest-severity gate
        re-evaluate node

    if effective score < threshold:
        repair weakest high-impact quality leaf
        re-evaluate node

    if effective score >= threshold and depth < required_depth:
        split node into <= 2 coherent children
        evaluate(each child)

    if every required terminal child passes:
        freeze baseline
        mark releasable
```

Apply a weakest-link release rule:

```text
release = all(required terminal nodes pass)
          and all(required hard gates pass)
          and evidence is fresh
```

Never release from a parent average.

## 6. Candidate search

Use a funnel, not serial nudging:

| Level | Candidate count | Comparison |
|---|---:|---|
| visual world / experience | 6–12 | round-robin sample or Swiss tournament |
| page / screen | 3–5 | blinded pairwise |
| region / flow step | 2–4 | targeted pairwise |
| component / state | 2–3 | side-by-side with interaction evidence |
| element | 1–2 | deterministic rubric and regression check |

Candidate diversity must be structural:

- different information sequence;
- different proof strategy;
- different relationship between product and brand;
- different interaction model;
- different compositional rhythm.

Changing only font, gradient, or radius does not create a new direction.

Rank pairwise comparisons before applying absolute scores. Pairwise judgment is easier to calibrate, but still vulnerable to position bias. Reverse sides, blind names, and record confidence.

## 7. State and memory

Project-local state:

```text
.top1-design/
├── GOAL.md
├── TASTE.md
├── QUALITY_TREE.json
├── ledger.jsonl
├── baselines/
├── references/
└── runs/
    └── 2026-08-05T153000Z/
        ├── evaluation.json
        ├── score.json
        ├── pairs.jsonl
        ├── decision.md
        └── evidence/
```

Use the ledger as append-only memory. A later agent should be able to reconstruct:

- what was known;
- what was compared;
- why a decision won;
- which deviations were intentional;
- what evidence would invalidate the decision.

Promote a rule into `TASTE.md` only after it succeeds across at least two surfaces or the user explicitly approves it as a brand rule.

## 8. Completion and escalation

Stop the active run when all required leaves pass. Continue later through scheduled regression checks, not perpetual styling.

Escalate to the user when:

- the goal and reference evidence favor conflicting directions;
- two repair cycles cause oscillation;
- a higher score requires changing product behavior or truthful copy;
- visual ambition conflicts with performance, accessibility, or platform convention;
- publishing, payment, tracking, or destructive changes require new authority.

The system is persistent, not autonomous beyond authority.
