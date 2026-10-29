import { defineConfig } from "astro/config";
import node from "@astrojs/node";

/**
 * 两种构建模式：
 *
 *   默认（npm run dev / npm run build）
 *     → 服务端渲染，带后台，能登录能保存，需要 Node 运行环境
 *
 *   STATIC_BUILD=1（npm run build:static）
 *     → 纯静态导出，只给 GitHub Pages 用，没有后台
 *
 * 原因是 GitHub Pages 不能执行代码，只能托管静态文件。
 */
const isStatic = process.env.STATIC_BUILD === "1";

export default defineConfig({
  // 站点地址：影响 canonical / OG / sitemap
  site: process.env.SITE_URL || "https://ppp12138sleep.github.io",

  output: isStatic ? "static" : "server",
  ...(isStatic ? {} : { adapter: node({ mode: "standalone" }) }),

  // 关掉开发工具条：它只在 npm run dev 时出现，
  // 但会挡住页面底部，演示时容易被误认为是站点的一部分
  devToolbar: { enabled: false },
});