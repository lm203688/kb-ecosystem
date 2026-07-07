// OracleMind 全站中文文案常量表
// 面向中文用户，所有UI文案统一管理

export const COPY = {
  // 导航
  nav: {
    home: '首页',
    predict: '开始推演',
    history: '历史记录',
    pricing: '价格方案',
    trust: '可信度看板',
    login: '登录',
    logout: '退出',
  },
  
  // Landing Hero
  hero: {
    title: '人生概率推演引擎',
    subtitle: '基于八字命理 + 多Agent AI辩论',
    description: '不是算命，是概率推演。用AI多视角分析，给你置信区间，你自己决定。',
    cta: '开始推演',
    secondaryCta: '了解更多',
    badge: 'AI驱动 · 多Agent辩论 · 概率化预测',
  },
  
  // 输入表单
  form: {
    title: '输入你的生辰信息',
    subtitle: '八字命理基于出生年月日时推算',
    name: '姓名',
    namePlaceholder: '你的名字（可选）',
    gender: '性别',
    male: '男',
    female: '女',
    year: '出生年份',
    month: '出生月份',
    day: '出生日期',
    hour: '出生时辰',
    hourPlaceholder: '选择时辰',
    submit: '开始推演',
    analyzing: '正在推演...',
    unknownTime: '时辰不详',
  },
  
  // 推演结果
  result: {
    title: '推演结果',
    confidence: '置信度',
    confidenceHigh: '高',
    confidenceMedium: '中',
    confidenceLow: '低',
    baziChart: '八字命盘',
    luckPillars: '大运流年',
    fiveElements: '五行分析',
    prediction: '概率推演',
    factors: '影响因素',
    chatWithAI: '与AI深聊',
    askQuestion: '追问任何问题...',
    send: '发送',
    newPrediction: '重新推演',
    saveResult: '保存结果',
  },
  
  // AI Chat
  chat: {
    title: 'AI深度对话',
    placeholder: '关于你的命盘，想问什么？',
    send: '发送',
    thinking: 'AI正在思考...',
    quickQuestions: '快捷问题',
    questions: [
      '我的事业运如何？',
      '今年有什么需要注意的？',
      '适合什么行业？',
      '感情运势如何？',
    ],
  },
  
  // 可信度看板
  trust: {
    title: '可信度看板',
    subtitle: '我们如何确保预测的可靠性',
    transparency: '透明度',
    dataSources: '数据来源',
    methodology: '方法论',
    accuracy: '准确率追踪',
    disclaimer: '本平台结果仅供娱乐参考，不构成任何决策建议',
  },
  
  // 价格方案
  pricing: {
    title: '选择适合你的方案',
    subtitle: '从免费体验到深度推演',
    free: '免费体验',
    freeDesc: '基础八字排盘',
    basic: '基础推演',
    basicDesc: '单次深度预测',
    pro: '专业版',
    proDesc: '多Agent辩论 + 流年分析',
    premium: '尊享版',
    premiumDesc: '全年运势 + 专属顾问',
    recommended: '推荐',
    perTime: '/次',
    perMonth: '/月',
    choose: '选择方案',
    mostPopular: '最受欢迎',
  },
  
  // 通用
  common: {
    loading: '加载中...',
    error: '出错了',
    retry: '重试',
    cancel: '取消',
    confirm: '确认',
    save: '保存',
    delete: '删除',
    edit: '编辑',
    close: '关闭',
    back: '返回',
    next: '下一步',
    previous: '上一步',
    seeMore: '查看更多',
    seeAll: '查看全部',
  },
  
  // 步骤指示器
  steps: {
    input: '输入信息',
    analyzing: 'AI推演中',
    result: '查看结果',
  },
  
  // 起卦仪式
  ritual: {
    title: '正在起卦',
    subtitle: 'AI正在分析你的命理数据...',
    steps: [
      '排列八字命盘',
      '推算大运流年',
      '分析五行强弱',
      '多Agent辩论中',
      '生成概率推演',
    ],
  },
  
  // 为什么选择我们
  whyUs: {
    title: '为什么选择 OracleMind',
    subtitle: '不是算命工具，是概率推演引擎',
    features: [
      {
        title: '概率化预测',
        desc: '不承诺确定结果，给出概率和置信区间',
      },
      {
        title: '多Agent辩论',
        desc: '4个AI Agent从不同角度分析，最终达成共识',
      },
      {
        title: '可验证结果',
        desc: '追踪预测准确率，用数据说话',
      },
      {
        title: '开源引擎',
        desc: '八字引擎开源，算法透明可审查',
      },
    ],
  },
} as const;
