from rest_framework import serializers

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
)


class ProfileSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()
    cv_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            "full_name", "preferred_name", "headline", "tagline", "about",
            "photo_url", "cv_url", "email", "phone", "location",
            "timezone_label", "github_url", "linkedin_url",
            "whatsapp_number", "available_for_work", "availability_note",
        ]

    def _abs(self, f):
        if not f:
            return None
        request = self.context.get("request")
        url = f.url
        return request.build_absolute_uri(url) if request else url

    def get_photo_url(self, obj):
        return self._abs(obj.photo)

    def get_cv_url(self, obj):
        return self._abs(obj.cv_file)


class ExperienceSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(source="tags_list", read_only=True)
    highlights = serializers.ListField(source="highlights_list", read_only=True)

    class Meta:
        model = Experience
        fields = [
            "id", "role", "organization", "organization_url", "location",
            "start_date", "end_date", "summary", "highlights", "tags",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(source="tags_list", read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id", "title", "slug", "short_description", "description",
            "image_url", "tags", "live_url", "repo_url", "outcome",
            "is_featured",
        ]

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ["id", "degree", "institution", "start_year", "end_year", "note"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = ["id", "title", "issuer", "date_earned", "credential_url"]


class SkillGroupSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(source="skills_list", read_only=True)

    class Meta:
        model = SkillGroup
        fields = ["id", "name", "skills"]


class GalleryImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = GalleryImage
        fields = ["id", "image_url", "title", "caption", "section"]

    def get_image_url(self, obj):
        if not obj.image:
            return None
        request = self.context.get("request")
        url = obj.image.url
        return request.build_absolute_uri(url) if request else url


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = ["id", "title", "issuer", "year", "description"]


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = ["id", "author", "author_title", "quote"]


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
