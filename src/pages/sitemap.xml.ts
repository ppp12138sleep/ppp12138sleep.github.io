import type { APIRoute } from "astro";
import { getCollection } from "astro:content";
import { site } from "../data/site.js";

/** 构建时自动生成 sitemap，域名取自 src/data/site.js 的 url */
export const GET: APIRoute = async () => {
  const projects = await getCollection("projects");
  const paths = ["/", ...projects.map((p) => `/projects/${p.id}/`)];

  const body = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${paths.map((p) => `  <url><loc>${new URL(p, site.url).href}</loc></url>`).join("\n")}
</urlset>
`;

  return new Response(body, {
    headers: { "Content-Type": "application/xml; charset=utf-8" },
  });
};
