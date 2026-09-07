# 开发期验证记录

这些记录保留“先复现失败、再修复验证”的证据。`red.log` 是针对旧版运行20项新增测试，17项预期失败；其余3项原有边界已正确。`green1.log` 对相同20项测试再次执行全部通过。

`design-red.log` 与 `design-green.log` 记录设计契约和样例入口的验证；`profile-red.log` 与 `profile-green.log` 记录平台允许重复约束参数、匿名列表节点和资源参数检查的整改。它们是开发历史，不表示当前交付仍有这些失败。

当前状态以父目录 `verification.json`、`unit-tests.json` 为准。开发日志不构成独立模型生成、平台编译或业务专家验证。额外标准约束依赖未安装，失败记录见 `optional-dependency.log`。
