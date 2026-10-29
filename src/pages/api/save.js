import fs from "node:fs/promises";
import path from "node:path";
import { saveSite } from "../../lib/store.js";

const TEXT_FIELDS = [
  "name",
  "nameEn",
  "headline",
  "headlineAccent",
  "tagline",
  "status",
  "jobSearch",
  "school",
  "location",
  "email",
  "github",
  "githubHandle",
  "resumeName",
];

const MAX_AVATAR_BYTES = 5 * 1024 * 1024;
const ALLOWED = {
  "image/jpeg": "jpg",
  "image/png": "png",
  "image/webp": "webp",
};

export const POST = async ({ request, redirect }) => {
  const form = await request.formData();
  const patch = {};

  for (const key of TEXT_FIELDS) {
    const value = form.get(key);
    if (typeof value === "string") patch[key] = value.trim();
  }

  // 复选框：勾选传 "on"，不勾选则完全没有这个字段
  patch.placeholder = form.get("placeholder") === "on";

  const seoTitle = form.get("seoTitle");
  const seoDescription = form.get("seoDescription");
  if (typeof seoTitle === "string" || typeof seoDescription === "string") {
    patch.seo = {
      title: typeof seoTitle === "string" ? seoTitle.trim() : undefined,
      description:
        typeof seoDescription === "string" ? seoDescription.trim() : undefined,
    };
  }

  // 头像：有文件就存到 data/uploads/，再用 /uploads/xxx 访问
  const avatar = form.get("avatar");
  if (avatar && typeof avatar === "object" && "size" in avatar && avatar.size > 0) {
    const ext = ALLOWED[avatar.type];
    if (!ext) {
      return new Response("头像只支持 JPG / PNG / WebP", { status: 400 });
    }
    if (avatar.size > MAX_AVATAR_BYTES) {
      return new Response("头像不能超过 5MB", { status: 400 });
    }

    const dir = path.resolve(process.cwd(), "data", "uploads");
    await fs.mkdir(dir, { recursive: true });
    const filename = `avatar-${Date.now()}.${ext}`;
    const buffer = Buffer.from(await avatar.arrayBuffer());
    await fs.writeFile(path.join(dir, filename), buffer);
    patch.avatar = `/uploads/${filename}`;
  }

  saveSite(patch);
  return redirect("/admin?saved=1");
};