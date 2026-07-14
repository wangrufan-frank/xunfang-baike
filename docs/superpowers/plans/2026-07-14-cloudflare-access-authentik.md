# Cloudflare Access 与 Authentik 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement task-by-task.

**Goal:** 以 Cloudflare Access 和 Authentik 为巡防百科提供不可绕过的账号密码访问控制。

**Architecture:** Cloudflare 代理域名并在边缘执行 Access 策略；阿里云 ECS 的 Authentik 通过 OIDC 验证通用账号；网站保持静态源站，后续迁移不影响认证策略。

**Tech Stack:** Cloudflare DNS/Zero Trust Access、Alibaba Cloud Linux 3、Docker Compose、Authentik、PostgreSQL、Redis、GitHub Pages。

## Global Constraints

- 不在 Git、网站文件、聊天或日志中保存账号密码、API Token、私钥或数据库密码。
- 未登录用户必须无法取得 HTML、CSS、JS、图片、视频与搜索索引。
- 仅允许通用账号 `xunfang-demo`；演示结束后轮换密码。
- 保留可迁回阿里云 DNS 的记录清单。

### Task 1: 建立 Cloudflare DNS 与 Access 边界

**Authority:** 用户需登录阿里云域名控制台与 Cloudflare 控制台；涉及修改域名服务器和 DNS 记录，执行前再次确认。

- [ ] 在 Cloudflare 添加 `xunfangbk.cn` 站点，导入现有记录并核对 `www` 的 GitHub Pages CNAME、根域记录与 CNAME 文件一致。
- [ ] 在阿里云域名控制台将域名服务器改为 Cloudflare 提供的两条名称服务器。
- [ ] 等待 Cloudflare 显示 zone 为 Active；用 `nslookup -type=NS xunfangbk.cn` 与浏览器检查 `www.xunfangbk.cn` 仍可访问。
- [ ] 在 Cloudflare Zero Trust 创建组织；添加 Generic OIDC 身份提供方的占位配置，回调 URL 使用 `https://<team>.cloudflareaccess.com/cdn-cgi/access/callback`。
- [ ] 创建 Self-hosted Application：域名 `www.xunfangbk.cn`、路径 `/*`；先不启用 Allow 策略，避免 Authentik 未就绪时锁死网站。

### Task 2: 在 ECS 部署 Authentik

**Authority:** 用户需提供 SSH 登录方式或在服务器终端执行命令；密码与密钥由用户在服务器本地生成和保存。

- [ ] 安装 Docker Engine 与 Docker Compose plugin，运行 `docker --version` 和 `docker compose version` 验证。
- [ ] 在 `/opt/authentik` 创建仅 root 可读的 `.env`，由服务器本地生成 `AUTHENTIK_SECRET_KEY`、PostgreSQL 密码和 Redis 密码；权限设为 `600`。
- [ ] 使用 Authentik 官方 Compose 模板部署 PostgreSQL、Redis、server 与 worker，数据卷挂载到 `/opt/authentik`。
- [ ] 将 `auth.xunfangbk.cn` DNS 记录指向 ECS，并通过反向代理与 Let’s Encrypt 或 Cloudflare Origin Certificate 提供 HTTPS。
- [ ] 访问 `https://auth.xunfangbk.cn/if/flow/initial-setup/` 完成管理员初始化；管理员凭据只保存在密码管理器。
- [ ] 在 Authentik 创建 OAuth2/OIDC Provider 与 Application，redirect URI 使用 Task 1 的 Cloudflare callback URL；复制 client ID、client secret、issuer/JWKS URL 到 Cloudflare OIDC 配置。

### Task 3: 启用策略、通用账号与验证

**Authority:** 用户需在 Authentik/Cloudflare 控制台创建并保管密码；我可协助逐项核对配置。

- [ ] 在 Authentik 创建用户 `xunfang-demo`，设置强密码和“演示人员”组；不在任何仓库文件写入密码。
- [ ] 在 Cloudflare Access 的 `www.xunfangbk.cn/*` Application 添加 Allow 策略：Include 使用 Authentik 登录方法；设置合理会话时长并启用登录页。
- [ ] 使用无痕窗口访问首页、栏目页、文章页、`css/style.css`、`js/nav.js`、`search-index.json`；每一项在登录前均必须显示 Access 登录而非返回源文件。
- [ ] 使用 `xunfang-demo` 完成登录，验证首页、搜索、主题切换、栏目页和文章页均可用。
- [ ] 访问 `https://www.xunfangbk.cn/cdn-cgi/access/logout`，确认登出后再次访问受保护资源会重新拦截。

### Task 4: 备份、交接与回滚

- [ ] 记录 Cloudflare DNS 记录清单、ECS 目录 `/opt/authentik`、容器名称、备份命令、Access Application ID 与管理员恢复流程；不记录任何 secret 值。
- [ ] 创建 PostgreSQL 逻辑备份并验证能列出 Authentik 数据库；将加密备份存入受控位置。
- [ ] 记录回滚步骤：先在阿里云 DNS 恢复相同记录，再将域名服务器切回阿里云；确认网站解析后停止或保留 Authentik。
- [ ] 演示结束后在 Authentik 重置 `xunfang-demo` 密码并确认旧会话已失效。
