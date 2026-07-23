import Reveal from "./Reveal.jsx";

export default function PageHeader({ eyebrow, title, lede, children }) {
  return (
    <Reveal as="header" className="page-head">
      {eyebrow && <div className="eyebrow">{eyebrow}</div>}
      <h1>{title}</h1>
      {lede && <p className="lede">{lede}</p>}
      {children}
    </Reveal>
  );
}
