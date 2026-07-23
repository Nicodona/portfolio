import { useCallback, useState } from "react";
import Reveal from "./Reveal.jsx";
import Lightbox from "./Lightbox.jsx";
import { sectionLabel } from "../context/PortfolioContext.jsx";

/* Clickable photo grid with a lightbox. `compact` renders the smaller
   strip used inside the Experience / Education / Projects pages;
   `showSection` adds the section chip used on the Gallery page. */
export default function PhotoGrid({ images, compact = false, showSection = false }) {
  const [idx, setIdx] = useState(null);
  const count = images.length;

  const step = useCallback(
    (d) => setIdx((i) => (i === null ? null : (i + d + count) % count)),
    [count]
  );

  if (!count) return null;

  return (
    <>
      <div className={`photo-grid${compact ? " compact" : ""}`}>
        {images.map((g, i) => (
          <Reveal
            key={g.id}
            as="button"
            className="gtile"
            type="button"
            onClick={() => setIdx(i)}
            aria-label={g.title ? `View ${g.title}` : "View photo"}
          >
            <img src={g.image_url} alt={g.title || "Gallery photo"} loading="lazy" />
            {showSection && <span className="gtag">{sectionLabel(g.section)}</span>}
            {g.title && <span className="glabel">{g.title}</span>}
          </Reveal>
        ))}
      </div>
      {idx !== null && (
        <Lightbox images={images} index={idx} onClose={() => setIdx(null)} onStep={step} />
      )}
    </>
  );
}
