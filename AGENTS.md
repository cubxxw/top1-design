# Agent instructions

Keep the installable Skill under `skills/top1-design`.

Before changing scoring behavior:

1. read `skills/top1-design/references/scoring.md`;
2. update or add a fixture;
3. run all tests;
4. preserve backward compatibility for `schema_version: "1.0"` unless the change is explicitly breaking.

Do not commit raw third-party website screenshots. Treat score 95 as a promotion threshold, not proof of objective quality.
