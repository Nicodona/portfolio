import logging
import threading

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

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
from .serializers import (
    AwardSerializer,
    CertificationSerializer,
    ContactMessageSerializer,
    EducationSerializer,
    ExperienceSerializer,
    GalleryImageSerializer,
    ProfileSerializer,
    ProjectSerializer,
    SkillGroupSerializer,
    TestimonialSerializer,
)

logger = logging.getLogger(__name__)


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """The public endpoints (track, contact, stats login) are called from the
    React app with plain fetch. Same-origin in production, throttled, and no
    state is readable without auth, so skipping CSRF here is a fair trade."""

    def enforce_csrf(self, request):
        return


class ContactThrottle(AnonRateThrottle):
    scope = "contact"


class LoginThrottle(AnonRateThrottle):
    scope = "login"


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _post_webhook(url, payload):
    if not url:
        return False
    try:
        requests.post(url, json=payload, timeout=8)
        return True
    except requests.RequestException:
        logger.warning("n8n webhook %s unreachable", url)
        return False


@api_view(["GET"])
@permission_classes([AllowAny])
def portfolio_payload(request):
    """Everything the public site needs, in one request."""
    ctx = {"request": request}
    published = {"is_published": True}
    return Response({
        "profile": ProfileSerializer(Profile.load(), context=ctx).data,
        "experiences": ExperienceSerializer(
            Experience.objects.filter(**published), many=True, context=ctx
        ).data,
        "projects": ProjectSerializer(
            Project.objects.filter(**published), many=True, context=ctx
        ).data,
        "education": EducationSerializer(
            Education.objects.filter(**published), many=True
        ).data,
        "certifications": CertificationSerializer(
            Certification.objects.filter(**published), many=True
        ).data,
        "skill_groups": SkillGroupSerializer(
            SkillGroup.objects.filter(**published), many=True
        ).data,
        "awards": AwardSerializer(
            Award.objects.filter(**published), many=True
        ).data,
        "gallery": GalleryImageSerializer(
            GalleryImage.objects.filter(**published), many=True, context=ctx
        ).data,
        "testimonials": TestimonialSerializer(
            Testimonial.objects.filter(**published), many=True
        ).data,
    })


@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([AllowAny])
def track_visit(request):
    data = request.data or {}
    visitor_id = str(data.get("visitor_id", ""))[:64]
    path = str(data.get("path", "/"))[:300]
    if not visitor_id:
        return Response({"detail": "visitor_id required"}, status=400)
    Visit.objects.create(
        visitor_id=visitor_id,
        path=path,
        referrer=str(data.get("referrer", ""))[:500],
        ip_address=_client_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
        country=str(data.get("country", ""))[:80],
    )
    return Response({"ok": True}, status=201)


@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([AllowAny])
@throttle_classes([ContactThrottle])
def contact(request):
    serializer = ContactMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    msg = serializer.save()

    def forward():
        ok = _post_webhook(settings.N8N_CONTACT_WEBHOOK, {
            "event": "portfolio_contact",
            "name": msg.name,
            "email": msg.email,
            "subject": msg.subject,
            "message": msg.message,
            "received_at": msg.created_at.isoformat(),
        })
        if ok:
            ContactMessage.objects.filter(pk=msg.pk).update(forwarded_to_n8n=True)

    threading.Thread(target=forward, daemon=True).start()
    return Response(
        {"ok": True, "detail": "Thanks for reaching out. I will get back to you soon."},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([AllowAny])
@throttle_classes([LoginThrottle])
def stats_login(request):
    user = authenticate(
        request,
        username=request.data.get("username", ""),
        password=request.data.get("password", ""),
    )
    if user is None or not user.is_staff:
        return Response({"detail": "Invalid credentials."}, status=401)
    login(request, user)
    return Response({"ok": True, "username": user.username})


@api_view(["POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
@permission_classes([AllowAny])
def stats_logout(request):
    logout(request)
    return Response({"ok": True})


@api_view(["GET"])
@permission_classes([IsAdminUser])
def stats(request):
    now = timezone.now()
    days = int(request.GET.get("days", 30))
    days = max(1, min(days, 365))
    since = now - timezone.timedelta(days=days)
    qs = Visit.objects.filter(created_at__gte=since)

    per_day = list(
        qs.annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(views=Count("id"), visitors=Count("visitor_id", distinct=True))
        .order_by("day")
    )
    top_pages = list(
        qs.values("path").annotate(views=Count("id")).order_by("-views")[:10]
    )
    top_referrers = list(
        qs.exclude(referrer="")
        .values("referrer")
        .annotate(views=Count("id"))
        .order_by("-views")[:10]
    )
    top_countries = list(
        qs.exclude(country="")
        .values("country")
        .annotate(views=Count("id"))
        .order_by("-views")[:10]
    )
    recent = list(
        qs.values("path", "referrer", "country", "created_at")[:25]
    )
    messages = ContactMessageSerializer(
        ContactMessage.objects.all()[:25], many=True
    ).data
    unread = ContactMessage.objects.filter(is_read=False).count()

    return Response({
        "range_days": days,
        "totals": {
            "views": qs.count(),
            "unique_visitors": qs.values("visitor_id").distinct().count(),
            "all_time_views": Visit.objects.count(),
            "all_time_visitors": Visit.objects.values("visitor_id")
            .distinct()
            .count(),
            "unread_messages": unread,
        },
        "per_day": per_day,
        "top_pages": top_pages,
        "top_referrers": top_referrers,
        "top_countries": top_countries,
        "recent_visits": recent,
        "recent_messages": messages,
        "generated_at": now.isoformat(),
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def stats_me(request):
    """Lets the stats page know whether a session is already active."""
    return Response({
        "authenticated": bool(
            request.user.is_authenticated and request.user.is_staff
        ),
        "username": request.user.username if request.user.is_authenticated else None,
    })
