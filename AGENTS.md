# AGENTS.md

给在本仓库工作的 AI 编码助手的操作手册。**先读这份，再动代码。**

## 0. 项目是什么

一个人的求职作品集网站：Astro 6 静态生成，全站深色 HUD 风格，中文内容。
只有 1 个运行时依赖（`astro`），没有数据库、没有后端、没有客户端框架。

阅读顺序：

1. `PRD.md` —— 为什么做、给谁看、内容策略（**产品意图以它为准**）
2. `TECH.md` —— 代码怎么组织的（**实现事实以它为准**）
3. `README.md` —— 使用者视角的操作说明
4. 本文件 —— 你怎么改、不许怎么改

若文档与代码冲突：以代码为准，并顺手更新文档。

---

## 1. 环境与命令

```bash
npm install          # 仅首次
npm run dev          # http://localhost:4321
npm run build        # 产物 dist/，同时做内容校验
npm run preview      # 预览构建结果
```

- Node ≥ 22.12（Astro 6 硬性要求；开发机是 24.18.0）。CI 里必须显式 `setup-node@22`，默认的 Node 20 会构建失败
- **没有测试套件**，`npm run build` 就是唯一的自动化门禁
- 没有 lint / prettier 配置，风格靠本文件约束

---

## 2. 硬性禁止

| 禁止 | 原因 |
| --- | --- |
| 把 `astro` 升到 7.x | 7.x 的内容集合在本机 Node 24 下加载 CJS 依赖会报 `require is not defined`，构建直接挂。**锁 6.x** |
| 引入 Tailwind / React / Vue / 动画库 | 会破坏"零 runtime"的前提；现有手写 CSS 已覆盖需求 |
| 引入外部字体 CDN | 国内可达性 + 首屏体积 |
| 在组件里写死颜色值 | 必须用 `:root` 的 token，否则换主题会破 |
| 删掉 `.demo-chip` 或 `placeholder` 开关 | 那是"尚未替换占位内容"的唯一提示 |
| 把手机号、身份证号、住址写进任何内容文件 | 站点是公开的，会被爬 |
| 提交 `node_modules/`、`dist/`、`.astro/` | 已在 `.gitignore` |
| 用脚本批量改含中文的文件（尤其 PowerShell 的 `Get-Content`/`Set-Content`） | 编码/换行极易损坏，曾把中文注释写成乱码。用带文件读写能力的编辑器工具 |
| 在等宽字体栈末尾去掉中文字体 | 中文会回落到宋体，页面立刻"出戏" |

---

## 3. 改动地图

| 想改什么 | 去哪里 |
| --- | --- |
| 姓名、学校、邮箱、GitHub、求职状态、SEO 文案 | `src/data/site.js` |
| 技能分组 | `src/data/skills.js` |
| 经历与奖项 | `src/data/timeline.js` |
| 新增/修改项目 | `src/content/projects/*.md` |
| 首页结构（区块顺序） | `src/pages/index.astro` |
| 首屏文案与按钮 | `src/components/Hero.astro` |
| 终端里的假命令 | `src/components/Terminal.astro` |
| 联系区三张卡 | `src/components/Contact.astro` |
| 配色、字号、间距、动效参数 | `src/styles/global.css` 的 `:root` 与对应块 |
| 滚动淡入 / 粒子 / 打字机 | `src/layouts/BaseLayout.astro` 底部 `<script>` |
| SEO / OG / JSON-LD | `src/layouts/BaseLayout.astro` 顶部 |
| sitemap | `src/pages/sitemap.xml.ts` |
| 占位插图、OG 图、favicon、占位简历 | `scripts/gen_assets.py`（改完跑一次） |

---

## 4. 代码规范

- **组件**：`.astro`，纯展示 + 从 `src/data` 读数据；不写业务状态
- **样式**：只写在 `src/styles/global.css`，按"区块注释 → 选择器"排列；不要新建组件级 `<style>`
- **类名**：BEM-lite，`block__element--modifier`，例：`link-card__value`、`btn--primary`
- **数据**：`src/data/*.js` 用 `export const`，字段命名小驼峰
- **注释**：中文，解释"为什么"而不是"是什么"；魔法数字要写来源
- **JS**：ES2020+，不用 TypeScript（只有 `content.config.ts` 例外）

---

## 5. 设计约束

这些不是审美偏好，是已定的规则。改之前先确认使用者同意。

### 颜色

- 同一屏**只允许一个元素**用 `--cyan` 作为视觉焦点
- `--amber` 只用于"旗舰项目"和"进行中"标签
- `--green` 只用于"可实习"状态点
- 层次靠**亮度**（`--bg` → `--surface` → `--surface-2`），不靠更多颜色

### 字体

```css
--font-display  /* 标题、数字：Bahnschrift → 中文回落黑体 */
--font-sans     /* 正文 */
--font-mono     /* 标签、数据、代码；末尾必须挂中文字体 */
```

中文不要用衬线；等宽块里的中文必须走黑体回落。

### 动效

- 只用 `transform` / `opacity`，不触发布局
- 必须处理 `prefers-reduced-motion: reduce`（JS 用 matchMedia 判断，CSS 用媒体查询）
- 常驻动画要能暂停（`visibilitychange`）
- 单个入场动效 ≤ 600ms；不要自动播放音视频
- 新增全屏动画前先算：帧率、GPU 层数、低端机表现

---

## 6. 内容规范

- 新增项目必须填齐：`title` `summary` `role` `period` `cover` `coverAlt` `stats`（≥ 2 条）
- `featured: true` 全站**只应有一个**
- `stats` 必须是**可量化的真实指标**（精度、延迟、功耗、成本），不要写"很好用"
- 占位内容必须在文案里能看出来是示例，**不得伪装成真实经历**
- 中英混排时数字与中文之间留空格（如 `STM32 采集`）
- 不要出现"致力于""热爱学习"这类无信息量的句子

---

## 7. 完成定义（DoD）

改完之后逐条确认：

- [ ] `npm run build` 通过，无警告级报错
- [ ] 四个路由都能打开：`/`、`/projects/env-node/`、`/projects/line-car/`、`/404.html`
- [ ] 390px 宽度无横向滚动
- [ ] 键盘 Tab 能走完首屏可交互元素
- [ ] 开 `prefers-reduced-motion` 后没有强制动画
- [ ] 新增/修改的文案在页面上渲染正常（**尤其 `src/data/*.js`，它没有 schema 校验**）
- [ ] 改动了结构或约定时，同步更新 `TECH.md`

---

## 8. 已验证的坑

1. **Astro 7 构建失败**：`require is not defined`（yaml / picomatch 等 CJS 包）。解决办法是留在 6.x，不要去 alias 或 polyfill。
2. **中文变宋体**：等宽字体（Consolas）没有中文字形，系统回落到 SimSun。修复方式唯一：在 `--font-mono` 末尾追加中文字体。
3. **Windows 构建偶发 `spawn EPERM`**：Vite 会调用 `net use` 探测网络盘，在受限环境里被拒绝。正常桌面环境下不会出现；受限环境下需要放宽权限再构建。
4. **`npm install` 报缓存 EPERM**：把 `npm_config_cache` 指向项目内的 `.npm-cache/`。
5. **修改 `astro.config.mjs` 的 `site` 不生效**：canonical / OG / sitemap 实际读的是 `src/data/site.js` 的 `url` 字段。**改那个**。
6. **GitHub Pages 子路径 404**：站内全是 `/img/...` 根路径，部署到 `/repo/` 会全挂。仓库名用 `<user>.github.io` 走根路径。

---

## 9. 当前待办（按优先级）

1. 真实内容替换：3 个项目、头像、简历 PDF、真实 EDA 截图
2. 移动端导航（`<760px` 目前没有任何跳转入口）
3. 图片灯箱（原理图/PCB 需要可放大）
4. `src/data/*.js` 加运行时校验（或迁移到 content collection 的 zod）
5. 上线：初始化 git → 推 GitHub → 配 Pages；同步改 `site.js` 的 `url` 与 `public/robots.txt`

> 不要主动做上面没被要求的事；尤其不要为了"更完善"而新增页面或功能，这个项目的克制是刻意设计的。
