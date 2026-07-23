import { useEffect, useMemo, useState } from "react";
import { getStats, statsLogin, statsLogout, statsMe } from "../api.js";

const RANGES = [7, 30, 90, 365];

/* Single-series bar chart: views per day. Inline SVG, hover tooltip,
   rounded data ends, recessive grid, sparse labels. */
function VisitsChart({ perDay, days }) {
  const [tip, setTip] = useState(null);

  const series = useMemo(() => {
    const byDay = Object.fromEntries(perDay.map((d) => [d.day, d]));
    const out = [];
    const today = new Date();
    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const key = d.toISOString().slice(0, 10);
      out.push({
        day: key,
        label: d.toLocaleDateString("en", { month: "short", day: "numeric" }),
        views: byDay[key]?.views || 0,
        visitors: byDay[key]?.visitors || 0,
      });
    }
    return out;
  }, [perDay, days]);

  const W = 900;
  const H = 220;
  const PAD = { top: 14, right: 8, bottom: 26, left: 34 };
  const innerW = W - PAD.left - PAD.right;
  const innerH = H - PAD.top - PAD.bottom;
  const max = Math.max(4, ...series.map((d) => d.views));
  const step = innerW / series.length;
  const barW = Math.max(2, Math.min(26, step - 2));
  const ticks = [0, Math.ceil(max / 2), max];
  const labelEvery = Math.ceil(series.length / 8);

  return (
    <div className="chart-wrap">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        style={{ width: "100%", height: "auto", display: "block" }}
        onMouseLeave={() => setTip(null)}
        role="img"
        aria-label="Page views per day"
      >
        {ticks.map((t) => {
          const y = PAD.top + innerH - (t / max) * innerH;
          return (
            <g key={t}>
              <line
                x1={PAD.left}
                x2={W - PAD.right}
                y1={y}
                y2={y}
                stroke="var(--border)"
                strokeWidth="1"
              />
              <text
                x={PAD.left - 8}
                y={y + 4}
                textAnchor="end"
                fontSize="10"
                fontFamily="JetBrains Mono, monospace"
                fill="var(--text-muted)"
              >
                {t}
              </text>
            </g>
          );
        })}
        {series.map((d, i) => {
          const h = (d.views / max) * innerH;
          const x = PAD.left + i * step + (step - barW) / 2;
          const y = PAD.top + innerH - h;
          return (
            <g key={d.day}>
              {/* generous hit target */}
              <rect
                x={PAD.left + i * step}
                y={PAD.top}
                width={step}
                height={innerH}
                fill="transparent"
                onMouseEnter={(e) => {
                  const box = e.currentTarget.ownerSVGElement.getBoundingClientRect();
                  setTip({
                    x: ((PAD.left + i * step + step / 2) / W) * box.width,
                    y: (y / H) * box.height,
                    d,
                  });
                }}
              />
              {d.views > 0 && (
                <rect
                  x={x}
                  y={y}
                  width={barW}
                  height={Math.max(h, 2)}
                  rx={Math.min(4, barW / 2)}
                  fill="var(--chart-mark)"
                  pointerEvents="none"
                />
              )}
              {i % labelEvery === 0 && (
                <text
                  x={PAD.left + i * step + step / 2}
                  y={H - 8}
                  textAnchor="middle"
                  fontSize="10"
                  fontFamily="JetBrains Mono, monospace"
                  fill="var(--text-muted)"
                >
                  {d.label}
                </text>
              )}
            </g>
          );
        })}
      </svg>
      {tip && (
        <div className="chart-tip" style={{ left: tip.x, top: tip.y }}>
          {tip.d.label} · {tip.d.views} views · {tip.d.visitors} visitors
        </div>
      )}
    </div>
  );
}

function RankTable({ title, rows, nameKey, header }) {
  return (
    <div className="panel">
      <h2>{title}</h2>
      {rows.length === 0 ? (
        <p style={{ fontSize: "0.86rem" }}>Nothing here yet.</p>
      ) : (
        <table className="stats-table">
          <thead>
            <tr>
              <th>{header}</th>
              <th style={{ textAlign: "right" }}>Views</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td>{r[nameKey]}</td>
                <td className="num">{r.views}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

function Login({ onDone }) {
  const [u, setU] = useState("");
  const [p, setP] = useState("");
  const [err, setErr] = useState(null);
  const [busy, setBusy] = useState(false);

  async function submit(e) {
    e.preventDefault();
    setBusy(true);
    setErr(null);
    try {
      await statsLogin(u, p);
      onDone();
    } catch (e2) {
      setErr(
        e2.status === 429
          ? "Too many attempts. Wait a minute and try again."
          : "Those credentials did not work."
      );
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-card">
      <h1>Private area</h1>
      <p>This dashboard shows visitor analytics and is for the site owner.</p>
      <form onSubmit={submit}>
        <input
          placeholder="Username"
          value={u}
          onChange={(e) => setU(e.target.value)}
          autoComplete="username"
        />
        <input
          placeholder="Password"
          type="password"
          value={p}
          onChange={(e) => setP(e.target.value)}
          autoComplete="current-password"
        />
        <button className="btn solid" disabled={busy}>
          {busy ? "Checking..." : "Sign in"}
        </button>
        {err && <div className="form-note err">{err}</div>}
      </form>
    </div>
  );
}

export default function StatsPage() {
  const [authed, setAuthed] = useState(null);
  const [days, setDays] = useState(30);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    statsMe()
      .then((r) => setAuthed(r.authenticated))
      .catch(() => setAuthed(false));
  }, []);

  useEffect(() => {
    if (!authed) return;
    setLoading(true);
    getStats(days)
      .then(setData)
      .catch(() => setAuthed(false))
      .finally(() => setLoading(false));
  }, [authed, days]);

  if (authed === null) return <div className="spin">Checking session…</div>;
  if (!authed) return <Login onDone={() => setAuthed(true)} />;
  if (!data || loading) return <div className="spin">Loading analytics…</div>;

  const t = data.totals;

  return (
    <div className="stats-shell">
      <div className="stats-head">
        <h1>Visitor analytics</h1>
        <div className="tools">
          <div className="range-picker">
            {RANGES.map((r) => (
              <button
                key={r}
                className={days === r ? "on" : ""}
                onClick={() => setDays(r)}
              >
                {r}d
              </button>
            ))}
          </div>
          <button
            className="btn ghost"
            onClick={() => statsLogout().then(() => setAuthed(false))}
          >
            Sign out
          </button>
        </div>
      </div>

      <div className="tiles">
        <div className="tile">
          <div className="label">Views · {data.range_days}d</div>
          <div className="value">{t.views}</div>
        </div>
        <div className="tile">
          <div className="label">Visitors · {data.range_days}d</div>
          <div className="value">{t.unique_visitors}</div>
        </div>
        <div className="tile">
          <div className="label">All time views</div>
          <div className="value">{t.all_time_views}</div>
        </div>
        <div className="tile">
          <div className="label">All time visitors</div>
          <div className="value">{t.all_time_visitors}</div>
        </div>
        <div className="tile">
          <div className="label">Unread messages</div>
          <div className="value" style={{ color: t.unread_messages ? "var(--accent-2)" : undefined }}>
            {t.unread_messages}
          </div>
        </div>
      </div>

      <div className="panel">
        <h2>Page views per day</h2>
        <VisitsChart perDay={data.per_day} days={data.range_days} />
      </div>

      <div className="panel-row">
        <RankTable
          title="Top pages"
          rows={data.top_pages}
          nameKey="path"
          header="Path"
        />
        <RankTable
          title="Top referrers"
          rows={data.top_referrers}
          nameKey="referrer"
          header="Referrer"
        />
      </div>

      <div className="panel-row">
        <div className="panel">
          <h2>Recent visits</h2>
          <table className="stats-table">
            <thead>
              <tr>
                <th>When</th>
                <th>Path</th>
                <th>From</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_visits.map((v, i) => (
                <tr key={i}>
                  <td>
                    {new Date(v.created_at).toLocaleString("en", {
                      month: "short",
                      day: "numeric",
                      hour: "2-digit",
                      minute: "2-digit",
                    })}
                  </td>
                  <td>{v.path}</td>
                  <td>{v.referrer || v.country || "direct"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="panel">
          <h2>Recent messages</h2>
          {data.recent_messages.length === 0 ? (
            <p style={{ fontSize: "0.86rem" }}>No messages yet.</p>
          ) : (
            data.recent_messages.map((m, i) => (
              <div className="msg-item" key={i}>
                <div>
                  <span className="who">
                    {m.name} · {m.email}
                  </span>
                </div>
                <div className="body">
                  {m.subject && <strong>{m.subject} — </strong>}
                  {m.message}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <p style={{ fontFamily: "var(--font-mono)", fontSize: "0.7rem", color: "var(--text-muted)" }}>
        Generated {new Date(data.generated_at).toLocaleString()} · Full detail
        lives in the Django admin.
      </p>
    </div>
  );
}
