# 部署指南

> 站点从 v2.0 起是**服务端渲染（SSR）**，需要能执行 Node 的运行环境。
> **GitHub Pages 只能托管静态文件，已经不能用了**（旧的静态版本仍在线，不会自动更新）。

## 为什么不能再用 GitHub Pages

| | 静态托管（Pages） | 服务端（Render / Vercel） |
| --- | --- | --- |
| 提供 HTML 文件 | ✅ | ✅ |
| 执行 Node 代码 | ❌ | ✅ |
| 后台保存能写文件 | ❌ | ✅ |
| 登录态 cookie | ❌ | ✅ |

后台的「保存修改」要写 `data/site.json`，这是 Pages 做不到的事。

---

## 方案 A：Render（推荐，免费）

### 1. 准备

代码已经在 GitHub：`ppp12138sleep/ppp12138sleep.github.io`

### 2. 创建服务

1. 打开 <https://render.com>，用 GitHub 账号登录
2. 点 **New → Blueprint**
3. 选仓库 `ppp12138sleep.github.io`，Render 会自动读到根目录的 `render.yaml`
4. 点 **Apply**

### 3. 填环境变量

创建时会要求填三个值：

| 变量 | 填什么 |
| --- | --- |
| `ADMIN_PASSWORD` | 你后台的登录密码（自己定，别用示例值） |
| `ADMIN_SECRET` | 点「Generate」随机生成即可 |
| `SITE_URL` | 先留空或填临时值，部署完拿到域名后再回来改 |

### 4. 等 2~5 分钟

构建命令是 `npm install && npm run build`，启动命令是 `node ./dist/server/entry.mjs`。
成功后会得到一个 `https://xxxx.onrender.com` 的地址。

### 5. 回填 SITE_URL

把上一步拿到的域名填进 `SITE_URL`（例如 `https://personal-portfolio-abc1.onrender.com`），保存后会自动重新部署。
这个值决定 canonical、分享卡片和 sitemap 里的链接。

### 6. 验证

| 检查 | 期望 |
| --- | --- |
| 打开首页 | 正常显示，左下角有「⚙ 后台」 |
| 点后台 → 输密码 | 进入编辑页 |
| 改个名字 → 保存 | 首页立刻变 |
| 上传头像 | 首屏头像换成新的 |

---

## 方案 B：Vercel

Vercel 是 Serverless，文件系统只读，`data/site.json` **写不进去**，需要先把存储换成数据库（KV / Postgres / Supabase）或改用 Vercel Blob。

如果你只是想跑起来给老师看，用方案 A 更省事。

---

## 方案 C：本地演示（不联网）

```bash
npm install
npm run dev
# 打开 http://localhost:4321
```

适合交作业时现场演示，或网络不通的时候。

---

## 免费套餐的限制（要知道）

1. **休眠**：Render 免费实例 15 分钟无访问会休眠，下次访问要等 30~60 秒唤醒
2. **磁盘不持久**：重新部署或重启后，`data/site.json` 会回到仓库里的版本
   - 解决办法：每次后台改完，把 `data/site.json` 提交一次
   ```bash
   git add data/site.json
   git commit -m "更新站点内容"
   git push
   ```
3. **上传的头像不持久**：`data/uploads/` 没提交到仓库，重新部署会丢
   - 长久的做法是把头像放进 `public/` 并改 `data/site.json` 的 `avatar` 指向它

---

## 常见问题

**构建失败：`Node version is not supported`**
→ `render.yaml` 里已经指定 `NODE_VERSION=22`，确认环境变量有没有被手动删掉。

**打开是 404 / 白屏**
→ 检查 Start Command 是不是 `node ./dist/server/entry.mjs`。

**后台能登录，保存没反应**
→ 看服务日志，多半是目录权限或磁盘只读；确认没用 Vercel。

**改了内容过几天消失了**
→ 免费实例磁盘重置，见上面「磁盘不持久」。把 `data/site.json` 提交进仓库最稳。