// RoboParts 4大新增功能（借鉴GR00T可组合技能库）
// 部署到Vercel Functions: robot-parts/website/api/

// 1. 零件组合方案库
const presetKits = [
  {
    id: "kit_6dof_arm",
    name: "6DOF机械臂方案",
    description: "6自由度机械臂完整方案，适合抓取/搬运",
    parts: [
      { category: "机械臂", spec: "6DOF, 负载≥2kg" },
      { category: "舵机", spec: "扭矩≥20kg·cm, 数量6" },
      { category: "控制器", spec: "支持6路PWM" },
      { category: "电源", spec: "12V/5A" },
      { category: "夹爪", spec: "电动, 行程≥50mm" }
    ],
    estimated_cost: "¥800-2000",
    difficulty: "中级",
    tags: ["机械臂", "抓取", "6DOF"]
  },
  {
    id: "kit_mobile_base",
    name: "移动底盘方案",
    description: "轮式移动底盘，适合巡检/搬运机器人",
    parts: [
      { category: "底盘", spec: "铝合金, ≥300mm" },
      { category: "电机", spec: "直流减速电机, 12V, 数量4" },
      { category: "驱动器", spec: "双H桥, 支持4路" },
      { category: "轮组", spec: "麦克纳姆轮, 直径60mm" },
      { category: "控制器", spec: "Arduino/树莓派" },
      { category: "电源", spec: "12V/10Ah锂电池" }
    ],
    estimated_cost: "¥500-1500",
    difficulty: "初级",
    tags: ["底盘", "移动", "麦克纳姆轮"]
  },
  {
    id: "kit_vision_grasp",
    name: "视觉抓取方案",
    description: "视觉识别+机械臂抓取完整方案",
    parts: [
      { category: "相机", spec: "RGB-D, 720p" },
      { category: "机械臂", spec: "6DOF, 带夹爪" },
      { category: "计算平台", spec: "Jetson Nano/树莓派4" },
      { category: "光源", spec: "LED环形光" },
      { category: "控制器", spec: "支持ROS2" }
    ],
    estimated_cost: "¥2000-5000",
    difficulty: "高级",
    tags: ["视觉", "抓取", "ROS"]
  },
  {
    id: "kit_3d_print",
    name: "3D打印转接方案",
    description: "跨品牌零件转接件3D打印方案",
    parts: [
      { category: "3D打印机", spec: "FDM, 200x200x200mm" },
      { category: "耗材", spec: "PLA/ABS/PETG" },
      { category: "转接件模型", spec: "STL文件, 可定制" },
      { category: "螺丝包", spec: "M2-M6, 多规格" }
    ],
    estimated_cost: "¥200-500",
    difficulty: "初级",
    tags: ["3D打印", "转接", "DIY"]
  },
  {
    id: "kit_bionic_arm",
    name: "仿生手臂方案",
    description: "仿生柔性驱动手臂，用人工肌肉/软体驱动",
    parts: [
      { category: "人工肌肉", spec: "电液纤维, 2mm直径" },
      { category: "驱动器", spec: "高压驱动, ≥2kV" },
      { category: "传感器", spec: "柔性应变传感器" },
      { category: "控制器", spec: "微控制器+功率放大" },
      { category: "结构件", spec: "3D打印柔性材料" }
    ],
    estimated_cost: "¥1000-3000",
    difficulty: "研究级",
    tags: ["仿生", "人工肌肉", "柔性驱动", "生物机器人"]
  },
  {
    id: "kit_swarm_robot",
    name: "群体机器人方案",
    description: "小型群体协作机器人方案",
    parts: [
      { category: "微型底盘", spec: "≤100mm, 全向轮" },
      { category: "通信模块", spec: "WiFi/Bluetooth/Zigbee" },
      { category: "定位模块", spec: "UWB/红外" },
      { category: "控制器", spec: "ESP32/STM32" },
      { category: "电源", spec: "微型锂电池" }
    ],
    estimated_cost: "¥300-800/台",
    difficulty: "中级",
    tags: ["群体", "协作", "微型"]
  },
  {
    id: "kit_humanoid",
    name: "人形机器人方案",
    description: "双足人形机器人基础方案",
    parts: [
      { category: "腿部舵机", spec: "总线舵机, ≥30kg·cm, 数量12" },
      { category: "手臂舵机", spec: "扭矩≥15kg·cm, 数量8" },
      { category: "躯干结构件", spec: "铝合金/碳纤维" },
      { category: "平衡传感器", spec: "IMU 6轴" },
      { category: "计算平台", spec: "Jetson Orin/树莓派" },
      { category: "电源", spec: "高压锂电池组" }
    ],
    estimated_cost: "¥3000-10000",
    difficulty: "专家级",
    tags: ["人形", "双足", "高级"]
  },
  {
    id: "kit_soft_robot",
    name: "软体机器人方案",
    description: "软体驱动机器人方案（含人工肌肉）",
    parts: [
      { category: "软体驱动器", spec: "气动/电液驱动" },
      { category: "硅胶材料", spec: "Ecoflex/ Dragonskin" },
      { category: "气泵/液压泵", spec: "微型, 可控" },
      { category: "传感器", spec: "柔性压力传感器" },
      { category: "控制器", spec: "微控制器+驱动" }
    ],
    estimated_cost: "¥500-2000",
    difficulty: "研究级",
    tags: ["软体", "柔性", "仿生"]
  },
  {
    id: "kit_bci_control",
    name: "脑机接口控制方案",
    description: "脑信号控制机器人方案",
    parts: [
      { category: "EEG采集", spec: "8-16通道" },
      { category: "信号放大", spec: "低噪声放大器" },
      { category: "处理平台", spec: "GPU计算平台" },
      { category: "机械臂", spec: "低延迟控制" },
      { category: "反馈设备", spec: "VR/触觉反馈" }
    ],
    estimated_cost: "¥5000-20000",
    difficulty: "研究级",
    tags: ["脑机接口", "BCI", "神经控制"]
  },
  {
    id: "kit_autonomous_nav",
    name: "自主导航方案",
    description: "SLAM自主导航机器人方案",
    parts: [
      { category: "激光雷达", spec: "2D/3D LiDAR" },
      { category: "深度相机", spec: "RGB-D" },
      { category: "计算平台", spec: "Jetson+CPU" },
      { category: "底盘", spec: "差速/全向" },
      { category: "IMU", spec: "9轴" },
      { category: "软件", spec: "ROS2+Nav2" }
    ],
    estimated_cost: "¥3000-8000",
    difficulty: "高级",
    tags: ["导航", "SLAM", "自主"]
  }
];

// 2. 跨品牌兼容性引擎
const compatibilityMatrix = {
  " servo": {
    "Dynamixel": ["RS485总线", "TTL总线"],
    "Lewansoul": ["TTL总线"],
    "Feetech": ["PWM", "RS485"],
    "MG996R": ["PWM"],
    "通用PWM": ["PWM"]
  },
  "controller": {
    "Arduino": ["PWM", "I2C", "UART"],
    "树莓派": ["PWM", "I2C", "UART", "SPI"],
    "Jetson": ["PWM", "I2C", "UART", "SPI", "GPIO"],
    "STM32": ["PWM", "I2C", "UART", "SPI", "CAN"]
  },
  "arm": {
    "Dynamixel机械臂": ["RS485"],
    "Lewansoul机械臂": ["TTL"],
    "通用6DOF": ["PWM"],
    "协作机器人": ["EtherCAT", "CANopen"]
  }
};

function checkCompatibility(partA, partB) {
  const aInterfaces = compatibilityMatrix[partA.category]?.[partA.brand] || [];
  const bInterfaces = compatibilityMatrix[partB.category]?.[partB.brand] || [];
  const common = aInterfaces.filter(i => bInterfaces.includes(i));
  return {
    compatible: common.length > 0,
    common_interfaces: common,
    need_adapter: common.length === 0,
    adapter_type: common.length === 0 ? "需要转接板/协议转换器" : null
  };
}

// 3. 自然语言需求匹配
function matchRequirement(text) {
  const keywords = {
    load: { pattern: /(\d+)\s*kg/i, field: "负载", value: null },
    budget: { pattern: /(\d+)\s*元/i, field: "预算", value: null },
    dof: { pattern: /(\d+)\s*dof|(\d+)\s*自由度/i, field: "自由度", value: null },
    type: { pattern: /机械臂|底盘|夹爪|视觉|人形|软体|群体/i, field: "类型", value: null }
  };
  
  const matched = {};
  for (const [key, rule] of Object.entries(keywords)) {
    const m = text.match(rule.pattern);
    if (m) matched[rule.field] = m[1] || m[0];
  }
  
  // 匹配预设方案
  let recommended = [];
  if (matched["类型"]) {
    recommended = presetKits.filter(k => 
      k.tags.some(t => matched["类型"].includes(t)) || k.name.includes(matched["类型"])
    );
  }
  if (matched["预算"]) {
    const budget = parseInt(matched["预算"]);
    recommended = recommended.length ? recommended : presetKits;
    recommended = recommended.filter(k => {
      const costs = k.estimated_cost.match(/\d+/g);
      return costs && parseInt(costs[0]) <= budget;
    });
  }
  
  return { requirements: matched, recommended_kits: recommended.slice(0, 5) };
}

// Vercel Functions 路由
export default function handler(req, res) {
  const { action } = req.query;
  
  if (action === 'kits') {
    // 获取方案库
    return res.status(200).json({ success: true, kits: presetKits });
  }
  
  if (action === 'match') {
    // 自然语言匹配
    const { text } = req.body || req.query;
    if (!text) return res.status(400).json({ error: "需要text参数" });
    return res.status(200).json({ success: true, ...matchRequirement(text) });
  }
  
  if (action === 'compatibility') {
    // 兼容性检查
    const { partA, partB } = req.body;
    if (!partA || !partB) return res.status(400).json({ error: "需要partA和partB" });
    return res.status(200).json({ success: true, ...checkCompatibility(partA, partB) });
  }
  
  if (action === 'trends') {
    // 零件技术趋势
    return res.status(200).json({
      success: true,
      trends: [
        { name: "电液纤维肌肉", source: "MIT", description: "2mm纤维举200倍自重，功率密度比肩生物肌肉", category: "人工肌肉", impact: "高" },
        { name: "柔性驱动器", source: "多机构", description: "气动/电液软体驱动，仿生运动", category: "软体机器人", impact: "高" },
        { name: "脑机接口", source: "Neuralink/Synchron", description: "脑信号直接控制机器人", category: "神经接口", impact: "中" },
        { name: "GR00T技能库", source: "NVIDIA", description: "可组合机器人技能，跨形态通用", category: "AI技能", impact: "高" },
        { name: "群体协作", source: "多机构", description: "群体机器人协作算法", category: "群体智能", impact: "中" }
      ]
    });
  }
  
  return res.status(200).json({
    success: true,
    endpoints: [
      "GET ?action=kits — 获取方案库",
      "POST ?action=match — 自然语言匹配",
      "POST ?action=compatibility — 兼容性检查",
      "GET ?action=trends — 技术趋势"
    ]
  });
}
