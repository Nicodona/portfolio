import { Link } from "react-router-dom";
import Reveal from "../components/Reveal.jsx";
import Socials from "../components/Socials.jsx";
import LinkOut from "../components/LinkOut.jsx";
import { ArrowOut } from "../components/Icons.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";

export default function HomePage() {
  const { data } = usePortfolio();
  const { profile } = data;

  const paragraphs = (profile.about || "").split(/\n\s*\n/).filter(Boolean);
  const initials = (profile.full_name || "N N")
    .split(" ")
    .map((w) => w[0])
    .slice(0, 2)
    .join("");
  const featured = data.projects.filter((p) => p.is_featured).slice(0, 2);
  const galleryCount = (data.gallery || []).length;
  const testimonials = data.testimonials || [];

  const explore = [
    {
      to: "/experience",
      title: "Experience",
      desc: `${data.experiences.length} roles across health research and school platforms.`,
    },
    {
      to: "/projects",
      title: "Projects",
      desc: `${data.projects.length} products built, shipped and running in production.`,
    },
    {
      to: "/education",
      title: "Education",
      desc: `Degrees, ${data.certifications.length} certifications and the honors behind them.`,
    },
    {
      to: "/skills",
      title: "Skills",
      desc: "The languages, frameworks and infrastructure I work with daily.",
    },
    ...(galleryCount
      ? [
          {
            to: "/gallery",
            title: "Gallery",
            desc: `${galleryCount} photos from work, school and beyond the desk.`,
          },
        ]
      : []),
    {
      to: "/contact",
      title: "Contact",
      desc: "Have a project in mind? My inbox is always open.",
    },
  ];

  return (
    <>
      <section className="hero">
        <Reveal className="hero-text">
          <div className="eyebrow">Hello, my name is</div>
          <h1>
            {profile.full_name}
            <span className="dot">.</span>
          </h1>
          <p className="headline">{profile.headline}</p>
          <p className="tagline">{profile.tagline}</p>
          <p className="loc">
            {profile.location} · {profile.timezone_label}
          </p>
          {profile.available_for_work && (
            <span className="availability">
              <span className="pulse" />
              {profile.availability_note || "Available for new projects"}
            </span>
          )}
          <div className="cta-row">
            <Link className="btn solid" to="/projects">
              See my work
            </Link>
            <Link className="btn ghost" to="/contact">
              Get in touch
            </Link>
            {profile.cv_url && (
              <a className="btn ghost" href={profile.cv_url} target="_blank" rel="noreferrer">
                Resume
              </a>
            )}
          </div>
          <Socials profile={profile} />
        </Reveal>
        <Reveal className="portrait">
          <div className="frame">
            {profile.photo_url ? (
              <img src={profile.photo_url} alt={profile.full_name} />
            ) : (
              <div className="monogram">{initials}</div>
            )}
          </div>
        </Reveal>
      </section>

      {paragraphs.length > 0 && (
        <section className="home-block">
          <div className="subhead">About me</div>
          <Reveal className="about-text">
            {paragraphs.map((p, i) => (
              <p key={i}>{p}</p>
            ))}
          </Reveal>
        </section>
      )}

      <section className="home-block">
        <div className="subhead">Explore</div>
        <div className="explore-grid">
          {explore.map((c) => (
            <Reveal key={c.to}>
              <Link className="explore-card" to={c.to}>
                <div className="top">
                  <h3>{c.title}</h3>
                  <ArrowOut />
                </div>
                <p>{c.desc}</p>
              </Link>
            </Reveal>
          ))}
        </div>
      </section>

      {featured.length > 0 && (
        <section className="home-block">
          <div className="subhead">Featured work</div>
          <div className="teaser-grid">
            {featured.map((p) => (
              <Reveal key={p.id} className="teaser">
                {p.image_url && (
                  <Link to="/projects" className="shot" aria-label={p.title}>
                    <img src={p.image_url} alt={p.title} loading="lazy" />
                  </Link>
                )}
                <h3>{p.title}</h3>
                <p>{p.short_description}</p>
                <div className="pills">
                  {p.tags.slice(0, 4).map((t) => (
                    <span className="pill" key={t}>
                      {t}
                    </span>
                  ))}
                </div>
              </Reveal>
            ))}
          </div>
          <Reveal className="see-all">
            <Link className="linkout" to="/projects">
              All projects <ArrowOut />
            </Link>
          </Reveal>
        </section>
      )}

      {testimonials.length > 0 && (
        <section className="home-block">
          <div className="subhead">Kind words</div>
          <div className="quote-grid">
            {testimonials.map((t) => (
              <Reveal key={t.id} className="quote">
                <blockquote>“{t.quote}”</blockquote>
                <div className="who">
                  {t.author}
                  {t.author_title ? ` · ${t.author_title}` : ""}
                </div>
              </Reveal>
            ))}
          </div>
        </section>
      )}

      <section className="home-block home-cta">
        <Reveal>
          <h2>Let’s build something that runs for years.</h2>
          <p>
            Whether it is a school platform, a research data pipeline or the
            server it all lives on, I would love to hear about it.
          </p>
          <div className="cta-row">
            <Link className="btn solid" to="/contact">
              Start a conversation
            </Link>
            {profile.email && <LinkOut href={`mailto:${profile.email}`}>{profile.email}</LinkOut>}
          </div>
        </Reveal>
      </section>
    </>
  );
}
