# ecp-semantic-release

把已确认的 ECP V3 技术语义模型闭包提交到目标 Workspace，创建不可变 Revision，执行原生 Candidate Compile，并按授权发布和核验。Hovo 0.3.0，合同 2.0.0。

输入不再包含独立 Mapping 成果；Ontology、SHACL、Mapping、Derivation、Evaluation、Lifecycle 和 Action Policy 已经共同属于 ecp-semantic-authoring 2.0.0 的一个闭包。

本技能不再生成旧 ZIP Package，也不使用 ECP Kit 1.7 旧导入路径。

本地合同检查：

```bash
python3 scripts/validate_contract.py --check-schemas
python3 scripts/validate_contract.py validate input /path/to/project/ecp-semantic-release/input.json --project-root /path/to/project
python3 scripts/validate_contract.py validate output /path/to/project/ecp-semantic-release/output.json --project-root /path/to/project
```

真实 COMPILE、PUBLISH 和 VERIFY_RUN 必须由任务环境提供目标平台访问能力与明确授权。
