const ACCESS_KEY = "jwt.access";
const REFRESH_KEY = "jwt.refresh";

let memAccess: string | null = null;
let memRefresh: string | null = null;

export type TokenPair = { access: string; refresh: string };

export function getAccessToken(): string | null {
  if (memAccess) return memAccess;
  const v = sessionStorage.getItem(ACCESS_KEY);
  memAccess = v;
  return v;
}

export function getRefreshToken(): string | null {
  if (memRefresh) return memRefresh;
  const v = sessionStorage.getItem(REFRESH_KEY);
  memRefresh = v;
  return v;
}

export function setTokens(tokens: TokenPair) {
  memAccess = tokens.access;
  memRefresh = tokens.refresh;
  sessionStorage.setItem(ACCESS_KEY, tokens.access);
  sessionStorage.setItem(REFRESH_KEY, tokens.refresh);
}

export function clearTokens() {
  memAccess = null;
  memRefresh = null;
  sessionStorage.removeItem(ACCESS_KEY);
  sessionStorage.removeItem(REFRESH_KEY);
}
