import { Link } from "react-router-dom";
import Reveal from "../components/Reveal.jsx";
import PageHeader from "../components/PageHeader.jsx";
import PhotoGrid from "../components/PhotoGrid.jsx";
import LinkOut from "../components/LinkOut.jsx";
import { ArrowOut } from "../components/Icons.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";

function fmt(dateStr) {
  if (!dateStr) return "Present";
  const d = new Date(dateStr);
  return d.toLocaleDateString("en", { month: "short", year: "numeric" });
}

export default function ExperiencePage() {
  const { data } = usePortfolio();
  const photos = (data.gallery || []).filter((g) => g.section === "work");

  return (
    <>
      <PageHeader
        eyebrow="Career"
        title="Experience"
        lede="Roles where I designed, built and ran the systems — from health
        research data pipelines to platforms schools depend on every day."
      />

      <div className="xp-list">
        {data.experiences.map((xp) => (
          <Reveal key={xp.id} className="card">
            <div className="dates">
              {fmt(xp.start_date)} — {fmt(xp.end_date)}
            </div>
            <div>
              <h3>
                {xp.role} ·{" "}
                {xp.organization_url ? (
                  <LinkOut href={xp.organization_url}>{xp.organization}</LinkOut>
                ) : (
                  <span className="org">{xp.organization}</span>
                )}
              </h3>
              {xp.location && <div className="where">{xp.location}</div>}
              <p className="sum">{xp.summary}</p>
              {xp.highlights.length > 0 && (
                <ul className="hl">
                  {xp.highlights.map((h, i) => (
                    <li key={i}>{h}</li>
                  ))}
                </ul>
              )}
              <div className="pills">
                {xp.tags.map((t) => (
                  <span className="pill" key={t}>
                    {t}
                  </span>
                ))}
              </div>
            </div>
          </Reveal>
        ))}
      </div>

      {photos.length > 0 && (
        <section className="page-photos">
          <div className="subhead">Moments from work</div>
          <PhotoGrid images={photos} compact />
          <Reveal className="see-all">
            <Link className="linkout" to="/gallery">
              See the full gallery <ArrowOut />
            </Link>
          </Reveal>
        </section>
      )}
    </>
  );
}
