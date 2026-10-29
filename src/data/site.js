/**
 * 站点信息的唯一出口。
 *
 * 真正的数据在 data/site.json（由 src/lib/store.js 读写），
 * 这里只做转出，让所有组件保持 `import { site } from "../data/site.js"` 不变。
 *
 * 想改内容有两条路：
 *   1. 浏览器打开 /admin 登录后台改（推荐，改完刷新即生效）
 *   2. 直接编辑 data/site.json 再重启服务
 */

import { site as store, sections } from "../lib/store.js";

/** 派生字段：导航由区块列表生成，避免两处维护 */
store.sections = sections;
store.nav = sections.map((s) => ({ href: `/#${s.id}`, label: s.label }));
store.links = store.links ?? [
  { label: "GitHub", url: store.github || "https://github.com/" },
];

export const site = store;
export { sections };