import { useEffect, useState } from "react";
import { Outlet, useLocation } from "react-router-dom";
import Spotlight from "./Spotlight.jsx";
import SiteHeader from "./SiteHeader.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";
import { track } from "../tracking.js";

const PAGE_TITLES = {
  "/experience": "Experience",
  "/projects": "Projects",
  "/education": "Education",
  "/skills": "Skills",
  "/gallery": "Gallery",
  "/contact": "Contact",
};

export default function Layout() {
  const { data, error, reload } = usePortfolio();
  const location = useLocation();
  const [accentFlipped, setAccentFlipped] = useState(false);

  useEffect(() => {
    track(location.pathname);
    window.scrollTo(0, 0);
    const sub = PAGE_TITLES[location.pathname];
    document.title = sub
      ? `${sub} · Njei Nicodemus`
      : "Njei Nicodemus | Full Stack Developer and Data Engineer";
  }, [location.pathname]);

  // A small reward for the curious: clicking the dot swaps the accents.
  function toggleAccent() {
    const root = document.documentElement;
    if (accentFlipped) {
      root.style.setProperty("--accent", "#0e9f6e");
      root.style.setProperty("--accent-tint", "rgba(14, 159, 110, 0.09)");
      root.style.setProperty("--accent-2", "#b45309");
      root.style.setProperty("--glow", "rgba(14, 159, 110, 0.05)");
    } else {
      root.style.setProperty("--accent", "#b45309");
      root.style.setProperty("--accent-tint", "rgba(180, 83, 9, 0.09)");
      root.style.setProperty("--accent-2", "#0e9f6e");
      root.style.setProperty("--glow", "rgba(180, 83, 9, 0.05)");
    }
    setAccentFlipped(!accentFlipped);
  }

  if (error) {
    return (
      <div className="spin">
        The portfolio could not load right now.{" "}
        <button className="retry" onClick={reload}>
          Try again
        </button>
      </div>
    );
  }
  if (!data) {
    return <div className="spin">Loading…</div>;
  }

  const { profile } = data;
  const hasGallery = (data.gallery || []).length > 0;

  const navItems = [
    ["/", "Home"],
    ["/experience", "Experience"],
    ["/projects", "Projects"],
    ["/education", "Education"],
    ["/skills", "Skills"],
    ...(hasGallery ? [["/gallery", "Gallery"]] : []),
    ["/contact", "Contact"],
  ];

  return (
    <>
      <Spotlight />
      <SiteHeader profile={profile} items={navItems} onAccentToggle={toggleAccent} />
      <main className="page">
        <Outlet />
      </main>
      <footer className="site-footer">
        <div className="page">Copyright 2026 martian Tech -dot404engineering</div>
      </footer>
    </>
  );
}
