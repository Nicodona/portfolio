# Portfolio

Repo `Nicodona/portfolio`, branch `main`. **This repo is public**: never put
passwords, server details or private notes in it.

Personal portfolio site, live at https://nico.martac.org.

- `backend/`: Django + DRF with a single SQLite file. `GET /api/portfolio/`
  returns the whole page payload; content (experience, projects, education,
  skills, gallery) is edited in the Django admin. `/stats` is a staff only
  visitor dashboard. The contact form forwards to an n8n webhook.
- `frontend/`: Vite + React, multi page (`/`, `/experience`, `/projects`,
  `/education`, `/skills`, `/gallery`, `/contact`). `PortfolioContext` fetches
  the payload once. Gallery photos carry a `section` (work, school, projects,
  life) that also shows them on the matching page.
- `deploy/deploy.sh` builds the frontend, ships it and rebuilds the container.
  Deploy only when the user says "deploy".

Rules: keep the copy to what is essential about the person (no talk about how
the site is built), plain English, no long dashes. Do not run
`seed_portfolio` on the live site: it overwrites edits made in the admin.
Check pages at desktop and phone width with no sideways scroll.
