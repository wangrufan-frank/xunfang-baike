# 巡防百科访问认证设计

## 目标

为静态巡防百科建立真正的访问前置条件。未认证用户不能直接获取网站页面或静态资源；现场演示人员使用一个通用账号密码登录。

## 架构

```text
学习者 → Cloudflare Access → www.xunfangbk.cn（GitHub Pages，后续可迁阿里云）
                         └→ Authentik（阿里云 ECS，auth.xunfangbk.cn）
```

Cloudflare Access 在边缘验证会话，未登录请求被拦截。Authentik 维护通用账号密码并作为 OIDC 身份提供方。网站不保存或校验账号密码。

## DNS 与托管

- 域名注册继续保留在阿里云；DNS 托管迁入 Cloudflare，可随时迁回阿里云 DNS。
- `www.xunfangbk.cn` 保持指向当前 GitHub Pages 源站，并由 Cloudflare 代理。
- 新增 `auth.xunfangbk.cn`，由 Cloudflare 代理至阿里云 ECS 上的 Authentik。
- 切换前导入并核对全部现有 DNS 记录；当前无企业邮箱或其他子域名服务。

## 认证与账号

- 部署 Authentik，创建唯一通用演示账号 `xunfang-demo`。
- 密码只在 Authentik 管理后台创建、重置和轮换，不出现在仓库、网站代码、部署文件或聊天记录中。
- Cloudflare Access 为 `www.xunfangbk.cn` 创建 Self-hosted Application，并只允许 Authentik 登录方式。
- 演示结束后应立即轮换通用账号密码；该模式不提供个人操作审计。

## 服务器部署

- 目标环境：Alibaba Cloud Linux 3.2104 U12（OpenAnolis）ECS。
- 安装 Docker Engine 与 Docker Compose；使用 Compose 部署 Authentik、PostgreSQL、Redis 和持久化卷。
- 对外只暴露 HTTPS 所需入口；管理与源站访问通过 Cloudflare 代理控制。
- 创建管理员恢复路径、持久卷备份和部署文档；不记录任何敏感值。

## 验收

- 无痕窗口直接访问首页、栏目页、文章页和静态资源均被 Cloudflare Access 拦截。
- 使用 `xunfang-demo` 登录后，网站、搜索和主题切换正常可用。
- 登出或会话过期后再次访问会被重新要求认证。
- DNS 解析、GitHub Pages 源站和 `auth.xunfangbk.cn` 的 HTTPS 证书正常。
- 所有凭据仅保存在 Cloudflare/Authentik/ECS 的受控环境中，Git 工作区无敏感文件。
