# Archived Version v1 — Plan — 断言 manifest 的 `$schema` 声明
> Task: 2026-10-29-schema-check
> Version: v1
> Status: superseded
> Archived: 2026-10-29 20:47 +0800
> Superseded by: v2
> Archive mode: file

## Change Summary

v1 的 R1 与 A1 自相矛盾：R1 要求断言不联网，A1 要求它「点名两个 404」。离线的断言无法知道某个 URL 是否 404 —— 这不是实现没做到，是验收标准本身写不成立。

实现到 Step 1 时测出来：按 R1 实现的检查在当前仓库返回 `STATUS: pass` 退出 0，而 A1 要求的是退出 2。两者不可能同时满足。

v2 删掉 A1 里「点名 404」那半，A1 改为只断言声明本身的合法性（非空、绝对 HTTPS、无重复键、pin 不变）。两个 404 移入 Follow-ups，由人处理，不在 CI 里检测。R1 不变。


## Archived Materials
- prd.md

## Restore
Read the archived v1 core docs from a new temporary restore root. Do not overwrite the current task root.
