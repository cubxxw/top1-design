---
name: top1-design
description: Evidence-driven UI design, redesign, critique, and recursive quality optimization for websites, landing pages, product interfaces, iOS apps, dashboards, onboarding, forms, design systems, typography, layout, color, interaction, motion, UX copy, accessibility, performance, responsive behavior, and SEO-facing surfaces. Use when an agent must create or improve an interface from a goal, compare it with high-taste references, capture real browser evidence, score quality at site/page/section/component/element/state granularity, run blinded pairwise design tournaments, iterate below a quality threshold, continue drilling down after a parent reaches 95, prevent visual drift, or build a long-running automated design harness.
---

# TOP1 DESIGN

Operate as an evidence-driven design director and QA harness. Do not invent taste from adjectives. Acquire it from product goals, observed references, explicit rubrics, browser evidence, and user outcomes.

Treat `95` as a promotion threshold. Never call it objective beauty, and never stop at a passing parent when required child depth remains.

The first commercial wedge is an automatic design final-review and redo Agent for AI-generated websites. Review any stable browser target; mutate only repositories whose adapter, build, test, authority, and rollback boundaries are verified.

## Start here

1. Inspect the project, product truth, incumbent UI, available browser tools, tests, and existing design artifacts.
2. Run `python <skill-dir>/scripts/init_harness.py <project-root>` when `.top1-design/` is absent. Preserve existing files unless the user authorizes replacement.
3. Read `.top1-design/GOAL.md`, `.top1-design/TASTE.md`, and `.top1-design/QUALITY_TREE.json`.
4. Copy and complete `.top1-design/PROJECT_PROFILE.example.json` only when repository signals cannot establish stage, runtime, or locked-area facts.
5. Run `scripts/diagnose_project.py` before reference acquisition or mutation. Record `greenfield`, `rescue`, or `governed` mode, review readiness, adapter status, and maximum change level.
6. Fill missing facts from the user's request and repository. Ask only when a missing choice would materially change the product.
7. Declare Release Bar coverage before implementation. Copy `.top1-design/RELEASE_MANIFEST.example.json` into the active run and list the required viewports, flows, states, and accessibility methods.
8. Read the reference file that owns the current phase:
   - maturity, adapter, and change granularity: `references/operating-modes.md`;
   - architecture and recursion: `references/architecture.md`;
   - score inputs and anchors: `references/scoring.md`;
   - Release Bar and product metrics: `references/release-bar.md`;
   - browser capture and flow replay: `references/browser-protocol.md`;
   - reference acquisition: `references/reference-library.md`;
   - specialist Skill routing: `references/orchestration.md`;
   - motion work: `references/motion.md`;
   - SEO-facing surfaces: `references/seo.md`;
   - existing Skill landscape: `references/skill-landscape.md`.

## Enforce the evidence hierarchy

Resolve conflicts in this order:

1. user goal, real product behavior, and legal/safety constraints;
2. observed user task evidence and approved brand system;
3. current browser evidence from the target;
4. source-specific reference principles;
5. platform guidance such as Apple HIG, WCAG, or Vercel guidelines;
6. general design heuristics;
7. model preference.

Never let a fashionable reference override the product's goal. Never copy another product's trademark, copy, illustration, or distinctive composition.

## Build the goal contract

Write a falsifiable goal before visual work:

- target user and context;
- job to be done;
- primary decision or action;
- promised value and supporting proof;
- emotional target;
- business outcome and measurement window;
- product mode: `persuade`, `operate`, `read`, or `experience`;
- required surfaces, viewports, states, and minimum scope depth;
- forbidden claims, patterns, and brand moves;
- autonomy boundary and actions requiring confirmation.

For an existing project, separate product defects from visual defects. Do not redesign a workflow merely to make a screenshot prettier.

## Acquire taste before generating

Create reference cards for at least:

- one whole-experience reference;
- one same-category product reference;
- one typography or layout reference;
- one interaction or motion reference;
- one anti-reference.

Capture live pages through Kimi WebBridge first when it is available or requested. Otherwise use an available real browser, Chrome, Computer Use, or Playwright. Follow `references/browser-protocol.md`.

For every reference, record:

- source URL and capture time;
- exact scope observed;
- observed facts;
- interpretation;
- transferable relationship;
- anti-copy boundary;
- contexts where the principle should not be used.

Do not score or generate until reference coverage exists, unless the user asks for a deliberately unreferenced exploration.

## Search broadly, converge narrowly

Use controlled abundance:

1. Generate 6–12 meaningfully different directions at the whole-experience level.
2. Reject variants that differ only in colors, fonts, or decorative effects.
3. Compare candidates blind and two at a time. Randomize left/right order and judge each pair twice with reversed order when the budget permits.
4. Use goal fit first, then design specificity, hierarchy, credibility, interaction, and craft.
5. Store comparison records as JSONL and run:

```bash
python <skill-dir>/scripts/rank_candidates.py <pairs.jsonl>
```

6. Keep the top two. Explain the losing principles, not only the winning look.
7. Implement one direction. Do not hybridize incompatible winners into a generic compromise.

At lower scope levels, use 2–4 targeted variants. Increase search breadth only when the current direction is genuinely unresolved.

Generate and break candidates in isolated workspaces. “Violence through volume” permits many experiments, not random churn in the user's main worktree. Land only the winning, reversible patch whose blast radius is enumerated.

## Evaluate with two trees

Maintain two orthogonal structures:

- **Scope tree:** experience → surface → region → component → element → state or motion frame.
- **Quality tree:** value → comprehension / credibility; experience → perception / operation.

Evaluate a specific scope node against specific quality leaves. Do not emit one undifferentiated “aesthetic score.”

Capture the target at stable desktop and mobile viewports plus relevant interactive states. Replay the primary task, not only the home screen.

Record:

- metric scores with anchor-based reasons;
- hard gates;
- confidence;
- direct evidence paths;
- reference IDs;
- defects with severity and expected user effect;
- proposed repair and regression risk.

Run:

```bash
python <skill-dir>/scripts/score_design.py <evaluation.json>
```

## Recurse instead of endlessly polishing

Apply this decision rule to the highest-impact unresolved node:

1. If a hard gate fails, repair it before aesthetic refinement.
2. If effective score is below threshold, repair the weakest quality leaf.
3. If effective score reaches threshold but required depth remains, split the scope into at most two coherent children and evaluate both.
4. If a child fails, the parent cannot pass.
5. If every required terminal child passes, freeze the baseline and stop the active run.

Split by user meaning, not arbitrary DOM size. Good splits include “decision content / product proof,” “input / confirmation,” or “rest / active motion.” Bad splits include “top 500 pixels / bottom 500 pixels” unless the visual composition itself is the issue.

Bound each active run:

- maximum two repair cycles per leaf before changing strategy;
- maximum one primary defect class per edit batch;
- maximum one new visual idea per component;
- escalate when repeated edits oscillate or evidence conflicts.

“Violence through volume” means a wider candidate search and deeper evidence, not random CSS churn.

## Use hard release gates

Never average these away:

- primary user task works;
- factual product content is true;
- keyboard and focus behavior work;
- contrast, semantics, labels, target sizes, and reduced-motion behavior meet the chosen standard;
- required responsive viewports have no clipping or accidental overflow;
- loading, empty, error, success, and destructive states exist where relevant;
- motion remains smooth on a representative mid-range device or is removed;
- performance budgets and Core Web Vitals pass where measurable;
- SEO-facing content is crawlable, unique, useful, and not generated only to manipulate ranking;
- privacy, consent, analytics, and publishing actions stay within authority.

Track visual, interaction, responsive, accessibility, and functional findings in the run's release manifest with severity and evidence. After the score report passes, run:

```bash
python <skill-dir>/scripts/assess_release.py \
  <project-root>/.top1-design/runs/<run-id>/RELEASE_MANIFEST.json
```

Do not call a candidate releasable until this assessor returns `release_candidate`. A valid exit code `2` means continue repair; exit code `1` means repair the evidence record.

## Route specialist Skills without surrendering judgment

Use `references/orchestration.md` to select specialists. Typical routing:

- art direction and anti-slop implementation → a frontend taste or frontend-design Skill;
- large style/palette/font lookup → UI UX Pro Max;
- deterministic interaction/a11y review → Vercel Web Interface Guidelines;
- browser critique and polish → Impeccable when installed;
- iOS platform behavior → Apple HIG and relevant SwiftUI Skills;
- regression evidence → Playwright, Storybook, axe, Lighthouse CI, and Web Vitals.

Treat specialist output as evidence. This Skill owns the goal, reference selection, two-tree state, score ledger, and release decision.

## Preserve cross-run memory

Write each run under `.top1-design/runs/<timestamp>/` and append the decision to `.top1-design/ledger.jsonl`.

Persist:

- goal version;
- diagnosis, operating mode, adapter status, and maximum change level;
- evaluated commit and URL;
- screenshots and state names;
- score report;
- pairwise comparisons;
- selected reference principles;
- accepted deviations;
- changes made;
- regressions introduced or prevented;
- next required scope nodes.

Promote stable decisions into `.top1-design/TASTE.md`. Do not promote a one-off preference after a single successful page.

## Schedule maintenance

For recurring automation, separate observation from mutation:

- daily: capture critical surfaces, replay primary flow, detect hard-gate and visual-baseline regressions;
- weekly: inspect the weakest quality leaves and stale reference evidence; propose one targeted improvement;
- monthly: recalibrate score anchors against approved examples and prune contradicted taste rules.

Default scheduled jobs to proposal-only. Allow automatic edits only for deterministic, reversible, test-backed fixes in explicitly approved paths. Never let a cron job continuously restyle production.

## Report completion

Return:

- outcome against the goal;
- diagnosed mode, adapter status, and actual change level;
- winning direction and borrowed principles;
- required scope depth reached;
- terminal node scores, confidence, and hard gates;
- browser evidence and tested flows;
- changes made;
- remaining risks and next descent node;
- the `assess_release.py` result, not only an internal high score.

Never claim “pixel perfect,” “95+,” or “TOP1” without an evaluation artifact that another reviewer can inspect.
