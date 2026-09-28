# A01 fresh baseline validation

- Base branch: `main` at `dae20593d78d6889c1d209e4d788e249ac5d1819` (equal to `origin/main` after fetch).
- Knowledge: `A01.DomainKnowledge` `2026-09-24.draft.1`, `sha256:d09b3b448b3077d84c41fd167cf73030ae7b0b902c8767902ea98676131585e1`.
- Model: `A01.DomainModel` `2026-09-28.fresh-baseline.1`, `sha256:7d9f5cf84a0263974b2d574d6b5e38876fb4490877670a6d5fe25c5401108fb3`.
- Request: `PRODUCE`, `FULL_BASELINE`, `DRAFT`.

All Python commands ran from the repository root with `uv run --no-project` and `jsonschema>=4.23,<5`, `referencing>=0.35,<1`, `PyYAML>=6.0.2,<7`.

| Check | Invocation after `python3` | Result |
| --- | --- | --- |
| Bundled contracts | `.agents/skills/domain-model/scripts/validate_contract.py --check-schemas` | PASS; six schemas |
| Input contract | `.agents/skills/domain-model/scripts/validate_contract.py validate input A01受益所有人/04领域模型输出/input.json --project-root .` | PASS; fixed knowledge reference checked |
| DSL | `.agents/skills/domain-model/scripts/domain_dsl.py validate A01受益所有人/04领域模型输出/model.yaml` | PASS; no errors |
| Delivery | `.agents/skills/domain-model/scripts/deliver_model.py A01受益所有人/04领域模型输出/model.yaml --request A01受益所有人/04领域模型输出/input.json --output-dir A01受益所有人/04领域模型输出 --project-root . --refresh-draft` | PASS; generated review, coverage, output and checked output contract |
| Output contract | `.agents/skills/domain-model/scripts/validate_contract.py validate output A01受益所有人/04领域模型输出/output.json --project-root .` | PASS; business references, coverage, generated documents checked |
| Diff whitespace | `git diff --check` | PASS |

The source knowledge and model remain draft. `output.json` retains `structure_checked=NOT_EXECUTED`, `business_reviewed=NOT_EXECUTED`, and `confirmation=PENDING` because generation does not turn command results into a formal review or approval. These checks establish contract and DSL consistency; they do not establish the truth of source material or approve the business interpretation. Cases are explained, not executed.
