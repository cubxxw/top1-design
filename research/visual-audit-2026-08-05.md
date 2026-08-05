# Seed reference visual audit

Captured with Kimi WebBridge on 2026-08-05. Raw images remain local-only; see `capture-manifest.json`.

## Granola

Observed:

- first viewport uses a strict two-column split;
- an oversized editorial headline carries identity;
- the right side shows a believable in-use note surface and meeting context;
- the palette is almost neutral, with one olive action color;
- product proof is visible before scrolling.

Transfer:

- make the product's core behavior the hero proof;
- allow one high-character typographic move while the product UI remains quiet;
- keep the action color scarce enough to retain meaning.

Do not transfer the exact serif, wording, meeting window, or brand color.

## Leonar Source

Observed:

- utility announcement, rounded primary navigation, breadcrumb, hero copy, and product card form distinct layers;
- the product card uses low-contrast borders and restrained shadow;
- recruiting semantics are visible inside the product surface;
- the headline is assertive while supporting copy remains conventional and readable.

Transfer:

- use quiet material tokens to create finish;
- put domain-specific evidence inside the product visual;
- separate global navigation, page location, promise, and proof.

Do not transfer the exact recruiter claims, colors, card content, or navigation shape.

## RON Design Lab

Observed:

- the composition is almost entirely typographic;
- extreme scale and large empty regions create confidence;
- navigation is a row of independent pill-like controls;
- a small floating action remains available without competing with the headline.

Transfer:

- treat type scale and whitespace as primary composition tools;
- use extreme scale only when the surface can afford low density.

Do not use this density for operational screens, complex forms, or long localized strings without adaptation.

## Attio

Observed:

- the first viewport contains a persistent navigation and a hero whose type is part of an ongoing blur/opacity animation;
- both a normal wait and an attempted finite-animation freeze produced an unsettled still;
- browser inspection found continuing animations, including infinite iterations.

Conclusion:

- this page cannot be evaluated reliably from one static first-viewport capture;
- collect a time sequence and interaction state before borrowing its current motion;
- use product-completion observations from settled downstream product surfaces, not this blurred still.

This is a useful failure case for the evidence protocol: a capture can be technically successful and still be invalid evidence.

## Other seeded references

Metaview, Common Room Signals, Clay, Juicebox, and Notion were captured and cataloged. Their transferable principles are stored in `skills/top1-design/references/reference-library.json`. Reinspect their current pages before a production decision because live sites change.
