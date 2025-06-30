from . import models
from django.urls import resolve

def moderation_counts(request):
    match = resolve(request.path_info)
    if match.namespace != 'admin':
        return {}

    pending_quote_count = models.QuoteSubmission.objects.filter(status='pending').count()
    pending_author_count = models.AuthorSubmission.objects.filter(status='pending').count()

    return {
        'pending_quote_count': pending_quote_count,
        'pending_author_count': pending_author_count,
    }