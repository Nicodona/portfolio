import { trackVisit } from "./api";

const VISITOR_KEY = "nn_visitor_id";

function visitorId() {
  let id = localStorage.getItem(VISITOR_KEY);
  if (!id) {
    id =
      (crypto.randomUUID && crypto.randomUUID().replace(/-/g, "")) ||
      Math.random().toString(36).slice(2) + Date.now().toString(36);
    localStorage.setItem(VISITOR_KEY, id);
  }
  return id;
}

let tracked = new Set();

export function track(path) {
  // One ping per path per page load keeps the numbers honest.
  if (tracked.has(path)) return;
  tracked.add(path);
  trackVisit({
    visitor_id: visitorId(),
    path,
    referrer: document.referrer || "",
    country: Intl.DateTimeFormat().resolvedOptions().timeZone || "",
  }).catch(() => {});
}
