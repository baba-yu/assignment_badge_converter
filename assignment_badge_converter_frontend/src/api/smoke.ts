import { login, internalHealth } from "./http";

export async function smoke(username: string, password: string) {
  await login(username, password);
  await internalHealth();
  return true;
}
