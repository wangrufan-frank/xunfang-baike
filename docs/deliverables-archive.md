# 外部交付物归档

网站运行代码不再保存演示视频、音频、PPT、DOCX、截图和视频制作工程。这些非运行交付物的已验证副本存放在：

```text
E:\xunfang-baike-deliverables
```

归档根目录保留原始相对结构：`deliverables/` 和 `video/`。根目录的 `manifest.tsv` 与仓库中的 `docs/deliverables-archive-manifest.tsv` 必须字节一致。

## 校验格式

清单为 UTF-8 TSV，每行依次是：`sha256`、`bytes`、`path`。路径使用 `/` 分隔，相对归档根目录。迁移完成时两边各有 77 个文件。

## 验证

`tools/archive_deliverables.py` 只适用于首次归档且目标目录为空；它会复制后比较每个文件的路径、大小和 SHA-256。当前仓库已经移除了源目录，不能再次用该命令覆盖现有归档。

对既有归档进行检查时，先确认两个清单字节一致：

```powershell
Get-FileHash E:\xunfang-baike-deliverables\manifest.tsv -Algorithm SHA256
Get-FileHash docs\deliverables-archive-manifest.tsv -Algorithm SHA256
```

随后使用 `Get-FileHash` 将归档中的每个文件与清单逐项比较；不能覆盖归档目录。

## 恢复

如需恢复历史交付物，先将归档内的 `deliverables/` 或 `video/` 复制回仓库根目录，再用 `manifest.tsv` 校验。旧 Git 提交同样保留这些文件，因此也可以通过 `git show <commit>:<path>` 恢复单个文件。不要把恢复出的二进制交付物重新提交到当前代码仓库。

`tools/generate_demo_ppt.js` 默认写入该归档目录；可用环境变量 `XUNFANG_DELIVERABLES_DIR` 指向另一份已验证归档。
