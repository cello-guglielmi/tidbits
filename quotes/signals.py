from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from utils.url_utils import absolute_url_builder
from django.conf import settings
from . import models

@receiver(pre_save, sender=models.QuoteSubmission)
def cache_old_status(sender, instance, **kwargs):
    if instance.pk:
        old = sender.objects.get(pk=instance.pk)
        instance.old_status = old.status
    else:
        instance.old_status = None

@receiver(post_save, sender=models.QuoteSubmission)
def on_qsub_status_change(sender, instance, created, **kwargs):
    if created or instance.status == instance.old_status:
        return
    
    if instance.status == 'approved':
        if not instance.author:
            return
        models.Quote.objects.create(
            sentence = instance.sentence,
            author = instance.author,
            mood = instance.mood,
            submitted_by = instance.submitted_by,
        )
        url= absolute_url_builder('quotes:user:entries')
        subject = "Your quote submission has been approved!"
        body = (
            f"Hi {instance.submitted_by.nickname},\n\n"
            f"We're happy to inform that your quote “{instance.sentence}” has been approved, and is now part of our quotes collection!\n"
            "You can view your contributions under 📕Entries:\n"
            f"{url}\n\n"
            "Thank you for your awesome contribution! 😊\n"
            "— The Tidbits Team"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.submitted_by.email], fail_silently=False)

    elif instance.status == 'rejected':
        if not instance.moderation_comment:
            return
        url= absolute_url_builder('accounts:user_profile')
        subject = "Your quote submission has been rejected."
        body = (
            f"Hi {instance.submitted_by.nickname},\n\n"
            f"We regret to inform you that your quote “{instance.sentence}” has been rejected by our moderation staff.\n"
            f"Reason: {instance.moderation_comment}\n\n"
            "You can view your submission history here:\n"
            f"{url}\n\n"
            "Feel free to revise and submit again if you'd like.\n"
            "— The Tidbits Team"
        )
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [instance.submitted_by.email], fail_silently=False)