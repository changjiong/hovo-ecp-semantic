# A01 Domain Model 0.3.0 Independent Audit

Verdict: **PARTIAL**. Targeted execution is **PASS**: 72/72 rerun checks passed, with 0 failed assertions. Overall status remains partial because this is bounded coverage, not a full 86-case replay or business confirmation.

Role: `verification_auditor`. Read-only enforcement: **instruction-only; parent runtime filesystem is unrestricted**.
Repository: `/home/lsnn/github/hovo-ecp-semantic`; branch `main`; Git SHA `c9d192e7b1da72b0e935add1150efc267d88d2c0`. Existing dirty paths were preserved.

## Stable rerun

The final rerun re-executed `72` saved commands from `2026-09-18T03:08:03.549905+00:00` to `2026-09-18T03:09:48.317464+00:00`. Model SHA-256 before and after: `50f9670bda15719f532fa59a655412c65f65fcf7f49ea888b108798a9bfb3d8c` / `50f9670bda15719f532fa59a655412c65f65fcf7f49ea888b108798a9bfb3d8c`; stable=`True`. Current output contract was PASS. An earlier stale digest observation was superseded by this stable rerun.

## Artifact hashes

- `model_yaml`: `50f9670bda15719f532fa59a655412c65f65fcf7f49ea888b108798a9bfb3d8c` (/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml)
- `model_output`: `20e7e8bd02bf41bf3a7734588c504f9efa14330be6b8777ad8f7a4a5b68427d2` (/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/output.json)
- `knowledge_output`: `0962cfa90d0c2ee6ca60d02cefc3c4e06229368b3537e12f8b2fb701c7c9f0d9` (/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/03领域知识输出/output.json)
- `domain_dsl_py`: `943295ca5298d15f035d19f6cbc22ab2a2cadb5e8493a08ea787ec2b87f5fac4` (/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py)
- `dsl_expression_py`: `7216ad356deab6006aec3c03d3bd1a5359c3fca9b08c127f080613f90440b981` (/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/dsl_expression.py)
- `dsl_graph_py`: `6fedd8a73501ededf15fd65ed2eb4b379b0daab1b4bc5d859b4d48a01f540820` (/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/dsl_graph.py)
- `validate_contract_py`: `4ebb4fe8b12d3ab12e8cca2feec3dafeadcddd439c4cbb4c7b87faebb07fae9b` (/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/validate_contract.py)

## Summary

| Scope | Count |
| --- | ---: |
| `total` | 72 |
| `passed` | 72 |
| `failed` | 0 |
| `static` | 2 |
| `unrelated_order` | 3 |
| `decimal_precision` | 3 |

## Failed assertions

None in the stable 72-command rerun.

## Case records

### static.dsl_validate [PASS]
Scope: `static`; duration `1402.202 ms`; exit `0`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py validate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml'`
Expected: `{"status":"PASS"}`
Actual: `{
  "errors": [],
  "status": "PASS"
}`

### static.contract_validate_output [PASS]
Scope: `static`; duration `10092.284 ms`; exit `0`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/validate_contract.py validate output '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/output.json' --project-root '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人'`
Expected: `{"status":"PASS"}`
Actual: `{
  "status": "PASS",
  "mode": "contract",
  "failures": [],
  "checked": {
    "direction": "output",
    "file": "/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/output.json",
    "projectRoot": "/home/lsnn/github/hovo-ecp-semantic/A01受益所有人",
    "stage": "domain-model",
    "artifactRefs": 8,
    "ids": {
      "id": 15
    },
    "evidenceReferences": 0,
    "businessReferences": "CHECKED",
    "coverage": "CHECKED",
    "dslVersion": "2.0.0",
    "generatedDocuments": "CHECKED"
  },
  "boundary": "验证结构、字节引用、业务标识与覆盖一致性；不证明来源真实、判断正确或确认人身份。"
}`

### generic.order_validate [PASS]
Scope: `unrelated_order`; duration `207.782 ms`; exit `0`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py validate /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/model.yaml`
Expected: `{"status":"PASS"}`
Actual: `{
  "errors": [],
  "status": "PASS"
}`

### generic.order_known [PASS]
Scope: `unrelated_order`; duration `210.74 ms`; exit `0`.
Input: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/known.json`; SHA-256 `f929d3aeeb42f14ad0e3c350f1925f8a5657d4206650113cbe4af9dedab66c88`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/model.yaml --rule M.CanFulfill --inputs /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/known.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### generic.order_unknown [PASS]
Scope: `unrelated_order`; duration `198.739 ms`; exit `0`.
Input: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/unknown.json`; SHA-256 `de78b118de57f7bd6ba4a5f165413eb39f4dca59771583ab7e4515417f2c66c4`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/model.yaml --rule M.CanFulfill --inputs /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/examples/order/unknown.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### threshold.standard1_25 [PASS]
Scope: `threshold`; duration `1359.913 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/std1_25.json`; SHA-256 `8c3167d5514f4e369093265f3ce0b8aea5cad59c77dc76991843cb46b594cc46`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Standard1 --inputs /tmp/a01-model-070-audit-inputs/std1_25.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### threshold.standard1_24_99 [PASS]
Scope: `threshold`; duration `1255.98 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/std1_2499.json`; SHA-256 `3d7187c426df5abec7c97a4c8fa5ff9e399de1903cb7fee16e693bd902f9af92`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Standard1 --inputs /tmp/a01-model-070-audit-inputs/std1_2499.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### threshold.standard2_vote_25 [PASS]
Scope: `threshold`; duration `1282.591 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/std2_vote_25.json`; SHA-256 `fee0ca60f4e8dcba1ba921aeb315265a529b68c0be03b5859a07a51357e10bb6`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Standard2 --inputs /tmp/a01-model-070-audit-inputs/std2_vote_25.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### paths.total_multi_0_40 [PASS]
Scope: `multipath`; duration `1269.359 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_total_multi.json`; SHA-256 `1069988e978357e15b37ce419e157b66951b84659222d5a4718440c41127a552`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityTotal --inputs /tmp/a01-model-070-audit-inputs/equity_total_multi.json`
Expected: `{"status":"KNOWN","value":"0.40"}`
Actual: `{
  "status": "KNOWN",
  "value": "0.40"
}`

### paths.total_incomplete [PASS]
Scope: `unknown`; duration `1277.009 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_total_incomplete.json`; SHA-256 `6b75fd33761387f05204a7e305250d75f41cda8d781dc5a4d2d01d297299a12d`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityTotal --inputs /tmp/a01-model-070-audit-inputs/equity_total_incomplete.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### promise.exemption_true [PASS]
Scope: `promise`; duration `1261.866 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/filing_exemption_true.json`; SHA-256 `591cad966db9b295dcd9033ee15da944438ff4f80b765db0d28e64505dc1195f`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FilingExemption --inputs /tmp/a01-model-070-audit-inputs/filing_exemption_true.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### promise.exemption_truthful_false [PASS]
Scope: `promise`; duration `1233.12 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/filing_exemption_promise_false.json`; SHA-256 `d80b33de4eedac49d8bddf4e204399e59d97cac55e9d5e668d452376914bb2a9`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FilingExemption --inputs /tmp/a01-model-070-audit-inputs/filing_exemption_promise_false.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### state.applicability_true [PASS]
Scope: `state_gate`; duration `1274.744 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/state_applicable_true.json`; SHA-256 `fb93278397cb8a842a12026f5e31ba00e0b6fc9f5866606b7701caaaaf9de912`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.StateApplicability --inputs /tmp/a01-model-070-audit-inputs/state_applicable_true.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### state.applicability_official_unknown [PASS]
Scope: `state_gate`; duration `1283.568 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/state_applicable_unknown.json`; SHA-256 `acbfbaedea3ee0588b6ec40b0c9d885ea7201fe9bd8966d2f0ff30d0803c6a3f`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.StateApplicability --inputs /tmp/a01-model-070-audit-inputs/state_applicable_unknown.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### state.simplification_all_gates [PASS]
Scope: `state_gate`; duration `1266.372 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/state_simplification_true.json`; SHA-256 `5d5b4e39496645f919a1ac952bdabecbdacf4a83ca92b901ab5073c98c35eca8`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.StateSimplification --inputs /tmp/a01-model-070-audit-inputs/state_simplification_true.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### state.simplification_risk_trigger [PASS]
Scope: `state_gate`; duration `1266.078 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/state_simplification_trigger.json`; SHA-256 `a3a65b16c5b6808c0b48dad102e621521420acf44155395fe5f68ee45c7dcf6c`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.StateSimplification --inputs /tmp/a01-model-070-audit-inputs/state_simplification_trigger.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### deadline.filing_online_same_day [PASS]
Scope: `deadline`; duration `1246.194 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/filing_due_online.json`; SHA-256 `508353baf59980e0640612400964d75125c10be8563926e2799069a86d69f01c`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FilingDue --inputs /tmp/a01-model-070-audit-inputs/filing_due_online.json`
Expected: `{"status":"KNOWN","value":"2026-04-01"}`
Actual: `{
  "status": "KNOWN",
  "value": "2026-04-01"
}`

### deadline.filing_onsite_30_days [PASS]
Scope: `deadline`; duration `1347.517 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/filing_due_onsite.json`; SHA-256 `1186f2e29dc68688ebbff5d90c2ee9abab889244da6fa28dffab5d395d84a0d6`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FilingDue --inputs /tmp/a01-model-070-audit-inputs/filing_due_onsite.json`
Expected: `{"status":"KNOWN","value":"2026-05-01"}`
Actual: `{
  "status": "KNOWN",
  "value": "2026-05-01"
}`

### deadline.filing_legacy_fixed_date [PASS]
Scope: `deadline`; duration `1246.605 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/filing_due_stock.json`; SHA-256 `955efff32db90d40abdc1e902548d8f765e7872a653c36dd07669406c4f25e4f`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FilingDue --inputs /tmp/a01-model-070-audit-inputs/filing_due_stock.json`
Expected: `{"status":"KNOWN","value":"2025-11-01"}`
Actual: `{
  "status": "KNOWN",
  "value": "2025-11-01"
}`

### deadline.update_plus_30 [PASS]
Scope: `deadline`; duration `1470.986 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/update_due.json`; SHA-256 `8f971acb0539602958f5d418ac161b7a79c9a3d0540dfd0e6ad29ce4faf20f45`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.UpdateDue --inputs /tmp/a01-model-070-audit-inputs/update_due.json`
Expected: `{"status":"KNOWN","value":"2026-10-01"}`
Actual: `{
  "status": "KNOWN",
  "value": "2026-10-01"
}`

### deadline.timing_pending_inside_window [PASS]
Scope: `deadline`; duration `1424.328 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/timing_pending_inside.json`; SHA-256 `374e842619c1d528d565e44836bf603bf81a08369a95534476e1aca82efd52ea`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.TimingPending --inputs /tmp/a01-model-070-audit-inputs/timing_pending_inside.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### deadline.timing_pending_after_correction [PASS]
Scope: `deadline`; duration `1481.339 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/timing_pending_corrected.json`; SHA-256 `bf1b294bde35ee3797c28b48e505bd536f38ca2d66f56da44dc8410dd1d07fd7`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.TimingPending --inputs /tmp/a01-model-070-audit-inputs/timing_pending_corrected.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### date.year_month_same [PASS]
Scope: `date`; duration `1469.853 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/date_ym_same.json`; SHA-256 `e75a6516dd887bdd8fb59b8126c51e26df2f5193e1bc19837989f797ff45d3ba`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.DateYearMonth --inputs /tmp/a01-model-070-audit-inputs/date_ym_same.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### date.year_month_diff [PASS]
Scope: `date`; duration `1304.067 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/date_ym_diff.json`; SHA-256 `a9794362a2f6b2204c7a9f08e775766ab80bf2740d8d245a3067a267b716fc89`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.DateYearMonth --inputs /tmp/a01-model-070-audit-inputs/date_ym_diff.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### closure.actual_and_rechecked [PASS]
Scope: `correction`; duration `1367.58 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/close_true.json`; SHA-256 `4c5f18f86cc435facf4ed46e51406c46534d4eca3b78f83723a2f83535044959`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CloseDifference --inputs /tmp/a01-model-070-audit-inputs/close_true.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### closure.promise_only_no_close [PASS]
Scope: `correction`; duration `1339.161 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/close_promise_only.json`; SHA-256 `69eb5db0aaf0c9609b6142db6787a4fb8b70fe9ccc575a67b17bf359b53c3c4f`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CloseDifference --inputs /tmp/a01-model-070-audit-inputs/close_promise_only.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### closure.actual_without_recheck [PASS]
Scope: `correction`; duration `1377.496 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/close_not_rechecked.json`; SHA-256 `93f080a50b01af245d81363da136828cb7e0b85f7aa48ac870370364d0fb3afe`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CloseDifference --inputs /tmp/a01-model-070-audit-inputs/close_not_rechecked.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### correction.major_filing_error [PASS]
Scope: `correction`; duration `1323.153 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/correction_action_major.json`; SHA-256 `4ce3bc0319ee066c37837c0a41d5ca99d9800108ecc69c24522b7cb03d767c6b`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CorrectionAction --inputs /tmp/a01-model-070-audit-inputs/correction_action_major.json`
Expected: `{"status":"KNOWN","value":"报告重大差异并跟踪"}`
Actual: `{
  "status": "KNOWN",
  "value": "报告重大差异并跟踪"
}`

### correction.minor_filing_error [PASS]
Scope: `correction`; duration `1398.735 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/correction_action_minor.json`; SHA-256 `937c78a227238d057812fa9998f59a40d145c57aaae5a39de4db00c0cb52cc87`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CorrectionAction --inputs /tmp/a01-model-070-audit-inputs/correction_action_minor.json`
Expected: `{"status":"KNOWN","value":"记录差异并提示客户"}`
Actual: `{
  "status": "KNOWN",
  "value": "记录差异并提示客户"
}`

### query.allowed_batch_with_remaining_quota [PASS]
Scope: `query_state`; duration `1310.101 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_allowed_batch.json`; SHA-256 `0dad4fde4e9e41516461560fc05283a439d972d48ce3061408646e0337f2f9c2`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.QueryAllowed --inputs /tmp/a01-model-070-audit-inputs/query_allowed_batch.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### query.allowed_after_quota_exhausted [PASS]
Scope: `query_state`; duration `1277.186 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_allowed_exhausted.json`; SHA-256 `fd2369a0b36227bb58bf69c7539f50e8f516271249372e9774dce56424e051c0`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.QueryAllowed --inputs /tmp/a01-model-070-audit-inputs/query_allowed_exhausted.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### query.daily_stop_at_boundary [PASS]
Scope: `query_state`; duration `1372.23 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/daily_stop_boundary.json`; SHA-256 `e6aa9599aa852adc37dfed5cd500f32ea125c140796212441ccb1994ff14651a`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.DailyStop --inputs /tmp/a01-model-070-audit-inputs/daily_stop_boundary.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### query.daily_stop_beyond_boundary [PASS]
Scope: `query_state`; duration `1559.916 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/daily_stop_beyond.json`; SHA-256 `92c57efb89fb12e1c87ba123e5cf69e5ffd28784947c085d9e43ddddbd69102a`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.DailyStop --inputs /tmp/a01-model-070-audit-inputs/daily_stop_beyond.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### query.partial_not_usable [PASS]
Scope: `query_state`; duration `1462.694 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_usable_partial.json`; SHA-256 `759f2142c6b4587e7abc6de842f9767873372317f0f5b78648238b197b7f1efa`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.QueryUsable --inputs /tmp/a01-model-070-audit-inputs/query_usable_partial.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### query.all_feedback_conditions [PASS]
Scope: `query_state`; duration `1436.675 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_usable_full.json`; SHA-256 `9010dade37dba5ce525ffd3a7c7b1392e04337657b0b3c6d68866e678fcb7705`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.QueryUsable --inputs /tmp/a01-model-070-audit-inputs/query_usable_full.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### query.request_mismatch [PASS]
Scope: `query_state`; duration `1404.461 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_match_wrong.json`; SHA-256 `d02e2819727c57ae31e0c402e6dc30a02e8f409926b12eb430de0101517ebeb5`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.QueryMatch --inputs /tmp/a01-model-070-audit-inputs/query_match_wrong.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### query.current_missing_verification [PASS]
Scope: `query_state`; duration `1480.222 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/current_query_missing_verification.json`; SHA-256 `2356660fe66fbadede994c278761d86cb094ab28ee2ae9c8b6816ce66ab0be25`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.CurrentQuery --inputs /tmp/a01-model-070-audit-inputs/current_query_missing_verification.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### query.invalid_requires_reverification [PASS]
Scope: `query_state`; duration `1478.797 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/reverification_invalid.json`; SHA-256 `22420e989fea5e51bcfe4dcc9c739c2ae643aad5d2d0ba2df1d36d733cc3ef69`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Reverification --inputs /tmp/a01-model-070-audit-inputs/reverification_invalid.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### parameters.gap [PASS]
Scope: `parameters`; duration `1486.708 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/parameter_gap.json`; SHA-256 `508969c2c2ae1f9b3d6c310d46c101068e5f5a500818e51bcfdc2372093c6e0e`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterContinuity --inputs /tmp/a01-model-070-audit-inputs/parameter_gap.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### parameters.contiguous [PASS]
Scope: `parameters`; duration `1493.322 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/parameter_contiguous.json`; SHA-256 `17b842263ec22e1c4caf8978ee43eeb165b2e1d5eab04288352c2c75591a180c`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterContinuity --inputs /tmp/a01-model-070-audit-inputs/parameter_contiguous.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### parameters.resend_needed [PASS]
Scope: `parameters`; duration `1599.274 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/resend_needed.json`; SHA-256 `a0d0a1b9b5da2d9f22412d72aadf3de677c014f3f98032dd69a5ee047b4a5816`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterResend --inputs /tmp/a01-model-070-audit-inputs/resend_needed.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### parameters.resend_not_needed [PASS]
Scope: `parameters`; duration `1713.813 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/resend_not_needed.json`; SHA-256 `792e9f3a4d2602d563b5c28cdbbeab6f1000664e64bad63ab865960b74927066`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterResend --inputs /tmp/a01-model-070-audit-inputs/resend_not_needed.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### parameters.send_when_continuous_and_accepting [PASS]
Scope: `parameters`; duration `1477.419 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/parameter_send_yes.json`; SHA-256 `6254e7134d5f5a1c8a5cf871df75158754068da1fb9a4e3005c1f40d05097474`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterSend --inputs /tmp/a01-model-070-audit-inputs/parameter_send_yes.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### parameters.block_when_gap [PASS]
Scope: `parameters`; duration `1510.652 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/parameter_send_no.json`; SHA-256 `8be50dff12e27c5ee4054ee8a9bebab5ce5e4848654053d8128582d2c6ca4562`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.ParameterSend --inputs /tmp/a01-model-070-audit-inputs/parameter_send_no.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### file.initial_response_not_usable [PASS]
Scope: `file_state`; duration `1489.157 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/file_usable_initial.json`; SHA-256 `759e5127a81eb0651726bc15022bcc081a44e367622d9478f2ae247f6bee42a9`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FileUsable --inputs /tmp/a01-model-070-audit-inputs/file_usable_initial.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`

### file.response_with_id_usable [PASS]
Scope: `file_state`; duration `1548.822 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/file_usable_yes.json`; SHA-256 `081a94ad5684df45067d3eb9c761081bb54d6ccc23f3dcc17b2606e5f8e3609d`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.FileUsable --inputs /tmp/a01-model-070-audit-inputs/file_usable_yes.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`

### paths.multi_direct_and_indirect [PASS]
Scope: `multipath`; duration `1476.321 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_paths_multi.json`; SHA-256 `b41c3bfc22fcb22721aaca3f00c791f79169d2265b571d5c49a7d3267636c1a3`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityPaths --inputs /tmp/a01-model-070-audit-inputs/equity_paths_multi.json`
Expected: `{"status":"KNOWN","value_unordered":["0.10","0.3000"]}`
Actual: `{
  "status": "KNOWN",
  "value": [
    "0.10",
    "0.3000"
  ]
}`
Note: Exact Decimal output preserves scale: 0.50*0.60 is emitted as 0.3000; this is expected precision behavior.

### paths.cycle_unknown [PASS]
Scope: `unknown_cycle`; duration `1412.376 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_paths_cycle.json`; SHA-256 `318ac3781082c9b82e11cb2689d0607568bc0ff17539f58f8834b88c0c9000e2`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityPaths --inputs /tmp/a01-model-070-audit-inputs/equity_paths_cycle.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### paths.unknown_collection_propagates [PASS]
Scope: `unknown`; duration `1420.0 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_paths_unknown_collection.json`; SHA-256 `71676999a16a67ba88caac844889145c918987f97526a8cf34c9208aa6f76c1c`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityPaths --inputs /tmp/a01-model-070-audit-inputs/equity_paths_unknown_collection.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### paths.unknown_end_constraint_blocks [PASS]
Scope: `unknown_constraint`; duration `1427.418 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_paths_unknown_end.json`; SHA-256 `3187d5d8cdeccbb52981103c1870ad054001ba73d0cc3e04af8aec9fb7ed77ca`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityPaths --inputs /tmp/a01-model-070-audit-inputs/equity_paths_unknown_end.json`
Expected: `{"status":"BLOCKED","has_constraint_failures":true}`
Actual: `{
  "constraint_failures": [
    {
      "action": "REVIEW",
      "constraint": "M.Constraint.RightInterval",
      "location": "/inputs/rights/0",
      "outcome": "UNKNOWN"
    }
  ],
  "status": "BLOCKED",
  "value": null
}`

### formation.continuous_merges_adjacent [PASS]
Scope: `formation`; duration `1417.613 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/formation_continuous.json`; SHA-256 `a144ffa54fe75d8ac3da67cdbbfa04c19c0a5563392bcd368af24e99841ce4f8`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Formation --inputs /tmp/a01-model-070-audit-inputs/formation_continuous.json`
Expected: `{"status":"KNOWN","value":"2024-05-01"}`
Actual: `{
  "status": "KNOWN",
  "value": "2024-05-01"
}`

### formation.interrupted_uses_current_interval [PASS]
Scope: `formation`; duration `1384.756 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/formation_interrupted.json`; SHA-256 `c53d10ded1efbcdaa835ea4073f1e8b91632f26eae8dcdceaf1be4d040d0e731`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Formation --inputs /tmp/a01-model-070-audit-inputs/formation_interrupted.json`
Expected: `{"status":"KNOWN","value":"2024-06-02"}`
Actual: `{
  "status": "KNOWN",
  "value": "2024-06-02"
}`

### formation.unknown_continuity_propagates [PASS]
Scope: `formation_unknown`; duration `1354.144 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/formation_flags_unknown.json`; SHA-256 `b2a9d4970a9771dbaab93e8161db33368bd7fdf86e13a4c34f175ce1e7b2147d`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Formation --inputs /tmp/a01-model-070-audit-inputs/formation_flags_unknown.json`
Expected: `{"status":"UNKNOWN","value":null}`
Actual: `{
  "status": "UNKNOWN",
  "value": null
}`

### formation.unknown_end_constraint_blocks [PASS]
Scope: `formation_unknown_constraint`; duration `1369.142 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/formation_unknown_end.json`; SHA-256 `a0a6affd3bc77ae28b220c63b8afd05939de67fc295dd2e5f352eb14f0e42a12`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Formation --inputs /tmp/a01-model-070-audit-inputs/formation_unknown_end.json`
Expected: `{"status":"BLOCKED","has_constraint_failures":true}`
Actual: `{
  "constraint_failures": [
    {
      "action": "REVIEW",
      "constraint": "M.Constraint.BeneficialOwnershipInterval",
      "location": "/inputs/history/0",
      "outcome": "UNKNOWN"
    }
  ],
  "status": "BLOCKED",
  "value": null
}`

### transition.diff_corrected_actual [PASS]
Scope: `correction`; duration `1390.213 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/diff_corrected_true.json`; SHA-256 `4f966d7fd2c302e0df99ef930bc0c4383ff92f3f05f2f09bd9b356ba7809aa63`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Difference --event CORRECTED --record /tmp/a01-model-070-audit-inputs/diff_corrected_true.json`
Expected: `{"status":"APPLIED","from":"处理中","to":"待复核"}`
Actual: `{
  "from": "处理中",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "待复核"
}`

### transition.diff_corrected_without_actual_correction [PASS]
Scope: `correction`; duration `1511.877 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/diff_corrected_false.json`; SHA-256 `493adfa0c58a1189eef6fd677debc2e6f1d774bb38a58effd0286ddb4f46a56c`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Difference --event CORRECTED --record /tmp/a01-model-070-audit-inputs/diff_corrected_false.json`
Expected: `{"status":"BLOCKED","reason_contains":"false"}`
Actual: `{
  "from": "处理中",
  "reason": "guard 为 false",
  "status": "BLOCKED",
  "to": "待复核"
}`

### transition.diff_resolve_after_recheck [PASS]
Scope: `correction`; duration `1361.528 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/diff_resolve_true.json`; SHA-256 `6a1f89cc8ab6837f90725ca6293f4a54af3f975b5eb2c9902355cfb84a65ef75`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Difference --event RECHECK --record /tmp/a01-model-070-audit-inputs/diff_resolve_true.json`
Expected: `{"status":"APPLIED","from":"待复核","to":"已解决"}`
Actual: `{
  "from": "待复核",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "已解决"
}`

### transition.diff_resolve_without_recheck [PASS]
Scope: `correction`; duration `1361.189 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/diff_resolve_unknown.json`; SHA-256 `c59410e83691244e116ec5548013f5719e2a05051b14c3447c8afc34b9818e7e`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Difference --event RECHECK --record /tmp/a01-model-070-audit-inputs/diff_resolve_unknown.json`
Expected: `{"status":"BLOCKED","reason_contains":"UNKNOWN"}`
Actual: `{
  "from": "待复核",
  "reason": "guard 为 UNKNOWN",
  "status": "BLOCKED",
  "to": "已解决"
}`

### transition.query_partial_feedback [PASS]
Scope: `query_state`; duration `1335.453 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_partial.json`; SHA-256 `500333b914233bb8cfb5b36c1e297bc8293f42b26ac03eb205147d0e7266224e`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Query --event PARTIAL --record /tmp/a01-model-070-audit-inputs/query_partial.json`
Expected: `{"status":"APPLIED","from":"待业务反馈","to":"待补全"}`
Actual: `{
  "from": "待业务反馈",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "待补全"
}`

### transition.query_failed_feedback [PASS]
Scope: `query_state`; duration `1345.978 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_failed.json`; SHA-256 `6d8f6be646c53e09d156c25259e1a6c2807ec1bdb33e0d520565424f0ae87ff1`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Query --event FAILED --record /tmp/a01-model-070-audit-inputs/query_failed.json`
Expected: `{"status":"APPLIED","from":"待业务反馈","to":"失败"}`
Actual: `{
  "from": "待业务反馈",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "失败"
}`

### transition.query_async_not_usable [PASS]
Scope: `query_state`; duration `1429.554 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_receive_pending.json`; SHA-256 `a5cb542a2089e685230b597d58d88d6aff078c8c16cf3126fd756d67cde4c1db`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Query --event FEEDBACK --record /tmp/a01-model-070-audit-inputs/query_receive_pending.json`
Expected: `{"status":"BLOCKED","reason_contains":"false"}`
Actual: `{
  "from": "待业务反馈",
  "reason": "guard 为 false",
  "status": "BLOCKED",
  "to": "收到结果"
}`

### transition.query_complete_feedback [PASS]
Scope: `query_state`; duration `1372.326 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/query_receive_yes.json`; SHA-256 `6b2b99a8c61d5e6b668594ce33509ec0315aba25debaf5a2970a5b618d523555`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Query --event FEEDBACK --record /tmp/a01-model-070-audit-inputs/query_receive_yes.json`
Expected: `{"status":"APPLIED","from":"待补全","to":"收到结果"}`
Actual: `{
  "from": "待补全",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "收到结果"
}`

### transition.report_feedback_supplement [PASS]
Scope: `report_state`; duration `1341.657 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/report_supplement.json`; SHA-256 `c3d038d65bcac538798b7d2a0ece82f00d5e3f1943017854710e8c8dd0ca8080`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Report --event SUPPLEMENT --record /tmp/a01-model-070-audit-inputs/report_supplement.json`
Expected: `{"status":"APPLIED","from":"已提交待反馈","to":"待补充"}`
Actual: `{
  "from": "已提交待反馈",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "待补充"
}`

### transition.report_missing_feedback_status [PASS]
Scope: `report_state`; duration `1353.67 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/report_feedback_unknown.json`; SHA-256 `e48e26dfcd8f5363feaf9de1b436f9044ad1ac5d84632a658cd8d1e9b362f768`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Report --event SUPPLEMENT --record /tmp/a01-model-070-audit-inputs/report_feedback_unknown.json`
Expected: `{"status":"BLOCKED","reason_contains":"UNKNOWN"}`
Actual: `{
  "from": "已提交待反馈",
  "reason": "guard 为 UNKNOWN",
  "status": "BLOCKED",
  "to": "待补充"
}`

### transition.report_feedback_wrong_reference [PASS]
Scope: `report_state`; duration `1290.459 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/report_feedback_mismatch.json`; SHA-256 `0fe054fdebf0848458e07755914b7891ee9fa411ca057fc04ca5d261b733488a`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Report --event SUPPLEMENT --record /tmp/a01-model-070-audit-inputs/report_feedback_mismatch.json`
Expected: `{"status":"BLOCKED","has_constraint_failures":true}`
Actual: `{
  "constraint_failures": [
    {
      "action": "BLOCK",
      "constraint": "M.Constraint.ReportFeedback",
      "location": "/record",
      "outcome": "VIOLATED"
    }
  ],
  "from": "已提交待反馈",
  "reason": "记录约束未通过",
  "status": "BLOCKED",
  "to": null
}`

### transition.case_first_feedback_number [PASS]
Scope: `case_state`; duration `1325.691 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/case_number.json`; SHA-256 `ee1df388dd137c74774d322655dc60893003e9a8b044f0eaff97a02799b08e75`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.Case --event NUMBER --record /tmp/a01-model-070-audit-inputs/case_number.json`
Expected: `{"status":"APPLIED","from":"已申请待反馈","to":"已取得编号"}`
Actual: `{
  "from": "已申请待反馈",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "已取得编号"
}`

### transition.file_initial_response_not_usable [PASS]
Scope: `file_state`; duration `1310.85 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/file_pending_response.json`; SHA-256 `476d3294bba540b1a7f7721a3661a225fcb0fc311f94b2e30aea8e2ee5455998`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.File --event FEEDBACK --record /tmp/a01-model-070-audit-inputs/file_pending_response.json`
Expected: `{"status":"BLOCKED","reason_contains":"false"}`
Actual: `{
  "from": "待业务应答",
  "reason": "guard 为 false",
  "status": "BLOCKED",
  "to": "可关联"
}`

### transition.file_id_and_matching_response [PASS]
Scope: `file_state`; duration `1412.36 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/file_usable_transition.json`; SHA-256 `b39bac6f6901d9d8087b5b5285cff657b1d5e0767ae30d21f022238679a71ff2`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.File --event FEEDBACK --record /tmp/a01-model-070-audit-inputs/file_usable_transition.json`
Expected: `{"status":"APPLIED","from":"待业务应答","to":"可关联"}`
Actual: `{
  "from": "待业务应答",
  "reason": "guard 为 true",
  "status": "APPLIED",
  "to": "可关联"
}`

### transition.file_response_mismatch_blocks [PASS]
Scope: `file_state`; duration `1349.729 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/file_response_mismatch.json`; SHA-256 `392a73e4b766572c82bd2ba7e7abe7a01066542f7e7377184867e0ee78e15dee`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py transition '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --machine M.Machine.File --event FEEDBACK --record /tmp/a01-model-070-audit-inputs/file_response_mismatch.json`
Expected: `{"status":"BLOCKED","has_constraint_failures":true}`
Actual: `{
  "constraint_failures": [
    {
      "action": "BLOCK",
      "constraint": "M.Constraint.FileFeedback",
      "location": "/record",
      "outcome": "VIOLATED"
    }
  ],
  "from": "待业务应答",
  "reason": "记录约束未通过",
  "status": "BLOCKED",
  "to": null
}`

### precision.standard1_below_threshold [PASS]
Scope: `decimal_precision`; duration `1427.309 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/std1_precision_below.json`; SHA-256 `ef2516ca4181183dc2a9456a797640389838455ae9503fa19942ce635772c22a`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Standard1 --inputs /tmp/a01-model-070-audit-inputs/std1_precision_below.json`
Expected: `{"status":"KNOWN","value":false}`
Actual: `{
  "status": "KNOWN",
  "value": false
}`
Note: Long Decimal below 0.25 remains false.

### precision.standard1_above_threshold [PASS]
Scope: `decimal_precision`; duration `1343.508 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/std1_precision_above.json`; SHA-256 `e59b1de3bd8a75d70cd75e6cf01d672ed8dd555e38860f7cbf93851ebb8575c6`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.Standard1 --inputs /tmp/a01-model-070-audit-inputs/std1_precision_above.json`
Expected: `{"status":"KNOWN","value":true}`
Actual: `{
  "status": "KNOWN",
  "value": true
}`
Note: Long Decimal above 0.25 remains true.

### precision.equity_total_exact_sum [PASS]
Scope: `decimal_precision`; duration `1196.495 ms`; exit `0`.
Input: `/tmp/a01-model-070-audit-inputs/equity_total_precision.json`; SHA-256 `248e685e7103842377461aac07dae41eff21f7cee593959d0af461713415c021`.
Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/scripts/domain_dsl.py evaluate '/home/lsnn/github/hovo-ecp-semantic/A01受益所有人/04领域模型输出/model.yaml' --rule M.Rule.EquityTotal --inputs /tmp/a01-model-070-audit-inputs/equity_total_precision.json`
Expected: `{"status":"KNOWN","value":"0.12345678901234567900"}`
Actual: `{
  "status": "KNOWN",
  "value": "0.12345678901234567900"
}`
Note: Exact sum retains all supplied Decimal digits and scale.

## Auxiliary qiaomu checks

- `qiaomu.validate_skill_on_domain_model`: exit `1`, counted=`False`. Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/semantic-foundry/scripts/validate_skill.py /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model`. Result: INAPPLICABLE_PACKAGE_VALIDATOR. semantic-foundry validator expects semantic-foundry package assets; domain-model lacks those required paths. No model behavior claim.
- `qiaomu.trigger_eval_on_domain_model`: exit `1`, counted=`False`. Command: `/home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/.venv/bin/python /home/lsnn/github/hovo-ecp-semantic/.agents/skills/semantic-foundry/scripts/trigger_eval.py /home/lsnn/github/hovo-ecp-semantic --cases /home/lsnn/github/hovo-ecp-semantic/.agents/skills/domain-model/evals/trigger_cases.json`. Result: INAPPLICABLE_ROUTER_CONTRACT. semantic-foundry trigger evaluator requires frontmatter description concept 本体; domain-model frontmatter does not satisfy that semantic-foundry-specific contract. Existing domain-model trigger-eval.json is static prior evidence, not rerun pass.

## Coverage and limits

Requested boundaries exercised: `25%/24.99`, `multi-path`, `UNKNOWN/cycle`, `continuous/interrupted formation dates`, `state-owned four-gate simplification`, `year-month/date and 30-day update`, `actual correction/recheck vs promise`, `correction feedback/request states`, `constraint blocking`, `Decimal precision`, `unrelated order sample`.

Evidence limits:
- 86 business cases were not all dynamically executed; explanations remain separate from execution evidence.
- No browser/UI/manual UI testing.
- No ECP import/publish/runtime or legal/business confirmation.
- No source schema/database/production path.
- Existing dsl-preview facts were not used as current DSL2 runtime inputs because their shape is legacy and incompatible.
- semantic-foundry qiaomu validators were inspected but not counted because they validate a different package contract, not domain-model behavior.
- This auditor did not modify implementation, tests, fixtures, configuration, documentation, Git, or production.
- The temporary JSON inputs and this report are under /tmp as authorized.
- No full 86-case replay is claimed; CLI coverage is targeted boundary coverage.

Safest next step: Keep this model/output byte pair fixed, then perform full 86-case replay with current DSL2-compatible input facts and obtain independent business review/confirmation.

This report proves targeted local CLI behavior only. It does not prove legal correctness, business confirmation, ECP publication, database mapping, production health, or UI behavior.
