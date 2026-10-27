import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/**
 * 项目集合 —— 加新项目 = 在 src/content/projects/ 里新建一个 .md
 * 字段写错会在 build 时报错，不会悄悄漏字段。
 */
const projects = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/projects" }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    role: z.string(),
    period: z.string(),
    status: z.enum(["done", "wip"]).default("done"),
    featured: z.boolean().default(false),
    order: z.number().default(99),
    tags: z.array(z.string()).default([]),
    cover: z.string(),
    coverAlt: z.string(),
    stats: z
      .array(
        z.object({
          value: z.string(),
          unit: z.string().optional(),
          label: z.string(),
        }),
      )
      .default([]),
    links: z
      .object({
        repo: z.string().optional(),
        demo: z.string().optional(),
        video: z.string().optional(),
      })
      .default({}),
  }),
});

export const collections = { projects };
