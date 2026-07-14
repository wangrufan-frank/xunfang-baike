var dailyCases = [
  {
    date: '2026-06-27',
    title: '「催泪喷射器实战应用」',
    body: '接报公园内一名疑似吸毒人员情绪亢奋失控。民警到场后发现对象处于精神亢奋状态，体壮力大。盾牌手维持安全距离，持喷射器民警顺风站位，发出标准警告，对象无视继续前进，民警以点射方式（每次≤1秒）对准面部喷射，喷射后立即侧移换位，对象捂脸伏地，随即上铐并告知善后措施。',
    tips: [
      '使用前检查风向：逆风不得使用，选择上风口站位',
      '每次点射不超过1秒，点射后立即移动位置',
      '控制后及时净化处理：清水冲洗，不要揉擦',
      '呼叫120到场评估，确认对象身体状况'
    ]
  }
];

Page({
  data: {
    show: { zhuangbei: true, qinwu: true, xunlian: true, jingqing: true, fagui: true, zoufang: true },
    daily: dailyCases[0],
    dailyIdx: 0,
    dailyTotal: dailyCases.length
  },
  onShow() {
    if (typeof this.getTabBar === 'function' && this.getTabBar()) {
      this.getTabBar().setData({ selected: 0 });
    }
  },
  onSearch(e) {
    var q = e.detail.value.toLowerCase().trim();
    if (!q) {
      this.setData({ show: { zhuangbei: true, qinwu: true, xunlian: true, jingqing: true, fagui: true, zoufang: true } });
      return;
    }
    var show = { zhuangbei: false, qinwu: false, xunlian: false, jingqing: false, fagui: false, zoufang: false };
    var cards = [
      { key: 'zhuangbei', text: '装备介绍 单警装备使用规范 伸缩警棍 催泪喷射器 手铐 执法记录仪' },
      { key: 'qinwu', text: '巡防勤务 内容整改中' },
      { key: 'xunlian', text: '警务训练 徒手 警械 战术 盾牌技术 盘查流程 搜身带离 战术站位' },
      { key: 'jingqing', text: '警情处置 内容整改中' },
      { key: 'fagui', text: '法条规范 执法依据速查 治安规范 赌博执法 法律依据 法言法语' },
      { key: 'zoufang', text: '走访送教 校园社区送教服务 校园反恐 金融反恐 校园培训' }
    ];
    cards.forEach(function(c) { if (c.text.indexOf(q) !== -1) show[c.key] = true; });
    this.setData({ show: show });
  },
  onPrev() { var i = this.data.dailyIdx; i = i > 0 ? i - 1 : dailyCases.length - 1; this.setData({ daily: dailyCases[i], dailyIdx: i }); },
  onNext() { var i = this.data.dailyIdx; i = i < dailyCases.length - 1 ? i + 1 : 0; this.setData({ daily: dailyCases[i], dailyIdx: i }); }
});
