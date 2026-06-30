var dailyCases = [
  {
    date: '2026-06-29',
    title: '「醉酒闹事处置」',
    body: '某日晚间，巡逻组接报一男子在烧烤摊酒后闹事，持酒瓶威胁周围群众。民警到场后先疏散围观人员，保持安全距离，语言安抚稳定情绪。待嫌疑人情绪松懈、放下酒瓶点烟时，盾牌手在前、抓捕手从侧翼突入，三人协同控制上铐。全程执法记录仪开启，事后向指挥中心报备。',
    tips: [
      '先疏散围观群众，避免人群刺激嫌疑人情绪',
      '保持安全距离≥2米，语言安抚为主，不单独近身',
      '盾牌在前，抓捕手侧翼，一人外围警戒',
      '抓住嫌疑人松懈瞬间，三人同时行动，一招制敌'
    ]
  },
  {
    date: '2026-06-28',
    title: '「伸缩警棍使用」',
    body: '巡逻组接到家暴警情，到场时一名男子情绪激动持木凳挥舞。民警口头警告无效后，盾牌手建立安全屏障，持棍手从侧翼以肩上戒备接近。男子冲向盾牌时，持棍手趁其注意力被吸引，以劈击技术击中其大腿外侧肌肉群使其失去锐气，随即三人协同上铐。',
    tips: [
      '使用前必须口头警告，给对象反应时间',
      '击打部位锁定大肌肉群，严禁打Head/胫骨/裆部',
      '使用后立即检查对象伤情，以制止为限度',
      '使用后记录并汇报，做处置情况说明'
    ]
  },
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
  onSearch(e) {
    var q = e.detail.value.toLowerCase().trim();
    if (!q) {
      this.setData({ show: { zhuangbei: true, qinwu: true, xunlian: true, jingqing: true, fagui: true, zoufang: true } });
      return;
    }
    var show = { zhuangbei: false, qinwu: false, xunlian: false, jingqing: false, fagui: false, zoufang: false };
    var cards = [
      { key: 'zhuangbei', text: '装备介绍 单警装备使用规范 伸缩警棍 催泪喷射器 手铐 执法记录仪' },
      { key: 'qinwu', text: '巡防勤务 每日勤务与任务规范 大型活动安保 群体事件处置 舆情导控' },
      { key: 'xunlian', text: '警务训练 徒手 警械 战术 快反 盾牌技术 盘查流程 武力升级 搜身带离' },
      { key: 'jingqing', text: '警情处置 常见警情处置流程 持刀警情 醉酒闹事 打架斗殴 家庭暴力' },
      { key: 'fagui', text: '法条规范 执法依据速查 治安规范 赌博执法 法律依据 法言法语' },
      { key: 'zoufang', text: '走访送教 校园社区送教服务 校园反恐 现场处置 金融反恐 校园培训' }
    ];
    cards.forEach(function(c) { if (c.text.indexOf(q) !== -1) show[c.key] = true; });
    this.setData({ show: show });
  },
  onPrev() { var i = this.data.dailyIdx; i = i > 0 ? i - 1 : dailyCases.length - 1; this.setData({ daily: dailyCases[i], dailyIdx: i }); },
  onNext() { var i = this.data.dailyIdx; i = i < dailyCases.length - 1 ? i + 1 : 0; this.setData({ daily: dailyCases[i], dailyIdx: i }); }
});
