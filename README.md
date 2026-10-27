# 个人主页 v1.0

物联网工程 2028 届 · 嵌入式硬件 / 物联网方案方向的个人主页。
用 [Astro](https://astro.build) 构建的纯静态站点，无后端、无数据库。

> **当前状态：示例内容。** 文案、数据、图片都是占位，用于确认版式。
> 替换真实内容后，把 `src/data/site.js` 里的 `placeholder: true` 改成 `false`，右下角提示会自动消失。

## 文档索引

| 文档 | 内容 | 谁该看 |
| --- | --- | --- |
| [PRD.md](PRD.md) | 需求、定位、内容策略、验收标准 | 你 / 产品视角 |
| [TECH.md](TECH.md) | 架构、数据模型、设计系统、已知技术债 | 你 / 开发者 |
| [AGENTS.md](AGENTS.md) | AI 助手的操作手册与红线 | AI / 协作者 |
| README（本文） | 怎么改内容、怎么部署 | 日常操作 |

---

## 快速开始

需要 Node.js 18 以上（建议 20+）。

```bash
npm install      # 第一次运行前执行
npm run dev      # 本地预览 http://localhost:4321
npm run build    # 生成静态站点到 dist/
npm run preview  # 预览构建结果
```

---

## 目录结构

```
src/
├── data/
│   ├── site.js        # ★ 名字、定位句、邮箱、导航、社交链接、SEO
│   ├── skills.js      # 技能地图
│   └── timeline.js    # 经历与奖项
├── content/
│   └── projects/      # ★ 每个项目一个 .md 文件
├── components/        # Hero / Terminal / 卡片 / 技能 / 时间线 / 联系 …
├── layouts/
│   └── BaseLayout.astro   # <head>、SEO、OG、JSON-LD、动效脚本
├── pages/
│   ├── index.astro           # 首页
│   ├── projects/[...slug].astro  # 项目详情页（由 md 自动生成）
│   ├── 404.astro
│   └── sitemap.xml.ts        # 自动生成 sitemap
└── styles/
    └── global.css     # ★ 设计变量与全部样式（改颜色/字体都在这里）
public/                # 静态资源：图片、简历 PDF、favicon、og.png
scripts/gen_assets.py  # 生成占位插图（上线前可删）
```

---

## 日常改内容（只需要动 4 个地方）

### 1. 改个人信息 → `src/data/site.js`

名字、定位句、状态徽章、学校、邮箱、简历文件名、导航、社交链接、SEO 描述，全在这一个文件里。

### 2. 改技能 → `src/data/skills.js`

每个技能三项：`name`（名称）、`level`（`strong` = 熟练 / `used` = 用过）、`note`（一句使用场景）。
**不要改成百分比进度条**——那是最没信息量的写法（见 PRD 5/F5）。

### 3. 改经历 → `src/data/timeline.js`

倒序排列，最新的在最上面。`now: true` 表示「正在进行」，时间线圆点会变成绿色。

### 4. 加项目 → `src/content/projects/新建一个.md`

复制任意一个现有文件，改开头这段（frontmatter）：

```markdown
---
title: "项目名"
summary: "一句话说清做了什么、解决了什么问题"   # 会显示在卡片上
role: "你在项目里的角色"
period: "2026.03 — 2026.06"
status: "done"          # done = 已完成，wip = 进行中
featured: true          # true = 首页旗舰大卡（只设一个）
order: 1                # 数字小的排前面
tags: ["STM32", "MQTT"]
cover: "/img/你的封面.png"     # 图片放 public/img/
coverAlt: "图片描述（给屏幕阅读器）"
stats:                  # 卡片上的 4 个关键数据
  - { value: "±0.3", unit: "℃", label: "温度精度" }
links:
  repo: "https://github.com/..."
---

## 一句话
正文用 Markdown 写，图片写成 `![说明](/img/xxx.png)`
```

文件名就是网址：`env-node.md` → `/projects/env-node/`。

> 字段写错会在 `npm run build` 时报错并告诉你哪一行错了，不会悄悄漏掉。

---

## 换图片和简历

- 图片放 `public/img/`，Markdown 里写 `/img/文件名.png`
- 封面图建议 1600×1000（16:10），压缩到 300KB 以内
- 简历放 `public/`，然后改 `src/data/site.js` 里的 `resume` 字段
- 换分享卡片图：替换 `public/og.png`（1200×630）

> 现在的 PCB / 原理图 / 架构图都是 `scripts/gen_assets.py` 画的**占位图**。
> 上线前换成你自己导出的 EDA 截图和实物照片，效果会好得多。

---

## 改视觉

`src/styles/global.css` 顶部是全部设计变量（Stark HUD 深色主题）：

```css
--bg: #070c14;       /* 页面底色：深蓝黑 */
--surface: #0c1826;  /* 卡片 / 面板，比底色亮一档 */
--line: rgba(96, 176, 255, 0.18);  /* 描边，带一点青 */
--ink: #e8f1fa;      /* 主文字 */
--ink-2: #a3b6cb;    /* 次要文字 */
--cyan: #4fd8ff;     /* 主色：强调、链接、数据、悬停 */
--amber: #f0b45a;    /* 金色：只用于「旗舰项目」「进行中」 */
--green: #35d6a4;    /* 状态点 */
```

**配色原则**：整站只有一档深蓝底 + 一档面板色，靠「亮度」分层；青色只出现在需要你注意的地方（数字、链接、悬停、编号），金色只做极少点缀。**不要同时给三个元素加强调色**，否则就没有重点了。
动效的开关在 `src/layouts/BaseLayout.astro` 的 `<script>` 里，尊重系统的「减少动态效果」设置。

---

## 部署

### Cloudflare Pages（推荐）

1. 把项目推到 GitHub
2. Cloudflare Pages → Connect to Git → 选仓库
3. Build command：`npm run build`；Output directory：`dist`
4. 绑定自定义域名

### Vercel

同样连 Git 仓库即可，框架会自动识别为 Astro。
注意：`*.vercel.app` 域名在国内部分网络打不开，**务必绑定自己的域名**。

### GitHub Pages

在仓库 Settings → Pages 选 GitHub Actions，用官方 Astro 模板即可。
访问速度一般，只适合先上线看看。

---

## 上线前检查清单

- [ ] `src/data/site.js` 的 `placeholder` 改成 `false`
- [ ] `site.url` 改成你的真实域名（影响 canonical / OG / sitemap）
- [ ] 邮箱、GitHub、Gitee 改成真实链接
- [ ] 换掉 `public/resume-preview.pdf` 和 `site.resume` 文件名
- [ ] 三个示例项目：要么换成真实项目，要么删掉 md 文件
- [ ] `public/robots.txt` 里的 sitemap 域名改成你的
- [ ] 替换 `public/og.png`（微信分享卡片会用它）
- [ ] 手机上打开一遍，确认没有横向滚动
- [ ] 用招聘方的视角看一遍：30 秒能不能说清你是谁

---

## 技术说明

- **Astro 6**：输出纯静态 HTML，默认不带 JS，首屏快。
  （v0.1 最初用 Astro 7，但本机 Node 24 + Vite 的模块加载器加载内容集合时会报
  `require is not defined`，降到 6.x 后稳定，功能不受影响。）
- **手写 CSS + 设计变量**，没有用 Tailwind。
  原因：你只写过一点 HTML/CSS，`--bg`、`.card` 这种写法比一堆工具类更好读、更好改。
- **字体三层**：
  - 标题 `--font-display`：Bahnschrift（Windows 自带的 DIN 系字体，数字和英文很有工业感），
    中文自动回落微软雅黑
  - 正文 `--font-sans`：系统黑体栈
  - 等宽 `--font-mono`：Consolas / JetBrains Mono，**末尾挂中文字体**——
    否则等宽字体里出现的汉字会被系统替换成宋体，又细又出戏（这就是之前那个问题的原因）
- **无外部字体请求**：全部走本机字体，国内加载零风险、零 KB。
- **背景动效**：全站有一层固定的缓慢流动光晕 + 极淡网格（`BaseLayout.astro` 里的 `.ambient`），
  首屏另有粒子网络（canvas）和 HUD 圆环（纯 CSS 旋转）；都受 `prefers-reduced-motion` 控制。
- **无 JS 也能看**：滚动淡入和终端打字机都是渐进增强，禁用 JS 后内容完整可见。
- **动画尊重 `prefers-reduced-motion`**。

## 已知待办

- [ ] 项目数量目前是 2 个完整 + 1 个进行中，建议按 PRD 附录 D 再补一个自制板卡项目
- [ ] 博客、`/uses` 页还没做（PRD P1）
- [ ] 微信二维码、真实头像还没放
