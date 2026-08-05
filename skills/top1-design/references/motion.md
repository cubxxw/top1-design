# Motion evaluation

## Motion has a job

Every motion must do at least one:

- explain causality;
- preserve spatial continuity;
- provide feedback;
- guide attention;
- reveal hierarchy;
- create a product-appropriate emotional peak.

If removal does not reduce comprehension, feedback, or intended emotion, remove it.

## Granularity

Evaluate motion at:

1. page choreography;
2. region entrance and exit;
3. component transition;
4. direct manipulation;
5. micro-feedback;
6. rest, active, interruption, completion, and reduced-motion states.

Capture before, midpoint, and after frames plus a short recording or trace when possible. A still screenshot cannot validate easing or continuity.

## Rubric

Check:

- trigger is understandable;
- origin and destination preserve object identity;
- duration matches distance and importance;
- easing feels physical and consistent;
- simultaneous motions have a clear leader;
- interruption and reversal work;
- layout remains stable;
- main-thread work and frame pacing meet budget;
- reduced-motion mode preserves meaning;
- hover-only behavior has touch and keyboard equivalents.

## Budgets

Use project-specific budgets. Reasonable starting assumptions:

- common micro-feedback: roughly 120–240 ms;
- standard state transition: roughly 180–360 ms;
- major narrative sequence: justify anything longer;
- no sustained decorative animation on operational UI;
- target smooth frame pacing on a representative mid-range device.

Do not force every animation into these ranges. Distance, platform, input, and brand character matter.

## High-ambition effects

Use WebGL, Canvas, scroll-driven motion, springs, View Transitions, or generative effects only when:

- the product mode and goal justify them;
- a simpler composition is already strong;
- there is a static or simpler fallback;
- the effect starts lazily and pauses offscreen;
- keyboard, touch, reduced-motion, and lower-power paths work;
- measured performance remains acceptable.

One extraordinary moment is usually stronger than many competing effects.
