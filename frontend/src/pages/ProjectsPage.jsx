import { Link } from "react-router-dom";
import Reveal from "../components/Reveal.jsx";
import PageHeader from "../components/PageHeader.jsx";
import PhotoGrid from "../components/PhotoGrid.jsx";
import LinkOut from "../components/LinkOut.jsx";
import { FolderIcon, ArrowOut } from "../components/Icons.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";

function Featured({ project, flip }) {
  const paragraphs = (project.description || "").split(/\n\s*\n/).filter(Boolean);
  return (
    <Reveal className="feature">
      <div className="shot" style={{ order: flip ? 2 : 1 }}>
        <div className="browser-bar">
          <span /> <span /> <span />
        </div>
        {project.image_url ? (
          <img src={project.image_url} alt={project.title} />
        ) : (
          <div className="placeholder">{project.title}</div>
        )}
      </div>
      <div className="info" style={{ order: flip ? 1 : 2 }}>
        <div className="kicker">Featured project</div>
        <h3>{project.title}</h3>
        <div className="desc">
          {paragraphs.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>
        {project.outcome && <div className="outcome">→ {project.outcome}</div>}
        <div className="pills">
          {project.tags.map((t) => (
            <span className="pill" key={t}>
              {t}
            </span>
          ))}
        </div>
        <div className="links">
          <LinkOut href={project.live_url}>Live site</LinkOut>
          <LinkOut href={project.repo_url}>Source</LinkOut>
        </div>
      </div>
    </Reveal>
  );
}

export default function ProjectsPage() {
  const { data } = usePortfolio();
  const featured = data.projects.filter((p) => p.is_featured);
  const others = data.projects.filter((p) => !p.is_featured);
  const photos = (data.gallery || []).filter((g) => g.section === "projects");

  return (
    <>
      <PageHeader
        eyebrow="Portfolio"
        title="Things I Have Built"
        lede="Products that are live and doing real work — school management
        platforms, mobile apps, data systems and the deployments behind them."
      />

      <div className="featured">
        {featured.map((p, i) => (
          <Featured key={p.id} project={p} flip={i % 2 === 1} />
        ))}
      </div>

      {others.length > 0 && (
        <>
          <div className="subhead">Other noteworthy work</div>
          <div className="project-grid">
            {others.map((p) => (
              <Reveal key={p.id} className="pcard">
                <div className="top">
                  <span className="folder">
                    <FolderIcon />
                  </span>
                  <span className="links">
                    {p.live_url && (
                      <a
                        className="linkout"
                        href={p.live_url}
                        target="_blank"
                        rel="noreferrer"
                        title="Live site"
                      >
                        <ArrowOut />
                      </a>
                    )}
                  </span>
                </div>
                <h3>{p.title}</h3>
                <p>{p.short_description}</p>
                <div className="pills">
                  {p.tags.slice(0, 5).map((t) => (
                    <span className="pill" key={t}>
                      {t}
                    </span>
                  ))}
                </div>
              </Reveal>
            ))}
          </div>
        </>
      )}

      {photos.length > 0 && (
        <section className="page-photos">
          <div className="subhead">Projects in the wild</div>
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
