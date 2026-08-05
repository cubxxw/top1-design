# Specialist orchestration

## Contents

1. Ownership
2. Routing matrix
3. Safe composition
4. Review independence
5. Scheduled operation

## 1. Ownership

TOP1 DESIGN remains the control plane. It owns:

- the goal contract;
- reference coverage and anti-copy boundary;
- scope and quality trees;
- pairwise tournament records;
- scoring ledger;
- release and escalation decision.

A specialist Skill supplies a proposal, rule set, implementation pattern, or independent audit. It does not silently replace the control plane.

## 2. Routing matrix

| Need | Preferred specialist | Returned evidence |
|---|---|---|
| bold art direction | frontend-design or design-taste Skill | direction, implementation, screenshots |
| style, palette, font, stack lookup | UI UX Pro Max | query and matched records |
| browser critique and anti-pattern scan | Impeccable | critique snapshot and deterministic findings |
| interaction and accessibility rules | Vercel Web Interface Guidelines | file/line findings |
| Apple platform convention | official Apple HIG plus SwiftUI/iOS Skills | platform-specific rationale and simulator evidence |
| React/Next performance | Vercel React best practices | code findings and metrics |
| component state validation | Storybook tests | rendered state evidence |
| end-to-end and visual regression | Playwright | trace, assertions, screenshots, diffs |
| automated accessibility | axe plus semantic tests | violation output and manual follow-ups |
| performance and SEO gates | Lighthouse CI and Web Vitals | reproducible budget report |
| live authenticated browsing | Kimi WebBridge or Chrome | real-session snapshot and screenshots |

Discover availability before assuming a specialist exists. Do not install a third-party Skill during a project run without reviewing its contents and receiving any authority the environment requires.

## 3. Safe composition

Use one specialist as the primary creator for an edit batch. Use different specialists as reviewers.

Avoid stacking multiple generation Skills in the same prompt. Their style rules can cancel into generic compromise.

Recommended sequence:

```text
TOP1 goal/reference contract
→ one creator Skill
→ browser evidence
→ one deterministic reviewer
→ one independent visual reviewer
→ TOP1 synthesis and score
```

Translate every finding into a scope × quality cell. Deduplicate symptoms that share a cause.

## 4. Review independence

When explicitly authorized to use independent agents, isolate:

- Reviewer A: goal, references, target evidence, no deterministic findings.
- Reviewer B: target evidence, deterministic checks, no Reviewer A opinion.

Synthesize only after both finish. This reduces anchoring.

When independent agents are unavailable or unauthorized, run the reviews sequentially and disclose the single-context limitation. Do not simulate independence by changing role labels in one uninterrupted judgment.

## 5. Scheduled operation

Use separate jobs:

### Observer

- captures approved routes and states;
- runs functional, accessibility, performance, and baseline checks;
- never edits production.

### Diagnostician

- maps new failures to scope × quality cells;
- compares with the last approved ledger;
- proposes one repair packet.

### Repairer

- runs only on approved paths and issue types;
- creates a branch or patch;
- runs the full gate suite;
- never deploys unless deployment was explicitly authorized.

### Curator

- detects stale reference links and contradictory taste rules;
- proposes catalog updates;
- never promotes a taste rule without human approval or repeated project evidence.

Use bounded concurrency and isolated workspaces. A shared live working directory makes visual baselines and state files race.
