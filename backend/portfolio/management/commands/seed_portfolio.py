"""Seed the portfolio database with Njei Nicodemus Mbacham's real content.

Safe to run more than once: existing rows are matched by natural keys and
updated, nothing is duplicated. Run with:

    python manage.py seed_portfolio
"""

from datetime import date

from django.core.management.base import BaseCommand

from portfolio.models import (
    Award,
    Certification,
    Education,
    Experience,
    Profile,
    Project,
    SkillGroup,
)


class Command(BaseCommand):
    help = "Seed the database with portfolio content from the CV."

    def handle(self, *args, **options):
        self.seed_profile()
        self.seed_experiences()
        self.seed_projects()
        self.seed_education()
        self.seed_certifications()
        self.seed_skills()
        self.seed_awards()
        self.stdout.write(self.style.SUCCESS("Portfolio content seeded."))

    def seed_profile(self):
        profile = Profile.load()
        profile.full_name = "Njei Nicodemus Mbacham"
        profile.preferred_name = "Nghan"
        profile.headline = "Full Stack Developer, Data Engineer and Health Tech Builder"
        profile.tagline = (
            "I build software that runs schools and health research programs in "
            "Cameroon. Complete web platforms, mobile apps, data pipelines and "
            "the servers they live on."
        )
        profile.about = (
            "I am a computer engineer from Bamenda, Cameroon. I graduated as the "
            "overall best graduate of my class at the National Higher Polytechnic "
            "Institute, University of Bamenda, and I have spent the years since "
            "then building systems that real people depend on every day. I enjoy "
            "owning the whole stack, from the React interface someone taps on "
            "their phone to the Linux server humming away in a rack.\n\n"
            "Right now I work as a Data Management Officer at the Tuberculosis "
            "Reference Laboratory of the Center for Health Promotion and "
            "Research. I design REDCap data capture systems, write Python ETL "
            "pipelines, and build Power BI dashboards that give investigators a "
            "live view of their studies. I was part of the team whose research "
            "earned WHO accreditation for pooled TB testing, and I helped launch "
            "instant point of care testing in a new city. It taught me to "
            "engineer for resilience first, because power and connectivity are "
            "never guaranteed here.\n\n"
            "Before that I built and deployed a complete school management "
            "platform with React, Django and PostgreSQL that schools in Bamenda "
            "still run on today, covering everything from admissions and fees to "
            "timetables and report cards. I also founded Dot404 Engineering, a "
            "small startup where I train interns and lead MVP projects, and I "
            "teach computer science part time. When I am not shipping software "
            "you will probably find me mentoring a student through their first "
            "program."
        )
        profile.email = "njeinicodona@gmail.com"
        profile.phone = "+237 680 949 841"
        profile.location = "Bamenda, Cameroon"
        profile.timezone_label = "GMT+1"
        profile.github_url = "https://github.com/nicodona"
        profile.linkedin_url = "https://www.linkedin.com/in/njei-nicodemus"
        profile.whatsapp_number = "237680949841"
        profile.available_for_work = True
        profile.availability_note = "Open to new projects and roles"
        profile.save()
        self.stdout.write("Profile updated.")

    def seed_experiences(self):
        rows = [
            {
                "role": "Data Management Officer",
                "organization": "CHPR, Tuberculosis Reference Laboratory",
                "location": "Bamenda, Cameroon",
                "start_date": date(2025, 12, 1),
                "end_date": None,
                "summary": (
                    "I run the data backbone of an active TB research "
                    "laboratory. I design and administer REDCap projects end to "
                    "end, build Python ETL pipelines that keep every export "
                    "traceable and reproducible, and ship Power BI dashboards "
                    "that investigators check every morning."
                ),
                "highlights": "\n".join([
                    "Contributed to the research that earned WHO accreditation "
                    "for pooled TB testing, covering study design, data "
                    "management and statistical reporting.",
                    "Provisioned and hardened the on premise REDCap server, "
                    "including backups, monitoring and uptime.",
                    "Co led the launch of the Near Point of Care TB project in "
                    "Ngaoundere on the Pluslife platform.",
                    "Automated exports, SharePoint sync, alerts and report "
                    "refreshes with Airflow, Power Automate and n8n.",
                ]),
                "tech_tags": "Python, pandas, polars, REDCap, Power BI, DAX, "
                             "Apache Airflow, n8n, SharePoint, Linux",
                "display_order": 1,
            },
            {
                "role": "Software Engineer",
                "organization": "CCEC Bamenda",
                "organization_url": "https://caromabamenda.org",
                "location": "Bamenda, Cameroon",
                "start_date": date(2023, 10, 1),
                "end_date": date(2025, 12, 1),
                "summary": (
                    "I engineered and deployed a complete school management "
                    "system covering students, staff, academics, finance and "
                    "communication, then kept it running in production. The "
                    "platform now lives on the public internet and handles "
                    "admissions, fees, marks, transcripts and timetables for "
                    "the whole school."
                ),
                "highlights": "\n".join([
                    "Built the full stack with a React frontend and a Django "
                    "REST backend on PostgreSQL.",
                    "Automated report cards, performance statistics and "
                    "dynamic charts for academic tracking.",
                    "Hardened the deployment with Ubuntu, firewall policies "
                    "and AWS based backups.",
                ]),
                "tech_tags": "React, Django, PostgreSQL, Docker, Ubuntu, AWS",
                "display_order": 2,
            },
            {
                "role": "IT Administrator",
                "organization": "Caroma",
                "location": "Bamenda, Cameroon",
                "start_date": date(2021, 1, 1),
                "end_date": date(2025, 10, 1),
                "summary": (
                    "Four years keeping an organization's technology healthy. "
                    "I configured and managed LAN and WAN networks, kept "
                    "backups and updates on schedule, supported users through "
                    "every kind of hardware and software issue, and automated "
                    "office workflows with SharePoint and Power Automate."
                ),
                "highlights": "",
                "tech_tags": "Networking, Windows, Ubuntu, SharePoint, "
                             "Power Automate, Backups",
                "display_order": 3,
            },
            {
                "role": "Computer Science Teacher and IT Assistant",
                "organization": "CCC Mankon",
                "location": "Bamenda, Cameroon",
                "start_date": date(2023, 9, 1),
                "end_date": None,
                "summary": (
                    "I teach programming, SQL and operating systems to advanced "
                    "level students, manage the school computer lab, and serve "
                    "as a regional mock examiner for ICT and computer science. "
                    "Teaching keeps me sharp and honest about what I really "
                    "understand."
                ),
                "highlights": "",
                "tech_tags": "Teaching, Python, SQL, Lab administration",
                "display_order": 4,
            },
            {
                "role": "Founder and CEO",
                "organization": "Dot404 Engineering",
                "location": "Bamenda, Cameroon",
                "start_date": date(2025, 5, 1),
                "end_date": None,
                "summary": (
                    "I founded a small engineering startup where we take MVP "
                    "projects from idea to delivery. I organize the teams, "
                    "review the work, fund the operation and train interns who "
                    "are getting their first real hands on experience in tech."
                ),
                "highlights": "",
                "tech_tags": "Leadership, Product, Mentoring, MVP delivery",
                "display_order": 5,
            },
        ]
        for row in rows:
            Experience.objects.update_or_create(
                role=row["role"], organization=row["organization"],
                defaults=row,
            )
        self.stdout.write(f"{len(rows)} experiences seeded.")

    def seed_projects(self):
        rows = [
            {
                "slug": "school-management-platform",
                "title": "Multi School Management Platform",
                "short_description": (
                    "A multi tenant SaaS platform that runs several schools "
                    "from one deployment, each with its own isolated database."
                ),
                "description": (
                    "Schools in my region were managing admissions, fees, "
                    "marks and timetables on paper and scattered spreadsheets. "
                    "I built a platform that puts all of it in one place, then "
                    "took it further and made it multi tenant, so a single "
                    "deployment serves many schools and every school's data "
                    "stays in its own database.\n\n"
                    "The system covers student records, fee tracking for the "
                    "finance office, mark entry with live validation, report "
                    "cards, transcripts, a timetable generator that "
                    "understands elective subjects sharing a slot, QR coded "
                    "documents and CSV bulk imports. A companion mobile app "
                    "lets teachers take attendance offline and sync when the "
                    "network returns.\n\n"
                    "It runs in production on a DigitalOcean droplet behind "
                    "Caddy, with Docker, PostgreSQL and automated backups."
                ),
                "tech_tags": "React, Django, DRF, PostgreSQL, Docker, Caddy, "
                             "React Native, n8n",
                "live_url": "",
                "repo_url": "",
                "outcome": "Serves multiple schools in production from one droplet.",
                "is_featured": True,
                "display_order": 1,
            },
            {
                "slug": "ccec-school-portal",
                "title": "CCEC School Portal",
                "short_description": (
                    "The complete online management system of a real school in "
                    "Bamenda, live on the public internet."
                ),
                "description": (
                    "This is the production deployment that started it all. "
                    "CCEC Bamenda runs its daily operations on this system: "
                    "online admissions with document uploads and automated "
                    "email replies, fee payment tracking, mark entry and "
                    "report cards, transcripts generated as PDFs, and a "
                    "timetable for every class and teacher.\n\n"
                    "I migrated it off Heroku onto a DigitalOcean droplet, "
                    "moved media storage to local disk, set up nightly "
                    "database backups, and wired n8n for transactional "
                    "email. It has been serving the school without drama "
                    "since."
                ),
                "tech_tags": "React, Django, PostgreSQL, Docker, Caddy, n8n",
                "live_url": "https://caromabamenda.org",
                "repo_url": "",
                "outcome": "Runs a real school's daily operations in production.",
                "is_featured": True,
                "display_order": 2,
            },
            {
                "slug": "teacher-mobile-app",
                "title": "Teacher Companion Mobile App",
                "short_description": (
                    "A React Native app that lets teachers take attendance "
                    "offline, plan lessons and chat with the school."
                ),
                "description": (
                    "Teachers needed the school system in their pocket, and "
                    "the network in Bamenda is not always kind. So the app "
                    "stores attendance locally when the connection drops and "
                    "syncs it back with an idempotent bulk endpoint when the "
                    "network returns, which means no lost registers and no "
                    "duplicates.\n\n"
                    "It also carries a server backed lesson planner, class "
                    "chat with cursor pagination, a personal timetable view "
                    "and mark entry. Built with Expo and shipped as an APK "
                    "to the teachers' own phones."
                ),
                "tech_tags": "React Native, Expo, Django, REST, Offline sync",
                "live_url": "",
                "repo_url": "",
                "outcome": "Attendance survives network outages without losing a record.",
                "is_featured": True,
                "display_order": 3,
            },
            {
                "slug": "clinical-research-data-platform",
                "title": "Clinical Research Data Infrastructure",
                "short_description": (
                    "The REDCap, ETL and Power BI stack behind active TB "
                    "research at a reference laboratory."
                ),
                "description": (
                    "Clinical research lives and dies by its data. At the TB "
                    "Reference Laboratory I provisioned and hardened an on "
                    "premise REDCap server, designed the data capture "
                    "instruments with branching logic and quality control "
                    "rules, and wrote the Python pipelines that clean and "
                    "load every export into SharePoint with a full audit "
                    "trail.\n\n"
                    "Power BI dashboards on top give investigators real time "
                    "enrollment, screening and diagnostics numbers. The work "
                    "supported the research that earned WHO accreditation "
                    "for pooled TB testing."
                ),
                "tech_tags": "REDCap, Python, pandas, polars, Power BI, "
                             "Airflow, n8n, SharePoint",
                "live_url": "",
                "repo_url": "",
                "outcome": "Supported research that earned WHO accreditation for pooled testing.",
                "is_featured": False,
                "display_order": 4,
            },
            {
                "slug": "ccc-marketing-website",
                "title": "City College of Commerce Website",
                "short_description": (
                    "A fast public marketing site for a college, built with "
                    "Vite and React."
                ),
                "description": (
                    "A clean nine page marketing site for City College of "
                    "Commerce Mankon: programs, admissions, campus life and a "
                    "portal link into the school management platform. All "
                    "content lives in a single data file so the school can "
                    "update text without touching components."
                ),
                "tech_tags": "React, Vite, CSS",
                "live_url": "",
                "repo_url": "",
                "outcome": "Gives the college a modern public face with a portal gateway.",
                "is_featured": False,
                "display_order": 5,
            },
            {
                "slug": "this-portfolio",
                "title": "This Portfolio",
                "short_description": (
                    "The site you are reading now: Django, React, SQLite "
                    "visitor analytics and n8n automation."
                ),
                "description": (
                    "I wanted my portfolio to be a working demonstration, not "
                    "just a page about me. The content you are reading comes "
                    "from a Django API and is fully editable from the admin "
                    "panel, right down to this sentence. Every visit is "
                    "logged to a lightweight SQLite database and rolled up "
                    "into a private stats dashboard, and the contact form "
                    "hands messages to n8n for automated follow up."
                ),
                "tech_tags": "Django, DRF, React, Vite, SQLite, n8n, Docker, Caddy",
                "live_url": "",
                "repo_url": "",
                "outcome": "Content managed from Django admin, analytics included.",
                "is_featured": False,
                "display_order": 6,
            },
        ]
        for row in rows:
            Project.objects.update_or_create(slug=row["slug"], defaults=row)
        self.stdout.write(f"{len(rows)} projects seeded.")

    def seed_education(self):
        rows = [
            {
                "degree": "Master of Science in Computer Engineering",
                "institution": "University of Bamenda, National Higher Polytechnic Institute",
                "start_year": "2023", "end_year": "2024",
                "note": "",
                "display_order": 1,
            },
            {
                "degree": "Bachelor of Engineering in Computer Engineering",
                "institution": "University of Bamenda, National Higher Polytechnic Institute",
                "start_year": "2019", "end_year": "2023",
                "note": "Overall Best Graduate of the class of 2023",
                "display_order": 2,
            },
            {
                "degree": "GCE Advanced Level",
                "institution": "Presbyterian Comprehensive Secondary School, Azire Bamenda",
                "start_year": "2016", "end_year": "2018",
                "note": "",
                "display_order": 3,
            },
            {
                "degree": "GCE Ordinary Level",
                "institution": "Government High School Batibo",
                "start_year": "2011", "end_year": "2016",
                "note": "",
                "display_order": 4,
            },
        ]
        for row in rows:
            Education.objects.update_or_create(
                degree=row["degree"], institution=row["institution"],
                defaults=row,
            )
        self.stdout.write(f"{len(rows)} education rows seeded.")

    def seed_certifications(self):
        rows = [
            ("Software Engineering", "ALX Africa", "April 2023", 1),
            ("Introduction to Cybersecurity", "Cisco Networking Academy", "April 2023", 2),
            ("Python Programming Essentials", "Cisco Networking Academy", "April 2023", 3),
            ("Web3 Basics", "Binance Africa", "April 2023", 4),
            ("Blockchain and NFT", "Binance Academy", "April 2023", 5),
            ("Introduction to Python Programming", "Alison", "April 2023", 6),
            ("Leadership and Civic Engagement", "YALI Network", "April 2023", 7),
        ]
        for title, issuer, earned, order in rows:
            Certification.objects.update_or_create(
                title=title, issuer=issuer,
                defaults={"date_earned": earned, "display_order": order},
            )
        self.stdout.write(f"{len(rows)} certifications seeded.")

    def seed_skills(self):
        rows = [
            ("Frontend", "React, JavaScript, Vite, HTML, CSS, Figma", 1),
            ("Backend and APIs", "Django, Django REST Framework, Node.js, "
                                 "REST API design, Authentication", 2),
            ("Mobile", "React Native, Expo, Flutter, Offline first sync", 3),
            ("Data Engineering", "Python, pandas, polars, SQL, ETL pipelines, "
                                 "Data validation, REDCap", 4),
            ("BI and Reporting", "Power BI, Power Query, DAX, Excel, VBA, "
                                 "KPI dashboards", 5),
            ("Automation", "n8n, Apache Airflow, Power Automate, "
                           "Scheduled jobs, Webhooks", 6),
            ("Infrastructure", "Linux, Ubuntu, Docker, Caddy, Nginx, "
                               "DigitalOcean, AWS, Networking, Bash", 7),
            ("Databases", "PostgreSQL, MySQL, SQLite, pgAdmin, Backups", 8),
        ]
        for name, skills, order in rows:
            SkillGroup.objects.update_or_create(
                name=name,
                defaults={"skills": skills, "display_order": order},
            )
        self.stdout.write(f"{len(rows)} skill groups seeded.")

    def seed_awards(self):
        rows = [
            {
                "title": "Overall Best Graduate",
                "issuer": "National Higher Polytechnic Institute, University of Bamenda",
                "year": "2023",
                "description": (
                    "Graduated top of the entire institute while working and "
                    "teaching at the same time."
                ),
                "display_order": 1,
            },
            {
                "title": "WHO Accreditation Contribution",
                "issuer": "World Health Organization",
                "year": "2026",
                "description": (
                    "Part of the research team whose pooled TB testing work "
                    "earned WHO accreditation."
                ),
                "display_order": 2,
            },
            {
                "title": "Student Union Project Coordinator",
                "issuer": "NAHPI Student Association",
                "year": "2023",
                "description": "Elected to coordinate student projects for the academic year.",
                "display_order": 3,
            },
        ]
        for row in rows:
            Award.objects.update_or_create(title=row["title"], defaults=row)
        self.stdout.write(f"{len(rows)} awards seeded.")
