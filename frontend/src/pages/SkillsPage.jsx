import Reveal from "../components/Reveal.jsx";
import PageHeader from "../components/PageHeader.jsx";
import { usePortfolio } from "../context/PortfolioContext.jsx";

export default function SkillsPage() {
  const { data } = usePortfolio();

  return (
    <>
      <PageHeader
        eyebrow="Toolbox"
        title="Skills"
        lede="The languages, frameworks and infrastructure I reach for — grouped
        the way I actually use them."
      />

      <div className="skills-grid">
        {data.skill_groups.map((g) => (
          <Reveal key={g.id} className="skill-group">
            <h3>{g.name}</h3>
            <ul>
              {g.skills.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </Reveal>
        ))}
      </div>
    </>
  );
}
