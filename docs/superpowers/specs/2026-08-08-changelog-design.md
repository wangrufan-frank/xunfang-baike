# 巡防百科更新记录板块设计

日期：2026-08-08
状态：已确认

## 1. 背景与目标

为巡防百科网站新增"更新记录"板块：供浏览学习的人员查看网站历次更新内容，风格类似游戏网站的版本更新提示。本次将记录"伤员救助与急救"内容的更新梗概。

## 2. 需求要点

- 入口位置：**方案 C**——独立页面 + 导航入口（首页不加入口）
- 导航入口：置于**导航栏首位**，**醒目配色**，让人第一眼就能发现
- 条目格式：**仅日期 + 内容描述**（无版本号）
- 历史记录：**只记本次**更新（不追溯补录历史）
- 手机端：**同等醒目与适配**

## 3. 设计

### ① 页面 `changelog.html`（根目录独立页）
- 结构参照现有 `search.html`（含导航占位、认证脚本、主题脚本、main.js/search.js）
- 面包屑：首页 > 更新记录
- 标题：📝 更新记录
- 内容区：按日期倒序渲染更新条目

### ② 数据与渲染
- 新增 `data/updates.json`：`{ "version": 1, "updates": [ {date, title, items[]} ] }`，以后每次更新追加一条
- 新增 `js/changelog.js`：读取 `data/updates.json`，渲染条目（日期 + 标题 + 内容列表）
- 本次更新条目（2026-08-08）：
  - 标题：新增"伤员救助与急救"内容
  - 列表：
    - 警情处置新增《救助类警情处置流程》（含现场舆情管控环节）
    - 实战训练新增《心肺复苏操作要点》《止血、包扎与伤员搬运》
    - 装备操作新增《急救包组成与使用》《AED 使用方法》
    - 教育学习新增《场所急救设施与AED部署检查》
    - 同步完善搜索索引、来源台账与站内导航

### ③ 导航入口（首位 + 最醒目）
- `js/nav.js` 的 `MODULES` 数组**第一项**加：`{ name: '更新记录', path: 'changelog.html', emoji: '📝', featured: true }`
- `renderNav` 中：`featured` 标记生成 `changelog-link` 类（与 `special`/`monthly-link` 区分）
- CSS 新增 `.nav-links a.changelog-link`：**始终填充的琥珀色徽章**（深色文字、高对比、圆角），比"本月精选"的金色描边更醒目
- 深度判断与 active 状态沿用现有逻辑（changelog.html 位于根目录，不影响模块目录判断）

### ④ 手机端适配（max-width:900px）
- 导航收起为汉堡菜单，`nav-links` 纵向下拉（背景 `--nav-bg`）
- 更新记录为下拉**第一项**，琥珀色实心徽章样式在纵向列表中同样生效，在导航背景上醒目
- 徽章在移动端微调：保证足够点击区域（如加大 padding）、不被裁切

### ⑤ 首页
- 不加入口

### ⑥ 验证
- `python tools/check_site_links.py`：新页面 + 导航链接无断链
- `python -m unittest discover -s tests -p "test_*.py"` 与 `node --test tests/auth_core.test.js` 全绿
- `python tools/build_search_index.py --check` 保持 93 条（changelog 页不纳入搜索索引，属元内容）

## 4. 不做什么

- 不追溯补录历史更新
- 不加版本号
- 首页不加更新记录入口
- 不将 changelog 页纳入搜索索引
- 不改动六个内容模块与既有数据台账

## 5. 风险与注意

- `js/nav.js` 的 MODULES 数组同时驱动深度判断与 active 状态：新增 `changelog.html` 位于根目录，需确认不干扰模块目录判断（实施时用现有逻辑验证）
- 醒目徽章样式需在各主题（暖警蓝/经典暖棕/日间浅色/夜间深色）下均对比清晰，使用主题变量 `--amber` 与对比色
- 只改该改的内容：仅新增 changelog.html、data/updates.json、js/changelog.js，并修改 js/nav.js 与 css/style.css 的导航入口相关部分
