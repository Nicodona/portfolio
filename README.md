# Njei Nicodemus — Portfolio

A full stack portfolio: Django REST backend with SQLite, a React front end
across seven pages, an admin-managed photo gallery, visitor analytics with a
private `/stats` dashboard, and n8n automation hooks. Runs on a DigitalOcean
droplet behind a shared Caddy at **https://nico.martac.org**.

## What is inside

```
Portfolio/
├── backend/          Django + DRF + SQLite (API, admin, tracking, seed data)
├── frontend/         Vite + React multi-page site + /stats dashboard
└── deploy/           docker-compose, Caddy snippet, env example, deploy script
```

The React build is compiled to `frontend/dist`, staged into
`backend/frontend_dist` by the deploy script, and served by WhiteNoise from
the same gunicorn process that serves the API. Unknown paths fall through to
`index.html`, so client-side routing survives a refresh.

### Pages

| Page | Route | Content source |
|---|---|---|
| Home | `/` | Profile, about, featured projects, testimonials |
| Experience | `/experience` | `Experience` rows + `work` gallery photos |
| Projects | `/projects` | `Project` rows + `projects` gallery photos |
| Education | `/education` | `Education`, `Award`, `Certification` + `school` photos |
| Skills | `/skills` | `SkillGroup` rows |
| Gallery | `/gallery` | All `GalleryImage` rows, filterable by section |
| Contact | `/contact` | Contact form → `ContactMessage` (+ optional n8n webhook) |

`PortfolioContext` fetches the whole payload once and shares it, so moving
between pages costs no extra requests.

### The gallery

`GalleryImage.section` decides where a photo appears. You pick it as a radio
button when uploading in the admin:

| Section | Appears on |
|---|---|
| `work` | Gallery **and** the Experience page |
| `school` | Gallery **and** the Education page |
| `projects` | Gallery **and** the Projects page |
| `life` | Gallery page only |

Every photo always shows on `/gallery`, where filter chips let visitors narrow
by section. With no photos at all the Gallery nav link hides itself and the
per-page photo strips disappear, so the site never renders an empty section.

### Backend endpoints

| Endpoint | Auth | Purpose |
|---|---|---|
| `GET /api/portfolio/` | public | Everything the site renders, in one payload |
| `POST /api/track/` | public | Logs a page view (anonymous visitor id) |
| `POST /api/contact/` | public, throttled | Saves a message and forwards it to n8n |
| `POST /api/stats/login/` | public, throttled | Session login for the stats page |
| `GET /api/stats/` | staff only | Aggregated analytics for the dashboard |
| `/admin/` | staff only | Full content management |

### Content lives in the admin

Everything on the site is editable at `/admin/`: profile text, photo, CV file,
experiences, projects (with screenshots), education, certifications, skill
groups, awards, testimonials and gallery photos. Changes appear immediately,
no redeploy needed. Visits and contact messages are browsable there too.

## Local development

```bash
# backend
cd backend
python -m venv venv
venv/Scripts/activate            # source venv/bin/activate on Linux/macOS
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# frontend (second terminal)
cd frontend
npm install
npm run dev
```

Open http://127.0.0.1:5173; the admin is at http://127.0.0.1:8000/admin/.
`python manage.py seed_portfolio` fills the database with starter content —
it updates in place and never duplicates, but it **overwrites admin edits to
the rows it seeded**, so stop running it once you start editing in the admin.

## Deploying to the droplet

One time setup:

1. **DNS** — add an A record for `nico` pointing at the droplet, and wait for
   it to resolve (`nslookup nico.martac.org`).
2. Copy `deploy/env.production.example` to `/opt/portfolio/.env` on the
   droplet and fill in a real `SECRET_KEY` and (later) the n8n webhook URLs.
   Confirm the Caddy docker network name with `docker network ls` and set
   `CADDY_NETWORK` accordingly.
3. Run the deploy script from this folder:
   ```bash
   bash deploy/deploy.sh
   ```
4. On the droplet, first time only:
   ```bash
   docker exec -it portfolio-web python manage.py seed_portfolio
   docker exec -it portfolio-web python manage.py createsuperuser
   ```
5. Append the block from `deploy/Caddyfile.snippet` to
   `/opt/lewa/deploy/Caddyfile` and reload Caddy. HTTPS is automatic once DNS
   resolves. The portfolio container serves the React build itself, so Caddy
   needs nothing mounted.

Every later deploy is just `bash deploy/deploy.sh` again. `entrypoint.sh` runs
`migrate --noinput` on start, so new migrations apply automatically. The
SQLite file and uploaded media live on the `portfolio_data` docker volume and
survive rebuilds.

> **Never name the compose service `web`, `db`, `caddy` or `n8n`.** Service
> names become DNS aliases on the shared docker network, and a stray `web`
> alias once hijacked traffic meant for another site on the same droplet.

## n8n automation

Two integration points, both optional and controlled by `.env`:

- **`N8N_CONTACT_WEBHOOK`** — every contact form submission POSTs the message
  to this webhook. Suggested workflow: Webhook → email yourself → optionally
  auto reply to the sender.
- **`N8N_VISIT_WEBHOOK`** — a cron friendly summary. Add to the droplet
  crontab, for example every Monday at 08:00:
  ```
  0 8 * * 1 docker exec portfolio-web python manage.py send_visit_summary --days 7
  ```
  The payload carries views, unique visitors, top pages, top referrers and new
  message count, ready to format into a weekly report.

## Analytics and privacy

Tracking is first party and lightweight: an anonymous random id in
localStorage, the path, referrer, user agent, IP and browser timezone, one row
per page view in SQLite. No cookies for visitors, no third party scripts. The
`/stats` dashboard (staff login required) shows daily views, unique visitors,
top pages, referrers, recent visits and messages, over 7, 30, 90 and 365 day
ranges.

## Configuration

No secrets are committed. Production settings come from `/opt/portfolio/.env`
on the server; see `deploy/env.production.example` for the full list of keys.

## Stack

Django 6 · Django REST Framework · SQLite · WhiteNoise · Gunicorn ·
React 19 · React Router · Vite · Docker · Caddy
