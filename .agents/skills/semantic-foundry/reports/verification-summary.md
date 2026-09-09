# 0.4.0 验证记录

日期：2026-09-09。结论：`partial`。技能结构、现有关键词路由、设计样例和标准 SHACL 检查通过；既有工具回归仍有一个旧路径用例错误，因此总验证状态保持 `FAILED`。

| 检查 | 实际结果 | 证据 |
| --- | --- | --- |
| 本技能包检查 | PASS；身份、必需文件、自编文档链接、四册 V2.1 与 Kit 原文摘要 | [package-check.log](verification-0.4.0-isolated/package-check.log) |
| qiaomu 包检查 | PASS，0 failures；有启发式提示，不证明安装完成 | 独立验证执行元技能 `scripts/validate_skill.py .`，结果见本次交接；没有将该命令输出另存为原始日志 |
| 既有关键词边界 | 16/16 PASS；模型调用未执行 | [trigger-eval.json](trigger-eval.json) |
| 既有工具回归 | 50项：49 PASS、0断言失败、1 ERROR、0跳过 | [unit-tests.json](verification-0.4.0-isolated/unit-tests.json)、[日志](verification-0.4.0-isolated/unit-tests.log) |
| 设计契约样例 | PASS | [design-contract.json](verification-0.4.0-isolated/design-contract.json) |
| 所有权合成切片 | PASS，10项检查 | [ownership-slice/verification.json](verification-0.4.0-isolated/ownership-slice/verification.json) |
| 手册参考工程 | 41/41 PASS | [handbook-reference/verification.json](verification-0.4.0-isolated/handbook-reference/verification.json) |
| 标准 SHACL | PASS，数据符合且目标集合与预期一致 | [standard-shacl.json](verification-0.4.0-isolated/standard-shacl.json) |

既有工具回归的唯一错误是 `tests/test_delivery_safety.py:48` 仍访问已删除的 `references/handbooks-v2/01-methodology.md`。该错误在写入测试副本前触发 `FileNotFoundError`，未检验当前 V2.1 的内容变更检测行为。没有添加旧路径兼容副本，没有修改/跳过该用例来获得全绿。测试代码修订授权尚未收到，新增引用、Scope 和包限制行为也没有新增针对性用例。

第一次使用系统 Python 3.12.3，缺少 rdflib，收集与样例执行失败，原始记录保存在 [首次验证](verification-0.4.0/verification.json)。随后按已有 `requirements-tested.txt` 与 `requirements-shacl.txt` 在隔离环境安装依赖，由 verification_auditor 重新执行既有入口，结果保存为[隔离环境完整报告](verification-0.4.0-isolated/verification.json)。未更改系统 Python 或项目依赖清单。

复核环境为 Python 3.12.3、rdflib 7.5.0、jsonschema 4.26.0、PyYAML 6.0.3、pyshacl 0.31.0；完整依赖和实际命令见报告。工具测试记录了579条 PyparsingDeprecationWarning，未因此跳过检查。报告中的输入指纹绑定当时的脚本和测试；本文只是结果索引，不能替代原始证据。

独立验证角色对实现、测试与配置只读；父运行时为 danger-full-access，因此只读由指令约束，不宣称运行时强制隔离。验证只写授权报告。

本轮未执行真实模型生成对照、业务用户确认、目标 ECP 导入识别、编译、Published Release、数据 Run、干净宿主安装或公开发布。参考工程和关键词结果不能替代这些证据。
