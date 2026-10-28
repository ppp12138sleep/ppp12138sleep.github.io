/**
 * 页面区块：导航、侧边位置指示器都从这里读，改一处两边同步
 */
const sections = [
  { id: "work", label: "项目" },
  { id: "skills", label: "技能" },
  { id: "timeline", label: "经历" },
  { id: "about", label: "关于" },
  { id: "contact", label: "联系" },
];

/**
 * 站点全局信息 —— 改这里就能改全站的名字、定位、联系方式
 * 注意：当前是示例内容（placeholder: true），上线前替换成真实信息。
 */
export const site = {
  // 示例内容标记：上线前把 placeholder 改成 false，右下角提示会自动消失
  placeholder: true,

  name: "潘赫",
  nameEn: "PAN HE",
  initials: "PH",

  // 首屏定位句（PRD 3.1 的 A 版）
  headline: "物联网工程 2028 届",
  headlineAccent: "嵌入式硬件 / 物联网方案",
  tagline:
    "从画板子到上云端——写固件、画 PCB、调通信协议，把传感器数据送到能用的地方。",

  // 状态徽章
  status: "2028 届 · 寻找 2027 寒假实习",
  jobSearch: "2027 寒假实习",

  school: "大连民族大学 · 物联网工程",
  location: "辽宁 · 大连",

  email: "2246724926@qq.com",
  github: "https://github.com/ppp12138sleep",
  githubHandle: "@ppp12138sleep",
  resume: "/resume-preview.pdf", // 占位：替换成你的简历 PDF
  resumeName: "潘赫-嵌入式硬件-2028届.pdf",

  sections,
  nav: sections.map((s) => ({ href: `/#${s.id}`, label: s.label })),

  // 用于 JSON-LD 的 sameAs，填完整网址
  links: [{ label: "GitHub", url: "https://github.com/ppp12138sleep" }],

  // 站点地址：部署后改成你的域名，用于 canonical / OG / sitemap
  url: "https://ppp12138sleep.github.io",

  seo: {
    title: "潘赫 · 嵌入式硬件 / 物联网方案",
    description:
      "大连民族大学物联网工程 2028 届本科生，方向嵌入式硬件与物联网方案。作品集：传感器节点、循迹小车、低功耗无线设备。寻找 2027 年寒假实习。",
  },
};
