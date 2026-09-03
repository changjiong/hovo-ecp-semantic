# Trust Report

## Authority boundary

The skill treats the user-provided ECP Semantic Authoring Kit 1.7 and ECP Semantic Profile 1.0 as the technical authority for generated ECP assets. External ontology projects and model knowledge are advisory only and cannot broaden the Profile.

## Permissions

- Local file writes: limited to requested semantic workspaces and skill-local reports.
- Network: not required for normal asset authoring.
- Remote ECP/GitHub mutation: only when explicitly requested and separately authorized.
- Secrets: must not be written into semantic assets.

## Fail-closed rules

- Unsupported ECP semantic construct -> reject.
- Missing required business/data fact -> `UNKNOWN`, `NEEDS_INPUT`, or local asset `BLOCKED`; never invent.
- Missing compiler-owned evidence -> `ECP_PREFLIGHT_REQUIRED`; never fabricate `compilerContract.expect`.
- Digest mismatch -> reject.
- Scope resource limits or completeness not provable -> reject rather than truncate.

## Human interaction boundary

Default mode is evidence-first Autonomous authoring. Clarification is limited to at most one round and five high-impact `OPEN` decisions. `CONFIRMED`, `INFERRED`, and low-risk reversible `ASSUMED` items do not require interruption. `BLOCKED` inputs stop only dependent assets. Multi-round Workshop mode requires an explicit user request.

## Evidence status

Local static validation and deterministic regression evidence exist. ECP Admin preflight, candidate compilation, release publication, and production replay remain `missing evidence` until independently supplied by the platform.
