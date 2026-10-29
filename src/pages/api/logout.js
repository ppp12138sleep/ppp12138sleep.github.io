import { clearSession } from "../../lib/auth.js";

export const POST = async ({ cookies, redirect }) => {
  clearSession(cookies);
  return redirect("/");
};