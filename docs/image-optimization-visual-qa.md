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
