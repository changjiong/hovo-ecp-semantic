# 四阶段交付合同

项目根目录按实际推进创建：

```text
domain-knowledge/
domain-model/
ecp-semantic-authoring/
ecp-semantic-release/
pipeline.json
```

不再创建 ecp-data-mapping 目录。

## 正式产物

- domain-knowledge：input.json、output.json、review.md、coverage.md 及知识结构化产物；
- domain-model：input.json、output.json、model.yaml、review.md、coverage；
- ecp-semantic-authoring：input.json、output.json、review.md，以及 Ontology、SHACL、V3 Mapping、Derivation、Evaluation、Lifecycle、Action Policy；
- ecp-semantic-release：input.json、output.json、review.md，以及真实 Revision、编译、Release、回读和 Run 回执引用。

中间文件留在各阶段 process/；历史版本进入各阶段 archive/。不建立旧路径兼容层。

## 交接

domain-model 的业务模型确认后，authoring 才可把平台与物理数据上下文引入。authoring 的语义实现确认和数据绑定确认都绑定同一精确 output.json；两份均有效后才允许 release。

release 不重新生成或修改技术语义资产。目标环境编译拒绝返回 authoring；release 只记录平台事实。

## 校验

各阶段由自己的 scripts/validate_contract.py 验证。semantic-foundry 的 scripts/validate_pipeline.py 只是四阶段可选总检查，不是单技能依赖。

结构校验不能替代责任人确认、V3 原生候选编译、发布、运行或业务验收。
