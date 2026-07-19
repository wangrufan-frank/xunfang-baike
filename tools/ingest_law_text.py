"""从纯文本文件读取法规全文，更新 legal-documents.json。

用法：
  1. 编辑 data/legal-texts/{law_id}.txt（格式见该文件顶部注释）
  2. 运行:  python tools/ingest_law_text.py              # 全部处理
           python tools/ingest_law_text.py --check       # 仅校验不改写
           python tools/ingest_law_text.py 治安管理处罚法  # 只处理一部

文本格式（极简单）：
  ## 第一章 总则           ← 章标题（两个 # 开头）
  ### 第一条               ← 条标题（三个 # 开头）
  条文正文第一段。
  条文正文第二段。         ← 条正文（空行分隔不同条）

  ### 第二条
  正文内容……
"""

from argparse import ArgumentParser
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / 'data' / 'legal-texts'
LEDGER_PATH = ROOT / 'data' / 'legal-documents.json'

# 法规文件列表：文件名（不含 .txt）= legal-documents.json 中的 id
LAW_FILES = {
    'zhian-guanli-chufa-fa': '治安管理处罚法',
    'renmin-jingcha-fa': '人民警察法',
    'jumin-shenfenzheng-fa': '居民身份证法',
    'xingzheng-anji-chengxu-guiding': '行政案件程序规定',
    'xianchang-zhizhi-guicheng': '现场制止操作规程',
}


def parse_law_text(text: str) -> list[dict]:
    """将纯文本解析为 chapters[] 结构。"""
    chapters = []
    current_chapter = None
    current_article = None

    lines = text.split('\n')

    for line in lines:
        line = line.rstrip()

        # 章标题：## 第一章 总则
        chapter_match = re.match(r'^##\s+(.+)$', line)
        if chapter_match:
            if current_chapter is not None:
                if current_article is not None:
                    current_chapter['articles'].append(current_article)
                    current_article = None
                chapters.append(current_chapter)

            title = chapter_match.group(1).strip()
            # 尝试提取章编号
            number_match = re.match(r'(第[一二三四五六七八九十百]+章)\s*(.*)', title)
            if number_match:
                number = number_match.group(1)
                chapter_title = number_match.group(2) or number
            else:
                number = title
                chapter_title = title

            current_chapter = {
                'number': number,
                'title': chapter_title,
                'articles': [],
            }
            continue

        # 条标题：### 第一条
        article_match = re.match(r'^###\s+(.+)$', line)
        if article_match:
            if current_chapter is None:
                current_chapter = {
                    'number': '',
                    'title': '',
                    'articles': [],
                }

            if current_article is not None:
                current_chapter['articles'].append(current_article)

            label = article_match.group(1).strip()
            number_match = re.match(r'第([一二三四五六七八九十百千零\d]+)条', label)
            if number_match:
                try:
                    number = _cn_to_int(number_match.group(1))
                except ValueError:
                    number = len(current_chapter['articles']) + 1
            else:
                number = len(current_chapter['articles']) + 1

            current_article = {
                'number': number,
                'label': label if label.startswith('第') else f'第{label}条',
                'paragraphs': [],
            }
            continue

        # 空行 → 可能在条与条之间，但如果正在收集中则忽略
        if not line.strip():
            continue

        # 正文行
        if current_article is not None:
            current_article['paragraphs'].append(line.strip())

    # 收尾
    if current_article is not None and current_chapter is not None:
        current_chapter['articles'].append(current_article)
    if current_chapter is not None:
        chapters.append(current_chapter)

    return chapters


def _cn_to_int(s: str) -> int:
    """将中文数字转为整数，如 '一百一十九' → 119。"""
    cn_map = {
        '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
        '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '十': 10, '百': 100, '千': 1000,
    }
    # 也支持阿拉伯数字
    if s.isdigit():
        return int(s)

    result = 0
    temp = 0
    for ch in s:
        if ch == '百':
            temp *= 100
            result += temp
            temp = 0
        elif ch == '十':
            if temp == 0:
                temp = 1
            temp *= 10
            result += temp
            temp = 0
        else:
            val = cn_map.get(ch)
            if val is None:
                raise ValueError(f'无法解析数字: {s!r} 中的 {ch!r}')
            temp += val
    result += temp
    return result


def ingest_one(law_id: str, ledger: dict, *, check_only: bool = False) -> bool:
    """读取一部法规的 txt 文件，更新 ledger。返回是否成功。"""
    txt_path = TEXT_DIR / f'{law_id}.txt'
    if not txt_path.exists():
        # 创建模板
        template = _make_template(law_id, ledger)
        txt_path.write_text(template, encoding='utf-8')
        print(f'📝 已创建模板: {txt_path}')
        print(f'   请在 VS Code 中打开此文件，按注释格式填入法规正文后再次运行。')
        return False

    text = txt_path.read_text(encoding='utf-8')
    chapters = parse_law_text(text)

    total_articles = sum(len(ch['articles']) for ch in chapters)
    if total_articles == 0:
        print(f'⚠️  {law_id}: 未解析到任何条文，请检查格式是否正确。')
        print(f'   格式：## 章标题  +  ### 第X条  +  正文段落')
        return False

    # 更新 ledger
    doc = next((d for d in ledger['documents'] if d['id'] == law_id), None)
    if doc is None:
        print(f'❌ legal-documents.json 中找不到 id={law_id}')
        return False

    if check_only:
        # 只打印校验信息
        print(f'🔍 {law_id}: {len(chapters)} 章, {total_articles} 条')
        for ch in chapters[:3]:
            arts = [a['label'] for a in ch['articles'][:3]]
            print(f'   {ch["number"]} {ch["title"]}: {", ".join(arts)}')
        if len(chapters) > 3:
            print(f'   ... 共 {len(chapters)} 章')
        return True

    doc['chapters'] = chapters
    doc['partial'] = False
    doc['verified_at'] = doc.get('verified_at', '2026-07-19')

    print(f'✅ {law_id}: {len(chapters)} 章, {total_articles} 条 → 已写入 legal-documents.json')
    return True


def _make_template(law_id: str, ledger: dict) -> str:
    """为一部法规生成模板文件。"""
    doc = next((d for d in ledger['documents'] if d['id'] == law_id), None)
    title = doc['title'] if doc else law_id
    source_url = doc.get('source_url', '') if doc else ''

    # 保留已有的条文作为示例
    existing_articles = []
    if doc:
        for ch in doc['chapters']:
            for art in ch['articles']:
                text = '\n'.join(art.get('paragraphs', []))
                existing_articles.append(f'### {art["label"]}\n{text}')

    existing_block = '\n\n'.join(existing_articles) if existing_articles else '### 第一条\n（在此填入正文）'

    return f'''# {title}
# 官方来源: {source_url}
#
# 填写说明（看完后可删除本注释）：
#   1. 从以下网站获取现行有效版本全文：
#      - 国家法律法规数据库: https://flk.npc.gov.cn
#      - 国家行政法规库: https://xzfg.moj.gov.cn
#   2. 按下面格式填入（"## 章名" + "### 第X条" + 正文段落）
#   3. 填完后运行: python tools/ingest_law_text.py
#   4. 然后运行: python tools/build_legal_pages.py
#
# 格式规则：
#   ## 第一章 总则         ← 两个 # 开头 = 章标题
#   ### 第一条              ← 三个 # 开头 = 条标题
#   条文正文第一段。         ← 条正文，多段就多行
#   条文正文第二段。
#                            ← 空行分隔不同条
#   ### 第二条
#   正文内容……
#
# ── 以下是模板正文，请替换为完整内容 ──

{existing_block}
'''


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('law', nargs='?', help='要处理的法规 id（不指定则全部处理）')
    parser.add_argument('--check', action='store_true', help='仅校验，不写入')
    args = parser.parse_args()

    ledger = json.loads(LEDGER_PATH.read_text(encoding='utf-8'))

    if args.law:
        # 支持中文名或 id
        law_id = args.law
        for lid, lname in LAW_FILES.items():
            if args.law in (lid, lname):
                law_id = lid
                break
        if law_id not in LAW_FILES:
            print(f'❌ 未知法规: {args.law}')
            print(f'   已知: {", ".join(LAW_FILES.keys())}')
            return 1
        ok = ingest_one(law_id, ledger, check_only=args.check)
        if not ok:
            return 1
    else:
        all_ok = True
        for law_id in LAW_FILES:
            ok = ingest_one(law_id, ledger, check_only=args.check)
            if not ok:
                all_ok = False
        if not all_ok and not args.check:
            return 1

    if not args.check:
        # 保留已有的完整法规（不在 LAW_FILES 中的也要保留）
        LAW_IDS = set(LAW_FILES.keys())
        for doc in ledger['documents']:
            if doc['id'] in LAW_IDS:
                continue  # 这些是我们要更新的
            # 其他法规保持不变

        LEDGER_PATH.write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
        print(f'\n📦 已写入 {LEDGER_PATH}')

        # 提示下一步
        print(f'👉 下一步: python tools/build_legal_pages.py')
        print(f'👉 然后验证: python -m unittest discover -s tests -p "test_*.py" -v')

    return 0


if __name__ == '__main__':
    sys.exit(main())
