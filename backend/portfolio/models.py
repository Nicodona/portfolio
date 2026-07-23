import uuid

from django.db import models


def _unique_name(folder, filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "bin"
    return f"{folder}/{uuid.uuid4().hex}.{ext}"


def profile_photo_path(instance, filename):
    return _unique_name("profile", filename)


def cv_path(instance, filename):
    return _unique_name("cv", filename)


def project_image_path(instance, filename):
    return _unique_name("projects", filename)


def gallery_image_path(instance, filename):
    return _unique_name("gallery", filename)


class SingletonModel(models.Model):
    """Only one row ever exists; saving always writes row pk=1."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Profile(SingletonModel):
    full_name = models.CharField(max_length=120, default="Njei Nicodemus Mbacham")
    preferred_name = models.CharField(max_length=60, blank=True, default="Nghan")
    headline = models.CharField(
        max_length=200,
        default="Full-Stack Developer & Health-Tech Engineer",
        help_text="The role line shown under your name in the hero.",
    )
    tagline = models.TextField(
        blank=True,
        help_text="One or two sentences shown in the hero under the headline.",
    )
    about = models.TextField(
        blank=True,
        help_text="The About section. Separate paragraphs with a blank line.",
    )
    photo = models.ImageField(upload_to=profile_photo_path, blank=True, null=True)
    cv_file = models.FileField(
        upload_to=cv_path, blank=True, null=True,
        help_text="Your CV as a PDF. Shown as a Download Resume button.",
    )
    email = models.EmailField(blank=True, default="njeinicodona@gmail.com")
    phone = models.CharField(max_length=40, blank=True, default="+237 680 949 841")
    location = models.CharField(max_length=120, blank=True, default="Bamenda, Cameroon")
    timezone_label = models.CharField(max_length=40, blank=True, default="GMT+1")
    github_url = models.URLField(blank=True, default="https://github.com/nicodona")
    linkedin_url = models.URLField(
        blank=True, default="https://www.linkedin.com/in/njei-nicodemus"
    )
    whatsapp_number = models.CharField(
        max_length=40, blank=True,
        help_text="International format without spaces, e.g. 237680949841. Used for the WhatsApp chat link.",
    )
    available_for_work = models.BooleanField(default=True)
    availability_note = models.CharField(
        max_length=120, blank=True, default="Available for new projects"
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profile"

    def __str__(self):
        return self.full_name


class Experience(models.Model):
    role = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    organization_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(
        blank=True, null=True, help_text="Leave empty for a current role."
    )
    summary = models.TextField(
        help_text="Two or three sentences on impact. Lead with outcomes and numbers."
    )
    highlights = models.TextField(
        blank=True, help_text="Optional bullet points, one per line."
    )
    tech_tags = models.CharField(
        max_length=400, blank=True,
        help_text="Comma separated, e.g. React, Django, PostgreSQL",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "-start_date"]

    def __str__(self):
        return f"{self.role} — {self.organization}"

    @property
    def tags_list(self):
        return [t.strip() for t in self.tech_tags.split(",") if t.strip()]

    @property
    def highlights_list(self):
        return [h.strip() for h in self.highlights.splitlines() if h.strip()]


class Project(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    short_description = models.CharField(
        max_length=300, help_text="One sentence for the card grid."
    )
    description = models.TextField(
        help_text="Problem, solution, impact. Separate paragraphs with a blank line."
    )
    image = models.ImageField(
        upload_to=project_image_path, blank=True, null=True,
        help_text="A screenshot. Wide format works best, around 1200x750.",
    )
    tech_tags = models.CharField(max_length=400, blank=True)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    outcome = models.CharField(
        max_length=200, blank=True,
        help_text="One measurable result, e.g. Runs daily for 1200+ students.",
    )
    is_featured = models.BooleanField(
        default=False, help_text="Featured projects get the large showcase layout."
    )
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    @property
    def tags_list(self):
        return [t.strip() for t in self.tech_tags.split(",") if t.strip()]


class Education(models.Model):
    degree = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    start_year = models.CharField(max_length=20, blank=True)
    end_year = models.CharField(max_length=20, blank=True)
    note = models.CharField(
        max_length=250, blank=True,
        help_text="e.g. Overall Best Graduate 2023",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} — {self.institution}"


class Certification(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=150)
    date_earned = models.CharField(max_length=40, blank=True)
    credential_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.title} ({self.issuer})"


class SkillGroup(models.Model):
    name = models.CharField(max_length=100, help_text="e.g. Backend, Data Engineering")
    skills = models.TextField(help_text="Comma separated list of technologies.")
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.name

    @property
    def skills_list(self):
        return [s.strip() for s in self.skills.split(",") if s.strip()]


class Award(models.Model):
    title = models.CharField(max_length=200)
    issuer = models.CharField(max_length=200, blank=True)
    year = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=300, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    author = models.CharField(max_length=120)
    author_title = models.CharField(max_length=200, blank=True)
    quote = models.TextField()
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.author}: {self.quote[:40]}"


class GalleryImage(models.Model):
    SECTION_WORK = "work"
    SECTION_SCHOOL = "school"
    SECTION_PROJECTS = "projects"
    SECTION_LIFE = "life"
    SECTION_CHOICES = [
        (SECTION_WORK, "Work — also shown on the Experience page"),
        (SECTION_SCHOOL, "School — also shown on the Education page"),
        (SECTION_PROJECTS, "Projects — also shown on the Projects page"),
        (SECTION_LIFE, "Life & community — shown on the Gallery page only"),
    ]

    image = models.ImageField(
        upload_to=gallery_image_path,
        help_text="A photo of you in action. Landscape around 1600px wide works best.",
    )
    section = models.CharField(
        max_length=20,
        choices=SECTION_CHOICES,
        default=SECTION_LIFE,
        help_text=(
            "Where this photo belongs. Every photo appears on the Gallery "
            "page; Work, School and Projects photos also appear on their "
            "matching page."
        ),
    )
    title = models.CharField(
        max_length=150, blank=True,
        help_text="Short label shown on the photo, e.g. Speaking at DevFest Bamenda.",
    )
    caption = models.CharField(
        max_length=300, blank=True,
        help_text="One sentence of context, shown in the enlarged view.",
    )
    display_order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.title or f"Photo #{self.pk}"


class Visit(models.Model):
    """One row per tracked page view. Kept intentionally small so SQLite
    stays fast for years of traffic."""

    visitor_id = models.CharField(
        max_length=64, db_index=True,
        help_text="Anonymous id generated in the browser and kept in localStorage.",
    )
    path = models.CharField(max_length=300)
    referrer = models.CharField(max_length=500, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True)
    country = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.path} @ {self.created_at:%Y-%m-%d %H:%M}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    forwarded_to_n8n = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.subject or self.message[:40]}"
