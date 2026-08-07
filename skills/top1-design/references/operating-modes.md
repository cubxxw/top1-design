# Project diagnosis and operating modes

## Contents

1. Product boundary
2. Mandatory diagnosis
3. Three operating modes
4. Change levels
5. Adapter policy
6. Controlled abundance
7. Escalation

## 1. Product boundary

The first product is an **automatic design final-review and redo Agent for
AI-generated websites**.

Keep two promises separate:

- browser review is stack-agnostic when the site has a stable, accessible URL;
- automatic code mutation is available only when the repository, adapter, tests,
  authority, and rollback boundary are verified.

Never translate “review any running website” into “safely rewrite any repository.”
A repository that cannot start reliably remains review-only or conditional.

## 2. Mandatory diagnosis

Before acquiring references or editing, run:

```bash
python <skill-dir>/scripts/diagnose_project.py <project-root> \
  --profile <project-root>/.top1-design/PROJECT_PROFILE.json \
  --target-url <verified-url> \
  --output <project-root>/.top1-design/diagnosis.json
```

The profile is optional; copy `PROJECT_PROFILE.example.json` when explicit stage,
runtime, or boundary facts are available. Repository heuristics have lower
confidence than a declared and verified project profile.

Diagnosis must establish:

- browser target readiness;
- framework and styling adapter;
- build, test, component, token, and governance signals;
- maturity mode and confidence;
- recommended and maximum change level;
- declared locked areas and actions that require confirmation.

Diagnosis selects an operating posture. It does not authorize a change or prove
the company's organizational maturity.

## 3. Three operating modes

| Mode | Typical condition | Default behavior | Valuable outcome |
|---|---|---|---|
| `greenfield` | little or no UI system | broad isolated generation, then implement one winner | from zero to a coherent direction |
| `rescue` | working UI with drift or weak system | preserve product structure, repair shared causes first | from inconsistent to unified |
| `governed` | mature tokens, components, tests, and review process | audit first, emit small reversible patches or PRs | prevent regression and find safe increments |

### Greenfield

Generate 6–12 structurally distinct experience directions in isolated
workspaces. The Agent may change composition, typography, component language, and
motion inside the declared product truth and workflow boundary.

### Rescue

Map the real system before editing:

```text
pages → shared components → tokens → drift → high-leverage repair
```

Prefer a token or shared-component fix when it improves many surfaces and its
blast radius is testable. Do not erase validated information architecture merely
because a replacement screenshot looks cleaner.

### Governed

Treat approved tokens, components, analytics contracts, accessibility standards,
and release processes as constraints. Default to audit or a small patch. Trend
evidence may justify an experiment, not a silent restyle.

## 4. Change levels

| Level | Scope | Typical mode |
|---:|---|---|
| 0 | review only | unsupported or unverified repository |
| 1 | one surface or page | governed, conditional adapter |
| 2 | shared components | rescue, governed with approval |
| 3 | design tokens | rescue |
| 4 | visual system | greenfield or explicitly approved rescue |
| 5 | product design direction | greenfield with product boundary confirmed |

Choose the highest-return level whose affected surfaces can be enumerated,
tested, reviewed, and rolled back. A larger edit is not inherently more
ambitious; unbounded blast radius is simply unverified.

## 5. Adapter policy

First-release automatic modification support is intentionally narrow:

- React or Next.js;
- Tailwind CSS;
- a stable local start path;
- a build boundary;
- a declared primary flow;
- tests or a test plan that can verify the affected scope.

React or Next.js without all conditions is `conditional`. Other stacks are
`review_only` until an adapter exists. Review evidence may still be produced for
Vue, Nuxt, Svelte, static HTML, Webflow, or a remote site if the browser target is
stable.

Never replace the core framework, introduce a high-risk dependency, or modify a
production branch merely to make the adapter fit.

## 6. Controlled abundance

“Violence through volume” means:

```text
many isolated candidates
→ cheap deterministic rejection
→ blinded pairwise tournament
→ deep browser verification of finalists
→ one small, reviewable winning patch
```

It does not mean repeated unbounded edits in the user's main worktree.

Keep human involvement at two planned points:

1. before the run: goal, product truth, locked areas, and maximum authority;
2. after the run: approve the evidence-backed winner or request a new direction.

Pause in the middle only when evidence conflicts, repair cycles oscillate, or
the winning move would cross an authority boundary.

## 7. Escalation

Escalate rather than infer permission when:

- product strategy, pricing, claims, or the primary workflow would change;
- a rescue-mode fix requires Level 4 or 5;
- a governed-mode fix exceeds the diagnosed maximum;
- the repository cannot start or test reliably;
- the change cannot be isolated or rolled back;
- browser evidence cannot demonstrate an improvement.
