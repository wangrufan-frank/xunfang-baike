# 巡防百科三级内容体系重建 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将巡防百科一次性改造成六个一级模块、20个二级分类、87篇三级文章的完整静态网站，并同步完成密码、图片、交叉引用、搜索和旧内容清理。

**Architecture:** 保留现有纯静态 HTML/CSS/JS 架构，六个模块继续使用原目录；`data/content-inventory.json` 作为构建与验收清单，页面仍为独立静态 HTML。新增只处理网站的搜索索引构建器和断链检查器，不运行会修改微信小程序的 `parse_html.py`。

**Tech Stack:** HTML5、CSS3、原生浏览器 JavaScript、Python 3 标准库、Node.js 内置测试运行器、Python `unittest`。

**Spec:** `docs/superpowers/specs/2026-07-17-site-content-rebuild-design.md`

## Global Constraints

- 三级结构固定为“一级主模块 → 二级分类 → 三级文章”，不建立第四级目录。
- 六个网站目录固定为 `zhuangbei/`、`qinwu/`、`xunlian/`、`jingqing/`、`fagui/`、`zoufang/`。
- 三级文章总数必须为87：26、13、13、5、17、13。
- 装备介绍中不单列伸缩警棍、催泪喷射器和手铐；三者合并到“九小件概览”。
- 通用用户名保持 `xunfang`，密码改为 `XFbk150225`，配置摘要为 `9329591fc43f75b2fb1a0aec5977e1ce20658b79ddb6a2e1d623af25af8593e7`。
- 不修改 `miniprogram/`，不得运行或修改 `parse_html.py`。
- 内容优先读取 `F:\frank第二大脑\frank知识库`，缺失部分使用政府和权威公开来源补齐。
- 允许使用知识库图片、政府公开图片、开放许可素材、自绘示意图和展示部署、装备配置或处置站位的现场照片。
- 外部图片必须本地化，明显无关的身份证号、电话号码等个人信息应处理；不执行专项保密筛查。
- 不保留“内容整改中”“待补充”、开发占位标记或空白文章页。
- 不在仓库中安装新依赖；Python工具只使用标准库。
- 保留用户已有未提交文件，不把无关 PPT 或其他工作区内容纳入提交。

---

## File Responsibility Map

| 文件或目录 | 责任 |
|---|---|
| `data/content-inventory.json` | 87篇文章、分类、来源、图片和交叉引用的唯一验收清单 |
| `data/legacy-url-map.json` | 旧URL到新URL的迁移、跳转或删除记录 |
| `tools/build_search_index.py` | 从静态HTML稳定生成并检查 `search-index.json` |
| `tools/check_site_links.py` | 检查HTML、锚点、图片、脚本和样式的本地链接 |
| `tests/test_site_structure.py` | 校验三级结构、页面合同、图片、搜索、旧内容清理 |
| `tests/auth_core.test.js` | 校验新密码摘要和Cookie行为 |
| `index.html` | 六个一级模块入口 |
| `js/nav.js` | 全站导航和模块名称 |
| `js/search.js` | 搜索加载、模块显示和结果链接 |
| `css/style.css` | 三级文章、来源、相关文章、图集和移动端样式 |
| 六个模块 `index.html` | 二级分类和三级文章入口 |
| 六个模块内 `*.html` | 87篇三级文章正文 |
| `img/<module>/<slug>/` | 本地化文章图片 |

### Static Article Contract

所有三级文章使用以下可机器检查的结构。实际标题、分类、摘要和章节正文取自内容清单与资料源，不保留模板变量：

```html
<div class="breadcrumb">
  <a href="../index.html">首页</a> &gt;
  <a href="index.html">一级模块</a> &gt;
  <a href="index.html#category-anchor">二级分类</a> &gt;
  <span class="current">三级文章</span>
</div>
<main class="page-container article-page" data-module="module-slug" data-category="二级分类">
  <header class="page-title">
    <h1>三级文章</h1>
    <p class="article-summary">完整摘要。</p>
  </header>
  <article class="article-content">
    <section class="content-section"><h2>文章模板要求的章节</h2><p>实质正文。</p></section>
  </article>
  <section class="source-list" aria-labelledby="source-title">
    <h2 id="source-title">资料来源</h2>
    <ul><li><a href="官方或本地说明">来源标题</a></li></ul>
  </section>
  <nav class="related-links" aria-label="相关内容"></nav>
  <nav class="page-nav" aria-label="文章导航"></nav>
</main>
```

---

### Task 1: 建立内容库存与结构测试基线

**Files:**
- Create: `data/content-inventory.json`
- Create: `data/legacy-url-map.json`
- Create: `tests/test_site_structure.py`
- Reference: `docs/superpowers/specs/2026-07-17-site-content-rebuild-design.md`

**Interfaces:**
- Produces: `content-inventory.json` 顶层 `{version, updated_at, modules}`；每篇文章包含 `module`、`module_title`、`category`、`category_anchor`、`title`、`slug`、`path`、`source_files`、`public_sources`、`images`、`related_pages`。
- Produces: `legacy-url-map.json` 顶层 `{version, mappings}`；每项包含 `old_path`、`new_path`、`action`，其中 `action` 只能是 `keep`、`redirect`、`remove`。
- Produces: 后续任务复用的 `load_inventory()`、`article_records()`、`assert_article_contract()` 测试辅助函数。

- [ ] **Step 1: 写内容库存失败测试**

在 `tests/test_site_structure.py` 写入：

```python
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "data" / "content-inventory.json"
EXPECTED_COUNTS = {
    "zhuangbei": 26,
    "qinwu": 13,
    "xunlian": 13,
    "jingqing": 5,
    "fagui": 17,
    "zoufang": 13,
}


def load_inventory():
    return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))


def article_records(module=None):
    records = [
        article
        for group in load_inventory()["modules"]
        for article in group["articles"]
    ]
    return [record for record in records if record["module"] == module] if module else records


def assert_article_contract(testcase, record):
    path = ROOT / record["path"]
    testcase.assertTrue(path.is_file(), record["path"])
    html = path.read_text(encoding="utf-8")
    testcase.assertIn(f'data-module="{record["module"]}"', html)
    testcase.assertIn(f'data-category="{record["category"]}"', html)
    testcase.assertIn(record["title"], html)
    testcase.assertIn("article-summary", html)
    testcase.assertIn("source-list", html)
    testcase.assertIn("related-links", html)
    testcase.assertIn("page-nav", html)


class ContentInventoryTests(unittest.TestCase):
    def test_inventory_has_exact_module_and_article_counts(self):
        inventory = load_inventory()
        counts = {
            module["slug"]: len(module["articles"])
            for module in inventory["modules"]
        }
        self.assertEqual(EXPECTED_COUNTS, counts)
        paths = [record["path"] for record in article_records()]
        self.assertEqual(87, len(paths))
        self.assertEqual(87, len(set(paths)))

    def test_inventory_records_have_required_fields(self):
        required = {
            "module", "module_title", "category", "category_anchor",
            "title", "slug", "path", "source_files", "public_sources",
            "images", "related_pages",
        }
        for record in article_records():
            self.assertEqual(set(), required.difference(record), record["path"])
            self.assertRegex(record["path"], r"^[a-z0-9-]+/[a-z0-9-]+\.html$")
            self.assertTrue(
                record["source_files"] or record["public_sources"],
                record["path"],
            )
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.ContentInventoryTests -v`
Expected: FAIL，原因是 `data/content-inventory.json` 不存在。

- [ ] **Step 3: 创建完整内容库存**

按照设计规范第2节逐项录入全部87篇文章。顶层结构固定为：

```json
{
  "version": 1,
  "updated_at": "2026-07-17",
  "modules": [
    {
      "slug": "zhuangbei",
      "title": "装备介绍",
      "categories": ["人身装备", "车载装备", "战术装备"],
      "articles": []
    },
    {
      "slug": "qinwu",
      "title": "勤务保障",
      "categories": ["大型活动安保", "公共秩序事件", "支点联防", "专项活动保障"],
      "articles": []
    },
    {
      "slug": "xunlian",
      "title": "警务训练",
      "categories": ["单兵技能训练", "小组协同训练"],
      "articles": []
    },
    {
      "slug": "jingqing",
      "title": "警情处置",
      "categories": ["醉酒类警情", "持刀类警情", "自伤类警情", "精神障碍类警情", "涉爆类警情"],
      "articles": []
    },
    {
      "slug": "fagui",
      "title": "执法规范",
      "categories": ["现场规范用语", "执法程序与法条应用", "法律法规库"],
      "articles": []
    },
    {
      "slug": "zoufang",
      "title": "教育培训",
      "categories": ["规章制度", "考核规范", "学习课程"],
      "articles": []
    }
  ]
}
```

将设计规范中的87个精确路径逐项写入 `articles`。每条 `source_files` 使用知识库绝对路径；`public_sources` 使用URL；未配置图片时 `images` 为 `[]`，不得省略字段。

- [ ] **Step 4: 创建旧URL映射**

先盘点现有模块HTML，再写入 `data/legacy-url-map.json`。必须至少覆盖：

```json
{
  "version": 1,
  "mappings": [
    {"old_path": "zhuangbei/shensuo-jinggun.html", "new_path": "zhuangbei/jiuxiaojian-gailan.html", "action": "redirect"},
    {"old_path": "zhuangbei/cuilei-pensheqi.html", "new_path": "zhuangbei/jiuxiaojian-gailan.html", "action": "redirect"},
    {"old_path": "zhuangbei/shoukao.html", "new_path": "zhuangbei/jiuxiaojian-gailan.html", "action": "redirect"},
    {"old_path": "rumen/index.html", "new_path": "zoufang/index.html", "action": "remove"}
  ]
}
```

- [ ] **Step 5: 运行库存测试**

Run: `python -m unittest tests.test_site_structure.ContentInventoryTests -v`
Expected: PASS，显示2个测试通过，87个路径唯一。

- [ ] **Step 6: 提交**

```powershell
git add data/content-inventory.json data/legacy-url-map.json tests/test_site_structure.py
git commit -m "docs: add site content rebuild inventory"
```

---

### Task 2: 更新通用密码和认证测试

**Files:**
- Modify: `js/auth-config.js`
- Modify: `tests/auth_core.test.js`

**Interfaces:**
- Consumes: `XunfangAuth.digestCredentials(username, password)`。
- Produces: `XunfangAuthConfig.digest === '9329591fc43f75b2fb1a0aec5977e1ce20658b79ddb6a2e1d623af25af8593e7'`。

- [ ] **Step 1: 先更新认证测试**

在 `tests/auth_core.test.js` 增加：

```javascript
test('accepts the configured replacement password digest', async () => {
    assert.equal(
        await auth.digestCredentials('xunfang', 'XFbk150225'),
        config.digest
    );
    assert.notEqual(
        await auth.digestCredentials('xunfang', 'xunfang'),
        config.digest
    );
});
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `node --test tests/auth_core.test.js`
Expected: FAIL，新的凭据摘要与旧配置不一致。

- [ ] **Step 3: 更新配置摘要**

将 `js/auth-config.js` 改为：

```javascript
var XunfangAuthConfig = Object.freeze({
    username: 'xunfang',
    digest: '9329591fc43f75b2fb1a0aec5977e1ce20658b79ddb6a2e1d623af25af8593e7',
    cookieName: 'xunfang_auth',
    maxAgeSeconds: 86400
});

if (typeof module !== 'undefined' && module.exports) {
    module.exports = XunfangAuthConfig;
}
```

- [ ] **Step 4: 运行认证测试**

Run: `node --test tests/auth_core.test.js`
Expected: PASS，全部认证测试通过。

- [ ] **Step 5: 提交**

```powershell
git add js/auth-config.js tests/auth_core.test.js
git commit -m "feat: update site authentication password"
```

---

### Task 3: 建立六模块导航、首页和公共三级页面合同

**Files:**
- Modify: `index.html`
- Modify: `js/nav.js`
- Modify: `js/search.js`
- Modify: `css/style.css`
- Modify: `zhuangbei/index.html`
- Modify: `qinwu/index.html`
- Modify: `xunlian/index.html`
- Modify: `jingqing/index.html`
- Modify: `fagui/index.html`
- Modify: `zoufang/index.html`
- Modify: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: `content-inventory.json` 六模块名称、分类和计数。
- Produces: 每个模块索引的 `<section id="..." class="article-group">` 分类锚点。
- Produces: `.article-page`、`.article-summary`、`.source-list`、`.related-links`、`.article-gallery` 公共样式。

- [ ] **Step 1: 写导航和索引失败测试**

在 `tests/test_site_structure.py` 增加：

```python
class NavigationStructureTests(unittest.TestCase):
    def test_home_and_nav_use_exact_six_modules(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        nav = (ROOT / "js" / "nav.js").read_text(encoding="utf-8")
        for title in ["装备介绍", "勤务保障", "警务训练", "警情处置", "执法规范", "教育培训"]:
            self.assertIn(title, home)
            self.assertIn(title, nav)
        for old_title in ["巡防勤务", "法条规范", "走访送教", "入门指南"]:
            self.assertNotIn(old_title, home)
            self.assertNotIn(old_title, nav)

    def test_module_indexes_expose_exact_category_anchors(self):
        for module in load_inventory()["modules"]:
            html = (ROOT / module["slug"] / "index.html").read_text(encoding="utf-8")
            for article in module["articles"]:
                self.assertIn(f'id="{article["category_anchor"]}"', html)
                self.assertIn(article["path"].split("/")[-1], html)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.NavigationStructureTests -v`
Expected: FAIL，首页仍含旧名称且模块索引没有完整分类锚点。

- [ ] **Step 3: 更新导航配置**

按设计规范第5.4节把 `MODULES` 更新为六个主模块加“本月精选”。保留现有主题选择器、退出登录和深度判断逻辑，仅更新模块配置及 `js/search.js` 中的模块显示表。

- [ ] **Step 4: 更新首页六张卡片**

首页每张卡片的文章数固定为26、13、13、5、17、13，并显示设计规范确认的二级分类名称。删除入门指南卡片，不删除“本月精选”区域。

- [ ] **Step 5: 重写六个模块索引**

每个 `index.html` 必须从内容库存逐项列出文章。分类采用：

```html
<section id="personal-equipment" class="article-group">
  <h2 class="list-section-title">人身装备</h2>
  <a href="jiuxiaojian-gailan.html" class="list-item">
    <div class="item-title">九小件概览</div>
    <div class="item-desc">九小件组成、运用场景、基础使用和安全检查。</div>
  </a>
</section>
```

其他分类使用库存中的 `category_anchor`、文章文件名、标题和准确摘要，不保留空状态。

- [ ] **Step 6: 添加公共样式**

在 `css/style.css` 追加聚焦样式，复用现有颜色变量：

```css
.article-summary { max-width: 48rem; color: var(--text-secondary); line-height: 1.75; }
.article-group { scroll-margin-top: 6rem; }
.content-section + .content-section { margin-top: 2rem; }
.source-list, .related-links { margin-top: 2rem; padding: 1.25rem; border-radius: 14px; background: var(--card-bg); }
.article-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; }
.article-gallery img { width: 100%; height: auto; border-radius: 12px; }
@media (max-width: 640px) {
    .source-list, .related-links { padding: 1rem; }
}
```

若现有变量名不同，使用 `style.css` 已定义的等价变量，不新增重复颜色系统。

- [ ] **Step 7: 运行结构测试**

Run: `python -m unittest tests.test_site_structure.NavigationStructureTests -v`
Expected: PASS。

- [ ] **Step 8: 提交**

```powershell
git add index.html js/nav.js js/search.js css/style.css zhuangbei/index.html qinwu/index.html xunlian/index.html jingqing/index.html fagui/index.html zoufang/index.html tests/test_site_structure.py
git commit -m "feat: establish three-level site navigation"
```

---

### Task 4: 完成装备介绍26篇文章

**Files:**
- Create/Modify: 设计规范第2.1节列出的26个 `zhuangbei/*.html`
- Modify: `zhuangbei/index.html`
- Modify: `data/content-inventory.json`
- Modify: `data/legacy-url-map.json`
- Modify: `tests/test_site_structure.py`
- Create: `img/zhuangbei/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；装备文章章节合同。
- Produces: 26个可独立访问、可搜索的装备页面。

- [ ] **Step 1: 写装备模块失败测试**

```python
class EquipmentContentTests(unittest.TestCase):
    def test_all_equipment_pages_follow_article_contract(self):
        records = article_records("zhuangbei")
        self.assertEqual(26, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_three_nine-piece_items_are_not_inventory_articles(self):
        paths = {record["path"] for record in article_records("zhuangbei")}
        self.assertNotIn("zhuangbei/shensuo-jinggun.html", paths)
        self.assertNotIn("zhuangbei/cuilei-pensheqi.html", paths)
        self.assertNotIn("zhuangbei/shoukao.html", paths)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.EquipmentContentTests -v`
Expected: FAIL，新增装备页尚不存在或不符合合同。

- [ ] **Step 3: 读取装备资料并逐篇撰写**

优先读取：

- `F:\frank第二大脑\frank知识库\03_Knowledge\警务技能\单警装备\`
- `F:\frank第二大脑\frank知识库\03_Knowledge\警务技能\最小作战单元\`
- 知识库内文件名含车载装备、阻车、救生、灭火、围挡、盾牌、约束带和云台的资料。

每篇严格使用“装备简介、组成与用途、适用场景、基础使用、使用前后检查、安全注意事项、维护保管、相关法规与训练、图片”章节。

- [ ] **Step 4: 合并九小件内容**

`jiuxiaojian-gailan.html` 必须包含伸缩警棍、催泪喷射器和手铐的清楚分项，并吸收原三篇页面中仍准确的基础内容。将原三条旧路径记录为 `redirect`，跳转目标均为 `jiuxiaojian-gailan.html`，跳转页不加入库存和搜索。

- [ ] **Step 5: 配置图片和相关链接**

图片放入对应 `img/zhuangbei/<slug>/`。至少建立：装备到相关训练、装备到警械使用程序、九小件到三个训练文章的交叉链接。

- [ ] **Step 6: 运行装备测试**

Run: `python -m unittest tests.test_site_structure.EquipmentContentTests -v`
Expected: PASS。

- [ ] **Step 7: 提交**

```powershell
git add zhuangbei img/zhuangbei data/content-inventory.json data/legacy-url-map.json tests/test_site_structure.py
git commit -m "feat: rebuild equipment content"
```

---

### Task 5: 完成勤务保障13篇文章

**Files:**
- Create/Modify: 设计规范第2.2节列出的13个 `qinwu/*.html`
- Modify: `qinwu/index.html`
- Modify: `data/content-inventory.json`
- Modify: `data/legacy-url-map.json`
- Modify: `tests/test_site_structure.py`
- Create: `img/qinwu/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；勤务文章章节合同。
- Produces: 13个勤务保障页面；旧“巡防勤务”显示名称被替换。

- [ ] **Step 1: 写勤务模块失败测试**

```python
class DutyContentTests(unittest.TestCase):
    def test_all_duty_pages_follow_article_contract(self):
        records = article_records("qinwu")
        self.assertEqual(13, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_duty_runtime_uses_new_labels(self):
        for path in (ROOT / "qinwu").glob("*.html"):
            html = path.read_text(encoding="utf-8")
            self.assertNotIn("巡防勤务", html)
            self.assertNotIn("群体性事件", html)
            self.assertNotIn("警卫任务", html)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.DutyContentTests -v`
Expected: FAIL。

- [ ] **Step 3: 读取勤务资料并逐篇撰写**

优先读取：

- `F:\frank第二大脑\frank知识库\03_Knowledge\警务技能\大型活动与专项安保.md`
- `F:\frank第二大脑\frank知识库\03_Knowledge\警务技能\巡防管理与勤务.md`
- `F:\frank第二大脑\frank知识库\03_Knowledge\警务技能\群体事件处置与舆情.md`
- 知识库内与苏超、演唱会、支点走访和联合巡逻相关资料。
- 《大型群众性活动安全管理条例》官方文本。

每篇使用“适用范围、法律和职责边界、勤务前检查、主要风险、现场服务与秩序维护、部门协同、群众沟通、突发情况报告、复盘要点”章节。

- [ ] **Step 4: 应用名称和内容边界**

页面统一使用“勤务保障”“公共秩序事件”“专项活动保障”。公共秩序事件页面只写公开原则、权利保障、沟通记录和注意事项，不写内部警力数量、路线、通信方式或非公开预案。

- [ ] **Step 5: 配置图片和交叉引用**

足球、演出和支点文章链接到相关装备、现场规范用语和大型活动法规；专项活动文章链接到现场秩序、记录和报告规范。

- [ ] **Step 6: 运行勤务测试并提交**

Run: `python -m unittest tests.test_site_structure.DutyContentTests -v`
Expected: PASS。

```powershell
git add qinwu img/qinwu data/content-inventory.json data/legacy-url-map.json tests/test_site_structure.py
git commit -m "feat: rebuild duty content"
```

---

### Task 6: 完成警务训练13篇文章

**Files:**
- Create/Modify: 设计规范第2.3节列出的13个 `xunlian/*.html`
- Modify: `xunlian/index.html`
- Modify: `data/content-inventory.json`
- Modify: `data/legacy-url-map.json`
- Modify: `tests/test_site_structure.py`
- Create: `img/xunlian/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；训练文章章节合同。
- Produces: 7篇单兵训练和6篇小组协同训练。

- [ ] **Step 1: 写训练模块失败测试**

```python
class TrainingContentTests(unittest.TestCase):
    def test_all_training_pages_follow_article_contract(self):
        records = article_records("xunlian")
        self.assertEqual(13, len(records))
        self.assertEqual(7, sum(record["category"] == "单兵技能训练" for record in records))
        self.assertEqual(6, sum(record["category"] == "小组协同训练" for record in records))
        for record in records:
            assert_article_contract(self, record)
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.TrainingContentTests -v`
Expected: FAIL。

- [ ] **Step 3: 读取训练资料并逐篇撰写**

优先读取知识库中的：

- `单警装备/`
- `巡逻盘查/`
- `快反处置/`
- `最小作战单元/`
- `蓝军对抗与教案/`
- `快反处置与考核标准.md`

每篇使用“训练目标、适用人员、场地和装备、安全检查、基础动作或协同要点、常见错误、训练组织、考核观察点、相关装备与法规”章节。

- [ ] **Step 4: 控制模块重复**

训练文章只讲能力训练和协同，不复制五类警情的到场处置流程。装备训练文章必须回链装备介绍；小组训练必须回链相关装备和训练考评文章。

- [ ] **Step 5: 运行训练测试并提交**

Run: `python -m unittest tests.test_site_structure.TrainingContentTests -v`
Expected: PASS。

```powershell
git add xunlian img/xunlian data/content-inventory.json data/legacy-url-map.json tests/test_site_structure.py
git commit -m "feat: rebuild training content"
```

---

### Task 7: 完成警情处置5篇文章

**Files:**
- Create/Modify: `jingqing/zuijiu-lei.html`
- Create/Modify: `jingqing/chidao-lei.html`
- Create: `jingqing/zishang-lei.html`
- Create: `jingqing/jingshen-zhangai-lei.html`
- Create: `jingqing/shebao-lei.html`
- Modify: `jingqing/index.html`
- Modify: `data/content-inventory.json`
- Modify: `data/legacy-url-map.json`
- Modify: `tests/test_site_structure.py`
- Create: `img/jingqing/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；九段警情文章合同。
- Produces: 五类警情各一篇完整基础处置文章。

- [ ] **Step 1: 写警情模块失败测试**

```python
class IncidentContentTests(unittest.TestCase):
    def test_all_incident_pages_follow_article_contract(self):
        records = article_records("jingqing")
        self.assertEqual(5, len(records))
        for record in records:
            assert_article_contract(self, record)
            html = (ROOT / record["path"]).read_text(encoding="utf-8")
            for heading in ["任务确认", "风险分析", "到场", "人员保护", "法律边界", "记录报告", "禁止性事项"]:
                self.assertIn(heading, html, record["path"])
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.IncidentContentTests -v`
Expected: FAIL。

- [ ] **Step 3: 撰写醉酒和持刀类文章**

复用知识库现有醉酒、持刀、快反处置资料，但按统一九段合同重写，删除与当前公开法规不一致的绝对化流程。

- [ ] **Step 4: 撰写自伤和精神障碍类文章**

使用《中华人民共和国精神卫生法》和公开急救、危机沟通资料。明确医疗诊断由医疗机构负责，网页只说明安全保护、沟通、协同和依法处置边界。

- [ ] **Step 5: 撰写涉爆类文章**

使用《民用爆炸物品安全管理条例》等公开材料。只写发现异常、隔离风险、疏散群众、立即报告和等待专业力量，禁止加入拆除、搬移、剪线、排除装置等操作方法。

- [ ] **Step 6: 运行警情测试并提交**

Run: `python -m unittest tests.test_site_structure.IncidentContentTests -v`
Expected: PASS。

```powershell
git add jingqing img/jingqing data/content-inventory.json data/legacy-url-map.json tests/test_site_structure.py
git commit -m "feat: rebuild incident content"
```

---

### Task 8: 完成执法规范17篇文章

**Files:**
- Create/Modify: 设计规范第2.5节列出的17个 `fagui/*.html`
- Modify: `fagui/index.html`
- Modify: `data/content-inventory.json`
- Modify: `data/public-sources.json`
- Modify: `tools/public_source_index.py`
- Modify: `tests/test_public_source_index.py`
- Modify: `tests/test_site_structure.py`
- Create: `img/fagui/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；现有公开来源台账。
- Produces: 五篇规范用语、五篇程序应用、七篇法规库文章。

- [ ] **Step 1: 写执法规范失败测试**

```python
class LegalContentTests(unittest.TestCase):
    def test_all_legal_pages_follow_article_contract(self):
        records = article_records("fagui")
        self.assertEqual(17, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_law_library_pages_show_effective_date_and_official_link(self):
        records = [record for record in article_records("fagui") if record["category"] == "法律法规库"]
        self.assertEqual(7, len(records))
        for record in records:
            html = (ROOT / record["path"]).read_text(encoding="utf-8")
            self.assertIn("施行日期", html)
            self.assertRegex(html, r'https://[^"\s]+')
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.LegalContentTests -v`
Expected: FAIL。

- [ ] **Step 3: 核验法规版本**

逐项核验设计规范第3.1节的官方入口。治安管理处罚法使用2025年修订、2026年1月1日施行版本；训练条令使用2025年1月1日起施行版本。记录法规名称、效力状态、公布/修订日期、施行日期和相关条款。

- [ ] **Step 4: 撰写规范用语和程序文章**

参考表达标明“示例而非唯一固定话术”。围观拍摄页面不得把正常拍摄一概描述为违法，不提供无依据的强制删图删视频话术。警告、传唤、强制传唤和警械使用分别说明法定条件，不写成固定升级阶梯。

- [ ] **Step 5: 撰写法规库并更新来源台账**

法规正文只在法规库维护，其他文章链接到法规库。调整 `tools/public_source_index.py` 和测试，使其覆盖新的87篇库存，但不再以 `review_status` 或“未审核”阻止内容完成；仍校验来源对象结构、URL格式和页面引用的来源ID存在。

- [ ] **Step 6: 运行执法与来源测试**

Run: `python -m unittest tests.test_site_structure.LegalContentTests tests.test_public_source_index -v`
Expected: PASS。

- [ ] **Step 7: 提交**

```powershell
git add fagui img/fagui data/content-inventory.json data/public-sources.json tools/public_source_index.py tests/test_public_source_index.py tests/test_site_structure.py
git commit -m "feat: rebuild legal content"
```

---

### Task 9: 完成教育培训13篇文章并移除入门指南生成体系

**Files:**
- Create/Modify: 设计规范第2.6节列出的13个 `zoufang/*.html`
- Modify: `zoufang/index.html`
- Modify: `data/content-inventory.json`
- Delete: `rumen/`
- Delete: `.generated-learning-pages.json`
- Delete: `data/learning-modules.json`
- Delete: `tools/build_learning_modules.py`
- Delete: `tools/learning_modules.py`
- Delete: `tests/test_learning_modules.py`
- Modify: `tests/test_sensitive_content_removal.py`
- Modify: `tests/test_site_structure.py`
- Create: `img/zoufang/<article-slug>/` 下实际使用的图片

**Interfaces:**
- Consumes: Static Article Contract；教育培训文章章节合同。
- Produces: 五篇规章制度、四篇考核规范、四篇学习课程；网站中无 `rumen`。

- [ ] **Step 1: 写教育培训和删除失败测试**

```python
class EducationContentTests(unittest.TestCase):
    def test_all_education_pages_follow_article_contract(self):
        records = article_records("zoufang")
        self.assertEqual(13, len(records))
        for record in records:
            assert_article_contract(self, record)

    def test_onboarding_module_is_removed_from_web_runtime(self):
        self.assertFalse((ROOT / "rumen").exists())
        self.assertFalse((ROOT / ".generated-learning-pages.json").exists())
        for path in [ROOT / "index.html", ROOT / "js" / "nav.js", ROOT / "search-index.json"]:
            self.assertNotIn("rumen", path.read_text(encoding="utf-8"))
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.EducationContentTests -v`
Expected: FAIL。

- [ ] **Step 3: 先迁移可复用入门内容**

从原五篇入门页中提取仍适用的内务、纪律、保密、沟通和学习边界内容，重写进教育培训相应文章。不得复制旧模块名称和五阶段课程结构。

- [ ] **Step 4: 撰写13篇教育培训文章**

优先使用知识库正式材料；内务、训练和涉酒规定使用设计规范列出的官方入口。本地体能和技能考核数值只能引用单位或市局正式材料，不能把其他地区招录测评标准当成本地在岗考核标准。

- [ ] **Step 5: 删除入门生成体系**

删除仅服务于 `rumen` 的目录、数据、工具和测试。重写 `tests/test_sensitive_content_removal.py` 中与旧网页“整改中”、旧模块名称和禁止“大型活动安保”等相冲突的断言；保留对明确废弃旧页面不存在的检查。不得修改其对 `miniprogram/` 当前状态的读取对象或改写小程序文件。

- [ ] **Step 6: 运行教育和全套Python测试**

Run: `python -m unittest tests.test_site_structure.EducationContentTests -v`
Expected: PASS。

Run: `python -m unittest discover -s tests -p "test_*.py"`
Expected: PASS；若旧测试因已批准的新模块名称失败，应更新测试意图，不得回退网站。

- [ ] **Step 7: 提交**

```powershell
git add -A -- zoufang rumen .generated-learning-pages.json data/learning-modules.json tools/build_learning_modules.py tools/learning_modules.py tests/test_learning_modules.py tests/test_sensitive_content_removal.py data/content-inventory.json tests/test_site_structure.py img/zoufang
git commit -m "feat: rebuild education content and remove onboarding"
```

---

### Task 10: 完成图片本地化和全站交叉引用

**Files:**
- Modify: `data/content-inventory.json`
- Modify: 六个模块内全部87个三级文章
- Create/Modify: `img/zhuangbei/`, `img/qinwu/`, `img/xunlian/`, `img/jingqing/`, `img/fagui/`, `img/zoufang/`
- Modify: `tests/test_site_structure.py`

**Interfaces:**
- Consumes: 每篇库存记录的 `images` 和 `related_pages`。
- Produces: 所有图片本地存在并有 `alt`；所有相关文章路径存在。

- [ ] **Step 1: 写图片和交叉引用失败测试**

```python
class MediaAndCrossReferenceTests(unittest.TestCase):
    def test_inventory_images_and_related_pages_exist(self):
        valid_paths = {record["path"] for record in article_records()}
        for record in article_records():
            for image in record["images"]:
                self.assertTrue((ROOT / image["path"]).is_file(), image["path"])
                self.assertTrue(image["alt"].strip(), image["path"])
                self.assertTrue(image["source"].strip(), image["path"])
            for related in record["related_pages"]:
                self.assertIn(related, valid_paths, (record["path"], related))
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_site_structure.MediaAndCrossReferenceTests -v`
Expected: FAIL，直到清单、文件和页面引用一致。

- [ ] **Step 3: 本地化外部图片**

将选定的政府公开图片、开放许可素材、现场照片或自绘图放入对应模块和文章slug目录。库存中每张图记录 `path`、`alt`、`caption`、`source`、`license`；知识库自有图的 `license` 写 `internal`。

- [ ] **Step 4: 完成交叉引用**

至少实现以下链路：装备↔训练、训练↔警情、警情↔执法规范、勤务↔执法规范、教育培训↔训练。每篇至少有一个相关页面，法规库文章可链接多个使用场景。

- [ ] **Step 5: 运行测试并提交**

Run: `python -m unittest tests.test_site_structure.MediaAndCrossReferenceTests -v`
Expected: PASS。

```powershell
git add data/content-inventory.json img zhuangbei qinwu xunlian jingqing fagui zoufang tests/test_site_structure.py
git commit -m "feat: add article media and cross references"
```

---

### Task 11: 构建搜索索引、旧URL跳转和断链检查器

**Files:**
- Create: `tools/build_search_index.py`
- Create: `tools/check_site_links.py`
- Modify: `search-index.json`
- Modify: `data/legacy-url-map.json`
- Create/Modify/Delete: 映射要求的旧HTML跳转页
- Create: `tests/test_search_index.py`
- Create: `tests/test_site_links.py`

**Interfaces:**
- Produces: `build_index(root: Path) -> list[dict]`。
- Produces: `check_index(root: Path, records: list[dict]) -> list[str]`。
- Produces: `check_site(root: Path) -> list[str]`。
- Search record fields: `title`、`module`、`category`、`desc`、`keywords`、`path`。

- [ ] **Step 1: 写搜索构建器失败测试**

```python
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("build_search_index", ROOT / "tools" / "build_search_index.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SearchIndexTests(unittest.TestCase):
    def test_index_matches_all_inventory_articles(self):
        records = MODULE.build_index(ROOT)
        self.assertEqual(87, len(records))
        self.assertEqual(87, len({record["path"] for record in records}))
        self.assertFalse(any(record["path"].startswith("rumen/") for record in records))
        self.assertEqual([], MODULE.check_index(ROOT, records))
```

- [ ] **Step 2: 运行测试并确认失败**

Run: `python -m unittest tests.test_search_index -v`
Expected: FAIL，因为工具尚不存在。

- [ ] **Step 3: 实现稳定搜索构建器**

使用 `html.parser.HTMLParser` 或明确的标准库解析逻辑读取库存中的87个HTML，提取 `h1`、`data-module`、`data-category`、`.article-summary` 和关键词标签。输出按 `path` 排序，`--check` 比较磁盘JSON与新生成结果并在不一致时返回1。

CLI合同：

```powershell
python tools/build_search_index.py
python tools/build_search_index.py --check
```

第一条写入 `search-index.json`；第二条只检查不写文件。

- [ ] **Step 4: 写并实现断链检查器**

`tests/test_site_links.py`：

```python
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_site_links", ROOT / "tools" / "check_site_links.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SiteLinkTests(unittest.TestCase):
    def test_site_has_no_broken_local_links(self):
        self.assertEqual([], MODULE.check_site(ROOT))
```

实现时解析所有网站HTML的 `href` 和 `src`，跳过 `http:`、`https:`、`mailto:`、`tel:` 和 `javascript:`，验证本地文件及 `#anchor`。排除 `.git/`、`.worktrees/`、`.superpowers/`、`deliverables/`、`docs/` 和 `miniprogram/`。

- [ ] **Step 5: 创建旧URL跳转页**

对 `action=redirect` 的映射创建最小静态跳转页，包含 canonical、meta refresh 和可点击后备链接；跳转页不得包含 `.article-page`，因此不会进入搜索。`action=remove` 的 `rumen` 不创建文件。

- [ ] **Step 6: 生成索引并运行测试**

Run: `python tools/build_search_index.py`
Expected: 输出 `Wrote 87 records to search-index.json`。

Run: `python -m unittest tests.test_search_index tests.test_site_links -v`
Expected: PASS。

- [ ] **Step 7: 提交**

```powershell
git add tools/build_search_index.py tools/check_site_links.py search-index.json data/legacy-url-map.json tests/test_search_index.py tests/test_site_links.py zhuangbei qinwu xunlian jingqing fagui zoufang
git commit -m "feat: regenerate search and migrate legacy pages"
```

---

### Task 12: 全站回归、浏览器验收和交付报告

**Files:**
- Create: `docs/site-content-rebuild-report.md`
- Create: `deliverables/site-content-rebuild-screenshots/` 下验收截图
- Modify: 仅限验收发现问题涉及的文件

**Interfaces:**
- Consumes: 全部前序任务产物。
- Produces: 可复现的自动测试结果、断链结果、页面计数、浏览器截图和未修改小程序确认。

- [ ] **Step 1: 运行全部自动测试**

```powershell
node --test tests/auth_core.test.js
python -m unittest discover -s tests -p "test_*.py"
python tools/build_search_index.py --check
python tools/check_site_links.py
git diff --check
git diff --exit-code -- miniprogram
```

Expected:

- Node测试全部PASS；
- Python测试全部PASS；
- 搜索检查返回0并报告87条；
- 断链检查返回0；
- `git diff --check` 无输出；
- `git diff --exit-code -- miniprogram` 无输出且返回0。

- [ ] **Step 2: 启动本地HTTP服务器**

Run: `python -m http.server 8000`
Expected: `Serving HTTP on ... port 8000`。

- [ ] **Step 3: 验收桌面和手机视口**

在 `http://localhost:8000` 检查1440×900和390×844：登录、退出、首页六张卡片、六个模块索引、20个分类锚点、每模块至少三篇不同类型文章、图片、来源、相关文章、上一篇/下一篇和搜索。

- [ ] **Step 4: 检查浏览器控制台**

修复所有资源404、JavaScript异常、重复ID、横向溢出、图片变形和移动端导航遮挡。每次修复后重新运行Task 12 Step 1的全部命令。

- [ ] **Step 5: 保存验收截图**

至少保存：首页桌面/手机、六个模块索引桌面/手机、装备/勤务/训练/警情/法规/教育各一篇代表文章桌面/手机，共26张。文件名使用 `<page>-desktop.png` 和 `<page>-mobile.png`。

- [ ] **Step 6: 编写交付报告**

`docs/site-content-rebuild-report.md` 必须包含：

- 87篇文章按模块计数；
- 知识库与公开来源摘要；
- 图片来源清单位置；
- 旧URL映射位置；
- 执行过的测试命令及结果；
- 断链检查结果；
- 截图目录；
- `miniprogram/` 无差异确认；
- 已知但不阻塞上线的问题；无问题时明确写“无”。

- [ ] **Step 7: 最终提交**

```powershell
git add -A -- ':!公安警察工作汇报PPT.pptx'
git commit -m "fix: resolve final responsive and content issues"
```

- [ ] **Step 8: 最终状态检查**

Run: `git status --short`
Expected: 只允许显示用户原有的未跟踪 PPT；不得存在本次实施产生的未提交文件。

---

## Execution Notes

- 本计划规模较大，推荐使用独立工作树执行；执行前调用 `superpowers:using-git-worktrees`。
- 推荐按Task 1—12顺序推进；内容模块任务可由不同执行者分别完成，但必须依次合入并在每次合入后运行结构测试。
- 内容撰写任务的评审重点是：是否符合三级清单、是否引用正确资料、是否满足文章合同、是否与其他模块重复或冲突。
- 不要为了让旧测试通过而恢复已经批准删除的旧模块名称或“整改中”空壳；应更新已经失效的测试意图。
- 任何需要联网下载的图片或官方材料，都先记录URL再下载，确保来源可追溯。
