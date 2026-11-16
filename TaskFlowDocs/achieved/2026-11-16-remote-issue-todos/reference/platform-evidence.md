# 平台接口证据

- GitHub REST Issues：`https://docs.github.com/en/rest/issues/issues`。Issue 端点返回项可能含 Pull Request，应检查 `pull_request`；按仓库和 issue number 定位，写操作需相应权限。
- GitHub REST 最佳实践：`https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api`。除具体端点另有说明外，POST、PUT、PATCH、DELETE 的条件请求不受支持。不能把读 ETag 后写入当作原子条件更新；重读只能减少窗口。
- GitHub CLI：`https://cli.github.com/manual/gh_api`。`gh api` 支持 `--hostname`、`--paginate`、`--slurp` 和从 stdin 输入请求体。需对自托管实例及实际安装版本验证。
- GitLab Issues：`https://docs.gitlab.com/api/issues/`。项目地址是项目 ID 或 URL 编码路径，issue 使用项目内 IID；更新支持 `add_labels`、`remove_labels` 和 `state_event`。`add_labels` 中不存在的标签可能被自动创建，须纳入权限与副作用设计；私有项目无权访问也可能返回 404。
- GitLab CLI：`https://docs.gitlab.com/cli/api/`。`glab api` 支持 `--hostname`、`--paginate`、从 stdin 输入 JSON；其文档声明 429 错误需按响应提示重试，不能将所有失败混为未写入。
- 本机可发现 `gh` 2.100.0，未发现 `glab`；不据此推断用户其他主机的安装或授权状态。

## 未验证
- GitLab 指定 Issue 写接口的条件更新能力尚无可确认的官方依据；不能宣称支持原子并发保护。
- 两平台真实私有、自托管实例及故障注入尚未运行；本证据只来自文档和本机只读命令。
## 真实 GitHub 只读验证
- 2026-11-16：使用项目内隔离配置执行实际 `remote-todo list-remote`，退出码 0，返回 1 条 Issue。单独对公开 API 按类型计数为 1 条 Issue、141 条 Pull Request，过滤结果与 Issue 数一致；未记录 Issue 内容。没有执行真实远端写入。

- 复核 GitLab CLI 官方文档：`--paginate --output ndjson` 每个对象一行，`--field description=@-` 从标准输入读取内容；本机无 `glab`，仍未进行真实客户端验证。
