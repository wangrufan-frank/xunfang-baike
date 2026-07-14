# 巡防百科敏感内容删除整改实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 从当前网站和微信小程序运行时文件中彻底移除已确认的敏感内容，并将警情处置栏目改为“内容整改中”。

**Architecture:** 先用标准库回归测试锁定禁止出现的文件、标题、链接和搜索记录，再删除详情页、收缩栏目入口并清理交叉引用。网站 HTML 是主要内容源；删除后运行已检查过的 `parse_html.py` 重建 qinwu、xunlian、zoufang 小程序数据，警情处置数据和占位页单独处理，最后机械过滤搜索索引并执行全库验证。

**Tech Stack:** 静态 HTML/CSS/JavaScript、微信小程序 JavaScript/WXML、Python 3 `unittest`、PowerShell、现有 `parse_html.py`

## Global Constraints

- 仅修改 `F:\frank第二大脑\xunfang-baike` 当前工作树，不修改 `F:\frank第二大脑\xunfang-baike-backup-2026-07-14`。
- 不清理或改写 Git 历史，不上传、推送或部署。
- 运行时文件不得保留指定内容的详情、摘要、入口、搜索记录或交叉推荐。
- `jingqing/index.html` 与小程序警情处置页必须保留并显示“内容整改中”。
- 指定详情 URL 必须失效，不创建详情占位页。
- 共享素材只有在无保留页面引用时才删除。
- 保留用户现有未跟踪文件 `公安警察工作汇报PPT.pptx`，不加入任何提交。

---

### Task 1: 建立整改回归测试

**Files:**
- Create: `tests/test_sensitive_content_removal.py`

**Interfaces:**
- Consumes: 仓库当前运行时文件、`search-index.json`、网站与小程序入口文件。
- Produces: `SensitiveContentRemovalTests`，作为后续每项删除的验收门禁。

- [ ] **Step 1: 编写失败测试**

测试定义以下常量：

```python
DELETED_PATHS = {
    'qinwu/yanchanghui-zhifa.html', 'qinwu/xiaoyuan-jinrong.html',
    'qinwu/yuqing-zhanshu.html', 'qinwu/chuzhi-yuan.html',
    'qinwu/kongzhi-daili.html', 'qinwu/shewen-yanlian.html',
    'qinwu/xuanchuan-quzheng.html', 'qinwu/yuqing-daokong.html',
    'xunlian/zhudong-hengyi.html', 'xunlian/xunlian-jiaoxuefa.html',
    'xunlian/shizi-fangyu.html', 'xunlian/sinengli-yaosu.html',
    'xunlian/gaishu-yuanze.html', 'xunlian/wuli-shengji.html',
    'jingqing/chidao-jingqing.html', 'jingqing/chidao-leiqing.html',
    'jingqing/dajia-douou.html', 'jingqing/jizhi-liucheng.html',
    'jingqing/keyi-cheliang.html', 'jingqing/renyuan-pancha.html',
    'jingqing/zuijiu-naoshi.html',
    'zoufang/xianchang-chuzhi.html', 'zoufang/zhengzhi-hexinqu.html',
    'zoufang/daxing-huodong.html',
}

FORBIDDEN_RUNTIME_TERMS = {
    '大型活动安保', '群体事件处置', '主动横移压缩空间战法',
    '训练教学法', '十字防御技能', '快反技能', '反恐基础理论',
    '现场处置执法规范', '政治核心区处置', '大型活动安保执法',
}
```

实现以下测试：逐一断言 `DELETED_PATHS` 不存在；扫描运行时扩展名 `.html/.js/.json/.wxml/.wxss`，排除 `.git`、`.worktrees`、`.superpowers`、`docs`、`deliverables` 与测试自身，断言 `FORBIDDEN_RUNTIME_TERMS` 和删除路径均无命中；解析 `search-index.json` 并断言路径不在删除集合；断言网站和小程序警情页包含“内容整改中”；断言 `miniprogram/data/jingqing.js` 等于 `module.exports = [];`；断言小程序首页不再含有 `醉酒闹事处置` 或 `家暴警情` 案例；解析所有本地 HTML `href` 并断言不存在指向缺失 HTML 的内部链接。警情文章中可能与其他保留课程共用的普通词语（例如“人员盘查”）不作为全库禁词，仅通过文件、路径、数据和入口断言清理。

- [ ] **Step 2: 运行测试确认整改前失败**

Run:

```powershell
python -m unittest tests.test_sensitive_content_removal -v
```

Expected: FAIL，至少报告指定详情文件仍存在、禁止标题仍在运行时文件中以及警情页缺少“内容整改中”。

- [ ] **Step 3: 提交测试**

```powershell
git add tests/test_sensitive_content_removal.py
git commit -m "test: define sensitive content removal checks"
```

### Task 2: 删除网站详情并收缩栏目页

**Files:**
- Delete: `qinwu/yanchanghui-zhifa.html`
- Delete: `qinwu/xiaoyuan-jinrong.html`
- Delete: `qinwu/yuqing-zhanshu.html`
- Delete: `qinwu/chuzhi-yuan.html`
- Delete: `qinwu/kongzhi-daili.html`
- Delete: `qinwu/shewen-yanlian.html`
- Delete: `qinwu/xuanchuan-quzheng.html`
- Delete: `qinwu/yuqing-daokong.html`
- Delete: `xunlian/zhudong-hengyi.html`
- Delete: `xunlian/xunlian-jiaoxuefa.html`
- Delete: `xunlian/shizi-fangyu.html`
- Delete: `xunlian/sinengli-yaosu.html`
- Delete: `xunlian/gaishu-yuanze.html`
- Delete: `xunlian/wuli-shengji.html`
- Delete: `jingqing/chidao-jingqing.html`
- Delete: `jingqing/chidao-leiqing.html`
- Delete: `jingqing/dajia-douou.html`
- Delete: `jingqing/jizhi-liucheng.html`
- Delete: `jingqing/keyi-cheliang.html`
- Delete: `jingqing/renyuan-pancha.html`
- Delete: `jingqing/zuijiu-naoshi.html`
- Delete: `zoufang/xianchang-chuzhi.html`
- Delete: `zoufang/zhengzhi-hexinqu.html`
- Delete: `zoufang/daxing-huodong.html`
- Modify: `qinwu/index.html`
- Modify: `xunlian/index.html`
- Modify: `jingqing/index.html`
- Modify: `zoufang/index.html`

**Interfaces:**
- Consumes: 已批准的删除清单。
- Produces: 无指定详情文件的静态站点栏目结构；警情栏目提供唯一整改占位页。

- [ ] **Step 1: 删除 24 个已确认详情文件**

使用 `apply_patch` 删除上方列出的全部文件；不存在的历史数据条目 `xunlian/duncha-zhanzhu.html` 与 `jingqing/jiating-baoli.html` 不创建也不纳入删除数。

- [ ] **Step 2: 更新四个栏目页**

`qinwu/index.html` 删除“大型活动安保”和“群体事件处置”全部分组与卡片，只保留页面通用结构；`xunlian/index.html` 删除 7 个数据入口（包括没有 HTML 的 `duncha-zhanzhu`）及三个空分组；`zoufang/index.html` 删除三个指定条目并将篇数改为 3；`jingqing/index.html` 删除搜索、篇数、标签、分组和详情链接，内容区只保留：

```html
<div class="page-container list-page">
  <div class="page-title">
    <h1>🚨 警情处置</h1>
  </div>
  <div class="empty-state">内容整改中</div>
</div>
```

- [ ] **Step 3: 运行回归测试观察剩余失败项**

Run: `python -m unittest tests.test_sensitive_content_removal -v`

Expected: 删除文件断言通过；首页、小程序、交叉引用和搜索索引相关断言仍失败。

- [ ] **Step 4: 提交网站详情与栏目整改**

```powershell
git add qinwu xunlian jingqing zoufang
git commit -m "fix: remove restricted site articles"
```

### Task 3: 清理保留页面中的入口与交叉引用

**Files:**
- Modify: `index.html`
- Modify: `xunlian/duncha-xietong.html`
- Modify: `xunlian/wuli-shengji-sanfang.html`
- Modify: `xunlian/zhanshu-zhanwei-xunluo.html`
- Modify: `zoufang/xiaoyuan-fankong.html`

**Interfaces:**
- Consumes: Task 2 的保留页面集合。
- Produces: 不再展示或链接指定内容的静态网站。

- [ ] **Step 1: 更新网站首页模块和每日一学**

删除“巡防勤务”模块卡；将“警情处置”卡改为“内容整改中”且不列篇数和旧标题；将警务训练计数按实际保留详情数更新；将走访送教计数改为 3，并只列保留内容。删除首页中来自已清空警情模块的每日案例、摘要和链接。

- [ ] **Step 2: 清除保留详情页中的交叉推荐**

删除 `duncha-xietong.html`、`wuli-shengji-sanfang.html` 对主动横移和训练教学法的推荐；删除 `zhanshu-zhanwei-xunluo.html` 对十字防御的推荐；删除 `zoufang/xiaoyuan-fankong.html` 对大型活动安保执法的推荐；删除所有指向本次详情路径的上一页/下一页链接并把保留文章串联到仍存在的相邻文章。

`video/十字防御姿势示意视频.mp4` 继续保留，因为 `xunlian/jietuo-fangyu.html` 仍在使用；该共享素材不是独立条目入口。

- [ ] **Step 3: 扫描并修复残余运行时命中**

Run:

```powershell
Get-ChildItem -File -Recurse | Where-Object { $_.Extension -in '.html','.js','.json','.wxml','.wxss' } | Select-String -SimpleMatch -Pattern '大型活动安保','群体事件处置','主动横移压缩空间战法','训练教学法','十字防御技能','快反技能','反恐基础理论','现场处置执法规范','政治核心区处置','大型活动安保执法'
```

Expected: 仅小程序数据和 `search-index.json` 仍可能命中，静态 HTML 不命中。

- [ ] **Step 4: 提交入口与交叉引用清理**

```powershell
git add index.html xunlian zoufang
git commit -m "fix: remove restricted site references"
```

### Task 4: 重建并整改微信小程序内容

**Files:**
- Modify (generated): `miniprogram/data/qinwu.js`
- Modify (generated): `miniprogram/data/xunlian.js`
- Modify: `miniprogram/data/jingqing.js`
- Modify (generated): `miniprogram/data/zoufang.js`
- Modify: `miniprogram/pages/index/index.js`
- Modify: `miniprogram/pages/index/index.wxml`
- Modify: `miniprogram/pages/jingqing/index/index.js`
- Modify: `miniprogram/pages/jingqing/index/index.wxml`
- Modify: `miniprogram/pages/jingqing/detail/detail.js`

**Interfaces:**
- Consumes: Task 2 和 Task 3 清理后的 HTML 内容源。
- Produces: 不含指定数据的小程序；警情页仅显示整改状态。

- [ ] **Step 1: 用已检查的维护脚本重建内容数据**

Run: `python parse_html.py`

Expected: qinwu 输出 0 篇；xunlian 只含实际保留的 HTML；zoufang 输出 3 篇；fagui 内容保持等价。

- [ ] **Step 2: 清空警情数据并改造栏目页**

将 `miniprogram/data/jingqing.js` 改为：

```javascript
module.exports = [];
```

`pages/jingqing/index/index.js` 不再导入或搜索文章，只维护 tab 选中状态；`index.wxml` 删除搜索框、篇数和列表，保留标题及 `<view class="empty-state">内容整改中</view>`。`detail.js` 不再导入旧数据，直接提示内容不可用并返回栏目页，避免旧小程序路径显示缓存逻辑。

- [ ] **Step 3: 清理小程序首页**

从 `pages/index/index.js` 的 `show`、搜索卡片和每日案例中移除 qinwu 以及已清空的警情内容；保留 jingqing 卡作为整改入口。从 `index.wxml` 删除巡防勤务卡，把警情卡改成“内容整改中”，并更新训练、走访送教计数和热词。

- [ ] **Step 4: 运行回归测试**

Run: `python -m unittest tests.test_sensitive_content_removal -v`

Expected: 小程序数据与占位页断言通过；只允许搜索索引相关断言继续失败。

- [ ] **Step 5: 提交小程序整改**

```powershell
git add miniprogram
git commit -m "fix: remove restricted mini program content"
```

### Task 5: 清理搜索索引并完成验证

**Files:**
- Modify: `search-index.json`

**Interfaces:**
- Consumes: `DELETED_PATHS` 与当前搜索索引数组。
- Produces: 只引用现存允许页面的合法 JSON 搜索索引。

- [ ] **Step 1: 机械过滤搜索索引**

以 `path` 为键删除 `DELETED_PATHS` 中的全部记录，保持剩余对象字段和 UTF-8 编码不变；不得手工重写内容字段。解析结果必须仍为 JSON 数组。

- [ ] **Step 2: 运行专项与既有测试**

Run:

```powershell
python -m unittest tests.test_sensitive_content_removal -v
python -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: 全部 PASS。

- [ ] **Step 3: 执行最终文件和关键词验证**

运行删除路径存在性检查、运行时关键词扫描、`search-index.json` JSON 解析、HTML 内链检查，以及 `git diff --check`。

Expected: 24 个指定详情文件均不存在；运行时文件不命中禁止标题或旧路径；搜索索引只含现存页面；HTML 无新增断链；`git diff --check` 无错误。

- [ ] **Step 4: 检查工作树边界**

Run:

```powershell
git status --short
git diff --stat HEAD~4..HEAD
```

Expected: 仅本计划涉及的整改和测试文件有变动；`公安警察工作汇报PPT.pptx` 仍保持未跟踪且未提交；备份目录无修改。

- [ ] **Step 5: 提交搜索索引整改**

```powershell
git add search-index.json
git commit -m "fix: purge restricted search records"
```
