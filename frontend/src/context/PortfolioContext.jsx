import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { getPortfolio } from "../api.js";

const PortfolioContext = createContext({ data: null, error: null, reload: () => {} });

export function PortfolioProvider({ children }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const reload = useCallback(() => {
    setError(null);
    getPortfolio()
      .then(setData)
      .catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  return (
    <PortfolioContext.Provider value={{ data, error, reload }}>
      {children}
    </PortfolioContext.Provider>
  );
}

export const usePortfolio = () => useContext(PortfolioContext);

/* Gallery sections, in display order. Keys mirror GalleryImage.SECTION_CHOICES
   on the backend; `page` is where that section also appears. */
export const GALLERY_SECTIONS = [
  { key: "work", label: "Work", page: "/experience" },
  { key: "school", label: "School", page: "/education" },
  { key: "projects", label: "Projects", page: "/projects" },
  { key: "life", label: "Life & Community", page: null },
];

export const sectionLabel = (key) =>
  GALLERY_SECTIONS.find((s) => s.key === key)?.label || key;
