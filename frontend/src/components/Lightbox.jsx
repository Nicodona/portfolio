import { useEffect } from "react";

/* Full-screen viewer. Owns keyboard navigation and the scroll lock;
   the parent owns which image is open. */
export default function Lightbox({ images, index, onClose, onStep }) {
  const count = images.length;
  const open = images[index];

  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight") onStep(1);
      if (e.key === "ArrowLeft") onStep(-1);
    };
    window.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [onClose, onStep]);

  if (!open) return null;

  return (
    <div
      className="lightbox"
      role="dialog"
      aria-modal="true"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <button className="lb-ctl lb-close" onClick={onClose} aria-label="Close">
        ✕
      </button>
      {count > 1 && (
        <button className="lb-ctl lb-prev" onClick={() => onStep(-1)} aria-label="Previous photo">
          ←
        </button>
      )}
      <img src={open.image_url} alt={open.title || "Gallery photo"} />
      {(open.title || open.caption) && (
        <div className="cap">
          {open.title && <div className="t">{open.title}</div>}
          {open.caption && <div className="c">{open.caption}</div>}
        </div>
      )}
      <div className="count">
        {index + 1} / {count}
      </div>
      {count > 1 && (
        <button className="lb-ctl lb-next" onClick={() => onStep(1)} aria-label="Next photo">
          →
        </button>
      )}
    </div>
  );
}
