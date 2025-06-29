from django.urls import reverse
from django.conf import settings

# Centralized absolute URL builder, useful for signals, emails, async jobs, etc.
# Even though currently used in one place, it's here for scalability and clarity.

def absolute_url_builder(view_url_name, *args, **kwargs):
    protocol = getattr(settings, 'URL_PROTOCOL', 'https')
    domain = settings.BASE_DOMAIN
    path = reverse(view_url_name, args=args, kwargs=kwargs)
    return f'{protocol}://{domain}{path}'