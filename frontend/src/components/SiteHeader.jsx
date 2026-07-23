import { useEffect, useState } from "react";
import { NavLink, useLocation } from "react-router-dom";
import Socials from "./Socials.jsx";

export default function SiteHeader({ profile, items, onAccentToggle }) {
  const [open, setOpen] = useState(false);
  const location = useLocation();

  // Close the mobile menu whenever the route changes.
  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  useEffect(() => {
    document.body.style.overflow = open ? "hidden" : "";
    return () => {
      document.body.style.overflow = "";
    };
  }, [open]);

  const first = (profile.full_name || "Njei Nicodemus").split(" ")[0];

  const links = items.map(([to, label]) => (
    <NavLink key={to} to={to} end={to === "/"} className={({ isActive }) => (isActive ? "on" : "")}>
      {label}
    </NavLink>
  ));

  return (
    <>
      <header className="site-header">
        <div className="bar">
          <NavLink to="/" className="brand" aria-label="Home">
            {first}
            <span
              className="dot"
              onClick={(e) => {
                e.preventDefault();
                onAccentToggle();
              }}
              title="You found something"
            >
              .
            </span>
          </NavLink>
          <nav className="header-nav" aria-label="Site navigation">
            {links}
          </nav>
          <button
            className={`burger${open ? " x" : ""}`}
            onClick={() => setOpen(!open)}
            aria-label={open ? "Close menu" : "Open menu"}
            aria-expanded={open}
          >
            <span />
            <span />
          </button>
        </div>
      </header>

      {open && (
        <div className="mobile-menu">
          <nav aria-label="Site navigation">{links}</nav>
          <Socials profile={profile} />
        </div>
      )}
    </>
  );
}
