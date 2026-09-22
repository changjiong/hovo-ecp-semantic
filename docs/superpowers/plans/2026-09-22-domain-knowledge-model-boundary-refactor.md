# Domain Knowledge / Domain Model Boundary Refactor Implementation Plan

> **For agentic workers:** implement this plan task-by-task; keep document parsing, business knowledge formation, domain modeling, and platform implementation as separate concerns.

**Goal:** Refine `domain-knowledge` and `domain-model` so that business questions are coverage axes, business concepts/rules are the knowledge core, MinerU remains an input adapter, cases validate knowledge, and the domain model remains a platform-independent semantic model rather than a shadow runtime.

**Architecture:** Keep the existing five-stage pipeline and the existing MinerU document-intake path. Change the first two stages' methodology and presentation: `domain-knowledge` synthesizes source-backed business knowledge and separates audit coverage from knowledge completeness; `domain-model` consumes fixed knowledge and models stable objects, relations, facts, judgments, time, and process without reinterpreting source documents or expanding execution machinery.

**Tech Stack:** Markdown skill specifications, Python deterministic renderers, existing JSON/YAML contracts.

**Spec:** Conversation-approved design on 2026-09-22.

## Global Constraints

- Keep MinerU 4.x V1 and Structured Document IR as the canonical raw-document intake path.
- Do not add compatibility layers or migration fallbacks.
- Do not change ECP-related skills in this PR.
- Do not regenerate A01 business artifacts in this PR; treat them as existing examples that may become stale against revised skill guidance.
- Do not add new domain-specific execution algorithms to Domain DSL.

## Review Focus

- Document coverage must not be presented as proof of knowledge completeness.
- Questions must remain traceable without becoming the primary knowledge artifact.
- Expert/institutional operating practices must remain distinguishable from normative source rules.
- Real/source/synthetic cases must be used for validation without circularly proving generated rules.
- Domain Model must map fixed knowledge without rereading original regulations or requiring all business logic to execute locally.

---

### Task 1: Refine domain-knowledge methodology and output reading order

**Files:**
- Modify: `.agents/skills/domain-knowledge/SKILL.md`
- Modify: `.agents/skills/domain-knowledge/references/business-delivery.md`
- Modify: `.agents/skills/domain-knowledge/references/acceptance.md`
- Modify: `.agents/skills/domain-knowledge/scripts/render_documents.py`
- Modify: `.agents/skills/domain-knowledge/manifest.json`

**Deliverable:** Rules and terms are explicitly the core business knowledge; questions are coverage/navigation; MinerU is input infrastructure; cases are validation assets; audit trace is secondary.

### Task 2: Refine domain-model completion criteria and execution boundary

**Files:**
- Modify: `.agents/skills/domain-model/SKILL.md`
- Modify: `.agents/skills/domain-model/references/business-modeling.md`
- Modify: `.agents/skills/domain-model/references/domain-dsl.md`
- Modify: `.agents/skills/domain-model/references/acceptance.md`
- Modify: `.agents/skills/domain-model/manifest.json`

**Deliverable:** Completion is driven by scoped confirmed knowledge being modeled or explicitly excluded; questions are a coverage check; cases remain upstream truth; complex algorithms are implementation concerns unless their business semantics require formal expression.

### Task 3: Verify the branch

**Checks:**
- Parse both modified manifests as JSON.
- Inspect deterministic renderer syntax after changes.
- Compare branch to `main`; only the two Domain skills plus this plan may change.
- Open a PR documenting scope, non-goals, and test limitations.
