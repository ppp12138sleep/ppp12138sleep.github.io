/**
 * 极简登录态：密码来自环境变量，校验通过后发一个签名 cookie。
 *
 * 这不是企业级方案（没有用户表、没有会话过期轮换），
 * 但足够挡住"随便点进来改内容的人"，而且零依赖。
 */

import crypto from "node:crypto";

const COOKIE_NAME = "ph_admin";

function password() {
  return process.env.ADMIN_PASSWORD || "panhe2026";
}

/** 密码变了，token 自动失效 */
function expectedToken() {
  return crypto
    .createHash("sha256")
    .update(password() + (process.env.ADMIN_SECRET || "ph-portfolio"))
    .digest("hex");
}

export function checkPassword(input) {
  const a = Buffer.from(String(input ?? ""));
  const b = Buffer.from(password());
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

export function isAuthed(cookies) {
  return cookies.get(COOKIE_NAME)?.value === expectedToken();
}

export function setSession(cookies) {
  cookies.set(COOKIE_NAME, expectedToken(), {
    path: "/",
    httpOnly: true,
    sameSite: "lax",
    maxAge: 60 * 60 * 24 * 7, // 7 天
  });
}

export function clearSession(cookies) {
  cookies.delete(COOKIE_NAME, { path: "/" });
}