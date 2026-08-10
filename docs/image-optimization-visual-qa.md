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

## Task 10 全站抽样验收（2026-08-10）

### 抽样与证据

最终验收从 `data/image-optimization-plan.json` 动态选择 18 个独立页面：每个模块保留一张已确认的视觉基线代表页，再选择模块内学习图/图片数量最高页，以及排除前两页后的补充长图文页。这样每模块有 3 页，超过“每模块至少 2 页并保留 6 个代表页”的要求。`python tools/visual_acceptance.py --list-samples` 已通过 18 页源文件结构检查，确认每页均有 `.learning-figure`、存在的本地图片、非空 `alt` 和 `figcaption`。

| 模块 | 页面 | 选择原因 | 1440×900 | 390×900 |
| --- | --- | --- | --- | --- |
| 装备操作 | `zhuangbei/zhifa-jiuyi.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/zhuangbei-zhifa-jiuyi-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zhuangbei-zhifa-jiuyi-390x900.png` |
| 装备操作 | `zhuangbei/yueshu-dai.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/zhuangbei-yueshu-dai-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zhuangbei-yueshu-dai-390x900.png` |
| 装备操作 | `zhuangbei/pochai-gongju.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/zhuangbei-pochai-gongju-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zhuangbei-pochai-gongju-390x900.png` |
| 实战训练 | `xunlian/geren-fanghu-anquan.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/xunlian-geren-fanghu-anquan-1440x900.png` | `.artifacts/visual-acceptance-sitewide/xunlian-geren-fanghu-anquan-390x900.png` |
| 实战训练 | `xunlian/xianchang-goutong-yingxiang.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/xunlian-xianchang-goutong-yingxiang-1440x900.png` | `.artifacts/visual-acceptance-sitewide/xunlian-xianchang-goutong-yingxiang-390x900.png` |
| 实战训练 | `xunlian/zhixue-baozha-banyun.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/xunlian-zhixue-baozha-banyun-1440x900.png` | `.artifacts/visual-acceptance-sitewide/xunlian-zhixue-baozha-banyun-390x900.png` |
| 警情处置 | `jingqing/zuijiu-lei.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/jingqing-zuijiu-lei-1440x900.png` | `.artifacts/visual-acceptance-sitewide/jingqing-zuijiu-lei-390x900.png` |
| 警情处置 | `jingqing/jingshen-zhangai-lei.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/jingqing-jingshen-zhangai-lei-1440x900.png` | `.artifacts/visual-acceptance-sitewide/jingqing-jingshen-zhangai-lei-390x900.png` |
| 警情处置 | `jingqing/jiuzhu-lei-jingqing-chuzhi.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/jingqing-jiuzhu-lei-jingqing-chuzhi-1440x900.png` | `.artifacts/visual-acceptance-sitewide/jingqing-jiuzhu-lei-jingqing-chuzhi-390x900.png` |
| 勤务须知 | `qinwu/gonggong-zhixu-goutong-jilu.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/qinwu-gonggong-zhixu-goutong-jilu-1440x900.png` | `.artifacts/visual-acceptance-sitewide/qinwu-gonggong-zhixu-goutong-jilu-390x900.png` |
| 勤务须知 | `qinwu/yinhang-zhidian-zoufang.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/qinwu-yinhang-zhidian-zoufang-1440x900.png` | `.artifacts/visual-acceptance-sitewide/qinwu-yinhang-zhidian-zoufang-390x900.png` |
| 勤务须知 | `qinwu/zhuanxiang-xianchang-zhixu.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/qinwu-zhuanxiang-xianchang-zhixu-1440x900.png` | `.artifacts/visual-acceptance-sitewide/qinwu-zhuanxiang-xianchang-zhixu-390x900.png` |
| 执法规范 | `fagui/panwen-shenfenzheng.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/fagui-panwen-shenfenzheng-1440x900.png` | `.artifacts/visual-acceptance-sitewide/fagui-panwen-shenfenzheng-390x900.png` |
| 执法规范 | `fagui/xingzheng-anji-chengxu-guiding.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/fagui-xingzheng-anji-chengxu-guiding-1440x900.png` | `.artifacts/visual-acceptance-sitewide/fagui-xingzheng-anji-chengxu-guiding-390x900.png` |
| 执法规范 | `fagui/xianchang-zhizhi-guicheng.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/fagui-xianchang-zhizhi-guicheng-1440x900.png` | `.artifacts/visual-acceptance-sitewide/fagui-xianchang-zhizhi-guicheng-390x900.png` |
| 教育学习 | `zoufang/changsuo-aed-jiancha.html` | 基线代表页 | `.artifacts/visual-acceptance-sitewide/zoufang-changsuo-aed-jiancha-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zoufang-changsuo-aed-jiancha-390x900.png` |
| 教育学习 | `zoufang/jichu-jingwu-kaohe.html` | 高图量/长图文 | `.artifacts/visual-acceptance-sitewide/zoufang-jichu-jingwu-kaohe-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zoufang-jichu-jingwu-kaohe-390x900.png` |
| 教育学习 | `zoufang/kecheng-ziliao-jiaoliu.html` | 补充长图文 | `.artifacts/visual-acceptance-sitewide/zoufang-kecheng-ziliao-jiaoliu-1440x900.png` | `.artifacts/visual-acceptance-sitewide/zoufang-kecheng-ziliao-jiaoliu-390x900.png` |

浏览器原始结构与布局结果保存在 `.artifacts/visual-acceptance-sitewide/browser-report.json`，状态为 `passed`，含 36 个视口结果、6 个代表页的四主题结果和零错误清单。Task 2 的 12 张正式基线截图仍保留在 `.artifacts/visual-acceptance-learning-figures/`，没有被本轮文件替代或冒充。

### 浏览器布局与人工复核

复用 `127.0.0.1:8765` auth-aware 本地静态夹具，经 Codex 应用内浏览器进入真实正文；未读取浏览器 Cookie/存储，也未改动生产认证文件。应用内浏览器会扣除滚动条和工具栏像素，因此控制视口使用 1455×909 / 405×935，最终 42 个 PNG（36 张暖警蓝双视口截图和 6 张夜间代表页截图）经 Pillow 逐文件核验，分别严格为 1440×900 / 390×900。六张夜间证据采用 `*-night-1440x900.png` 文件名。

36 个双视口结果全部满足：最终路径仍为目标正文、`auth-pending` 已解除、正文连续且长度正常；`documentElement.scrollWidth <= window.innerWidth + 5`；`.learning-figure`、media、图片和图注 bounding box 均非零，左右边界不超过 `documentElement.clientWidth + 1`；图片已完成加载；图注无自身横向裁剪；横向截图偏移为 0；首张学习图滚入后与 900px 截图视口相交。

六个代表页通过站点主题控件逐一切换暖警蓝、经典暖棕、日间浅色和夜间深色。图注文字与沿 DOM 祖先找到的首个不透明背景的实测对比度依次为 6.72:1、6.04:1、7.03:1、11.40:1，均高于 4.5:1；四主题下页面均无横向溢出，配图边界保持完整。首次计算曾把透明图注/figure 背景错误当成纯黑，已改为沿祖先查找有效背景后复测；不保留该次假阴性结论。

人工查看了六个模块代表页的 390×900 暖警蓝截图、各模块的长图文/高图量样本以及 1440×900 夜间代表页。移动层文字、人物/器材/步骤/空间关系和相邻图注可辨；图注换行正常；正文在图片前后连续；未发现抽象装饰图、重复占位图或与正文流程矛盾的内容。本轮未发现需要继续修改 HTML、CSS 或 SVG 的视觉缺陷。

### 运行限制

当前 bundled Python 解释器未安装 `playwright` 模块。因此直接运行 `python tools/visual_acceptance.py` 会在完成 18 页 source audit 后以退出码 2 明确报告 `BLOCKED`，并在 `.artifacts/visual-acceptance-sitewide/report.json` 写入 `status: blocked`；它不会把未执行的 Python Playwright 截图写成通过。真实浏览器验收由上述 Codex 应用内浏览器完成，独立证据在 `browser-report.json` 中为 `status: passed`。脚本本身已具备 Playwright 可用时的 36 视口截图、页面横向溢出、学习图/图片/图注零尺寸与裁剪失败判定。
