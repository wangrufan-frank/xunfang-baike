# 公开资料索引维护说明

公开资料索引是内容的一部分。每次新增、修改或删除内容时，必须在同一次变更中同步维护 `data/public-sources.json`，并重新生成静态引用。`coverage_status: verified` 只表示人工打开网页后确认存在主题、概念或局部内容相似；它不表示来源完整支持本站文字。

来源相似性核验与有权人员的保密审查相互独立。生成工具不得自动批准页面，也不得把 `review_status` 改为 `approved`。页面是否适合公开，仍须按本单位制度完成业务、保密和发布审查。

## 新增页面

1. 在四个内容目录中新增非 `index.html` 页面，并按现有结构为每个一级知识点使用一个 `.step-card`。
2. 在台账 `pages` 中登记页面路径、标题和稳定 `page_id`，保持 `review_status: pending`、`reviewed_by: null`、`reviewed_at: null`。
3. 为每个知识点登记稳定 `point_id`、位置、标题、来源编号和具体的相似内容说明。
4. 实际打开来源正文，确认网页身份和相似点后，才填写核验日期并将来源及覆盖状态标为 `verified`。

## 新增知识点

在 HTML 增加 `.step-card` 的同一次提交中，向对应页面的 `points` 增加记录。新知识点必须关联至少一个已核验来源路径；不得先生成无来源知识点再补录。位置、标题和 `point_id` 必须与页面保持一致。

## 修改知识点

修改标题或实质内容后，重新打开现有来源并判断相似关系是否仍然成立。同步更新台账标题、`coverage_note` 和核验日期；原来源不再相似时，先寻找并核验替代来源。修改后由有权人员另行判断是否需要重新进行业务或保密审查。

## 删除内容

删除知识点或页面时，同步删除对应的台账映射。检查被引用来源是否仍被其他知识点使用；只有完全没有引用时才删除来源记录。不得在台账中保留已经不存在的页面或知识点。

## 替换失效来源

来源打不开、正文变更或主体无法确认时，将其视为不可继续使用的正式来源。寻找并实际打开相似网页，登记新来源及核验日期，更新所有相关 `source_ids` 和相似内容说明；确认不再被引用后再移除旧来源。找不到相似公开内容时，保持 `pending` 并停止生成合格版本。

## 每次变更的执行顺序

在仓库根目录依次运行：

```powershell
python tools/public_source_index.py check
python tools/public_source_index.py write
python tools/public_source_index.py write --check
python tools/public_source_index.py report --output docs/public-source-index-audit.md
python -m unittest tests.test_public_source_index.PublicSourceProductionTests -v
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

严格检查必须先通过，才可写入页面。`write --check` 应显示 0 个页面待变更，证明再次生成不会产生差异。审计报告用于人工复核来源覆盖与独立审查状态，不是发布批准记录。

## 人工复核要点

- 每个来源都应能打开正文，并记录可确认的标题、发布主体、网址和核验日期。
- `coverage_note` 要写明具体相似点；只覆盖局部或存在差异时，也要明确说明差异。
- 页面中每个一级知识点都应有编号引用，页面底部应有完整来源列表，链接应指向原始网页。
- `review_status` 由有权人员独立填写；来源覆盖完成不改变 pending 状态，也不得自动批准公开发布。
