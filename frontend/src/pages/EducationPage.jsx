import { Link } from "react-router-dom";
import Reveal from "../components/Reveal.jsx";
import PageHeader from "../components/PageHeader.jsx";
import PhotoGrid from "../components/PhotoGrid.jsx";
import LinkOut from "../components/LinkOut.jsx";
import { ArrowOut } from "../components/Icons.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";

export default function EducationPage() {
  const { data } = usePortfolio();
  const photos = (data.gallery || []).filter((g) => g.section === "school");

  return (
    <>
      <PageHeader
        eyebrow="Background"
        title="Education & Recognition"
        lede="The degrees, certifications and honors behind the work."
      />

      <div className="edu-list xp-list">
        {data.education.map((ed) => (
          <Reveal key={ed.id} className="card">
            <div className="dates">
              {ed.start_year} — {ed.end_year}
            </div>
            <div>
              <h3>{ed.degree}</h3>
              <div className="where">{ed.institution}</div>
              {ed.note && (
                <p className="sum" style={{ color: "var(--accent-2)" }}>
                  {ed.note}
                </p>
              )}
            </div>
          </Reveal>
        ))}
      </div>

      {data.awards.length > 0 && (
        <>
          <div className="subhead">Honors</div>
          <Reveal>
            {data.awards.map((a) => (
              <div className="award" key={a.id}>
                <div className="yr">{a.year}</div>
                <div>
                  <div className="t">
                    {a.title}
                    {a.issuer ? ` · ${a.issuer}` : ""}
                  </div>
                  {a.description && <div className="d">{a.description}</div>}
                </div>
              </div>
            ))}
          </Reveal>
        </>
      )}

      {data.certifications.length > 0 && (
        <>
          <div className="subhead">Certifications</div>
          <div className="cert-grid">
            {data.certifications.map((c) => (
              <Reveal key={c.id} className="cert">
                <div className="t">
                  {c.credential_url ? (
                    <LinkOut href={c.credential_url}>{c.title}</LinkOut>
                  ) : (
                    c.title
                  )}
                </div>
                <div className="i">
                  {c.issuer}
                  {c.date_earned ? ` · ${c.date_earned}` : ""}
                </div>
              </Reveal>
            ))}
          </div>
        </>
      )}

      {photos.length > 0 && (
        <section className="page-photos">
          <div className="subhead">School days</div>
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
