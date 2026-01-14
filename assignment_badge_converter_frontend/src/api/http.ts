import { clearTokens, getAccessToken, getRefreshToken, setTokens, type TokenPair } from "./auth";

const API_BASE = "http://localhost:8081";

let refreshInFlight: Promise<string> | null = null;

async function parseError(res: Response): Promise<string> {
  const text = await res.text().catch(() => "");
  return `${res.status} ${res.statusText}${text ? `: ${text}` : ""}`;
}

async function refreshAccessToken(): Promise<string> {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error("No refresh token");

  // refresh の多重発火を抑止（同時401で1回だけrefresh）
  if (!refreshInFlight) {
    refreshInFlight = (async () => {
      const res = await fetch(`${API_BASE}/api/v1/external/auth/token/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      });

      if (!res.ok) {
        clearTokens();
        throw new Error(`refresh failed: ${await parseError(res)}`);
      }

      const data = (await res.json()) as { access: string; refresh?: string };

      // refresh が返ってこない構成もあるので、既存 refresh を温存
      const next: TokenPair = { access: data.access, refresh };
      setTokens(next);

      return data.access;
    })().finally(() => {
      refreshInFlight = null;
    });
  }

  return refreshInFlight;
}

export async function fetchWithAuth(input: string, init: RequestInit = {}): Promise<Response> {
  const access = getAccessToken();
  const headers = new Headers(init.headers);

  if (access) headers.set("Authorization", `Bearer ${access}`);

  // JSON を多用する前提で、指定が無ければ付ける（必要なら外してください）
  if (!headers.has("Content-Type") && init.body) {
    headers.set("Content-Type", "application/json");
  }

  const first = await fetch(input, { ...init, headers });

  if (first.status !== 401) return first;

  // 401 → refresh → retry
  const newAccess = await refreshAccessToken();
  headers.set("Authorization", `Bearer ${newAccess}`);

  return fetch(input, { ...init, headers });
}

export async function login(username: string, password: string): Promise<void> {
  const res = await fetch(`${API_BASE}/api/v1/external/auth/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });

  if (!res.ok) {
    throw new Error(`login failed: ${await parseError(res)}`);
  }

  const tokens = (await res.json()) as TokenPair;
  setTokens(tokens);
}

export type SignUpPayload = {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
};

export type SignUpResponse = {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
};

export async function signup(payload: SignUpPayload): Promise<SignUpResponse> {
  const res = await fetch(`${API_BASE}/api/v1/external/auth/signup/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error(`signup failed: ${await parseError(res)}`);
  }

  return (await res.json()) as SignUpResponse;
}

export async function internalHealth(): Promise<void> {
  const res = await fetchWithAuth(`${API_BASE}/api/v1/internal/health/`, { method: "GET" });
  if (!res.ok) throw new Error(`internal health failed: ${await parseError(res)}`);
}
