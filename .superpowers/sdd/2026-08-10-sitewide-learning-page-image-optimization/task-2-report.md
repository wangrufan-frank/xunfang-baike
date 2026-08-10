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

结果：未完成。浏览器被站点登录守卫重定向至登录页；尝试启动附带测试会话 Cookie 的临时本地验收服务后，服务未能在 `127.0.0.1:8765` 建立监听。按控制要求停止继续排查，避免视觉工具阻塞实现提交。

截图路径：无（未生成）。

## 未解决问题

- 尚未在真实页面正文中完成六页桌面端/移动端截图。
- 尚未浏览器确认图片文字实际可读性、移动端无横向滚动、图注换行和深色主题容器对比度。
- 六张图的 `acceptance_status` 保持 `not-reviewed`；用户明确接受六张代表图之前不应开始 Task 3。

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

因此六页 `acceptance_status` 保持 `not-reviewed`，1440×900 与 390×900 页面级截图、横向滚动、图注换行和夜间主题对比仍未验收，不能标记为通过。
