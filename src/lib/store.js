/**
 * 站点数据仓库。
 *
 * 数据存在 data/site.json 里 —— 后台页面写这个文件，所有页面读它。
 * 之所以用「同一个对象原地修改」而不是每次重新读文件：
 * 组件里是 `import { site }` 拿到对象引用，只有对象本身不变，
 * 后台保存后其它页面才能立刻读到新值。
 */

import fs from "node:fs";
import path from "node:path";

const DATA_DIR = path.resolve(process.cwd(), "data");
const DATA_FILE = path.join(DATA_DIR, "site.json");

/** 首次运行时写进 site.json 的初始值（等于现在的页面内容） */
const DEFAULTS = {
  placeholder: true,

  name: "潘赫",
  nameEn: "PAN HE",
  avatar: "/avatar.jpg",

  headline: "物联网工程 2028 届",
  headlineAccent: "嵌入式硬件 / 物联网方案",
  tagline:
    "从画板子到上云端——写固件、画 PCB、调通信协议，把传感器数据送到能用的地方。",

  status: "2028 届 · 寻找 2027 寒假实习",
  jobSearch: "2027 寒假实习",

  school: "大连民族大学 · 物联网工程",
  location: "辽宁 · 大连",

  email: "2246724926@qq.com",
  github: "https://github.com/ppp12138sleep",
  githubHandle: "@ppp12138sleep",

  resume: "/resume-preview.pdf",
  resumeName: "潘赫-嵌入式硬件-2028届.pdf",

  url: "https://ppp12138sleep.github.io",

  seo: {
    title: "潘赫 · 嵌入式硬件 / 物联网方案",
    description:
      "大连民族大学物联网工程 2028 届本科生，方向嵌入式硬件与物联网方案。作品集：传感器节点、循迹小车、低功耗无线设备。寻找 2027 年寒假实习。",
  },
};

/** 区块顺序：导航、侧边指示器都从这里读 */
export const sections = [
  { id: "work", label: "项目" },
  { id: "skills", label: "技能" },
  { id: "timeline", label: "经历" },
  { id: "about", label: "关于" },
  { id: "contact", label: "联系" },
];

function loadFromDisk() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, "utf8"));
  } catch {
    return null;
  }
}

function persist() {
  fs.mkdirSync(DATA_DIR, { recursive: true });
  fs.writeFileSync(DATA_FILE, JSON.stringify(site, null, 2), "utf8");
}

/** 全站共享的唯一对象；后台保存时原地更新 */
export const site = { ...DEFAULTS, ...(loadFromDisk() || {}) };

// 第一次运行：把默认值落盘，方便你直接打开 data/site.json 看结构
if (!fs.existsSync(DATA_FILE)) persist();

/** 后台保存：只更新传入的字段，其余保持不变 */
export function saveSite(patch) {
  for (const [key, value] of Object.entries(patch)) {
    if (value === undefined || value === "") continue;
    if (key === "seo" && typeof value === "object") {
      site.seo = { ...site.seo, ...value };
    } else {
      site[key] = value;
    }
  }
  persist();
  return site;
}