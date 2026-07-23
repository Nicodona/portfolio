import { useState } from "react";
import PageHeader from "../components/PageHeader.jsx";
import PhotoGrid from "../components/PhotoGrid.jsx";
import { usePortfolio, GALLERY_SECTIONS } from "../context/PortfolioContext.jsx";

export default function GalleryPage() {
  const { data } = usePortfolio();
  const [filter, setFilter] = useState("all");
  const gallery = data.gallery || [];

  // Only offer chips for sections that actually have photos.
  const sections = GALLERY_SECTIONS.filter((s) =>
    gallery.some((g) => g.section === s.key)
  );
  const filtered =
    filter === "all" ? gallery : gallery.filter((g) => g.section === filter);

  return (
    <>
      <PageHeader
        eyebrow="Beyond the desk"
        title="Gallery"
        lede="Photos from work, school and everything in between. Work and
        school photos also live on their own pages."
      />

      {sections.length > 1 && (
        <div className="filter-row" role="group" aria-label="Filter photos">
          <button
            className={`chip${filter === "all" ? " on" : ""}`}
            onClick={() => setFilter("all")}
          >
            All · {gallery.length}
          </button>
          {sections.map((s) => (
            <button
              key={s.key}
              className={`chip${filter === s.key ? " on" : ""}`}
              onClick={() => setFilter(s.key)}
            >
              {s.label} · {gallery.filter((g) => g.section === s.key).length}
            </button>
          ))}
        </div>
      )}

      {filtered.length > 0 ? (
        <PhotoGrid images={filtered} showSection />
      ) : (
        <p className="empty-note">No photos here yet.</p>
      )}
    </>
  );
}
