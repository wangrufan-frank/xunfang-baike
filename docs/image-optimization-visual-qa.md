# 学习页面图片视觉验收记录

日期：2026-08-10

## 本轮范围

本轮建立 `.learning-figure` 共享样式，并为六个模块各完成一张原创教材信息图。图稿均使用 `viewBox="0 0 760 520"`，包含可辨认的人物、器材或场景对象，以及 `<title>` 和 `<desc>`。

| 页面 | 图稿 | 聚焦结构检查 | 1440×900 截图 | 390×900 截图 |
| --- | --- | --- | --- | --- |
| `zhuangbei/zhifa-jiuyi.html` | `img/learning/zhuangbei/zhifa-jiuyi-structure.svg` | 通过 | 未生成 | 未生成 |
| `xunlian/geren-fanghu-anquan.html` | `img/learning/xunlian/geren-fanghu-anquan-checklist.svg` | 通过 | 未生成 | 未生成 |
| `jingqing/zuijiu-lei.html` | `img/learning/jingqing/zuijiu-lei-chuzhi-flow.svg` | 通过 | 未生成 | 未生成 |
| `qinwu/gonggong-zhixu-goutong-jilu.html` | `img/learning/qinwu/gonggong-zhixu-goutong-record.svg` | 通过 | 未生成 | 未生成 |
| `fagui/panwen-shenfenzheng.html` | `img/learning/fagui/panwen-shenfenzheng-procedure.svg` | 通过 | 未生成 | 未生成 |
| `zoufang/changsuo-aed-jiancha.html` | `img/learning/zoufang/changsuo-aed-jiancha.svg` | 通过 | 未生成 | 未生成 |

聚焦结构检查确认每页恰有一个 `.learning-figure`，图片使用 `loading="lazy"`，资源路径存在，`alt` 与 `figcaption` 非空；每张 SVG 可解析且具备 `viewBox`、`title` 和 `desc`；共享 CSS 包含响应式图片尺寸、640px 单列规则和打印避免分页规则。

## 截图限制

浏览器访问本地代表页时被站点登录守卫重定向到登录页，无法看到正文。随后尝试启动仅用于本地视觉验收、自动附带测试会话 Cookie 的临时 HTTP 服务，但该进程未能在 `127.0.0.1:8765` 建立监听，连接检查失败。按任务控制要求停止继续排查，未生成截图文件。

因此以下项目尚未完成浏览器级确认：图片内文字在 1440×900 与 390×900 下的实际可读性、移动端横向滚动、图注实际换行，以及夜间主题容器对比度。上述项目需在具备有效站点会话的浏览器中由用户或后续验收补做；在用户明确接受六张代表图之前，不应开始 Task 3。

## Fix round 1（2026-08-10）

- 六张 SVG 已将深色正文 `.t` 与亮色标题/编号 `.light` 分层；琥珀色圆内编号使用 `.dark`，按颜色值计算，深色文字对琥珀底对比度约 4.65:1。深蓝标题条上的白字对比度约 10.97:1。
- 六张 SVG 均增加 `max-width: 500px` 下显示的移动专用信息层，并精简文字和重排关系。移动层全部文字源字号不低于 25px；按 390px 页面中约 344px 图片宽度估算，实际字号约 11.3px。
- focused tests 已验证每张图的标题与编号使用显式亮/暗色类、没有会被 `.t` 覆盖的 `fill="#fff"` 文字展示属性，并验证每张图恰有一个移动层且其中所有文字字号不低于 25px。
- 使用临时 auth-aware 静态服务器在响应头写入 `auth-config.js` 既有 digest Cookie，已成功进入真实代表页正文，未修改生产认证文件。批量截图第一次因浏览器执行环境覆盖全局 `parseFloat` 而中断；最小修正后第二次在 `.learning-figure` 定位的 3 秒环境上限处超时。按控制要求停止继续尝试。

截图仍未生成，六页 `acceptance_status` 继续保持 `not-reviewed`。页面级 1440×900 / 390×900 滚动、图注换行与夜间主题检查仍是明确 blocker，不能写为通过。
