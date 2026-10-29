import { defineConfig } from "astro/config";
import node from "@astrojs/node";

// 站点地址：影响 canonical / OG / sitemap
// 部署到 Render / Vercel 时，用环境变量 SITE_URL 覆盖
export default defineConfig({
  site: process.env.SITE_URL || "http://localhost:4321",

  // 从「构建时生成静态页」改为「请求时由服务端渲染」：
  // 后台改完内容，刷新页面就能看到，不需要重新构建
  output: "server",
  adapter: node({ mode: "standalone" }),

  // 关掉开发工具条：它只在 npm run dev 时出现，
  // 但会挡住页面底部，演示时容易被误认为是站点的一部分
  devToolbar: { enabled: false },
});