import fs from "node:fs/promises";
import path from "node:path";

const TYPES = {
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".png": "image/png",
  ".webp": "image/webp",
};

/** 处理上传的头像：防止路径穿越，只认 data/uploads 下的图片 */
export const GET = async ({ params }) => {
  const name = path.basename(params.file || "");
  const ext = path.extname(name).toLowerCase();

  if (!TYPES[ext]) {
    return new Response("Not found", { status: 404 });
  }

  const file = path.resolve(process.cwd(), "data", "uploads", name);
  try {
    const data = await fs.readFile(file);
    return new Response(data, {
      headers: {
        "Content-Type": TYPES[ext],
        // 文件名带时间戳，可以长期缓存
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch {
    return new Response("Not found", { status: 404 });
  }
};