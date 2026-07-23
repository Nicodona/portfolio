from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Award,
    Certification,
    ContactMessage,
    Education,
    Experience,
    GalleryImage,
    Profile,
    Project,
    SkillGroup,
    Testimonial,
    Visit,
)

admin.site.site_header = "Njei Nicodemus — Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your portfolio content"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = ["photo_preview"]
    fieldsets = (
        ("Identity", {
            "fields": (
                "full_name", "preferred_name", "headline", "tagline", "about",
            )
        }),
        ("Photo and CV", {"fields": ("photo", "photo_preview", "cv_file")}),
        ("Contact", {
            "fields": (
                "email", "phone", "location", "timezone_label",
                "github_url", "linkedin_url", "whatsapp_number",
            )
        }),
        ("Availability", {"fields": ("available_for_work", "availability_note")}),
    )

    @admin.display(description="Current photo")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:180px;border-radius:12px;" />',
                obj.photo.url,
            )
        return "No photo uploaded yet."

    def has_add_permission(self, request):
        return not Profile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = [
        "role", "organization", "start_date", "end_date",
        "display_order", "is_published",
    ]
    list_editable = ["display_order", "is_published"]
    search_fields = ["role", "organization"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "title", "is_featured", "live_url", "display_order", "is_published",
    ]
    list_editable = ["is_featured", "display_order", "is_published"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["image_preview"]
    search_fields = ["title"]

    @admin.display(description="Current image")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;" />',
                obj.image.url,
            )
        return "No image uploaded yet."


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ["degree", "institution", "start_year", "end_year",
                    "display_order", "is_published"]
    list_editable = ["display_order", "is_published"]


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ["title", "issuer", "date_earned",
                    "display_order", "is_published"]
    list_editable = ["display_order", "is_published"]


@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "skills", "display_order", "is_published"]
    list_editable = ["display_order", "is_published"]


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ["title", "issuer", "year", "display_order", "is_published"]
    list_editable = ["display_order", "is_published"]


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["author", "author_title", "display_order", "is_published"]
    list_editable = ["display_order", "is_published"]


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ["preview", "title", "section", "caption",
                    "display_order", "is_published"]
    list_editable = ["section", "display_order", "is_published"]
    list_filter = ["section", "is_published"]
    list_display_links = ["preview", "title"]
    readonly_fields = ["image_preview"]
    radio_fields = {"section": admin.VERTICAL}
    fields = ["image", "image_preview", "section", "title", "caption",
              "display_order", "is_published"]

    @admin.display(description="Photo")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:52px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"

    @admin.display(description="Current photo")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:220px;border-radius:8px;" />',
                obj.image.url,
            )
        return "Upload a photo above."


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ["created_at", "path", "visitor_id", "ip_address",
                    "country", "referrer"]
    list_filter = ["created_at"]
    search_fields = ["path", "visitor_id", "ip_address", "referrer"]
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["created_at", "name", "email", "subject",
                    "is_read", "forwarded_to_n8n"]
    list_editable = ["is_read"]
    list_filter = ["is_read", "forwarded_to_n8n"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message",
                       "created_at", "forwarded_to_n8n"]

    def has_add_permission(self, request):
        return False
