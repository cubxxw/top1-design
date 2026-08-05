# Contributing

TOP1 DESIGN accepts improvements that make design judgment more reproducible without pretending that taste is fully objective.

## Good contributions

- a rubric with explicit anchors and failure examples;
- a deterministic check with tests;
- a reference card that identifies a transferable principle and its source;
- an evaluation fixture that exposes a scoring or orchestration failure;
- a browser adapter that preserves evidence and provenance;
- a clearer stop, escalation, or safety rule.

## Pull request requirements

1. Explain which failure mode the change fixes.
2. Add or update a fixture when behavior changes.
3. Run `python -m unittest discover -s tests -v`.
4. Run the Skill validator described in `.github/workflows/validate.yml`.
5. Do not commit third-party website screenshots without explicit permission.
6. Do not add a style merely because it is fashionable; document the product contexts where it works and fails.

Reference cards must separate observed fact, interpretation, transferable principle, and anti-copy boundary.

Scores must remain auditable. Do not add an opaque “AI quality score” without its inputs, anchors, confidence, and evidence.
