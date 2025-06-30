from . import models
from django.urls import resolve
from django.utils import timezone
import datetime

def submission_moderation(request):
    match = resolve(request.path_info)
    if match.namespace != 'admin':
        return {}
    
    pending_quote_subs = models.QuoteSubmission.objects.filter(status='pending')
    pending_author_subs = models.AuthorSubmission.objects.filter(status='pending')

    now = timezone.now()
    monday = now - datetime.timedelta(days=100)# days=now.weekday())
    start = monday.replace(hour=0, minute=0, second=0, microsecond=0)

    quote_subs_count = models.QuoteSubmission.objects.filter(created_at__gt=start).count()
    quote_apprs_count = models.QuoteSubmission.objects.filter(created_at__gt=start, status='approved').count()
    quote_rejs_count = models.QuoteSubmission.objects.filter(created_at__gt=start, status='rejected').count()

    pending_quote_count = pending_quote_subs.count()
    pending_author_count = pending_author_subs.count()

    # last_week = timezone.now() - timezone.timedelta(weeks=1)
    # recent_quotes = quote_subs.filter(created_at__gte=last_week)
    # recent_authors = author_subs.filter(created_at__gte=last_week)

    recent_quotes = pending_quote_subs.order_by('-created_at')[:10]
    recent_authors = pending_author_subs.order_by('-created_at')[:10]

    return {
        'pending_quote_count': pending_quote_count,
        'pending_author_count': pending_author_count,
        'recent_quote_submissions': recent_quotes,
        'recent_author_submissions': recent_authors,
        'quote_subs_count': quote_subs_count,
        'quote_apprs_count': quote_apprs_count,
        'quote_rejs_count': quote_rejs_count,
    }