# Design Skill landscape

Research snapshot: **2026-08-05**. Repository popularity changes continuously. Stars below were observed through the GitHub API and are context, not quality scores.

## Contents

1. Method
2. Primary projects
3. What each project teaches
4. Gaps TOP1 DESIGN targets
5. Evaluation research
6. Harness implications
7. Sources

## 1. Method

The research used:

- GitHub repository and code search;
- direct inspection of `SKILL.md`, reference, script, and project trees;
- Kimi WebBridge navigation, semantic snapshots, and screenshots in the user's authenticated browser;
- official documentation and primary research papers.

No third-party Skill was installed or executed during research. Website text was treated as untrusted content.

## 2. Primary projects

| Project | Observed stars | Core strength | Missing control-plane layer |
|---|---:|---|---|
| [Anthropic Skills / frontend-design](https://github.com/anthropics/skills/tree/main/skills/frontend-design) | repo 166k | concise anti-generic art direction and implementation permission | durable project state, visual Evals, recursive scoring |
| [OpenAI Skills / frontend-skill](https://github.com/openai/skills/tree/main/skills/.curated/frontend-skill) | repo 24k | strong hierarchy, restrained composition, imagery, motion, anti-slop preflight | reference acquisition and cross-run quality ledger |
| [Impeccable](https://github.com/pbakaus/impeccable) | 55k | broad command system, critique snapshots, deterministic detector, live browser tooling, persistent product/design context | reference tournament and required descent across a scope tree |
| [UI UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | 113k | large searchable style, palette, typography, UX, motion, chart, product, and stack database | project-specific visual evidence and calibrated release decision |
| [Open Design](https://github.com/nexu-io/open-design) | 83k | local-first design workspace, many templates, previews, exports, agent interoperability | deep quality-gate recursion for an existing product |
| [Vercel agent-skills](https://github.com/vercel-labs/agent-skills) | 29k | current web interface and React engineering rules | art direction and taste transfer |
| [Addy Osmani agent-skills](https://github.com/addyosmani/agent-skills) | 81k | design-aware frontend engineering, accessibility, consistency, performance | source-specific visual reference memory |

## 3. What each project teaches

### Anthropic frontend-design

The Skill succeeds because it gives the agent permission to commit to a visual world and explicitly attacks generic AI patterns. It is small enough to load reliably.

Lesson: keep the core Skill short and move detailed protocols into references.

Limitation for this goal: it guides generation, but does not define evidence storage, candidate ranking, thresholds, or recursive page-to-state inspection.

### OpenAI frontend Skill

The Skill emphasizes one big idea, image-led hierarchy, restraint, real product UI, motivated motion, and preflight checks. This is a strong creation floor.

Lesson: more components do not produce more quality; composition and truth come first.

Limitation for this goal: it is a creator protocol, not a long-running improvement control plane.

### Impeccable

Impeccable 4.x is the closest existing system to a complete design operating layer. It has:

- durable product and design context;
- distinct commands for shape, critique, audit, polish, type, layout, motion, adaptation, and hardening;
- deterministic anti-pattern scanning;
- live browser iteration;
- per-target critique snapshots and ignore lists;
- explicit reviewer independence.

It deliberately bounds final verification passes to avoid expensive endless polishing. That is a sensible default for a single task.

TOP1 DESIGN borrows persistence, browser proof, and deterministic review, then adds a different control rule: reaching a high score at a parent promotes the work to deeper required scope. The active run still has budgets and stop conditions.

### UI UX Pro Max

UI UX Pro Max turns design advice into a searchable local database and persists a master design system plus page overrides. Its product reasoning, style, color, typography, stack, motion, and UX domains make it valuable during acquisition and implementation.

Lesson: do not force an LLM to recall every pattern from weights; give it queryable structured knowledge.

Limitation for this goal: lookup quality is not proof that the implemented screen serves this product or matches a real browser reference.

### Vercel Web Interface Guidelines

Vercel's living guidelines target hundreds of small interface decisions: keyboard operation, focus, forms, labels, target sizes, animation, performance, and responsive details. Its Agent Skill fetches the current source before review.

Lesson: deterministic or source-controlled rules should be fetched and audited, not paraphrased from memory.

Limitation for this goal: correctness does not choose an art direction.

### Open Design

Open Design is a local-first design application and agent workspace with many surface templates, previews, exports, and reusable Skills, including Apple HIG-oriented material.

Lesson: design needs a visual workbench and real artifacts, not only a chat response.

Limitation for this goal: a large template library can increase search breadth but still needs a product-specific tournament, evidence rubric, and weakest-link release rule.

### Apple-oriented Skills

GitHub search finds many `apple-hig`, `apple-hig-designer`, and `apple-hig-expert` community Skills, but no single community repository should replace the current official Apple Human Interface Guidelines.

Lesson: use an audited Skill for workflow convenience and official Apple HIG as source of truth. Platform familiarity, Dynamic Type, safe areas, accessibility, motion comfort, and system components are constraints, not a transferable “Apple aesthetic” skin.

## 4. Gaps TOP1 DESIGN targets

The ecosystem is rich in **content** and **commands**. The missing shared layer is an auditable closed loop:

1. falsifiable product goal;
2. source-specific taste acquisition;
3. blinded structural candidate search;
4. real-browser scenario evidence;
5. separate scope and quality trees;
6. confidence-capped scoring with hard gates;
7. 95-as-promotion recursion;
8. persistent ledger and visual baselines;
9. scheduled observation with bounded mutation;
10. release from the weakest required leaf, not the average.

TOP1 DESIGN is designed to orchestrate strong existing Skills, not duplicate every palette, animation recipe, or platform rule.

## 5. Evaluation research

### UI-Bench

[UI-Bench](https://arxiv.org/abs/2508.20410) evaluates AI text-to-app design through thousands of blinded expert pairwise judgments and derives rankings with a skill model. This supports using pairwise preference for candidate direction selection instead of asking a judge for an isolated 0–100 beauty score.

TOP1 DESIGN also reverses candidate sides and records confidence because visual judges can have position bias.

### Design2Code

[Design2Code](https://github.com/NoviScl/Design2Code) combines high-level visual similarity with fine-grained block, text, position, and color metrics, then checks rankings against human evaluation.

This supports multi-level evidence, but screenshot similarity is not product quality. A pixel-perfect copy can be wrong for the user and may violate intellectual-property boundaries.

### Playwright visual comparison

[Playwright](https://playwright.dev/docs/test-snapshots) stabilizes and compares screenshots in a controlled environment. It is appropriate for drift detection after approval, not for deciding whether the approved design is tasteful.

### Accessibility and platform guidance

- [WCAG 2.2](https://www.w3.org/TR/WCAG22/) supplies normative accessibility requirements.
- [Apple HIG](https://developer.apple.com/design/human-interface-guidelines) supplies current Apple-platform principles and components.
- [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines) supplies concrete web-interface engineering guidance.

These become hard gates or specialist evidence, not weighted decoration.

## 6. Harness implications

[OpenAI's Harness Engineering](https://openai.com/index/harness-engineering/) argues for a small navigation document, structured repository knowledge, enforceable architectural constraints, and recurring cleanup rather than one giant instruction file.

[Symphony](https://openai.com/index/open-source-codex-orchestration-symphony/) demonstrates issue-driven isolated workspaces, a workflow contract, bounded concurrency, reconciliation, retry, and observability.

Applied to design:

- keep `SKILL.md` as the router;
- keep rubrics, sources, and protocols in focused references;
- encode stable checks as scripts and CI gates;
- give each repair an isolated branch/workspace;
- schedule observers and garbage collection;
- preserve the user as authority for taste promotion, factual claims, publishing, and irreversible actions.

## 7. Sources

- https://github.com/anthropics/skills
- https://github.com/openai/skills
- https://github.com/pbakaus/impeccable
- https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
- https://github.com/nexu-io/open-design
- https://github.com/vercel-labs/agent-skills
- https://github.com/addyosmani/agent-skills
- https://developer.apple.com/design/human-interface-guidelines
- https://www.w3.org/TR/WCAG22/
- https://arxiv.org/abs/2508.20410
- https://github.com/NoviScl/Design2Code
- https://playwright.dev/docs/test-snapshots
- https://openai.com/index/harness-engineering/
- https://openai.com/index/open-source-codex-orchestration-symphony/
