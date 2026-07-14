"""Parse HTML source files and generate miniprogram data JS files."""
import os
import re
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

BASE = os.path.dirname(os.path.abspath(__file__))

MODULES = {
    'qinwu': 'qinwu',
    'xunlian': 'xunlian',
    'fagui': 'fagui',
    'zoufang': 'zoufang',
}

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_h1(html):
    """Extract icon and title from <h1>."""
    m = re.search(r'<h1>(.*?)</h1>', html)
    if not m:
        return '', ''
    text = m.group(1).strip()
    # Extract leading emoji as icon
    emoji_m = re.match(r'^([\U0001F300-\U0001FAFF☀-➿‍️#⃣\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF✂-➰Ⓜ-\U0001F251\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF]+)\s*', text)
    if emoji_m:
        icon = emoji_m.group(1)
        title = text[emoji_m.end():].strip()
    else:
        icon = ''
        title = text
    return icon, title

def parse_meta_tags(html):
    """Extract tags from .meta section, skip reading-time tags."""
    meta_m = re.search(r'<div class="meta">(.*?)</div>', html, re.DOTALL)
    if not meta_m:
        return [], ''
    meta_html = meta_m.group(1)
    tags = re.findall(r'<span class="tag">(.*?)</span>', meta_html)
    # Filter out reading-time tags, collect real tags
    real_tags = []
    section = ''
    for i, t in enumerate(tags):
        if '预计阅读' in t:
            continue
        if i == 0:
            section = t
        real_tags.append(t)
    return real_tags, section

def parse_quick_card(html):
    """Extract quickCard from .quick-card div."""
    qc_m = re.search(r'<div class="quick-card">(.*?)</div>\s*<div class="step-card', html, re.DOTALL)
    if not qc_m:
        return None
    qc_html = qc_m.group(1)

    icon_m = re.search(r'<div class="quick-icon">(.*?)</div>', qc_html)
    icon = icon_m.group(1).strip() if icon_m else ''

    h2_m = re.search(r'<h2>(.*?)</h2>', qc_html)
    title = h2_m.group(1).strip() if h2_m else ''

    qt_m = re.search(r'<div class="quick-tags">(.*?)</div>', qc_html, re.DOTALL)
    tags = re.findall(r'<span class="tag">(.*?)</span>', qt_m.group(1)) if qt_m else []

    flow_m = re.search(r'<div class="quick-flow">(.*?)</div>', qc_html)
    flow = flow_m.group(1).strip() if flow_m else ''

    return {'title': title, 'tags': tags, 'flow': flow}

def parse_steps(html):
    """Extract all step cards."""
    steps = []
    # Find all step-card blocks
    step_blocks = re.finditer(
        r'<div class="step-card (step-\w+)">(.*?)(?=<div class="step-card|</div>\s*<div class="page-nav")',
        html, re.DOTALL
    )

    for block in step_blocks:
        color_class = block.group(1)
        body = block.group(2)

        color_map = {'step-red': 'red', 'step-blue': 'blue', 'step-orange': 'orange',
                     'step-green': 'green', 'step-purple': 'purple'}
        color = color_map.get(color_class, 'blue')

        # Step num
        num_m = re.search(r'<div class="step-num">(.*?)</div>', body)
        num_raw = num_m.group(1).strip() if num_m else '1'
        try:
            num = int(num_raw)
        except ValueError:
            num = num_raw  # '!' stays as '!'

        # Step title
        title_m = re.search(r'<div class="step-title">(.*?)</div>', body)
        title = title_m.group(1).strip() if title_m else ''

        # Step lead
        lead_m = re.search(r'<div class="step-lead">(.*?)</div>', body, re.DOTALL)
        lead = lead_m.group(1).strip() if lead_m else ''
        # Clean lead: remove extra whitespace/newlines
        lead = re.sub(r'\s+', ' ', lead).strip()

        # Media
        media = None
        media_m = re.search(r'<div class="step-media[^>]*>(.*?)</div>', body, re.DOTALL)
        if media_m:
            media_text = media_m.group(1).strip()
            if 'img' in media_m.group(0) or '📷' in media_text:
                media = {'type': 'img', 'label': media_text}
            elif 'video' in media_m.group(0) or '🎬' in media_text:
                media = {'type': 'video', 'label': media_text}
            else:
                media = {'type': 'img', 'label': media_text}

        # Expandable content
        expandable = False
        content = ''
        expand_label = ''
        expandable_m = re.search(r'<div class="expandable">(.*?)</div>\s*<button class="expand-btn">(.*?)</button>', body, re.DOTALL)
        if expandable_m:
            expandable = True
            expand_label = expandable_m.group(2).strip().replace('▸ ', '')
            # Get text from expandable-full
            full_m = re.search(r'<div class="expandable-full">(.*?)</div>', expandable_m.group(1), re.DOTALL)
            if full_m:
                content = full_m.group(1).strip()
        else:
            # Non-expandable: get step-text directly
            st_m = re.search(r'<div class="step-text">(.*?)</div>', body, re.DOTALL)
            if st_m:
                content = st_m.group(1).strip()

        # Clean HTML from content
        content = clean_html(content)

        step = {
            'num': num,
            'title': title,
            'color': color,
            'lead': lead,
            'content': content,
            'expandable': expandable,
        }
        if media:
            step['media'] = media

        steps.append(step)

    return steps

def clean_html(text):
    """Remove HTML tags and decode entities, preserve line breaks."""
    # Replace <br> with newlines
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Remove remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common entities
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&').replace('&nbsp;', ' ').replace('&quot;', '"')
    # Strip leading whitespace from each line
    lines = text.split('\n')
    lines = [l.strip() for l in lines]
    text = '\n'.join(lines)
    # Collapse multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def parse_page_nav(html):
    """Extract prev/next navigation."""
    nav_m = re.search(r'<div class="page-nav">(.*?)</div>', html, re.DOTALL)
    if not nav_m:
        return None, None

    nav_html = nav_m.group(1)
    links = re.findall(r'<a href="([^"]+)">(.*?)</a>', nav_html)
    prev_id = None
    next_id = None
    for href, text in links:
        # Remove .html extension
        slug = href.replace('.html', '')
        if '←' in text:
            prev_id = slug
        elif '→' in text:
            next_id = slug

    return prev_id, next_id

def parse_desc_from_lead(steps):
    """Build desc from step titles."""
    if not steps:
        return ''
    titles = [s['title'] for s in steps[:6]]
    return ' · '.join(titles)

def parse_flow_from_steps(steps):
    """Build flow string from step titles."""
    if not steps:
        return ''
    parts = []
    for i, s in enumerate(steps):
        prefix = '!' if s['num'] == '!' else str(i + 1)
        if len(s['title']) > 20:
            parts.append(s['title'][:20] + '…')
        else:
            parts.append(s['title'])
    return '📋 ' + ' → '.join(parts)

def parse_module_index(module_dir):
    """Parse index.html to get section groupings and article order."""
    index_path = os.path.join(BASE, module_dir, 'index.html')
    if not os.path.exists(index_path):
        return [], {}

    html = read_file(index_path)

    # Find all sections and their articles
    sections = []
    section_map = {}

    # Pattern: <div class="list-section-title">SECTION</div> followed by <a> items
    parts = re.split(r'<div class="list-section-title">(.*?)</div>', html)
    # parts[0] is before first section
    for i in range(1, len(parts), 2):
        section_name = parts[i].strip()
        section_html = parts[i + 1] if i + 1 < len(parts) else ''

        items = re.findall(r'<a href="([^"]+)"[^>]*>.*?<div class="item-title">(.*?)</div>.*?<div class="item-desc">(.*?)</div>', section_html, re.DOTALL)

        section_map[section_name] = []
        for href, title, desc in items:
            slug = href.replace('.html', '')
            icon_match = re.match(r'^([^\w\s]+)\s*', title.strip())
            icon = icon_match.group(1) if icon_match else ''
            item_title = title.strip()[len(icon):].strip() if icon else title.strip()
            section_map[section_name].append({
                'id': slug,
                'icon': icon,
                'title': item_title,
                'desc': desc.strip()
            })

        if section_map[section_name]:
            sections.append(section_name)

    # Get total count and overall icon from page-title
    h1_m = re.search(r'<h1>(.*?)</h1>', html)
    module_icon = ''
    if h1_m:
        icon_match = re.match(r'^([^\w\s]+)\s*', h1_m.group(1).strip())
        module_icon = icon_match.group(1) if icon_match else ''

    return sections, section_map, module_icon

def parse_article(filepath, section_name):
    """Parse a single article HTML file."""
    html = read_file(filepath)

    icon, title = parse_h1(html)
    tags, html_section = parse_meta_tags(html)
    quick_card = parse_quick_card(html)
    steps = parse_steps(html)
    prev_id, next_id = parse_page_nav(html)

    # Always prefer section_name from index.html (the official grouping)
    final_section = section_name if section_name else html_section

    # Build desc from step titles
    desc = parse_desc_from_lead(steps)

    # Build flow
    flow = parse_flow_from_steps(steps)

    # Use quickCard tags for article tags (better curated)
    qc = quick_card if quick_card else {'title': title, 'tags': tags[:3] if tags else [], 'flow': flow}
    article_tags = qc.get('tags', [])[:4] if qc.get('tags') else tags[:4]

    return {
        'id': os.path.splitext(os.path.basename(filepath))[0],
        'title': title,
        'icon': icon,
        'section': final_section,
        'desc': desc,
        'tags': article_tags,
        'flow': flow,
        'quickCard': qc,
        'steps': steps,
        'prevId': prev_id,
        'nextId': next_id
    }

def escape_js_string(s):
    """Escape a string for JS single-quoted string."""
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    return s

def format_step(step, indent='      '):
    """Format a step object as JS."""
    props = []
    props.append(f'{indent}  num: {json.dumps(step["num"])}')
    props.append(f'{indent}  title: {json.dumps(step["title"], ensure_ascii=False)}')
    props.append(f'{indent}  color: {json.dumps(step["color"])}')
    props.append(f'{indent}  lead: {json.dumps(step["lead"], ensure_ascii=False)}')
    props.append(f'{indent}  content: {json.dumps(step["content"], ensure_ascii=False)}')
    props.append(f'{indent}  expandable: {json.dumps(step.get("expandable", True))}')
    if step.get('media'):
        props.append(f'{indent}  media: {{type: {json.dumps(step["media"]["type"])}, label: {json.dumps(step["media"]["label"], ensure_ascii=False)}}}')
    return f'{indent}{{\n' + ',\n'.join(props) + f'\n{indent}}}'

def format_article(a):
    """Format a single article as JS object string."""
    props = []
    props.append(f'    id: {json.dumps(a["id"])}')
    props.append(f'    title: {json.dumps(a["title"], ensure_ascii=False)}')
    props.append(f'    icon: {json.dumps(a["icon"], ensure_ascii=False)}')
    props.append(f'    section: {json.dumps(a["section"], ensure_ascii=False)}')
    props.append(f'    desc: {json.dumps(a["desc"], ensure_ascii=False)}')
    props.append(f'    tags: {json.dumps(a["tags"], ensure_ascii=False)}')
    props.append(f'    flow: {json.dumps(a["flow"], ensure_ascii=False)}')

    qc = a['quickCard']
    qc_props = []
    qc_props.append(f'      title: {json.dumps(qc["title"], ensure_ascii=False)}')
    qc_props.append(f'      tags: {json.dumps(qc["tags"], ensure_ascii=False)}')
    qc_props.append(f'      flow: {json.dumps(qc["flow"], ensure_ascii=False)}')
    props.append('    quickCard: {\n' + ',\n'.join(qc_props) + '\n    }')

    step_strs = [format_step(s) for s in a['steps']]
    props.append('    steps: [\n' + ',\n'.join(step_strs) + '\n    ]')

    props.append(f'    prevId: {json.dumps(a["prevId"])}')
    props.append(f'    nextId: {json.dumps(a["nextId"])}')
    return '  {\n' + ',\n'.join(props) + '\n  }'

def process_module(module_dir):
    """Process a single module: parse all HTML, generate data JS."""
    print(f'\n=== Processing {module_dir} ===')

    sections, section_map, module_icon = parse_module_index(module_dir)
    print(f'  Sections: {sections}')
    for s in sections:
        print(f'    {s}: {len(section_map[s])} articles')

    # Build id->article mapping from index
    index_articles = {}
    for section_name, items in section_map.items():
        for item in items:
            index_articles[item['id']] = {
                'section': section_name,
                'icon': item['icon'],
                'index_title': item['title'],
                'index_desc': item['desc']
            }

    # Parse each HTML file
    articles = []
    html_dir = os.path.join(BASE, module_dir)
    for filename in sorted(os.listdir(html_dir)):
        if filename == 'index.html' or not filename.endswith('.html'):
            continue

        filepath = os.path.join(html_dir, filename)
        article_id = filename.replace('.html', '')

        # Get section from index
        index_info = index_articles.get(article_id, {})
        section_name = index_info.get('section', '')

        print(f'  Parsing: {filename} -> section={section_name}')

        try:
            article = parse_article(filepath, section_name)
            # Override with index data if available
            if index_info.get('icon') and not article['icon']:
                article['icon'] = index_info['icon']
            if index_info.get('index_desc') and not article['desc']:
                article['desc'] = index_info['index_desc']
            articles.append(article)
        except Exception as e:
            print(f'    ERROR: {e}')

    # Reorder articles based on index order
    ordered = []
    id_map = {a['id']: a for a in articles}
    for section_name in sections:
        for item in section_map.get(section_name, []):
            if item['id'] in id_map:
                ordered.append(id_map[item['id']])
    # Add any articles not in index
    for a in articles:
        if a not in ordered:
            ordered.append(a)

    print(f'  Total articles: {len(ordered)}')

    return ordered

def generate_js(module_name, articles):
    """Generate JS file content."""
    lines = ['module.exports = [']
    for i, a in enumerate(articles):
        comma = ',' if i < len(articles) - 1 else ''
        lines.append(format_article(a) + comma)
    lines.append('];')
    lines.append('')
    return '\n'.join(lines)

def main():
    for module_dir, module_name in MODULES.items():
        articles = process_module(module_dir)
        js_content = generate_js(module_name, articles)

        output_path = os.path.join(BASE, 'miniprogram', 'data', f'{module_name}.js')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f'  -> Wrote {output_path} ({len(articles)} articles)')

    print('\nDone!')

if __name__ == '__main__':
    main()
