# Task 2 实施报告

## 实现摘要

- 在 `css/style.css` 增加共享 `.learning-figure`、`.learning-figure__media`、图片、图注、640px 移动端与打印样式合同。
- 为装备操作、实战训练、警情处置、勤务须知、执法规范、教育学习六个模块各绘制一张原创 SVG 教材信息图；图稿不依赖外部素材，均含响应式 `viewBox`、`title`、`desc` 和可辨认的人物、器材或场景关系。
- 将六张图以统一 `<figure class="learning-figure">` 结构插入 brief 指定段落，补齐对应 `alt` 和 `figcaption`。
- 同步 `data/content-inventory.json` 的 `images[]`，并将 `data/image-optimization-plan.json` 六条记录更新为 `current_images: 1`、资产 `complete`、实施 `complete`。精确图稿尚待用户视觉确认，故验收状态保持真实的 `not-reviewed`。
- 新增共享样式合同测试，并先见证其因缺少 `.learning-figure` 失败，再实现样式使其通过。

## 文件清单

### SVG

- `img/learning/zhuangbei/zhifa-jiuyi-structure.svg`
- `img/learning/xunlian/geren-fanghu-anquan-checklist.svg`
- `img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg`
- `img/learning/qinwu/gonggong-zhixu-goutong-record.svg`
- `img/learning/fagui/panwen-shenfenzheng-procedure.svg`
- `img/learning/zoufang/changsuo-aed-jiancha.svg`

### HTML

- `zhuangbei/zhifa-jiuyi.html`
- `xunlian/geren-fanghu-anquan.html`
- `jingqing/zuijiu-lei.html`
- `qinwu/gonggong-zhixu-goutong-jilu.html`
- `fagui/panwen-shenfenzheng.html`
- `zoufang/changsuo-aed-jiancha.html`

### CSS、台账、测试与文档

- `css/style.css`
- `data/content-inventory.json`
- `data/image-optimization-plan.json`
- `tests/test_image_optimization.py`
- `docs/image-optimization-visual-qa.md`

## 测试与视觉检查

### TDD RED

命令：

```powershell
python -m unittest tests.test_image_optimization -v
```

结果：新增 `test_learning_figure_styles_cover_media_caption_mobile_and_print` 按预期失败，失败原因仅为 `css/style.css` 缺少 `.learning-figure`；其余 8 项通过。

### 结构验证

命令：

```powershell
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_image_optimization.py
python tools/check_site_links.py
```

结果：

- 单元测试：29/29 通过。
- 图片台账校验：93 pages checked，0 validation errors。
- 站内链接校验：129 pages checked，无 broken links 或 anchors。

### 聚焦静态视觉合同检查

检查每个代表页恰有一个 `.learning-figure`，资源引用、lazy loading、非空 `alt` 与 `figcaption` 完整；六张 SVG 均可解析且具备 `viewBox`、`title`、`desc`；共享 CSS 具备响应式图片、640px 单列和打印规则。结果：六页与共享 CSS 全部通过。

### 浏览器视觉检查与截图

计划视口：1440×900、390×900。

结果：完成。通过仅限本地验收的 auth-aware 静态服务器进入六个真实代表页，未改动生产认证文件。六页在两个视口下均确认：最终 URL 未跳转到 `auth.html`、认证等待类已移除、配图位于视口中、图片加载完成、图注可见、页面无横向滚动。另逐页切换夜间主题，确认图片与图注可见、正文背景和图注文字保持对比且无横向溢出。

截图路径：`.artifacts/visual-acceptance-learning-figures/`，正式文件共 12 张；桌面捕获视口以 1455×909 抵消滚动条区域，输出 6 张严格为 1440×900 的 PNG；移动捕获视口以 405×935 校准，输出 6 张严格为 390×900 的 PNG。逐页文件名已记录在 `docs/image-optimization-visual-qa.md`。

## 未解决问题

- 浏览器级验收已无 blocker。
- 六张图的 `acceptance_status` 保持 `not-reviewed`，表示仍待用户在 Task 2 人工确认点接受代表图风格；用户确认前不应开始 Task 3。

## Fix round 1

### 修复内容

- 修复六张 SVG 的文字颜色级联冲突：正文使用 `.t`，深色底标题与编号使用显式 `.light`，琥珀色圆内编号使用显式 `.dark`。不再使用会被 `.t` 类覆盖的 `fill="#fff"` 文字展示属性。
- 为六张 SVG 各增加一个移动专用简化层，在 SVG 自身 `@media (max-width:500px)` 下覆盖桌面图层。移动层重新组织信息层级，所有文字源字号不低于 25px，按 390px 页面中约 344px 图片宽度估算为约 11.3px。
- 新增 focused tests：`test_representative_svgs_use_explicit_light_text_class` 与 `test_representative_svgs_have_readable_mobile_layer`。

### 验证结果

```powershell
python -m unittest tests.test_image_optimization tests.test_site_structure -v
python tools/check_image_optimization.py
python tools/check_site_links.py
```

- 单元测试：31/31 通过。
- 图片台账校验：93 pages checked，0 validation errors。
- 站内链接校验：129 pages checked，无 broken links 或 anchors。

### 页面截图状态

临时 auth-aware server 使用 `auth-config.js` 既有 digest Cookie，已确认浏览器能进入真实正文，且未修改生产认证边界。批量截图仍未产出：第一次因浏览器执行环境中的 `parseFloat` 问题中断；第二次在 `.learning-figure` 定位的环境超时上限处中断。已按控制要求停止浏览器尝试。

因此当时六页 `acceptance_status` 保持 `not-reviewed`；该截图 blocker 已在 Fix round 2 解决。

## Fix round 2

### 根因与修复

- `127.0.0.1:8765` auth-aware fixture 实际可正常返回页面和 `Set-Cookie`。此前定位超时的根因是浏览器环境对单次 `.learning-figure` 选择器解析设有 3 秒上限，而首次页面加载可能超过该上限，并非认证服务失效。
- 改为等待 `domcontentloaded` 后有界轮询元素数量，再滚动至配图区域并以 `fullPage: false` 截图。初次显式裁剪错误地使用文档原点，造成移动图右侧标签疑似被截；该批截图已废弃。最终使用 1455×909 / 405×935 校准视口抵消浏览器滚动条区域，正确捕获配图所在视口。

### 验收证据

- 12 张正式 PNG 全部存在且非空：6 张 1440×900、6 张 390×900。
- 六页两个视口共 12 次检查均满足：目标 URL 保持不变、无 `auth-pending`、配图可见、图片加载完成、图注可见、`scrollWidth <= clientWidth + 1`。名义 1440 宽测试的 `scrollWidth = clientWidth = 1425`，名义 390 宽测试的 `scrollWidth = clientWidth = 375`；移动端 figure/image 右边界分别为 358.67px / 346.80px，均未越过 375px 内容区。
- 正确重采后的六张移动截图已逐张确认右侧信息卡和标签完整可见，不再使用以文档原点裁剪的错误截图。
- 六页夜间主题逐页检查均满足：`data-theme="night"`、正文背景 `rgb(16, 25, 35)`、图注颜色 `rgb(197, 209, 219)`、图片加载完成、无横向溢出。
- 浏览器级验收结论：通过；用户风格确认仍待 Task 2 人工确认点。
