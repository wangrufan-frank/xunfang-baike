const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = '巡防百科项目组';
pptx.subject = '巡防百科网站项目汇报';
pptx.title = '巡防百科网站项目汇报';
pptx.company = '巡防百科';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'Microsoft YaHei',
  bodyFontFace: 'Microsoft YaHei',
  lang: 'zh-CN'
};
pptx.defineLayout({ name: 'CUSTOM_WIDE', width: 13.333, height: 7.5 });
pptx.layout = 'CUSTOM_WIDE';

const W = 13.333;
const H = 7.5;
const C = {
  navy: '082B4C',
  blue: '0D5C91',
  sky: '1C8CCF',
  ice: 'EAF4FA',
  paper: 'F6F9FC',
  ink: '16324A',
  muted: '607589',
  white: 'FFFFFF',
  gold: 'E7B65A',
  green: '25936A',
  line: 'D6E2EA'
};
const assets = path.join(__dirname, '..', 'deliverables', 'assets');
const out = path.join(__dirname, '..', 'deliverables', '巡防百科网站项目汇报.pptx');

function rect(slide, x, y, w, h, fill, line = fill, radius = false) {
  slide.addShape(radius ? pptx.ShapeType.roundRect : pptx.ShapeType.rect, {
    x, y, w, h, rectRadius: radius ? 0.08 : undefined,
    fill: { color: fill }, line: { color: line, transparency: line === fill ? 100 : 0 }
  });
}

function frame(slide, x, y, w, h, line = C.line, radius = false) {
  slide.addShape(radius ? pptx.ShapeType.roundRect : pptx.ShapeType.rect, {
    x, y, w, h, rectRadius: radius ? 0.08 : undefined,
    fill: { color: C.white, transparency: 100 }, line: { color: line, width: 1 }
  });
}

function text(slide, value, x, y, w, h, opts = {}) {
  slide.addText(value, {
    x, y, w, h, margin: 0,
    fontFace: 'Microsoft YaHei', fontSize: 16, color: C.ink,
    breakLine: false, fit: 'shrink', valign: 'mid',
    ...opts
  });
}

function footer(slide, n) {
  slide.addShape(pptx.ShapeType.line, { x: 0.55, y: 7.02, w: 12.2, h: 0, line: { color: C.line, width: 0.7 } });
  text(slide, '巡防百科网站项目汇报', 0.6, 7.11, 3.2, 0.18, { fontSize: 8.5, color: C.muted });
  text(slide, String(n).padStart(2, '0'), 12.15, 7.08, 0.55, 0.2, { fontSize: 9, bold: true, color: C.blue, align: 'right' });
}

function title(slide, number, heading, subheading = '') {
  text(slide, number, 0.62, 0.45, 0.45, 0.32, { fontSize: 12, bold: true, color: C.gold, charSpacing: 1.5 });
  text(slide, heading, 0.62, 0.86, 8.8, 0.56, { fontSize: 28, bold: true, color: C.navy });
  if (subheading) text(slide, subheading, 0.64, 1.46, 9.9, 0.28, { fontSize: 11, color: C.muted });
}

function image(slide, filename, x, y, w, h) {
  slide.addImage({ path: path.join(assets, filename), x, y, w, h, sizing: { type: 'cover', x, y, w, h } });
}

function badge(slide, label, x, y, w, color) {
  rect(slide, x, y, w, 0.34, color, color, true);
  text(slide, label, x, y + 0.01, w, 0.26, { fontSize: 9.5, bold: true, color: C.white, align: 'center' });
}

function card(slide, x, y, w, h, heading, body, accent) {
  rect(slide, x, y, w, h, C.white, C.line, true);
  rect(slide, x, y, 0.08, h, accent, accent);
  text(slide, heading, x + 0.28, y + 0.25, w - 0.48, 0.32, { fontSize: 15, bold: true, color: C.navy });
  text(slide, body, x + 0.28, y + 0.72, w - 0.5, h - 0.94, { fontSize: 10.5, color: C.muted, breakLine: false, valign: 'top' });
}

// 1. Cover
{
  const s = pptx.addSlide();
  s.background = { color: C.navy };
  s.addShape(pptx.ShapeType.arc, { x: 8.6, y: -1.1, w: 5.8, h: 5.8, adjustPoint: 0.3, line: { color: C.sky, transparency: 85, width: 2 } });
  s.addShape(pptx.ShapeType.arc, { x: 9.4, y: -0.2, w: 4.6, h: 4.6, adjustPoint: 0.3, line: { color: C.gold, transparency: 70, width: 1.2 } });
  badge(s, '基层巡防知识快速查询平台', 0.75, 0.83, 2.6, C.blue);
  text(s, '巡防百科网站\n项目汇报', 0.75, 1.55, 6.8, 1.55, { fontSize: 34, bold: true, color: C.white, breakLine: false, valign: 'mid' });
  text(s, '以知识沉淀支撑一线巡防实战，以便捷查询提升日常工作效率', 0.8, 3.32, 6.8, 0.38, { fontSize: 15, color: 'C8D9E6' });
  rect(s, 0.8, 4.45, 5.85, 1.25, '0D3B63', '0D3B63', true);
  text(s, '已形成六大业务模块\n支持分类浏览、站内搜索、图文与视频辅助', 1.08, 4.68, 5.25, 0.78, { fontSize: 13, color: C.white, breakLine: false, valign: 'mid' });
  text(s, '汇报人：________    汇报时间：________', 0.8, 6.47, 5.5, 0.24, { fontSize: 10, color: 'B4CADB' });
}

// 2. Background
{
  const s = pptx.addSlide(); s.background = { color: C.paper }; title(s, '01', '建设背景：基层知识获取的现实需求', '将分散资料转化为一线人员“找得到、看得懂、用得上”的知识服务');
  const items = [
    ['资料分散', '规章、流程、培训材料和经验做法分布在不同载体，集中查找不便。', C.blue],
    ['查询耗时', '面对具体任务时，需要在有限时间内定位对应的操作要点与规范依据。', C.sky],
    ['经验难沉淀', '图文、示意和案例内容缺少统一入口，难以持续积累与更新。', C.green]
  ];
  items.forEach((item, i) => { const x = 0.7 + i * 4.18; card(s, x, 2.25, 3.72, 2.55, item[0], item[1], item[2]); text(s, String(i + 1).padStart(2, '0'), x + 0.28, 3.95, 0.55, 0.35, { fontSize: 23, bold: true, color: 'D7E7F1' }); });
  rect(s, 0.7, 5.38, 11.9, 0.92, 'E3F0F8', 'E3F0F8', true);
  text(s, '建设目标：把常用巡防知识沉淀为可持续更新、可快速查询、可随时访问的轻量化平台。', 1.0, 5.65, 11.2, 0.3, { fontSize: 15, bold: true, color: C.navy, align: 'center' }); footer(s, 2);
}

// 3. Method
{
  const s = pptx.addSlide(); s.background = { color: C.white }; title(s, '02', '建设思路：从知识库到巡防百科', '通过统一整理、结构化呈现和持续维护，让内容可以不断生长');
  const steps = [
    ['知识沉淀', 'Obsidian 知识库\n收集与归档'], ['内容整理', '按主题分类\n提炼图文要点'], ['网站发布', '网页模块化呈现\n支持搜索浏览'], ['持续更新', '新增资料及时补充\n迭代完善内容']
  ];
  steps.forEach((step, i) => { const x = 0.72 + i * 3.15; rect(s, x, 2.45, 2.48, 1.62, i === 2 ? C.navy : C.ice, i === 2 ? C.navy : C.line, true); text(s, String(i + 1), x + 0.22, 2.68, 0.38, 0.25, { fontSize: 12, bold: true, color: i === 2 ? C.gold : C.blue }); text(s, step[0], x + 0.22, 3.02, 2.05, 0.3, { fontSize: 15, bold: true, color: i === 2 ? C.white : C.navy }); text(s, step[1], x + 0.22, 3.45, 2.03, 0.45, { fontSize: 10.5, color: i === 2 ? 'D7E7F1' : C.muted, valign: 'mid' }); if (i < 3) { s.addShape(pptx.ShapeType.chevron, { x: x + 2.6, y: 3.03, w: 0.32, h: 0.4, fill: { color: C.gold }, line: { color: C.gold } }); } });
  image(s, 'home.png', 3.65, 4.68, 6.05, 1.72); frame(s, 3.65, 4.68, 6.05, 1.72, C.line, true); text(s, '知识库不是终点，而是网站内容持续更新的基础。', 0.92, 5.4, 2.18, 0.5, { fontSize: 12, bold: true, color: C.blue, valign: 'mid' }); footer(s, 3);
}

// 4. Architecture
{
  const s = pptx.addSlide(); s.background = { color: C.paper }; title(s, '03', '网站总体架构', '围绕基层巡防常见任务，构建六类可直接进入的内容模块');
  const modules = [['装备介绍', C.blue], ['巡防勤务', C.green], ['警务训练', '6D72C3'], ['警情处置', 'B65454'], ['法条规范', '8D6B3E'], ['走访送教', '1F9E9B']];
  modules.forEach((m, i) => { const row = Math.floor(i / 3), col = i % 3; const x = 0.75 + col * 3.95, y = 2.18 + row * 1.35; rect(s, x, y, 3.45, 0.95, C.white, C.line, true); rect(s, x, y, 0.1, 0.95, m[1], m[1]); text(s, String(i + 1).padStart(2, '0'), x + 0.3, y + 0.27, 0.36, 0.24, { fontSize: 10, bold: true, color: m[1] }); text(s, m[0], x + 0.78, y + 0.2, 2.35, 0.34, { fontSize: 16, bold: true, color: C.navy }); text(s, '按主题集中呈现，便于进入与浏览', x + 0.78, y + 0.57, 2.35, 0.16, { fontSize: 8.8, color: C.muted }); });
  image(s, 'home.png', 8.63, 4.95, 3.2, 1.8); frame(s, 8.63, 4.95, 3.2, 1.8, C.line, true); footer(s, 4);
}

// 5. Features
{
  const s = pptx.addSlide(); s.background = { color: C.white }; title(s, '04', '核心功能：快速定位所需知识', '以“分类入口 + 站内搜索 + 图文视频”的方式降低信息获取门槛');
  image(s, 'search.png', 6.95, 1.92, 5.65, 3.5); frame(s, 6.95, 1.92, 5.65, 3.5, C.line, true);
  card(s, 0.75, 2.0, 2.75, 1.05, '分类浏览', '从六大模块进入，适合明确知道业务方向时快速查看。', C.blue);
  card(s, 3.75, 2.0, 2.75, 1.05, '站内搜索', '输入关键词即可在已整理内容中定位相关页面。', C.green);
  card(s, 0.75, 3.42, 2.75, 1.05, '图文结合', '用步骤、图片与要点呈现信息，降低理解成本。', '6D72C3');
  card(s, 3.75, 3.42, 2.75, 1.05, '视频辅助', '对动作和流程类内容，提供更直观的学习参考。', C.gold);
  rect(s, 0.75, 5.18, 5.75, 0.74, C.navy, C.navy, true); text(s, '让常用知识从“资料里”走到“现场需要时”。', 1.02, 5.4, 5.22, 0.25, { fontSize: 13.5, bold: true, color: C.white, align: 'center' }); footer(s, 5);
}

// 6. Scenario
{
  const s = pptx.addSlide(); s.background = { color: C.paper }; title(s, '05', '典型场景：一次快速查询', '当面对具体任务时，通过三步完成从问题到要点的快速定位');
  const scenes = [['进入网站', '打开首页，选择对应业务模块。', 'home.png'], ['搜索或选择模块', '通过关键词或分类页定位主题内容。', 'search.png'], ['查看操作要点', '阅读图文说明、示意与视频辅助内容。', 'detail.png']];
  scenes.forEach((sc, i) => { const x = 0.62 + i * 4.25; rect(s, x, 2.02, 3.72, 3.8, C.white, C.line, true); badge(s, `STEP ${i + 1}`, x + 0.24, 2.24, 0.85, i === 1 ? C.green : C.blue); image(s, sc[2], x + 0.24, 2.76, 3.24, 1.72); frame(s, x + 0.24, 2.76, 3.24, 1.72, C.line, true); text(s, sc[0], x + 0.25, 4.78, 3.15, 0.26, { fontSize: 14, bold: true, color: C.navy }); text(s, sc[1], x + 0.25, 5.17, 3.14, 0.34, { fontSize: 10, color: C.muted, valign: 'top' }); if (i < 2) s.addShape(pptx.ShapeType.chevron, { x: x + 3.82, y: 3.65, w: 0.25, h: 0.38, fill: { color: C.gold }, line: { color: C.gold } }); }); footer(s, 6);
}

// 7. Live demo
{
  const s = pptx.addSlide(); s.background = { color: C.navy }; badge(s, '现场演示', 0.75, 0.65, 1.05, C.gold); text(s, '让知识真正可用', 0.75, 1.22, 6.4, 0.56, { fontSize: 28, bold: true, color: C.white }); text(s, '现场打开网站，展示模块浏览与站内搜索；以真实页面证明项目已具备使用基础。', 0.78, 1.92, 5.5, 0.48, { fontSize: 12, color: 'D3E2ED' });
  const demo = [['1', '访问网站', '打开 www.xunfangbk.cn'], ['2', '进入模块', '选择“警情处置”'], ['3', '站内搜索', '输入关键词并查看详情']];
  demo.forEach((d, i) => { const y = 2.72 + i * 0.93; rect(s, 0.78, y, 5.55, 0.68, '0D3B63', '0D3B63', true); rect(s, 0.98, y + 0.14, 0.4, 0.4, C.gold, C.gold, true); text(s, d[0], 0.98, y + 0.16, 0.4, 0.22, { fontSize: 11, bold: true, color: C.navy, align: 'center' }); text(s, d[1], 1.64, y + 0.14, 1.25, 0.22, { fontSize: 12, bold: true, color: C.white }); text(s, d[2], 3.0, y + 0.16, 2.9, 0.2, { fontSize: 10, color: 'C9DCE9' }); });
  rect(s, 0.78, 5.72, 5.55, 0.62, '173F62', '173F62', true); text(s, '如网络或操作异常：立即播放本地 3 分钟使用演示视频。', 1.0, 5.93, 5.1, 0.2, { fontSize: 10.5, color: 'F7D99A', align: 'center' });
  image(s, 'module-jingqing.png', 7.05, 1.1, 5.45, 4.85); frame(s, 7.05, 1.1, 5.45, 4.85, '7AA1B9', true); text(s, '演示重点：看得到、找得快、用得上', 7.16, 6.35, 5.1, 0.25, { fontSize: 11, bold: true, color: 'D3E2ED', align: 'center' });
}

// 8. Value
{
  const s = pptx.addSlide(); s.background = { color: C.white }; title(s, '06', '阶段成果与推广价值', '以可访问的网站形式，把知识沉淀转化为可被基层人员直接使用的服务');
  const values = [['已形成网站入口', '统一网址访问，支持电脑与手机浏览。', C.blue], ['已搭建内容框架', '围绕六类巡防主题进行模块化组织。', C.green], ['具备持续更新基础', '知识库整理与网站发布形成可迭代链路。', '6D72C3'], ['支持推广与扩展', '可在内容完善后逐步推进更广范围使用。', C.gold]];
  values.forEach((v, i) => { const x = 0.72 + (i % 2) * 6.05, y = 2.1 + Math.floor(i / 2) * 1.62; rect(s, x, y, 5.52, 1.22, C.paper, C.line, true); rect(s, x + 0.23, y + 0.27, 0.53, 0.53, v[2], v[2], true); text(s, String(i + 1), x + 0.23, y + 0.4, 0.53, 0.18, { fontSize: 10, bold: true, color: C.white, align: 'center' }); text(s, v[0], x + 1.0, y + 0.22, 3.95, 0.28, { fontSize: 15, bold: true, color: C.navy }); text(s, v[1], x + 1.0, y + 0.66, 4.15, 0.25, { fontSize: 10.5, color: C.muted }); });
  rect(s, 0.72, 5.63, 11.63, 0.6, C.ice, C.ice, true); text(s, '推广价值：将“个人整理的知识”逐步转化为“可共享、可查询、可持续维护的工作资源”。', 1.0, 5.84, 11.05, 0.21, { fontSize: 12.5, bold: true, color: C.blue, align: 'center' }); footer(s, 8);
}

// 9. Roadmap
{
  const s = pptx.addSlide(); s.background = { color: C.paper }; title(s, '07', '下一步计划', '在现有网站基础上持续完善内容、优化体验，并逐步拓展应用场景');
  const plans = [['内容完善', '持续补充常用流程、图文要点和案例资料。'], ['访问管理优化', '完善展示与访问方式，提升使用稳定性。'], ['微信小程序迁移', '将成熟内容逐步适配至移动端使用场景。'], ['推广应用', '结合实际需求试用、反馈与持续迭代。']];
  plans.forEach((p, i) => { const x = 0.72 + i * 3.12; s.addShape(pptx.ShapeType.line, { x: x + 0.36, y: 2.5, w: i < 3 ? 2.75 : 0, h: 0, line: { color: C.line, width: 1.4 } }); rect(s, x, 2.1, 0.75, 0.75, i === 3 ? C.gold : C.blue, i === 3 ? C.gold : C.blue, true); text(s, String(i + 1), x, 2.33, 0.75, 0.2, { fontSize: 13, bold: true, color: C.white, align: 'center' }); text(s, p[0], x, 3.2, 2.55, 0.3, { fontSize: 15, bold: true, color: C.navy }); text(s, p[1], x, 3.68, 2.55, 0.52, { fontSize: 10.3, color: C.muted, valign: 'top' }); });
  rect(s, 0.72, 5.55, 11.7, 0.72, C.navy, C.navy, true); text(s, '以巡防实战需求为导向，让网站成为基层知识服务的长期载体。', 1.03, 5.8, 11.08, 0.24, { fontSize: 14, bold: true, color: C.white, align: 'center' });
  text(s, '网址：www.xunfangbk.cn', 4.6, 6.55, 4.1, 0.24, { fontSize: 11, color: C.blue, bold: true, align: 'center' }); footer(s, 9);
}

fs.mkdirSync(path.dirname(out), { recursive: true });
pptx.writeFile({ fileName: out });
