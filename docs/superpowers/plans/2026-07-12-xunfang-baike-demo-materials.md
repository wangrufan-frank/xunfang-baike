# 巡防百科网站演示材料制作 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 制作一套用于推动巡防百科网站推广的领导汇报 PPT 和一条现场备用使用演示视频。

**Architecture:** PPT 使用网站真实截图和深蓝警务风格说明项目价值；视频以电脑浏览器录屏、字幕和鼠标高亮展示一次完整查询路径。现场先实机演示网站，异常时播放本地 MP4。

**Tech Stack:** PowerPoint `.pptx`、PptxGenJS 或 PowerPoint 编辑、浏览器录屏、HyperFrames、FFmpeg、LibreOffice/Poppler。

## Global Constraints

- 参考 `公安警察工作汇报PPT.pptx` 的配色与版式，不复用无关主题、占位文字或第三方图片。
- PPT 为 16:9、9 页；视频为 16:9、1080P、2 分 50 秒至 3 分 10 秒。
- 不展示密码、Cookie、个人账号或其他敏感信息。
- 只使用可核实的项目事实；不使用未经确认的成效数据。
- 现场入口为 `https://www.xunfangbk.cn`，并准备本地 MP4 备份。

---

### Task 1: 准备内容与视觉素材

**Files:**
- Create: `deliverables/巡防百科网站项目汇报-素材清单.md`
- Create: `deliverables/assets/`
- Read: `公安警察工作汇报PPT.pptx`、`index.html`、`search-index.json`

**Produces:** 供 PPT 和视频共用的网页截图、六大模块名称和素材清单。

- [ ] **Step 1: 创建素材目录**

Run: `New-Item -ItemType Directory -Force 'deliverables/assets' | Out-Null`

- [ ] **Step 2: 截取网页素材**

在 1920×1080 浏览器窗口保存 `home.png`、`module-jingqing.png`、`search.png`、`detail.png`、`video-detail.png` 至 `deliverables/assets/`。关闭通知与书签栏，图片不得出现账号、密码或无关窗口。

- [ ] **Step 3: 写入素材清单**

在素材清单中记录每张图片的文件名、来源页、对应 PPT 页和用途。核对模块名称为“装备介绍、巡防勤务、警务训练、警情处置、法条规范、走访送教”。

- [ ] **Step 4: 检查并提交**

逐张以全屏方式查看截图，确认投影下文字清晰、无加载错误和敏感信息。提交命令：`git add deliverables/巡防百科网站项目汇报-素材清单.md && git commit -m "docs: add demo material asset inventory"`。

### Task 2: 制作领导汇报 PPT

**Files:**
- Create: `deliverables/巡防百科网站项目汇报.pptx`
- Read: `公安警察工作汇报PPT.pptx`、`deliverables/巡防百科网站项目汇报-素材清单.md`

**Produces:** 9 页、可投影展示的领导汇报 PPT。

- [ ] **Step 1: 按固定顺序建立页面**

依次创建：`巡防百科网站项目汇报`、`建设背景：基层知识获取的现实需求`、`建设思路：从知识库到巡防百科`、`网站总体架构`、`核心功能：快速定位所需知识`、`典型场景：一次快速查询`、`现场演示`、`阶段成果与推广价值`、`下一步计划`。

- [ ] **Step 2: 写入固定短文案**

第 2 页使用“资料分散、查询耗时、经验难沉淀”；第 3 页使用“知识沉淀 → 内容整理 → 网站发布 → 持续更新”；第 9 页使用“内容完善、访问管理优化、微信小程序迁移、推广应用”。每页正文最多三组信息。

- [ ] **Step 3: 应用视觉与截图**

使用深蓝主色、白色正文、浅灰辅助色和模板的章节编号、卡片、流程图语言。封面、架构、功能、场景页分别放入首页、模块、搜索和详情截图，禁止保留模板图片或占位文字。

- [ ] **Step 4: 设置现场切换提示**

第 7 页写“现场演示：模块浏览与站内搜索”；演讲者备注写“页面无法加载时立即播放本地备份视频，不停留在错误页面”。

- [ ] **Step 5: 内容与视觉验收**

运行：`python -m markitdown 'deliverables/巡防百科网站项目汇报.pptx' | Select-String -Pattern '添加标题|占位|Lorem|案件汇报|扫黑除恶'`。预期无输出。使用缩略图或导出 PDF 检查标题不截断、截图清晰、页边距充足；修复后再次检查。

- [ ] **Step 6: 提交 PPT**

Run: `git add deliverables/巡防百科网站项目汇报.pptx && git commit -m "docs: add xunfang-baike leadership presentation"`

### Task 3: 录制网站使用教程视频

**Files:**
- Create: `deliverables/巡防百科网站使用演示.mp4`
- Create: `deliverables/巡防百科网站使用演示-字幕与旁白.md`
- Create: `deliverables/video-source/`

**Produces:** 可脱网播放的 1080P 本地 MP4。

- [ ] **Step 1: 写入六段脚本**

字幕与旁白文件必须按以下时段编排：`0:00–0:15` 平台定位、`0:15–0:40` 六大模块、`0:40–1:10` 按场景浏览、`1:10–1:50` 站内搜索、`1:50–2:25` 图文与视频详情、`2:25–3:00` 持续更新服务基层实战。

- [ ] **Step 2: 录制固定操作路径**

录制“打开首页 → 展示六大模块 → 进入警情处置 → 使用站内搜索 → 打开图文/视频详情 → 回到首页”。窗口固定为 1920×1080，隐藏通知、个人资料、书签栏和任何认证信息。

- [ ] **Step 3: 合成并导出**

添加开头标题“巡防百科：基层巡防知识快速查询平台”、简短字幕和点击/搜索位置的鼠标高亮；不添加夸张转场或背景音乐。导出 H.264、1920×1080 的 `deliverables/巡防百科网站使用演示.mp4`。

- [ ] **Step 4: 验收并提交**

断网后从本地完整播放 MP4，抽查 `0:15`、`0:40`、`1:10`、`1:50`、`2:25`，确认字幕、鼠标、音量、画面无遮挡且无敏感信息。提交命令：`git add deliverables/巡防百科网站使用演示-字幕与旁白.md deliverables/巡防百科网站使用演示.mp4 && git commit -m "docs: add website usage demonstration video"`。

### Task 4: 联调与现场彩排

**Files:**
- Create: `deliverables/现场演示检查清单.md`
- Read: `deliverables/巡防百科网站项目汇报.pptx`、`deliverables/巡防百科网站使用演示.mp4`

**Produces:** 汇报当天可直接执行的检查清单。

- [ ] **Step 1: 写入连通性检查**

清单包含：投影电脑连接手机热点、访问 `https://www.xunfangbk.cn`、确认 HTTPS 锁标识、打开首页、搜索、一个模块页、一个详情页和一个视频页。

- [ ] **Step 2: 写入设备与备份检查**

清单包含：投影为 16:9、浏览器缩放为 100%、PPT 第 7 页后进入浏览器、MP4 可本地播放、音量清晰。

- [ ] **Step 3: 完成两次彩排**

第一次按“PPT 第 1–6 页 → 实机网站 → PPT 第 8–9 页”完成；第二次模拟网页无法加载并切换 MP4。记录两次总时长和发现的问题。

- [ ] **Step 4: 提交检查清单**

Run: `git add deliverables/现场演示检查清单.md && git commit -m "docs: add presentation rehearsal checklist"`
