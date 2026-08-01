# 八月每月一学实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 发布八月“汛期高温叠加：巡防现场风险识别”文章，同时将七月文章保留为可访问的往期内容。

**Architecture:** `meiyueyixue/index.html` 继续承载当前月份的正文，`2026-07.html` 作为七月归档页。两页共享 `monthlyData` 元数据，并通过根元素的 `data-monthly-issue` 选择各自应渲染的期号；八月页面在正文末尾提供公开来源链接。公开来源台账登记新增的归档页，保证内容页清单与文件系统一致。

**Tech Stack:** 静态 HTML、原生 JavaScript、SVG、JSON、Python `unittest`。

**已确认的执行修订（2026-08-02）：** 原 Task 1 与 Task 2 合并为同一个 TDD 交付任务：先写入并验证失败测试，再立即完成页面、元数据、封面和来源台账，使测试转绿后统一提交与复核。这样避免提交一个必然失败的中间任务。

## 全局约束

- 文章只写巡防先期处置、自我防护、信息上报和专业协同边界，不写涉水救援或排险的操作步骤。
- 八月内容依据应急管理部 2026-07-20 发布的《汛期高温叠加，这些安全常识必知》做原创归纳，不复制原文。
- `data/public-sources.json` 中新增页面保持 `review_status: "pending"`，不得将其自动设为 `approved`。
- 不新增第三方依赖；封面仅使用本地 SVG。

---

### Task 1: 建立八月当前页与七月归档的回归测试

**Files:**
- Modify: `tests/test_site_structure.py`
- Modify: `tests/test_public_source_index.py`

**Interfaces:**
- Consumes: `meiyueyixue/data.js` 中的 `monthlyData.current` 和期号键；`meiyueyixue/2026-07.html` 的归档文件路径。
- Produces: 对八月当前期、七月归档链接和内容清单总数的自动化回归约束。

- [ ] **Step 1: 写入失败测试，约束当前期、归档页和元数据。**

  在 `tests/test_site_structure.py` 的 `NavigationStructureTests` 中新增：

  ```python
  def test_monthly_issue_keeps_july_archive_and_selects_august(self):
      data = (ROOT / "meiyueyixue" / "data.js").read_text(encoding="utf-8")
      current = (ROOT / "meiyueyixue" / "index.html").read_text(encoding="utf-8")
      archive = ROOT / "meiyueyixue" / "2026-07.html"

      self.assertIn('current: "2026-08"', data)
      self.assertIn('"2026-07"', data)
      self.assertIn('"2026-08"', data)
      self.assertIn('2026-07.html', data)
      self.assertTrue(archive.is_file())
      self.assertIn('data-monthly-issue="2026-08"', current)
      self.assertIn('汛期高温叠加：巡防现场风险识别', current)
      self.assertIn('data-monthly-issue="2026-07"', archive.read_text(encoding="utf-8"))
  ```

- [ ] **Step 2: 运行测试，确认它因八月期号和归档页尚不存在而失败。**

  Run: `python -m unittest tests.test_site_structure.NavigationStructureTests.test_monthly_issue_keeps_july_archive_and_selects_august -v`

  Expected: FAIL，断言当前期为 `2026-08` 或断言 `meiyueyixue/2026-07.html` 存在失败。

- [ ] **Step 3: 更新来源索引计数断言。**

  在 `tests/test_public_source_index.py` 中把新增归档页后的固定计数改为：

  ```python
  self.assertEqual(len(pages), 112)
  counts = {
      'fagui': 23, 'xunlian': 24, 'zhuangbei': 30,
      'zoufang': 16, 'jingqing': 5, 'qinwu': 13,
      'meiyueyixue': 1,
  }
  ```

  并将 CLI 断言中的 `111 pages` 改为 `112 pages`，将生产台账摘要中的 `PASS: 111 pages, 153 points;` 改为 `PASS: 112 pages, 153 points;`。

- [ ] **Step 4: 运行来源索引测试，确认它因归档页和台账尚未同步而失败。**

  Run: `python -m unittest tests.test_public_source_index.PublicSourceIndexCliTests.test_inventory_command_reports_current_counts -v`

  Expected: FAIL，现有命令仍输出 `111 pages, 0 points`。

### Task 2: 发布八月文章并保留七月归档

**Files:**
- Create: `meiyueyixue/2026-07.html`
- Create: `img/monthly/2026-08-cover.svg`
- Modify: `meiyueyixue/index.html`
- Modify: `meiyueyixue/data.js`
- Modify: `data/public-sources.json`

**Interfaces:**
- Consumes: `monthlyData.articles[issue]` 的 `theme`、`summary`、`image` 和 `file` 字段。
- Produces: `2026-08` 为当前期；`2026-07.html` 为可打开的往期页；来源索引中存在 `meiyueyixue/2026-07.html`。

- [ ] **Step 1: 新增七月归档页。**

  将当前 `meiyueyixue/index.html` 的七月正文原样迁入 `meiyueyixue/2026-07.html`。在根元素写入：

  ```html
  <html lang="zh-CN" data-monthly-issue="2026-07">
  ```

  将页内脚本中期号选择改为：

  ```javascript
  var currentKey = document.documentElement.getAttribute('data-monthly-issue') || monthlyData.current;
  ```

  归档页保留导航、封面和往期卡片；数据中的七月 `file` 固定为 `2026-07.html`。

- [ ] **Step 2: 将当前页改为八月文章。**

  在 `meiyueyixue/index.html` 根元素写入 `data-monthly-issue="2026-08"`，并用以下六个一级段落替换原七月正文：

  1. `一、八月巡防的叠加风险`：说明暴雨、强对流和高温会叠加影响能见度、道路通行、人员状态和现场秩序。
  2. `二、出勤前先核四类信息`：天气预警、警情地点、人员与装备、支援联络。
  3. `三、到场先看五处风险`：积水和井盖、临水边界、雷电与裸露电气、能见度与交通、热暴露与围观聚集。
  4. `四、先期处置的安全边界`：设置警戒和绕行提示、劝离非必要人员、动态上报；超出能力范围时等待消防、应急、医疗等专业力量。
  5. `五、把天气变化纳入动态评估`：出现降雨增强、雷电、积水加深、人员不适或人流聚集时，重新评估并调整站位和警力。
  6. `六、勤务结束后的复盘清单`：记录预警、现场变化、风险提示、上报时间、协同与移交情况。

  在正文末尾加入“公开资料参考”段落，链接至：

  ```html
  <a href="https://www.mem.gov.cn/kp/zrzh/" target="_blank" rel="noopener noreferrer">应急管理部：汛期高温叠加，这些安全常识必知</a>
  ```

  同时将期号选择逻辑替换为 Task 2 Step 1 的 `data-monthly-issue` 逻辑。

- [ ] **Step 3: 更新月份元数据和封面。**

  在 `meiyueyixue/data.js` 中：

  ```javascript
  current: "2026-08"
  ```

  保留原 `2026-07` 条目并把其 `file` 设为 `2026-07.html`；新增 `2026-08` 条目，主题为 `汛期高温叠加：巡防现场风险识别`，封面路径为 `img/monthly/2026-08-cover.svg`，文件为 `index.html`。新增 SVG 使用蓝灰色雨云、橙色高温日轮和简洁巡防标识，不嵌入文字与外链资源。

- [ ] **Step 4: 同步公开来源台账。**

  在 `data/public-sources.json` 的 `pages` 新增：

  ```json
  {
    "page_id": "meiyueyixue-2026-07",
    "path": "meiyueyixue/2026-07.html",
    "title": "执法现场风险评估 — 本月精选 — 巡防百科",
    "review_status": "pending",
    "reviewed_by": null,
    "reviewed_at": null,
    "points": []
  }
  ```

  并在 `sources` 新增：

  ```json
  {
    "source_id": "official-mem-rainy-heat-2026",
    "title": "汛期高温叠加，这些安全常识必知",
    "publisher": "应急管理部",
    "platform": "中华人民共和国应急管理部",
    "url": "https://www.mem.gov.cn/kp/zrzh/",
    "published_at": "2026-07-20",
    "verified_at": "2026-08-02",
    "verification_status": "verified",
    "similarity_note": "公开资料用于核验汛期与高温叠加时的安全风险提示；本站文章仅作巡防先期处置与协同边界的原创归纳。",
    "source_level": 1,
    "last_checked_at": "2026-08-02"
  }
  ```

  不把来源核验状态当作发布审批；八月当前页的公开参考链接由正文直接展示。

- [ ] **Step 5: 运行定向测试，确认通过。**

  Run: `python -m unittest tests.test_site_structure.NavigationStructureTests.test_monthly_issue_keeps_july_archive_and_selects_august tests.test_public_source_index.PublicSourceIndexCliTests.test_inventory_command_reports_current_counts -v`

  Expected: PASS。

- [ ] **Step 6: 提交内容与测试。**

  ```bash
  git add tests/test_site_structure.py tests/test_public_source_index.py meiyueyixue/index.html meiyueyixue/2026-07.html meiyueyixue/data.js img/monthly/2026-08-cover.svg data/public-sources.json
  git commit -m "feat: publish August monthly learning article"
  ```

### Task 3: 生成索引并完成站点验证

**Files:**
- Modify: `search-index.json`（仅当生成工具报告有差异时）
- Modify: `docs/public-source-index-audit.md`（由来源索引工具生成）

**Interfaces:**
- Consumes: Task 2 中的 HTML、来源台账与测试更新。
- Produces: 无漂移的来源索引、搜索索引和站内链接验证结果。

- [ ] **Step 1: 校验并生成公开来源索引。**

  Run:

  ```powershell
  python tools/public_source_index.py check
  python tools/public_source_index.py write
  python tools/public_source_index.py write --check
  python tools/public_source_index.py report --output docs/public-source-index-audit.md
  ```

  Expected: `check` 显示 112 页、153 个知识点；`write --check` 显示 `CHECK: 0 of 112 pages would change.`。

- [ ] **Step 2: 更新并验证搜索索引和站内链接。**

  Run:

  ```powershell
  python tools/build_search_index.py
  python tools/build_search_index.py --check
  python tools/check_site_links.py
  ```

  Expected: 搜索索引无陈旧差异，链接检查通过并能解析 `meiyueyixue/2026-07.html`。

- [ ] **Step 3: 运行完整自动化验证。**

  Run:

  ```powershell
  python -m unittest discover -s tests -p "test_*.py" -v
  node --test tests/auth_core.test.js
  git diff --check
  ```

  Expected: 全部命令以退出码 0 结束；如果仓库中存在与本次无关的既有失败，记录具体失败项而不改动无关代码。

- [ ] **Step 4: 提交生成的可追踪文件。**

  ```bash
  git add search-index.json docs/public-source-index-audit.md
  git commit -m "chore: refresh August content indexes"
  ```
