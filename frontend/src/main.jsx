import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./index.css";
import { PortfolioProvider } from "./context/PortfolioContext.jsx";
import Layout from "./components/Layout.jsx";
import HomePage from "./pages/HomePage.jsx";
import ExperiencePage from "./pages/ExperiencePage.jsx";
import ProjectsPage from "./pages/ProjectsPage.jsx";
import EducationPage from "./pages/EducationPage.jsx";
import SkillsPage from "./pages/SkillsPage.jsx";
import GalleryPage from "./pages/GalleryPage.jsx";
import ContactPage from "./pages/ContactPage.jsx";
import StatsPage from "./pages/StatsPage.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <PortfolioProvider>
        <Routes>
          <Route path="/stats" element={<StatsPage />} />
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/experience" element={<ExperiencePage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/education" element={<EducationPage />} />
            <Route path="/skills" element={<SkillsPage />} />
            <Route path="/gallery" element={<GalleryPage />} />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </PortfolioProvider>
    </BrowserRouter>
  </StrictMode>
);
