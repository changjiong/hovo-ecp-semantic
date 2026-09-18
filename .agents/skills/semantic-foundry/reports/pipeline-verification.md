# 五技能本地验证记录

日期：2026-09-09。semantic-foundry 0.5.0 与五个0.1.0生产技能。本轮没有运行旧测试套件，没有新增或修改测试代码，没有 ECP 操作。

## 已执行范围

verification_auditor 使用 gpt-5.6-luna / max 独立审阅，父运行时权限下只读为指令约束。使用既有隔离 Python `/tmp/semantic-foundry-040.irn1r4/venv/bin/python`，设置 `PYTHONDONTWRITEBYTECODE=1`。

| 检查 | 实际结果 |
| --- | --- |
| `scripts/validate_pipeline.py --check-schemas` | exit 0；12份 Schema 元结构及全部 `$ref` 离线解析通过：共享合同1份、编排合同1份、五阶段输入/输出10份 |
| 六个入口身份与版本 | 0 mismatch；五技能0.1.0、编排0.5.0；恰好6个根入口，没有嵌套入口 |
| 新增/修改 Markdown 链接 | 审阅时27份文档、73个本地链接，0缺失、0越出六技能集合 |
| Python AST 与 JSON 语法 | 审阅时271份 Python、80份 JSON；AST、JSON解析及重复键检查无错误 |
| 首次 qiaomu 包检查 | 编排通过；五技能因缺 adapter_targets 失败，之后已补齐并复核 |
| 首次来源包检查 | 03手册摘要不一致；已审阅既有提交差异并明确更新清单，原文未改 |
| 修复后的六个 qiaomu 包检查 | 根代理执行同一静态入口；全部 exit 0 / ok=true / 0 failures |
| 修复后的 `scripts/validate_skill.py .` | 根代理执行；exit 0 / PASS / 0 warnings，24份权威文件摘要核对通过 |
| `git diff --check` | exit 0 |

修复后的原始结构化工具输出、命令和相关文件摘要见 [pipeline-static-checks.json](pipeline-static-checks.json)。这是静态检查，不是回归测试或独立专家批准。Schema 的 meta 校验通过不代表交接文件所有正反例都已执行；本轮尚未用实际业务输入执行 stage input/output。

## 提示与未验证项

qiaomu 静态检查仍给出编排6条、新技能各5条提示。README 已写本地同级安装、自然示例及边界；检查器使用固定短语和 npx 命令启发式，当前没有远程安装声明，因此不为消除提示而编造安装证据。新技能没有触发评估用例，保留为 scaffold candidate，未声称 Production/Governed 门禁完成。

五技能真实模型触发/生成、输入上下文隔离、专家确认、干净安装、当前数据源发现、ECP 导入/编译/发布/Run 与业务验收均为 NOT_EXECUTED。交接确认检查能验证结构、绑定及摘要，不能认证责任人身份或业务结论。

参考资料初始摘要漂移的具体差异与处理见 [建设记录](pipeline-creation.md)。0.4.0报告只证明历史范围，不转作五技能流程证据。
