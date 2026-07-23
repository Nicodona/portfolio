"""Post a visitor summary to the n8n webhook so automations (email,
WhatsApp and anything else n8n can reach) can report on traffic.

Run from cron on the droplet, for example every Monday morning:

    docker exec portfolio-web python manage.py send_visit_summary --days 7
"""

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.utils import timezone

from portfolio.models import ContactMessage, Visit


class Command(BaseCommand):
    help = "Send a visit summary to the n8n webhook."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7)

    def handle(self, *args, **options):
        if not settings.N8N_VISIT_WEBHOOK:
            self.stdout.write("N8N_VISIT_WEBHOOK is not set, nothing to do.")
            return

        days = options["days"]
        since = timezone.now() - timezone.timedelta(days=days)
        qs = Visit.objects.filter(created_at__gte=since)

        payload = {
            "event": "portfolio_visit_summary",
            "days": days,
            "views": qs.count(),
            "unique_visitors": qs.values("visitor_id").distinct().count(),
            "top_pages": list(
                qs.values("path").annotate(views=Count("id")).order_by("-views")[:5]
            ),
            "top_referrers": list(
                qs.exclude(referrer="")
                .values("referrer")
                .annotate(views=Count("id"))
                .order_by("-views")[:5]
            ),
            "new_messages": ContactMessage.objects.filter(
                created_at__gte=since
            ).count(),
            "generated_at": timezone.now().isoformat(),
        }

        requests.post(settings.N8N_VISIT_WEBHOOK, json=payload, timeout=15)
        self.stdout.write(self.style.SUCCESS(
            f"Summary sent: {payload['views']} views, "
            f"{payload['unique_visitors']} visitors in the last {days} days."
        ))
