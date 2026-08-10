# 学习页面图片视觉验收记录

日期：2026-08-10

## 本轮范围

本轮建立 `.learning-figure` 共享样式，并为六个模块各完成一张原创教材信息图。图稿均使用 `viewBox="0 0 760 520"`，包含可辨认的人物、器材或场景对象，以及 `<title>` 和 `<desc>`。

| 页面 | 图稿 | 聚焦结构检查 | 1440×900 截图 | 390×900 截图 |
| --- | --- | --- | --- | --- |
| `zhuangbei/zhifa-jiuyi.html` | `img/learning/zhuangbei/zhifa-jiuyi-structure.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/zhuangbei-zhifa-jiuyi-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/zhuangbei-zhifa-jiuyi-390x900.png` |
| `xunlian/geren-fanghu-anquan.html` | `img/learning/xunlian/geren-fanghu-anquan-checklist.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/xunlian-geren-fanghu-anquan-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/xunlian-geren-fanghu-anquan-390x900.png` |
| `jingqing/zuijiu-lei.html` | `img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/jingqing-zuijiu-lei-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/jingqing-zuijiu-lei-390x900.png` |
| `qinwu/gonggong-zhixu-goutong-jilu.html` | `img/learning/qinwu/gonggong-zhixu-goutong-record.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/qinwu-gonggong-zhixu-goutong-jilu-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/qinwu-gonggong-zhixu-goutong-jilu-390x900.png` |
| `fagui/panwen-shenfenzheng.html` | `img/learning/fagui/panwen-shenfenzheng-procedure.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/fagui-panwen-shenfenzheng-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/fagui-panwen-shenfenzheng-390x900.png` |
| `zoufang/changsuo-aed-jiancha.html` | `img/learning/zoufang/changsuo-aed-jiancha.svg` | 通过 | `.artifacts/visual-acceptance-learning-figures/zoufang-changsuo-aed-jiancha-1440x900.png` | `.artifacts/visual-acceptance-learning-figures/zoufang-changsuo-aed-jiancha-390x900.png` |

聚焦结构检查确认每页恰有一个 `.learning-figure`，图片使用 `loading="lazy"`，资源路径存在，`alt` 与 `figcaption` 非空；每张 SVG 可解析且具备 `viewBox`、`title` 和 `desc`；共享 CSS 包含响应式图片尺寸、640px 单列规则和打印避免分页规则。

## 浏览器视觉验收

使用仅限本地验收的 auth-aware 静态服务器，在响应头写入 `auth-config.js` 已有摘要对应的测试 Cookie；生产认证文件未改动。浏览器逐页确认最终 URL 仍为目标正文、`html.auth-pending` 已移除、`.learning-figure` 恰有一个且位于截图视口中、图片加载完成、图注可见。

十二张正式截图均在配图滚入视口、横向滚动位置归零后以 `fullPage: false` 生成。为抵消浏览器截图时扣除的滚动条区域，桌面捕获视口校准为 1455×909，得到 6 张严格为 1440×900 的 PNG；移动捕获视口校准为 405×935，得到 6 张严格为 390×900 的 PNG。逐文件像素核验全部通过。

两个视口下每页均满足 `documentElement.scrollWidth <= documentElement.clientWidth + 1`，未发现页面级横向滚动；名义 1440 宽测试中 `scrollWidth = clientWidth = 1425`，名义 390 宽测试中 `scrollWidth = clientWidth = 375`。移动端 `.learning-figure` 的右边界为 358.67px、图片右边界为 346.80px，均在 375px 内容区内。正确重采后的六张移动截图也确认右侧标签完整可见；图稿、人物或器材、信息关系与图注均可辨。六页还逐页切换至 `night` 主题检查，正文背景为 `rgb(16, 25, 35)`、图注文字为 `rgb(197, 209, 219)`，图片和图注保持可见且无横向溢出。

浏览器级视觉验收已通过。六页 `acceptance_status` 暂仍保持 `not-reviewed`，仅用于表示尚待用户在 Task 2 人工确认点接受代表图风格；它不再表示截图或浏览器检查缺失。在用户确认前不开始 Task 3。

## Fix round 1（2026-08-10）

- 六张 SVG 已将深色正文 `.t` 与亮色标题/编号 `.light` 分层；琥珀色圆内编号使用 `.dark`，按颜色值计算，深色文字对琥珀底对比度约 4.65:1。深蓝标题条上的白字对比度约 10.97:1。
- 六张 SVG 均增加 `max-width: 500px` 下显示的移动专用信息层，并精简文字和重排关系。移动层全部文字源字号不低于 25px；按 390px 页面中约 344px 图片宽度估算，实际字号约 11.3px。
- focused tests 已验证每张图的标题与编号使用显式亮/暗色类、没有会被 `.t` 覆盖的 `fill="#fff"` 文字展示属性，并验证每张图恰有一个移动层且其中所有文字字号不低于 25px。
- 使用临时 auth-aware 静态服务器在响应头写入 `auth-config.js` 既有 digest Cookie，已成功进入真实代表页正文，未修改生产认证文件。批量截图第一次因浏览器执行环境覆盖全局 `parseFloat` 而中断；最小修正后第二次在 `.learning-figure` 定位的 3 秒环境上限处超时。按控制要求停止继续尝试。

上述问题已在 Fix round 2 中通过延长本地页面就绪判定、改用元素计数轮询并生成真实页面截图解决。

## Fix round 2（2026-08-10）

- 复用 `127.0.0.1:8765` auth-aware fixture 后确认六页均返回真实正文，没有跳转到 `auth.html`。先前失败的根因是浏览器环境对单次选择器解析设有 3 秒上限，而首次页面加载可能超过该上限；改为等待 `domcontentloaded` 后对元素数量做有界轮询。
- 生成并逐张检查上表列出的 12 张正式截图。初次精确裁剪错误使用文档原点，造成移动图右侧标签疑似被截；该批截图已废弃。最终先将配图滚入视口，再以 `fullPage: false` 截图，并使用 1455×909 / 405×935 校准视口抵消浏览器滚动条区域，保证 PNG 文件像素严格为 1440×900 / 390×900 且配图完整。
- 每页在两个视口下均通过认证状态、配图可见、图片加载、图注可见与页面横向溢出检查；六页在夜间主题下也通过背景、图注对比与溢出检查。
- 当前无浏览器级 blocker；后续唯一人工门槛是用户确认六张代表图的整体视觉方向。

## Fix round 3（2026-08-10）

- 最终复核发现 `qinwu/gonggong-zhixu-goutong-jilu.html` 桌面截图与 `zoufang/changsuo-aed-jiancha.html` 移动截图带有非零横向截图偏移警告；两张正式 PNG 已在 `scrollX = 0` 后重新生成并覆盖。
- 重采后两张截图均完整显示站点标识、页头与配图左右边界，像素尺寸仍分别为 1440×900 与 390×900。其余十张正式截图不受影响，当前不再有截图偏移警告。
