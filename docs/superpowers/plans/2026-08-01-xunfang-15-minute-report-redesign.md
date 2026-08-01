# “巡防百科”15分钟汇报重构 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 交付一套可在 15 分钟内完成的 11 页汇报 PPT、60 秒网站录屏和配套讲解稿。

**Architecture:** PPT 以真实录屏和真实网站截图建立认知，再以四个场景页验证网站价值，最后以资料库、双端登录和更新表格收束。录屏、截图、PPT 和 DOCX 均输出到外部交付物归档；仓库仅保存可重复生成的讲解稿数据、构建脚本改动、测试和本计划。

**Tech Stack:** `@oai/artifact-tool`、PowerPoint PPTX、FFmpeg/ffprobe、Python 3.12、`python-docx`、Poppler/LibreOffice、现有外部交付物归档。

## Global Constraints

- 输出共 11 页，设计讲解不超过 12 分钟，连同播放、翻页与交流缓冲不超过 15 分钟。
- 第 2 页录屏固定为 60 秒，路径为“输入密码 → 首页 → 模块 → 搜索 → 详情 → 手机端”；不能展示实际密码、个人账号或浏览器通知。
- 第 3—7 页必须采用“左侧两张关联手机截图 + 右侧大结论”母版；标题不小于 40pt，结论不小于 32pt，正文和表格不小于 28pt。
- 第 8 页使用脱敏后的电脑资料库截图；第 9 页使用电脑端和手机端真实登录截图；第 10 页只使用 3 行 × 3 列更新表格。
- 脱敏与访问方式统一表述为“网站内容已作脱敏整理，并设置进入密码；作为学习参考使用，正式文件优先。”不添加未经验证的安全能力表述。
- 交付物只能写入 `E:\xunfang-baike-deliverables\deliverables\` 及其 `video-source\` 子目录，不能重新提交二进制交付物到网站仓库。
- PPT 的生成和编辑必须使用 `@oai/artifact-tool`，不得使用 `python-pptx` 或旧的 `tools/generate_demo_ppt.js`。

---

## File Structure

- Create: `data/xunfang-15-minute-report-speaker-notes.json` — 11 页讲解稿的唯一内容源。
- Modify: `tools/build_xunfang_report_speaker_notes.py` — 移除对 36 页的硬编码，继续兼容旧 36 页讲解稿并支持新 11 页数据源。
- Create: `tests/test_xunfang_15minute_report_speaker_notes.py` — 11 页数据、时长、关键边界和 DOCX 结构测试。
- Create: `tests/verify_xunfang_15minute_report.py` — 对外部最终 PPTX 的页数、关键文字和占位符进行检查。
- Create outside repo: `E:\xunfang-baike-deliverables\deliverables\assets\report-15min\` — PPT 使用的脱敏截图、录屏兜底图和素材台账。
- Create outside repo: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-demo.mp4` — 60 秒录屏。
- Create outside repo: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-report.pptx` — 最终 PPT。
- Create outside repo: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-speaker-notes.docx` — 最终讲解稿。

### Task 1: 建立脱敏素材台账与页面映射

**Files:**
- Create: `E:\xunfang-baike-deliverables\deliverables\assets\report-15min\asset-manifest.txt`
- Create: `E:\xunfang-baike-deliverables\deliverables\assets\report-15min\desktop-materials.png`
- Create: `E:\xunfang-baike-deliverables\deliverables\assets\report-15min\login-desktop.png`
- Create: `E:\xunfang-baike-deliverables\deliverables\assets\report-15min\login-mobile.png`
- Copy from: `E:\xunfang-baike-deliverables\deliverables\site-content-rebuild-screenshots\*.png`

**Interfaces:**
- Consumes: 现有首页、模块、详情和手机端截图；用户电脑中的资料目录；电脑端和手机端登录页。
- Produces: 后续 PPT 与录屏共享的命名素材，以及每张图的来源、脱敏状态和所用页码。

- [ ] **Step 1: 创建独立素材目录并写入空台账标题。**

  Run:

  ```powershell
  New-Item -ItemType Directory -Force 'E:\xunfang-baike-deliverables\deliverables\assets\report-15min' | Out-Null
  Set-Content -LiteralPath 'E:\xunfang-baike-deliverables\deliverables\assets\report-15min\asset-manifest.txt' -Encoding utf8 -Value "文件`t来源`tPPT页码`t脱敏检查`n"
  ```

- [ ] **Step 2: 复制并命名第 3—7 页所需的手机端截图。**

  保存下列配对，每对均代表同一任务路径：

  ```text
  03-home-mobile.png + 03-search-mobile.png
  04-zhuangbei-index-mobile.png + 04-zhuangbei-article-mobile.png
  05-fagui-index-mobile.png + 05-fagui-article-mobile.png
  06-xunlian-index-mobile.png + 06-xunlian-article-mobile.png
  07-jingqing-index-mobile.png + 07-jingqing-article-mobile.png
  ```

  如原归档没有对应的装备注释页，先用原站在手机视口重新截取后再继续；不使用桌面截图替代。

- [ ] **Step 3: 截取第 8、9 页的用户素材。**

  `desktop-materials.png` 只显示已脱敏的文件/目录清单，遮盖不宜展示的路径、文件名、修改人、账号和元数据；`login-desktop.png`、`login-mobile.png` 显示进入密码界面，但密码输入框为空且不展示浏览器保存的凭据。

- [ ] **Step 4: 完成资产台账。**

  每行填写 `文件名、来源、PPT 页码、脱敏检查`；例如：

  ```text
  06-xunlian-index-mobile.png	现有归档截图	6	已检查：无账号、密码和浏览器通知
  desktop-materials.png	汇报人电脑资料目录	8	已遮盖：路径与不宜展示文件名
  ```

- [ ] **Step 5: 全屏检查并验证输入。**

  逐张打开截图，确认手机图中文字可放大、无密码或个人信息；运行：

  ```powershell
  Get-ChildItem 'E:\xunfang-baike-deliverables\deliverables\assets\report-15min' -File | Select-Object Name,Length
  ```

  Expected: 10 张以上 PNG 文件与 `asset-manifest.txt` 均存在，且目录中没有空文件。

### Task 2: 制作并验证 60 秒录屏

**Files:**
- Create: `E:\xunfang-baike-deliverables\deliverables\video-source\xunfang-15-minute-demo\script.txt`
- Create: `E:\xunfang-baike-deliverables\deliverables\video-source\xunfang-15-minute-demo\capture-checklist.txt`
- Create: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-demo.mp4`

**Interfaces:**
- Consumes: Task 1 的登录与站点素材、`https://www.xunfangbk.cn` 的实际页面。
- Produces: 第 2 页可嵌入或本地播放的 1920×1080、60 秒 MP4，以及同路径的静态关键帧。

- [ ] **Step 1: 写入严格 60 秒旁白脚本。**

  `script.txt` 必须使用以下六段，录音后总时长控制在 `00:58—01:00`：

  ```text
  00:00—00:08  输入进入密码，进入网站。
  00:08—00:16  首页集中呈现六类业务入口。
  00:16—00:26  从一个代表性模块进入任务相关内容。
  00:26—00:40  关键词搜索用于直接定位内容。
  00:40—00:50  详情页把图文要点集中在同一页面。
  00:50—01:00  手机端也保持同样的查阅路径。
  ```

- [ ] **Step 2: 按固定环境录屏。**

  使用 1920×1080 浏览器窗口，隐藏通知、收藏栏、账号头像、自动填充密码与其它应用窗口；按脚本完成一次连续操作，单独录制旁白或在后期加入字幕。每次搜索与跳转完成后停留至少 1 秒，避免观众看不清页面。

- [ ] **Step 3: 以 HyperFrames 或 FFmpeg 完成剪辑。**

  保留操作原声或清晰旁白，不添加背景音乐和花哨转场；只添加六段简短字幕和淡入淡出。导出 H.264、1920×1080、`yuv420p` 的最终 MP4，并从 `00:08` 导出 `demo-fallback-frame.png` 到 Task 1 的素材目录。

- [ ] **Step 4: 校验时长和可播放性。**

  Run:

  ```powershell
  ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 'E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-demo.mp4'
  ```

  Expected: 数值大于等于 `58` 且小于等于 `60`。本地播放一次，分别检查 8、16、26、40、50 秒位置的画面与字幕。

### Task 3: 将讲解稿改为可支持 11 页的内容源与构建器

**Files:**
- Create: `data/xunfang-15-minute-report-speaker-notes.json`
- Modify: `tools/build_xunfang_report_speaker_notes.py`
- Create: `tests/test_xunfang_15minute_report_speaker_notes.py`
- Test: `tests/test_xunfang_report_speaker_notes.py`

**Interfaces:**
- Consumes: 已确认的设计说明、60 秒录屏时间码与 11 页标题。
- Produces: `build_document(content_path, output_path, expected_slides=None)`，它可从任意连续页码 JSON 生成 DOCX；新 JSON 输出 11 页讲解稿。

- [ ] **Step 1: 写入先失败的 11 页数据测试。**

  在新测试文件中加入：

  ```python
  def test_has_eleven_ordered_slides_and_twelve_minute_script():
      payload = json.loads(CONTENT.read_text(encoding="utf-8"))
      slides = payload["slides"]
      assert [slide["number"] for slide in slides] == list(range(1, 12))
      assert sum(slide["suggested_seconds"] for slide in slides) <= 720
      text = "\n".join(slide["script"] + slide["transition"] for slide in slides)
      assert "内容已作脱敏整理，并设置进入密码" in text
      assert "正式文件优先" in text
  ```

- [ ] **Step 2: 运行测试确认当前状态失败。**

  Run:

  ```powershell
  python -m unittest tests.test_xunfang_15minute_report_speaker_notes -v
  ```

  Expected: FAIL，原因是新 JSON 与通用 11 页构建支持尚不存在。

- [ ] **Step 3: 写入 11 页讲解 JSON。**

  每页使用 `number`、`title`、`suggested_seconds`、`cue`、`script`、`transition` 六个字段；标题和秒数固定为：

  ```text
  1 封面 20；2 60秒网站效果录屏 60；3 网站能做什么 45；
  4 日常巡逻准备 80；5 法规与业务查询 80；6 训练备课 80；
  7 复盘讨论与走访送教 80；8 我是怎么搭建的 90；
  9 脱敏与访问方式 70；10 后续更新布局 90；11 结束页 25。
  ```

  第 2 页 `cue` 必须写明“播放 xunfang-15-minute-demo.mp4，播放失败则显示 demo-fallback-frame.png”；第 4—7 页每页按“现实任务 → 截图路径 → 便利结论”三段写作。

- [ ] **Step 4: 最小化修改 DOCX 构建器。**

  将原 `build_document` 中的 `len(payload["slides"]) != 36` 改为：

  ```python
  expected = expected_slides if expected_slides is not None else len(payload["slides"])
  if len(payload["slides"]) != expected:
      raise ValueError(f"Speaker notes must contain exactly {expected} slides")
  ```

  同时让 `add_cover` 和 `add_usage_guide` 从 JSON 的 `title`、`audience`、`estimated_minutes` 读取文字；章节分页使用 `payload.get("section_starts", [1])`，保留旧 JSON 的 36 页默认行为。

- [ ] **Step 5: 生成 DOCX 并运行回归测试。**

  Run:

  ```powershell
  python tools/build_xunfang_report_speaker_notes.py --content data/xunfang-15-minute-report-speaker-notes.json --output 'E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-speaker-notes.docx'
  python -m unittest tests.test_xunfang_15minute_report_speaker_notes tests.test_xunfang_report_speaker_notes -v
  ```

  Expected: 两个测试模块均 PASS，DOCX 存在且有 11 个“第X页”标题。

- [ ] **Step 6: 提交可重复生成的讲解稿源。**

  Run:

  ```powershell
  git add data/xunfang-15-minute-report-speaker-notes.json tools/build_xunfang_report_speaker_notes.py tests/test_xunfang_15minute_report_speaker_notes.py
  git commit -m "docs: add 15-minute report speaker notes"
  ```

### Task 4: 以 Artifact Tool 制作 11 页 PPT

**Files:**
- Create in a temporary artifact workspace: `$TMP_DIR\build-xunfang-15-minute-report.mjs`
- Create in a temporary artifact workspace: `$TMP_DIR\source-notes.txt`
- Create: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-report.pptx`
- Test: `tests/verify_xunfang_15minute_report.py`

**Interfaces:**
- Consumes: Task 1 素材目录、Task 2 MP4 和静态关键帧、Task 3 的 11 页 JSON。
- Produces: 16:9 的 11 页 PPTX；每个页面与 JSON 同页号、同标题、同讲解时长。

- [ ] **Step 1: 先写 PPT 结构验证器并确认它失败。**

  `tests/verify_xunfang_15minute_report.py` 使用 `zipfile` 和 `xml.etree.ElementTree`，检查：文件存在、`ppt/slides/slide*.xml` 恰好 11 个、文本中含“分类可找、搜索可查、手机可用”“内容已作脱敏整理”“后续更新布局”，且不含“添加标题”“Lorem”“TODO”。

  Run:

  ```powershell
  python tests/verify_xunfang_15minute_report.py
  ```

  Expected: FAIL，原因是新 PPTX 尚不存在。

- [ ] **Step 2: 初始化 Artifact Tool 工作区。**

  设置 `SKILL_DIR` 为 presentations 技能目录，设置 `$TMP_DIR` 为工作区内临时目录，设置 `$FINAL_PPTX` 为最终 PPTX 路径；运行：

  ```powershell
  node "$SKILL_DIR\container_tools\setup_artifact_tool_workspace.mjs" --workspace "$TMP_DIR"
  ```

  在实现前读取 `$SKILL_DIR\style_guidelines.md`、`artifact_tool_docs\API_QUICK_START.md` 与 `artifact_tool_docs\api\API_DOCS.md`。

- [ ] **Step 3: 在 `.mjs` 内定义唯一页面数据并按 11 页生成。**

  页面数组必须与 Task 3 的页码、标题完全一致。第 3—7 页使用同一 `addDualMobileSlide(slide, leftImage, rightImage, label, headline, body)` 函数；函数只生成两部等高手机框、一个红色场景标签、一个右侧大标题和两行正文。第 8 页生成电脑资料截图加“归集、筛选、脱敏、结构化”；第 9 页生成双端登录图加三点说明；第 10 页生成以下表格：

  ```text
  补充内容｜按模块补充新装备、新规范和新场景｜内容覆盖更贴近实际任务
  定期维护｜定期收集、复核、更新和下线｜保持资料可用、可查
  移动端优化｜优化字体、目录、图片、视频和搜索｜手机查阅更清晰、更方便
  ```

- [ ] **Step 4: 放入录屏与故障兜底。**

  第 2 页以视频缩略图、播放图标与“60秒演示”提示形成播放页。若 Artifact Tool 支持嵌入本地媒体，则嵌入 `xunfang-15-minute-demo.mp4`；若其 API 不支持嵌入，则在缩略图上设置指向同目录 MP4 的本地动作链接，并在演讲者备注写明“播放失败切换 demo-fallback-frame.png”。无论哪种实现，都要在 PPT 同目录保留 MP4 和关键帧。

- [ ] **Step 5: 导出并验证文本结构。**

  Run:

  ```powershell
  node "$TMP_DIR\build-xunfang-15-minute-report.mjs"
  python tests/verify_xunfang_15minute_report.py
  ```

  Expected: 构建成功且验证器输出 `presentation verified: 11 slides, no placeholders`。

- [ ] **Step 6: 提交 PPT 验证器。**

  Run:

  ```powershell
  git add tests/verify_xunfang_15minute_report.py
  git commit -m "test: verify 15-minute report presentation"
  ```

### Task 5: 渲染、视觉 QA 与 15 分钟彩排

**Files:**
- Create: `E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-qa.txt`
- Modify if needed: Task 2 MP4、Task 3 JSON、Task 4 PPTX。

**Interfaces:**
- Consumes: 三份最终交付物与设计说明中的页面验收标准。
- Produces: 已逐页检查、可在会议室大屏播放的最终交付物和 QA 记录。

- [ ] **Step 1: 渲染并逐页检查 PPT。**

  Run:

  ```powershell
  python "$SKILL_DIR\container_tools\render_slides.py" 'E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-report.pptx'
  python "$SKILL_DIR\container_tools\slides_test.py" 'E:\xunfang-baike-deliverables\deliverables\xunfang-15-minute-report.pptx'
  ```

  逐页以全尺寸查看渲染图；确认第 3—7 页均有两张手机截图、右侧标题不换行、第 8 页资料截图已脱敏、第 9 页空密码框未显示凭据、第 10 页三行表格完整可读。

- [ ] **Step 2: 渲染并检查讲解稿。**

  使用 documents 技能规定的 `render_docx.py` 将 DOCX 转为页面 PNG；检查每页有清晰标题、建议时间、操作提示和衔接语，不出现标题孤行、文字裁切或意外空白。

- [ ] **Step 3: 做一次完整计时彩排。**

  使用 PPT 播放、第 2 页视频和 DOCX 讲解稿完成一遍完整彩排；记录开始、视频结束、场景页结束、PPT 结束四个时间点。总时长超过 15 分钟时，优先压缩第 4—7 页的口头举例，不缩小 PPT 字号，不加快视频播放。

- [ ] **Step 4: 写入 QA 结果并进行最终验证。**

  `xunfang-15-minute-qa.txt` 每页记录“页码、检查结果、修复项”；最后记录 MP4 时长、DOCX 页数、彩排总时长。运行：

  ```powershell
  python tests/verify_xunfang_15minute_report.py
  python -m unittest tests.test_xunfang_15minute_report_speaker_notes tests.test_xunfang_report_speaker_notes -v
  ```

  Expected: 两项命令均 PASS，QA 记录中的彩排总时长不大于 15:00。

- [ ] **Step 5: 校验外部归档而不覆盖它。**

  新交付物确认无误后，更新外部归档的 `manifest.tsv` 与仓库副本 `docs/deliverables-archive-manifest.tsv`，并验证两份清单 SHA-256 一致；不得运行首次归档工具覆盖现有归档目录。
