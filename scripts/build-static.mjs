/**
 * 静态构建：给 GitHub Pages 用。
 *
 * 静态模式下没有 Node，所以必须把"需要服务端"的页面移出去再构建，
 * 否则 Astro 会尝试预渲染 /admin 和 /api，直接报错。
 *
 * 构建完会自动移回来，仓库里始终是完整版本。
 */

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const pagesDir = path.join(root, "src", "pages");
const stashDir = path.join(root, ".static-stash");

// 这些目录只在服务端模式有意义
const SERVER_ONLY = ["admin", "api", "uploads"];

function stash() {
  fs.rmSync(stashDir, { recursive: true, force: true });
  fs.mkdirSync(stashDir, { recursive: true });

  for (const name of SERVER_ONLY) {
    const from = path.join(pagesDir, name);
    if (fs.existsSync(from)) {
      fs.renameSync(from, path.join(stashDir, name));
      console.log(`  移出 ${name}/`);
    }
  }
}

function restore() {
  for (const name of SERVER_ONLY) {
    const from = path.join(stashDir, name);
    if (fs.existsSync(from)) {
      fs.renameSync(from, path.join(pagesDir, name));
      console.log(`  移回 ${name}/`);
    }
  }
  fs.rmSync(stashDir, { recursive: true, force: true });
}

console.log("静态构建：临时移出仅服务端可用的页面");
stash();

let code = 1;
try {
  const result = spawnSync("npx", ["astro", "build"], {
    stdio: "inherit",
    shell: true,
    env: { ...process.env, STATIC_BUILD: "1" },
  });
  code = result.status ?? 1;
} finally {
  restore();
}

if (code === 0) {
  // 让 GitHub Pages 不要走 Jekyll，避免下划线开头的目录被忽略
  fs.writeFileSync(path.join(root, "dist", ".nojekyll"), "");
  console.log("静态构建完成 → dist/");
}

process.exit(code);