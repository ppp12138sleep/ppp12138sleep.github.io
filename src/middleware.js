import { defineMiddleware } from "astro:middleware";
import { isAuthed } from "./lib/auth.js";

/** 没登录就不能进后台、不能调保存接口 */
export const onRequest = defineMiddleware((context, next) => {
  const { pathname } = context.url;

  const needsAuth =
    (pathname.startsWith("/admin") && pathname !== "/admin/login") ||
    pathname.startsWith("/api/save") ||
    pathname.startsWith("/api/upload");

  if (needsAuth && !isAuthed(context.cookies)) {
    return context.redirect("/admin/login");
  }

  return next();
});