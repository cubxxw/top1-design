# Reference library protocol

## Contents

1. Purpose
2. Coverage model
3. Reference card
4. From observation to principle
5. Selection
6. Freshness and rights

## 1. Purpose

The library externalizes taste. It prevents an agent from averaging its training distribution into a generic interface.

A reference is not a style name. It is a source-specific example of a relationship that works in a stated context.

Bad:

```text
Make it like Attio.
```

Good:

```text
Use Attio's relationship between restrained first-viewport copy and immediate
high-fidelity product proof. Preserve this product's category, brand, and layout.
```

## 2. Coverage model

Tag references by:

- mode: persuade, operate, read, experience;
- product category;
- scope depth: site, page, region, component, element, state;
- quality branch: comprehension, credibility, perception, operation;
- platform and viewport;
- evidence freshness;
- positive reference or anti-reference.

Before a major direction search, cover:

- whole-experience composition;
- same-category semantics;
- product proof;
- typography and layout;
- interaction or motion;
- at least one anti-reference.

Use `reference-library.json` as the seed catalog, not a timeless ranking.

## 3. Reference card

Create one JSON or Markdown card per observed scope:

```yaml
id: granola-home-product-hero
source_url: https://www.granola.ai/
captured_at: 2026-08-05T15:30:00Z
scope: landing/hero
mode: persuade
quality_branches: [comprehension, credibility, perception, operation]
observed:
  - High-fidelity product behavior dominates the first viewport.
  - The narrative follows before, during, and after a meeting.
interpretation:
  - Product behavior is the proof, not a decorative mockup.
transfer:
  - Make the user's core task manipulable early.
avoid_copy:
  - Do not copy branding, wording, illustration, or exact choreography.
fails_when:
  - The product is not interactive or the demo cannot stay reliable.
rights: link-only
```

Do not place interpretation in `observed`.

## 4. From observation to principle

Use this chain:

```text
pixel → relationship → user effect → product principle → implementation option
```

Example:

```text
pixel:
  thin low-alpha border plus small radius and no loud shadow
relationship:
  the product surface feels finished without competing with content
user effect:
  faster trust and scanning
principle:
  use restrained material cues for operational UI
implementation option:
  tokenized 1px border, 12–16px radius, state-specific tint
```

Transfer the principle, not the pixel values.

## 5. Selection

Choose references by relevance:

```text
relevance = goal similarity
          × user-context similarity
          × scope match
          × evidence freshness
          × implementation feasibility
```

Do not choose only the most beautiful site. Choose the best teacher for the current cell.

Use contrasting references to expose decisions:

- expressive brand world vs. operational restraint;
- text-led proof vs. interactive proof;
- editorial hierarchy vs. data density;
- native convention vs. novel interaction.

The agent must state what it is deliberately not borrowing.

## 6. Freshness and rights

Revisit dynamic websites before a new release. Store `captured_at` and mark observations stale when the source materially changes.

Default raw third-party screenshots to local-only evidence:

- do not publish without permission or a defensible license;
- do not use them as distributable templates;
- do not train or fine-tune on them by implication;
- store source URL and author attribution;
- remove private, personal, or account-specific data.

Public catalogs should contain metadata, observations, and recapture instructions.
