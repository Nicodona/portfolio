import { ArrowOut } from "./Icons.jsx";

export default function LinkOut({ href, children }) {
  if (!href) return null;
  return (
    <a className="linkout" href={href} target="_blank" rel="noreferrer">
      {children}
      <ArrowOut />
    </a>
  );
}
