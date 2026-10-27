# 技术文档

> 配套文档：[PRD.md](PRD.md)（做什么、为什么）· [README.md](README.md)（怎么用）
> 本文档描述**已经实现的代码**，不是计划。如果两者冲突，以代码为准，并回来改这份文档。

| 项 | 值 |
| --- | --- |
| 版本 | v1.0（2026-10-27） |
| 框架 | Astro 6.4.8（SSG） |
| Node | 24.18.0（**最低 22.12**，Astro 6 硬性要求） |
| 依赖数量 | 1 个直接依赖：`astro` |
| 源码 | 24 个文件，~2140 行 CSS |
| 构建产物 | 18 个文件，~360 KB |

---

## 1. 架构总览

纯静态站点。**没有服务端、没有数据库、没有客户端框架**。所有页面在构建时生成成 HTML，运行时只有三段不到 200 行的内联脚本。

```
内容源                     构建时                         产物
─────────────────────────────────────────────────────────────────
src/content/projects/*.md ─┐
src/data/*.js             ─┼→ Astro SSG ─→ dist/
src/pages/*.astro         ─┘                 ├─ index.html
                                            ├─ projects/<slug>/index.html
public/（图片/PDF/图标）   ─────复制──────→   ├─ 404.html
                                            ├─ sitemap.xml
                                            └─ _astro/*.css
```

### 构建期 vs 运行期

| 阶段 | 发生什么 |
| --- | --- |
| 构建 | 读取 content collection（zod 校验 frontmatter）→ `getStaticPaths` 生成详情页 → 内联 CSS 提取 → 输出静态文件 |
| 运行 | 浏览器只做三件事：滚动淡入、背景粒子、终端打字。**没有 hydration，没有 React/Vue runtime** |

这也是首屏 JS 能控制在 ~2 KB 的原因：页面里没有框架，只有内联 `<script>`。

---

## 2. 技术选型与偏差记录

| 层 | 选择 | 理由 |
| --- | --- | --- |
| 框架 | Astro 6 | 内容型站点零 JS 输出；`getStaticPaths` + Markdown 直接满足"加项目只改一个文件" |
| 样式 | **手写 CSS + 自定义属性** | 使用者的 CSS 基础只有入门水平，`--bg` / `.card` 比工具类可读；同时少一层构建依赖 |
| 语言 | JavaScript（非 TS） | 降低维护门槛；只有 `content.config.ts` 用了 TS（Astro 约定） |
| 动效 | 原生 CSS + 少量 JS | 不引入动画库；全部基于 `transform` / `opacity` |
| 字体 | 系统字体栈 | 无外部请求，国内零加载风险 |

### 与 PRD 的偏差

| PRD 写的 | 实际 | 原因 |
| --- | --- | --- |
| Astro 7.x | **6.4.8** | 7.x 的内容集合在本机 Node 24 + Vite 下加载 `yaml`/`picomatch` 等 CJS 包时报 `require is not defined`，构建直接失败；6.x 稳定，API 一致 |
| Tailwind CSS | 手写 CSS | 见上；且设计高度定制（HUD 光效），工具类反而更啰嗦 |
| 亮色为主 + 深色块 | **全站深色（Stark HUD）** | 使用者在评审后改了主意（PRD v1.2） |
| Google Fonts | 系统字体 | 国内可达性 + 体积 |
| 手写 sitemap.xml | `src/pages/sitemap.xml.ts` 构建时生成 | 避免域名维护两处 |

---

## 3. 目录结构

```
├── astro.config.mjs          # 只有 site 配置
├── package.json              # 1 个依赖
├── PRD.md / README.md / TECH.md / AGENTS.md
├── scripts/
│   └── gen_assets.py         # 生成占位插图、OG 图、favicon、占位简历 PDF
├── public/                   # 原样复制的静态资源
│   ├── img/*.svg             # 6 张占位图（PCB / 原理图 / 架构图 / 波形）
│   ├── og.png                # 1200×630 分享卡片
│   ├── favicon.svg
│   ├── apple-touch-icon.png
│   ├── resume-preview.pdf    # 占位简历
│   └── robots.txt
└── src/
    ├── content.config.ts     # 项目集合的 zod schema
    ├── content/projects/     # ★ 每个项目一个 .md
    │   ├── env-node.md       # 旗舰
    │   ├── line-car.md
    │   └── door-sensor.md    # 进行中
    ├── data/                 # ★ 手写数据模块（无校验）
    │   ├── site.js           # 姓名、定位、邮箱、GitHub、导航、SEO、url
    │   ├── skills.js         # 技能分组
    │   └── timeline.js       # 经历与奖项
    ├── layouts/BaseLayout.astro   # <head>、SEO、ambient 背景、三段内联脚本
    ├── components/           # 11 个纯展示组件
    ├── pages/
    │   ├── index.astro
    │   ├── projects/[...slug].astro
    │   ├── 404.astro
    │   └── sitemap.xml.ts
    └── styles/global.css     # ~2140 行，唯一样式文件
```

### 为什么样式只有一个文件

组件级 `<style>` 会把设计系统切碎，改一个颜色要翻十几个文件。现在所有 token 在 `:root`，组件样式按块排列并用注释分隔，搜索类名即可定位。

---

## 4. 内容模型

### 4.1 项目（有校验）

`src/content.config.ts` 用 zod 定义，**字段写错会在 build 时报错并指出行号**。

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `title` | string | ✅ | 卡片和详情页标题 |
| `summary` | string | ✅ | 一句话，出现在卡片上 |
| `role` | string | ✅ | 你的角色（硬件岗会看） |
| `period` | string | ✅ | 如 `2026.03 — 2026.06` |
| `status` | `done` \| `wip` | 默认 `done` | `wip` 显示"进行中"琥珀标签 |
| `featured` | boolean | 默认 false | 首页旗舰大卡，只应有一个 |
| `order` | number | 默认 99 | 升序排列 |
| `tags` | string[] | 默认 [] | 技术标签，显示为 chip |
| `cover` | string | ✅ | `/img/xxx.svg`，放 `public/img/` |
| `coverAlt` | string | ✅ | 无障碍描述 |
| `stats` | `{value, unit?, label}[]` | 默认 [] | 卡片上的 4 个关键指标 |
| `links.repo` / `.demo` / `.video` | string | 可选 | 详情页侧栏按钮 |

正文是 Markdown，支持 GFM 表格。图片用 `![alt](/img/xxx.svg)`。

### 4.2 站点 / 技能 / 经历（无校验）

`src/data/*.js` 是普通 ES 模块导出。**优点**是改起来直观，**缺点**是字段写错不会有任何提示，只会在页面上渲染成 `undefined`。修改这三份数据后必须肉眼检查页面。

### 4.3 数据流向

```
site.js ──→ BaseLayout（SEO / JSON-LD）· Header · Hero · About · Contact · Footer
skills.js ─→ Skills.astro
timeline.js → Timeline.astro
content/projects/*.md ─→ index.astro（列表）· [...slug].astro（详情）
```

---

## 5. 路由与页面

| 路由 | 文件 | 渲染方式 |
| --- | --- | --- |
| `/` | `index.astro` | 静态，遍历 collection 排序后渲染 |
| `/projects/<slug>/` | `[...slug].astro` | `getStaticPaths` 按 md 文件名生成 |
| `/404.html` | `404.astro` | 静态；Cloudflare/GitHub Pages 会自动使用 |
| `/sitemap.xml` | `sitemap.xml.ts` | 构建时生成 XML（GET endpoint） |

**详情页 URL 即文件名**：`env-node.md` → `/projects/env-node/`。

---

## 6. 组件清单

| 组件 | 职责 | 关键 props |
| --- | --- | --- |
| `BaseLayout` | head/SEO/JSON-LD、ambient 背景、三段内联脚本 | `title` `description` `image` `type` |
| `Header` | 吸顶导航、品牌标志（内联 SVG 六边形）、GitHub 图标、简历按钮 | — |
| `Hero` | 首屏文案、状态徽章、双 CTA、HUD 圆环 | 读 `site` |
| `Terminal` | 伪终端窗口，逐字打印 | 无（内容写死） |
| `SectionHead` | 区块标题（编号 / 英文眼眉 / 中文标题 / 说明） | `index` `en` `title` `desc` `link` |
| `FlagshipCard` | 旗舰项目大卡 | `project` |
| `ProjectCard` | 常规项目卡（含"进行中"状态） | `project` |
| `Skills` | 技能分组网格 | 读 `skillGroups` |
| `Timeline` | 经历时间线 | 读 `timeline` |
| `About` | 关于我 + 事实卡 | 读 `site` |
| `Contact` | 三个大号入口卡 | 读 `site` |
| `Footer` | 版权与邮箱 | 读 `site` |

所有组件都是**纯展示 + 读全局数据**，没有状态、没有事件（少数交互在 BaseLayout 的脚本里统一委托）。

---

## 7. 设计系统

### 7.1 颜色 token

| Token | 值 | 语义 | 使用约束 |
| --- | --- | --- | --- |
| `--bg` | `#070c14` | 页面底 | — |
| `--surface` / `--surface-2` | `#0c1826` / `#12202f` | 卡片、面板 | 靠亮度分层 |
| `--line` | `rgba(96,176,255,.18)` | 描边 | 所有分割线 |
| `--ink` / `--ink-2` / `--ink-3` | `#e8f1fa` / `#a3b6cb` / `#7c90a6` | 文字三档 | `--ink-3` 对 `--bg` 约 5:1 |
| `--cyan` | `#4fd8ff` | 强调 | **同一屏只允许一个元素用它当焦点** |
| `--amber` | `#f0b45a` | 金色 | 仅"旗舰项目""进行中" |
| `--green` | `#35d6a4` | 状态 | 仅"可实习"状态点 |

### 7.2 字体三层

```css
--font-display: Bahnschrift, "DIN Alternate", ..., "Microsoft YaHei";  /* 标题、数字 */
--font-sans:    Inter, "HarmonyOS Sans SC", "Microsoft YaHei", ...;    /* 正文 */
--font-mono:    "JetBrains Mono", Consolas, ..., "Microsoft YaHei";    /* 标签、代码、数据 */
```

> **关键约束**：等宽栈末尾必须挂中文字体。否则中文会回落到系统"等宽中文字体"= 宋体，又细又出戏。

### 7.3 断点

| 断点 | 变化 |
| --- | --- |
| `≤960px` | 首屏单列、旗舰卡上下堆叠、HUD 圆环隐藏、侧栏取消 sticky |
| `≤760px` | 技能/项目/关于单列、导航链接隐藏（**已知缺口**）、统计两列 |
| `≤420px` | 姓名缩到 30px、卡片底部改为纵向 |

---

## 8. 动效系统

分三层，**全部可降级**：

### 8.1 背景层（常驻）

| 元素 | 实现 | 参数 |
| --- | --- | --- |
| 光晕 ×2 | CSS `radial-gradient` + `translate3d` 关键帧 | 26s / 34s，`alternate` |
| 网格 | 两个 `linear-gradient` 拼 76px 网格 + `mask` 渐隐 | 5% 透明度 |
| 粒子网络 | `<canvas>`，节点漂移，距离 < 152px 连线 | 节点数 `clamp(30, 78, 面积/19000)`，DPR 上限 2 |

粒子脚本在 `BaseLayout`，**全站生效**；页面隐藏时 `cancelAnimationFrame`，避免后台耗电。

### 8.2 首屏层

- HUD 圆环 ×3：纯 CSS `rotate`，72s / 46s（反向）/ 94s
- 环绕光点 ×2：内外圈反向旋转，24s / 32s
- 终端打字机：逐字 38–78ms，每行出结果后停 260ms；`visibilitychange` 立即中断

### 8.3 交互层

| 元素 | 效果 |
| --- | --- |
| 项目卡 hover | 上浮 5px + 边框变青 + 顶部流光 + 图片 `scale(1.05)` + 底部暗渐变 + 标题变青 |
| 联系卡 hover | 上浮 6px + 青边 + **扫光横穿** + 箭头斜移 + 标题变色 |
| 滚动进入 | `IntersectionObserver` 双向 toggle：进入淡入、完全离开复位（可重复触发） |

### 8.4 降级规则

```js
if (!matchMedia("(prefers-reduced-motion: reduce)").matches) { /* 才启动 */ }
```

- 减少动效：粒子不启动、reveal 不启用（内容直接可见）、CSS 动画被媒体查询压到 0.001ms
- 无 JS：内容完整可见，只是没有动画
- 触摸设备：`@media (hover: none)` 取消 hover 位移（避免"粘住"）

---

## 9. SEO 与元信息

| 项 | 实现位置 |
| --- | --- |
| `<title>` / description | `BaseLayout`（详情页用 md 的 `summary`） |
| canonical | `new URL(Astro.url.pathname, site.url)` |
| OG / Twitter | `og.png`（1200×630，脚本生成） |
| JSON-LD | `Person`，含 `sameAs`（GitHub）、`knowsAbout`、`affiliation` |
| sitemap | `sitemap.xml.ts`，遍历 collection |
| robots | `public/robots.txt`（**域名仍是 example.com，上线前必须改**） |
| 语义结构 | 每页唯一 `h1`，区块用 `<section>` + `h2` |

---

## 10. 性能

| 指标 | 目标 | 现状 |
| --- | --- | --- |
| 首屏 JS | ≤ 100 KB | ~2 KB（三段内联脚本，无框架） |
| CSS | — | 单个 ~30 KB 文件（未压缩） |
| 图片 | ≤ 300 KB/张 | 占位 SVG 均 < 20 KB |
| 字体请求 | 0 | 0（全系统字体） |
| 外部依赖 | 0 | 0（无 CDN、无统计脚本） |

优化点已做：图片 `loading="lazy"` + 显式宽高（防 CLS）、DPR 上限 2、`transform`/`opacity` 动画、后台暂停动画。

---

## 11. 构建与部署

```bash
npm install
npm run dev      # localhost:4321
npm run build    # → dist/
npm run preview
```

**当前状态：未部署，也没有 git 仓库。** `site.url` 仍是 `https://example.com`。

部署路径（详见 PRD 与 README）：

- 源码推到 GitHub → 用 GitHub Actions / Cloudflare Pages 执行 `npm run build`，产物目录 `dist`
- 或用 `python -m http.server -d dist` 做本地预览（仅同机可见）

> 注意：GitHub Pages 的**项目仓库**会部署到子路径（`/repo/`），而站内全是 `/img/...` 根路径引用，会 404。要么仓库名用 `<user>.github.io`（根路径），要么配 `base` —— 前者更省事。

---

## 12. 可访问性

已做：
- `:focus-visible` 焦点环（青色，2px）
- 跳转链接（`.skip-link`）
- 所有交互元素有 `aria-label` 或可见文本
- 图片有 `alt`（封面图在 frontmatter 里强制必填）
- `lang="zh-CN"`、`color-scheme`
- 文字对比度：正文 ≥ 7:1，次要文字 ≥ 5:1
- 装饰层（粒子、圆环、光晕）全部 `aria-hidden="true"` + `pointer-events: none`

未做：
- 未跑 axe / Lighthouse 自动审计
- 键盘 Tab 顺序未人工验证

---

## 13. 已知限制与技术债

| # | 问题 | 影响 | 优先级 |
| --- | --- | --- | --- |
| 1 | **移动端（<760px）导航链接被隐藏，且无汉堡菜单** | 手机用户无法跳转到各区块 | 高 |
| 2 | 原理图/PCB 图不能点击放大 | 硬件岗看不清楚标注 | 高 |
| 3 | 三份 `src/data/*.js` 无字段校验 | 拼错字段静默渲染成空 | 中（可迁移到 zod schema） |
| 4 | 内容全是占位（项目、图、简历 PDF） | 不能直接拿去找工作 | 高（非技术问题） |
| 5 | `robots.txt`、`sitemap` 域名仍是 `example.com` | 上线后 SEO 指向错误 | 中 |
| 6 | 无 git 仓库、无 CI | 没有版本历史、无法自动部署 | 中 |
| 7 | 无任何自动化测试 | 改动靠肉眼 | 低（静态站收益有限） |
| 8 | 首屏三个动效同时运行 | 低端机可能掉帧（未实测） | 低 |

---

## 14. 扩展指南

### 加一个项目

1. 复制 `src/content/projects/env-node.md`
2. 改 frontmatter（`order` 决定顺序，`featured: true` 变成旗舰卡）
3. 图片放 `public/img/`，正文用 Markdown
4. `npm run build` —— 字段错了会报错

### 改配色

只改 `:root` 里的 token。**不要**在组件里写死十六进制，否则暗色主题会破。

### 换字体

改三个 `--font-*`。如果引入中文字体文件，务必只保留站内用到的字符（子集化），否则单文件 3–5 MB。

### 加一个页面

在 `src/pages/` 建 `.astro` 文件，用 `BaseLayout` 包裹，顶部加个 `<SectionHead>` 即风格统一。

### 加一个数据模块

参照 `skills.js`：`export const xxx = [...]`，然后在组件里 `import` 并 `map`。**记得在页面里肉眼检查**——它没有 schema 保护。

---

## 15. 决策记录（ADR 摘要）

| 决策 | 结论 | 代价 |
| --- | --- | --- |
| SSG 而非 SSR | 静态输出 | 无动态能力（留言、搜索需另加） |
| 单 CSS 文件 | 集中管理 | 文件长（~2100 行），靠注释分块 |
| 无 UI 框架 | 零 runtime | 复杂交互要手写 |
| 全站深色 | 符合使用者审美 | 打印/亮环境可读性略差 |
| 系统字体 | 零请求 | 跨平台观感不完全一致 |
| 占位素材脚本化 | 可一键重生成 | 上线前必须替换全部 |
