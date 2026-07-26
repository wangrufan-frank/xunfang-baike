# 巡防百科

巡防百科是一个完全公开的静态知识网站，使用 HTML、CSS、原生 JavaScript 和 JSON 数据构建。网站发布到 GitHub Pages，并通过 `CNAME` 绑定自定义域名；`.nojekyll` 用于避免 GitHub Pages 的 Jekyll 处理影响静态资源。

## 项目定位

当前仓库唯一维护的运行产品是静态网站。原微信小程序及其转换脚本已经退役，历史版本仍可通过 Git 提交记录恢复。

网站保留登录页和浏览器 Cookie 门禁以维持既有使用体验，但它只是访问提示和便利门槛，不是服务端访问控制。网站内容按公开资料管理，不应把这层前端门禁用于保护敏感信息。

## 目录结构

- `index.html`、`css/`、`js/`：网站入口、样式和交互。
- `jingqing/`、`qinwu/`、`fagui/`、`zhuangbei/`、`zoufang/`、`xunlian/`：六个内容模块。
- `data/`：内容库存、法规、来源索引和少量汇报源数据。
- `tools/`：搜索、法规、来源和站内链接维护工具。
- `tests/`：网站结构、内容、认证和维护工具测试。
- `docs/`：内容维护、归档、设计和实施记录。

## 环境要求

- Python 3.12
- Node.js 20

安装用于 Word 讲解稿生成和测试的 Python 依赖：

```powershell
python -m pip install -r requirements.txt
```

## 本地预览

在仓库根目录运行：

```powershell
python -m http.server 8000
```

然后访问 `http://localhost:8000/`。不要直接双击 HTML 文件预览，因为搜索索引和浏览器安全策略依赖 HTTP 服务。

## 完整验证

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
node --test tests/auth_core.test.js
python tools/build_search_index.py --check
python tools/check_site_links.py
python tools/public_source_index.py check
```

第一条命令会执行所有 Python 测试；其中两个面向未来学习页功能的测试可能显示为跳过。其余命令分别验证认证工具、搜索索引、站内链接和公开来源台账。

## 内容维护

新增或修改文章时，同一次变更中维护 `data/content-inventory.json` 与 `data/public-sources.json`，然后运行：

```powershell
python tools/public_source_index.py check
python tools/public_source_index.py write --check
python tools/build_search_index.py --check
python tools/check_site_links.py
```

更详细的来源和索引操作说明见 [docs/public-source-maintenance.md](docs/public-source-maintenance.md)。来源台账用于内容可追溯性；本公开网站不将业务或保密审查状态作为仓库发布门槛。

## 部署

将经验证的 `master` 推送到 GitHub 后，GitHub Pages 会发布静态文件。部署配置的关键文件是根目录 `CNAME` 和 `.nojekyll`。GitHub Actions 会在推送和拉取请求时运行相同的核心验证，不会上传交付物。

## 外部交付物

演示视频、音频、PPT、DOCX、截图和视频制作工程已迁至：

```text
E:\xunfang-baike-deliverables
```

该目录不属于代码仓库；其 SHA-256 清单副本在 [docs/deliverables-archive-manifest.tsv](docs/deliverables-archive-manifest.tsv)。恢复、校验和重新生成汇报文件的规则见 [docs/deliverables-archive.md](docs/deliverables-archive.md)。

## 已退役的小程序

`miniprogram/` 与旧的 `parse_html.py` 已从当前运行树移除。若需研究旧实现，请从小程序退役前的 Git 提交恢复，不要重新把它作为网站运行依赖。
