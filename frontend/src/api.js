const API_BASE = import.meta.env.VITE_API_BASE || "";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  let data = null;
  try {
    data = await res.json();
  } catch {
    data = null;
  }
  if (!res.ok) {
    const err = new Error(data?.detail || `Request failed (${res.status})`);
    err.status = res.status;
    throw err;
  }
  return data;
}

export const getPortfolio = () => request("/api/portfolio/");

export const sendContact = (payload) =>
  request("/api/contact/", { method: "POST", body: JSON.stringify(payload) });

export const trackVisit = (payload) =>
  request("/api/track/", { method: "POST", body: JSON.stringify(payload) });

export const statsLogin = (username, password) =>
  request("/api/stats/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });

export const statsLogout = () =>
  request("/api/stats/logout/", { method: "POST", body: "{}" });

export const statsMe = () => request("/api/stats/me/");

export const getStats = (days = 30) => request(`/api/stats/?days=${days}`);
