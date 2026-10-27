/**
 * 技能地图 —— 顺序按 PRD 3.4：硬件岗视角在前，方案岗视角在后
 * level: "strong" = 能独立做 | "used" = 用过 / 做过
 */
export const skillGroups = [
  {
    id: "hardware",
    index: "01",
    title: "硬件设计",
    note: "能独立走完「原理图 → PCB → 打样 → 焊接 → 调试」",
    skills: [
      {
        name: "原理图与 PCB（立创 EDA）",
        level: "strong",
        note: "两层板，50×40mm 以内；做过 5 块板，含 1 次返修",
      },
      {
        name: "焊接与返修",
        level: "strong",
        note: "0603 贴片、QFN 手焊、热风枪吹 BGA 不敢说熟练",
      },
      {
        name: "仪器调试",
        level: "strong",
        note: "万用表、示波器、逻辑分析仪；常用来抓 I2C 时序和电源纹波",
      },
      {
        name: "电源设计",
        level: "used",
        note: "LDO / DC-DC 降压、锂电池充放电、低功耗休眠",
      },
      {
        name: "元器件选型与 BOM",
        level: "used",
        note: "按成本、供货、封装权衡，会看 datasheet 的关键参数",
      },
    ],
  },
  {
    id: "mcu",
    index: "02",
    title: "MCU 与平台",
    note: "主力是 STM32 与 ESP32，裸机和 RTOS 都写过",
    skills: [
      {
        name: "STM32（HAL + 寄存器）",
        level: "strong",
        note: "F103 / F411；ADC、DMA、定时器 PWM、I2C、SPI、低功耗模式",
      },
      {
        name: "ESP32 / ESP8266",
        level: "strong",
        note: "ESP-IDF 与 Arduino 双线；WiFi 配网、MQTT 上报",
      },
      {
        name: "FreeRTOS",
        level: "used",
        note: "任务划分、队列、信号量；踩过优先级反转的坑",
      },
      {
        name: "嵌入式 Linux",
        level: "used",
        note: "树莓派上跑过 Python 采集服务，驱动只到「能改」的程度",
      },
      {
        name: "51 单片机 / Arduino",
        level: "used",
        note: "入门用过，现在基本不碰",
      },
    ],
  },
  {
    id: "comm",
    index: "03",
    title: "通信与协议",
    note: "从板级总线到上云链路都能自己调通",
    skills: [
      {
        name: "UART / SPI / I2C",
        level: "strong",
        note: "能看时序图定位问题；写过软件模拟 I2C 救急",
      },
      {
        name: "MQTT",
        level: "strong",
        note: "EMQX 自建 broker，QoS1、遗嘱消息、断线重连都调过",
      },
      {
        name: "WiFi / TCP-IP / HTTP",
        level: "used",
        note: "能读懂抓包，会排查 DNS 与 DHCP 问题",
      },
      {
        name: "Modbus / RS485",
        level: "used",
        note: "课设里做过从站，CRC 校验自己实现过",
      },
      {
        name: "BLE / LoRa",
        level: "used",
        note: "BLE 广播做过 Beacon；LoRa 只在实验箱上调过",
      },
    ],
  },
  {
    id: "cloud",
    index: "04",
    title: "云与方案",
    note: "能把数据变成别人看得懂的东西（方案岗重点）",
    skills: [
      {
        name: "数据可视化",
        level: "strong",
        note: "ECharts 网页看板、微信小程序实时曲线",
      },
      {
        name: "Python 上位机",
        level: "strong",
        note: "PyQt / Flask，串口采集 + 存库 + 画图",
      },
      {
        name: "云平台",
        level: "used",
        note: "阿里云 IoT 物模型、规则引擎转发到数据库",
      },
      {
        name: "数据库",
        level: "used",
        note: "SQLite、MySQL 建表和查询；InfluxDB 用过一次",
      },
      {
        name: "C / C++ / JavaScript",
        level: "used",
        note: "C 是主力；C++ 会用到类；JS 够写页面和小程序",
      },
      {
        name: "Git / VS Code / PlatformIO",
        level: "used",
        note: "日常工具链，会用分支和 Pull Request",
      },
    ],
  },
];
