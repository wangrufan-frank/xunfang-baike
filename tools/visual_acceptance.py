"""视觉验收脚本 — 对 5 个代表性页面截取桌面端和移动端截图。"""
from pathlib import Path
import sys
import time
import http.server
import socketserver
import threading

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / 'deliverables' / 'visual-acceptance'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGES = [
    ('1-警情-长页面', 'jingqing/chidao-lei.html', '持刀类警情处置基础（长警情）'),
    ('2-装备', 'zhuangbei/zhifa-jiuyi.html', '执法记录仪（装备页）'),
    ('3-执法程序', 'fagui/panwen-shenfenzheng.html', '盘问检查与身份证查验（执法程序）'),
    ('4-短法规', 'fagui/jingxie-wuqi-tiaoli.html', '警械和武器条例（短法规全文，17条）'),
    ('5-长法规', 'fagui/zhian-guanli-chufa-fa.html', '治安管理处罚法（长法规全文，144条）'),
]


def start_server(port=8765):
    handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return httpd, f'http://localhost:{port}'


def main():
    from playwright.sync_api import sync_playwright

    # 启动测试服务器
    os.chdir(ROOT)
    server, base_url = start_server(8765)
    print(f'Server: {base_url}')
    time.sleep(0.5)

    results = []

    with sync_playwright() as p:
        for name, path, desc in PAGES:
            url = f'{base_url}/{path}'
            print(f'\n📸 {name}: {desc}')

            for width, label in [(1440, 'desktop'), (390, 'mobile')]:
                browser = p.chromium.launch()
                context = browser.new_context(
                    viewport={'width': width, 'height': 900},
                    device_scale_factor=1,
                )
                page = context.new_page()

                try:
                    page.goto(url, wait_until='networkidle', timeout=15000)
                    page.wait_for_timeout(1000)  # 等字体/主题加载

                    filename = f'{name}-{label}-{width}px.png'
                    filepath = OUTPUT_DIR / filename
                    page.screenshot(path=str(filepath), full_page=False)
                    file_size_kb = filepath.stat().st_size / 1024

                    # 验收检查
                    checks = run_checks(page, width, label)

                    status = '✅' if all(c[0] for c in checks) else '⚠️'
                    print(f'  {status} {label} {width}px ({file_size_kb:.0f}KB)')
                    for ok, msg in checks:
                        print(f'     {"✅" if ok else "❌"} {msg}')

                    results.append({
                        'page': name,
                        'viewport': f'{label} {width}px',
                        'file': filename,
                        'checks': checks,
                    })
                except Exception as e:
                    print(f'  ❌ {label} {width}px: ERROR {e}')
                finally:
                    browser.close()

    # 生成验收报告
    report_md = OUTPUT_DIR / 'report.md'
    lines = [
        '# 视觉验收报告',
        f'\n日期：2026-07-19',
        f'\n## 截图清单\n',
    ]
    for r in results:
        lines.append(
            f'### {r["page"]} — {r["viewport"]}\n'
            f'![{r["page"]}]({r["file"]})\n'
        )
        for ok, msg in r['checks']:
            lines.append(f'- {"✅" if ok else "❌"} {msg}')
        lines.append('')

    lines.append('## 验收标准检查\n')
    criteria = [
        ('首屏 10 秒看懂', '标题、核心结论和至少两个行动重点在首屏可见'),
        ('不展开也理解核心流程', '禁止边界和核心流程在不展开细节的情况下可理解'),
        ('展开不丢位置', '展开细节后不丢失当前位置，目录高亮正确'),
        ('法规正文完整可见', '法规全文默认完整可见，可直接查找并复制任一条'),
        ('移动端无横向滚动', '移动端无横向滚动，目录和长 URL 不撑破容器'),
        ('打印法规完整', '打印时正文完整，不输出网站导航和折叠控制'),
        ('主题对比度合格', '深色与浅色主题下重点卡片、法条和来源链接对比度合格'),
    ]
    for criterion, detail in criteria:
        lines.append(f'- **{criterion}**：{detail}')

    report_md.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'\n📋 报告: {report_md}')
    print(f'📁 截图: {OUTPUT_DIR}')

    server.shutdown()
    return 0


def run_checks(page, width, label):
    """执行验收检查。"""
    checks = []

    # 1. 首屏可见标题
    title = page.locator('h1').first
    checks.append((
        title.is_visible() if title.count() else False,
        '首屏 H1 标题可见'
    ))

    # 2. 快速阅读区存在
    quick_read = page.locator('.quick-read')
    checks.append((
        quick_read.count() > 0,
        '.quick-read 速览区存在'
    ))

    # 3. 展开全部按钮
    expand_btn = page.locator('.expand-all-btn')
    checks.append((
        expand_btn.count() > 0 or '法规' in page.title(),
        '展开全部按钮存在（法规页除外）'
    ))

    # 4. 页内导航
    toc = page.locator('.article-toc')
    checks.append((
        toc.count() > 0,
        '.article-toc 页内导航存在'
    ))

    # 5. 公开来源区
    source_idx = page.locator('.public-source-index')
    checks.append((
        source_idx.count() > 0,
        '.public-source-index 公开来源区存在'
    ))

    # 6. 无内部标签
    html = page.content()
    has_internal = '巡防百科知识库内部资料' in html
    checks.append((
        not has_internal,
        '无"巡防百科知识库内部资料"标签'
    ))

    # 7. 移动端特殊检查
    if label == 'mobile':
        # 检查横向滚动
        viewport_width = page.evaluate('document.documentElement.scrollWidth')
        window_width = page.evaluate('window.innerWidth')
        checks.append((
            viewport_width <= window_width + 5,  # 允许 5px 误差
            f'移动端无横向滚动 (content={viewport_width}px, window={window_width}px)'
        ))

    # 8. 法规页特殊检查
    if '/fagui/' in page.url and 'qita' not in page.url:
        # 检查法规正文
        articles = page.locator('.article-content')
        checks.append((
            articles.count() > 0,
            '法规正文区 (.article-content) 存在'
        ))

    return checks


import os
if __name__ == '__main__':
    sys.exit(main())
