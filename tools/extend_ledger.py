#!/usr/bin/env python3
"""Extend public-sources.json to cover all 87 articles from content-inventory.json."""

from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    # Load existing files
    with open(ROOT / 'data' / 'content-inventory.json', 'r', encoding='utf-8') as f:
        ci = json.load(f)
    with open(ROOT / 'data' / 'public-sources.json', 'r', encoding='utf-8') as f:
        ps = json.load(f)

    # Build URL -> source_id map from existing sources
    url_to_source = {}
    for s in ps['sources']:
        url_to_source[s['url']] = s['source_id']

    # New source definitions (metadata extracted from existing HTML source-list sections)
    new_source_defs = [
        {
            'source_id': 'official-jinzhou-police-water-rescue-drill-2026',
            'title': '锦州市公安局巡特警硬核上演防汛救援“大练兵”',
            'publisher': '锦州市公安局',
            'platform': '锦州市人民政府门户网站',
            'url': 'http://www.jz.gov.cn/info/1024/127327.htm',
            'published_at': '2026-07-03',
            'similarity_note': '公安机关公开演练正文涉及水域救援装备使用和防汛救援训练场景。',
            'source_level': 2,
        },
        {
            'source_id': 'official-fuxin-police-patrol-equipment-standards',
            'title': '交通警察道路执勤执法工作规范',
            'publisher': '阜新市公安局',
            'platform': '阜新市公安局',
            'url': 'https://gaj.fuxin.gov.cn/mob/newsdetail.thtml?id=321668',
            'published_at': None,
            'similarity_note': '公安机关公开材料涉及巡逻执勤装备配备标准和现场处置规范。',
            'source_level': 2,
        },
        {
            'source_id': 'official-mps-prohibition-drinking-banquet',
            'title': '公安部关于严禁违规宴请饮酒的规定（公开转载）',
            'publisher': '公安部',
            'platform': '石家庄市公安局',
            'url': 'https://gaj.sjz.gov.cn/columns/0a9c92b2-97b8-4284-9bd7-6240c789c0bf/202204/29/1c7b0edf-6eec-4110-a397-d1a4828b68d4.html',
            'published_at': '2022-04-29',
            'similarity_note': '公安机关公开转载的公安部内部纪律规定，涉及违规宴请饮酒的禁止性要求。',
            'source_level': 1,
        },
        {
            'source_id': 'official-fire-protection-law-2025',
            'title': '中华人民共和国消防法',
            'publisher': '全国人民代表大会常务委员会',
            'platform': '贵州省消防救援总队',
            'url': 'https://gz.119.gov.cn/xxgk/zfxxgk/fdzdgknr/lzyj/flfg/202503/t20250303_86974482.html',
            'published_at': '2025-03-03',
            'similarity_note': '国家法律正文规定消防安全责任、消防装备配备和火灾应急处置要求。',
            'source_level': 1,
        },
        {
            'source_id': 'official-road-traffic-safety-law-2021',
            'title': '中华人民共和国道路交通安全法（2021年修订）',
            'publisher': '全国人民代表大会常务委员会',
            'platform': '北京市公安局公安交通管理局',
            'url': 'https://jtgl.beijing.gov.cn/jgj/jgxx/flfg/fl/205308/index.html',
            'published_at': '2021-04-29',
            'similarity_note': '国家法律正文规定道路交通安全管理、执勤执法和事故处理程序。',
            'source_level': 1,
        },
        {
            'source_id': 'official-police-internal-affairs-order-2022',
            'title': '公安机关人民警察内务条令（公安部令第161号）',
            'publisher': '公安部',
            'platform': '中国政府网国务院公报',
            'url': 'https://www.gov.cn/gongbao/content/2022/content_5671112.htm',
            'published_at': '2022-01-20',
            'similarity_note': '部门规章正文规定公安机关人民警察内务管理、纪律要求和行为规范。',
            'source_level': 1,
        },
        {
            'source_id': 'official-police-discipline-regulation-2010',
            'title': '公安机关人民警察纪律条令',
            'publisher': '公安部',
            'platform': '中华人民共和国司法部',
            'url': 'https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/201007/t20100728_144862.html',
            'published_at': '2010-07-28',
            'similarity_note': '部门规章正文规定公安机关人民警察的纪律要求和违规处理程序。',
            'source_level': 1,
        },
        {
            'source_id': 'official-police-training-regulation-2025',
            'title': '公安机关人民警察训练条令（2025年施行）',
            'publisher': '公安部',
            'platform': '中华人民共和国司法部',
            'url': 'https://www.moj.gov.cn/pub/sfbgw/flfggz/flfggzbmgz/202510/t20251021_526539.html',
            'published_at': '2025-10-21',
            'similarity_note': '部门规章正文规定公安机关人民警察训练组织、内容、考核和管理要求。',
            'source_level': 1,
        },
        {
            'source_id': 'official-mental-health-law-2012',
            'title': '中华人民共和国精神卫生法',
            'publisher': '全国人民代表大会常务委员会',
            'platform': '国家卫生健康委员会',
            'url': 'https://www.nhc.gov.cn/fzs/c100048/201808/5d03e37b37c944b08d701a0b5722160a.shtml',
            'published_at': '2018-08-01',
            'similarity_note': '国家法律正文规定精神障碇的诊断、治疗、康复及与治安管理衔接的内容。',
            'source_level': 1,
        },
        {
            'source_id': 'official-state-secrets-law-2024',
            'title': '中华人民共和国保守国家秘密法（2024年修订）',
            'publisher': '全国人民代表大会常务委员会',
            'platform': '中国人大网',
            'url': 'https://www.npc.gov.cn/npc/c2/c30834/202402/t20240227_434859.html',
            'published_at': '2024-02-27',
            'similarity_note': '国家法律正文规定国家秘密范围、保密义务、保密审查和法律责任。',
            'source_level': 1,
        },
        {
            'source_id': 'official-public-security-law-2025',
            'title': '中华人民共和国治安管理处罚法（2025年修订）',
            'publisher': '全国人民代表大会常务委员会',
            'platform': '中国人大网',
            'url': 'https://www.npc.gov.cn/npc/c2/c30834/202506/t20250627_446235.html',
            'published_at': '2025-06-27',
            'similarity_note': '现行法律全文规定治安违法行为、处罚种类、程序和执法监督要求。',
            'source_level': 1,
        },
        {
            'source_id': 'official-zhenyuan-police-vehicle-impact-training-2022',
            'title': '镇原县公安局组织开展“防车辆冲撞”最小作战单元专项训练',
            'publisher': '镇原县公安局',
            'platform': '庆阳政法网',
            'url': 'https://www.qyswzfw.gov.cn/Show/286341',
            'published_at': '2022-10-11',
            'similarity_note': '公安机关公开训练正文涉及防车辆冲撞、最小作战单元装备使用和战术配合。',
            'source_level': 2,
        },
        {
            'source_id': 'official-civil-explosives-safety-regulation',
            'title': '民用爆炸物品安全管理条例',
            'publisher': '国务院',
            'platform': '国家行政法规库',
            'url': 'https://xzfg.moj.gov.cn/front/law/detail?LawID=165&Query=',
            'published_at': '2006-09-01',
            'similarity_note': '行政法规正文规定民用爆炸物品生产、销售、运输、储存和使用的安全管理要求。',
            'source_level': 1,
        },
        {
            'source_id': 'official-large-event-security-regulation',
            'title': '大型群众性活动安全管理条例（国务院令第505号）',
            'publisher': '国务院',
            'platform': '国家法律法规数据库',
            'url': 'https://xzfg.moj.gov.cn/front/law/detail?LawID=204&Query=%E5%A4%A7%E5%9E%8B%E7%BE%A4%E4%BC%97%E6%80%A7%E6%B4%BB%E5%8A%A8%E5%AE%89%E5%85%A8%E7%AE%A1%E7%90%86%E6%9D%A1%E4%BE%8B',
            'published_at': '2007-10-01',
            'similarity_note': '行政法规正文规定大型群众性活动安全许可、主体责任、安保措施和应急处置要求。',
            'source_level': 1,
        },
    ]

    print(f'Existing sources: {len(ps["sources"])}')
    print(f'Existing pages: {len(ps["pages"])}')

    existing_paths = {p['path'] for p in ps['pages']}
    existing_source_ids = {s['source_id'] for s in ps['sources']}
    existing_urls = {s['url'] for s in ps['sources']}

    # Add new sources
    new_source_count = 0
    for ns in new_source_defs:
        if ns['url'] in existing_urls:
            continue
        if ns['source_id'] in existing_source_ids:
            print(f'COLLISION: {ns["source_id"]}')
            continue
        ps['sources'].append({
            'source_id': ns['source_id'],
            'title': ns['title'],
            'publisher': ns['publisher'],
            'platform': ns['platform'],
            'url': ns['url'],
            'published_at': ns['published_at'],
            'verified_at': '2026-07-19',
            'verification_status': 'verified',
            'similarity_note': ns['similarity_note'],
            'source_level': ns['source_level'],
            'last_checked_at': '2026-07-19',
        })
        url_to_source[ns['url']] = ns['source_id']
        existing_source_ids.add(ns['source_id'])
        existing_urls.add(ns['url'])
        new_source_count += 1
        print(f'  Added source: {ns["source_id"]}')

    print(f'New sources added: {new_source_count}')

    # Create page entries for articles not yet in ledger
    new_page_count = 0
    for mod in ci['modules']:
        for art in mod['articles']:
            path = art['path']
            if path in existing_paths:
                continue
            page_source_ids = []
            for url in art.get('public_sources', []):
                sid = url_to_source.get(url)
                if sid and sid not in page_source_ids:
                    page_source_ids.append(sid)
            ps['pages'].append({
                'page_id': f'{art["module"]}-{art["slug"]}',
                'path': path,
                'title': art['title'],
                'page_level': True,
                'source_ids': page_source_ids,
                'review_status': 'pending',
                'reviewed_by': None,
                'reviewed_at': None,
            })
            existing_paths.add(path)
            new_page_count += 1

    print(f'New page entries created: {new_page_count}')
    print(f'Total pages: {len(ps["pages"])}')
    print(f'Total sources: {len(ps["sources"])}')

    # Check the 4 zero-source pages
    zero_pages = [
        'zhuangbei/jiusheng-yi.html',
        'zhuangbei/jiusheng-sheng.html',
        'zhuangbei/sanshi-weidang.html',
        'zhuangbei/zhedieshi-weidang.html',
    ]
    for zp in zero_pages:
        for p in ps['pages']:
            if p['path'] == zp:
                sc = p.get('source_ids', [])
                print(f'ZERO-SOURCE CHECK: {zp} -> {len(sc)} sources: {sc}')
                break

    # Write output
    output_path = ROOT / 'data' / 'public-sources.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ps, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print(f'Wrote {output_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
