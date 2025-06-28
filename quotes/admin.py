from django.contrib import admin
from django.contrib import messages
from django.db.models import Count
from . import models
from . import forms
from django.utils.safestring import mark_safe
from django.db import transaction
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

# Register your models here.


@admin.register(models.Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at', 'mood', 'author', 'num_likes', 'num_faves', 'submitted_by']
    list_editable = ['mood',] # 'likes']
    list_filter = ['mood']
    search_fields = ['sentence', 'author__name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # annotate each Quote with a _likes_count attribute
        return qs.annotate(likes_count=Count('likes'), fave_count=Count('bookmarked_by'))

    def num_likes(self, obj):
        return obj.likes_count
    
    def num_faves(self, obj):
        return obj.fave_count
    
    num_likes.admin_order_field = 'likes_count'
    num_faves.admin_order_field = 'fave_count'

@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'nationality', 'portrait', 'id']
    list_filter = ['nationality']
    search_fields = ['name', 'nationality']

@admin.register(models.Nationality)
class NationalityAdmin(admin.ModelAdmin):
    search_fields = ['name']


#==========================================================
# Considered building a custom admin dashboard app
# But Django's admin already provides 99% of functionality
#==========================================================

@admin.register(models.QuoteSubmission)
class QuoteSubmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'author_status', 'mood', 'submitted_by', 'created_at', 'reviewed_by', 'updated_at']
    search_fields = ['sentence', 'mood', 'author', 'author_status']
    list_filter = ['status']
    list_editable = ['mood']
    readonly_fields = ['status', 'author_status', 'author', 'new_author_submission', 'created_at', 'submitted_by', 'updated_at', 'reviewed_by']
    fieldsets = (
        (None, {
            'fields': ('sentence', 'mood', 'status', 'moderation_comment')
        }),
        ('Author Information', {
            'fields': ('author_status', 'author', 'new_author_submission')
        }),
        ('Audit Trail', {
            'classes': ('collapse',),
            'fields': ('submitted_by', 'created_at', 'reviewed_by', 'updated_at')
        }),
    )
    actions = ['approve_submissions', 'reject_submissions']

    def author_status(self, obj):
        return 'Valid ✔' if obj.author else 'Submission ⚠️'  

    @admin.action(description='Approve Selected Submissions')
    def approve_submissions(self, request, queryset):
        # Could be collapsed into a one-pass loop, aggregating error results over individual iteration.
        # But for clarity and because selected rows are supposedly few at a time, we'll go with separate filters.
        not_pending = queryset.exclude(status='pending')
        missing_author = queryset.filter(author=None)
        to_approve = queryset.filter(status='pending').exclude(author=None)
        if not_pending.exists():
            self.message_user(request, f'{not_pending.count()} of selected submissions are not pending approval.', level=messages.ERROR)
        if missing_author.exists():
            self.message_user(request, f'{missing_author.count()} of selected submissions do not have an approved author.', level=messages.ERROR)
        
        if to_approve.exists():
            message = (
                "Hi {nickname},\n\n"
                "We're happy to inform that your quote '{sentence}' has been approved, and is now part of our quotes collection!\n"
                "You can view your contributions under 📕Entries:\n"
                "{url}\n\n"
                "We kindly thank you for your awesome contribution! 😊\n"
                "— The Tidbits Team"
            )
            for subm in to_approve:
                models.Quote.objects.create(
                    sentence = subm.sentence,
                    author = subm.author,
                    mood = subm.mood,
                    submitted_by = subm.submitted_by,
                )
                subm.status = 'approved'
                subm.reviewed_by = request.user
                subm.save()
                send_mail("Your quote submission has been approved!",
                          message.format(
                              nickname=subm.submitted_by.nickname,
                              sentence=subm.sentence,
                              url=request.build_absolute_uri(reverse('quotes:user:user_contributions'))
                          ),
                          settings.DEFAULT_FROM_EMAIL,
                          [subm.submitted_by.email],
                          fail_silently=False,
                )
            self.message_user(request, f'{to_approve.count()} of selected submissions were successfully approved!', level=messages.SUCCESS)

    @admin.action(description='Reject Selected Submissions')
    def reject_submissions(self, request, queryset):
        not_pending = queryset.exclude(status='pending')
        missing_comment = queryset.filter(moderation_comment='')
        to_reject = queryset.filter(status='pending').exclude(moderation_comment='')
        if not_pending.exists():
            self.message_user(request, f'{not_pending.count()} of selected submissions are not pending approval.', level=messages.ERROR)
        if missing_comment.exists():
            self.message_user(request, f'{missing_comment.count()} of selected submissions are missing a moderation comment.', level=messages.ERROR)
        
        if to_reject.exists():
            message = (
                "Hi {nickname},\n\n"
                "We regret to inform you that your quote '{sentence}' has been rejected by our moderation staff.\n"
                "Reason: {comment}\n\n"
                "You can view your submission history here:\n"
                "{url}\n\n"
                "Feel free to revise and submit again if you'd like.\n"
                "— The Tidbits Team"
            )
            for subm in to_reject:             
                subm.status = 'rejected'
                subm.reviewed_by = request.user
                subm.save()
                send_mail("Your quote submission has been rejected.",
                          message.format(
                              nickname=subm.submitted_by.nickname,
                              sentence=subm.sentence,
                              comment=subm.moderation_comment,
                              url=request.build_absolute_uri(reverse('accounts:user_profile'))
                          ),
                          settings.DEFAULT_FROM_EMAIL,
                          [subm.submitted_by.email],
                          fail_silently=False,
                )
            self.message_user(request, f'{to_reject.count()} of selected submissions were successfully rejected.', level=messages.SUCCESS)

@admin.register(models.AuthorSubmission)
class AuthorSubmissionAdmin(admin.ModelAdmin):
    form = forms.AuthorSubmissionAdminForm
    list_display = ['__str__', 'status', 'author_obj', 'created_at', 'submitted_by', 'updated_at', 'reviewed_by']
    search_fields = ['name']
    list_filter = ['status']
    readonly_fields = ['status', 'author_obj', 'created_at', 'submitted_by', 'updated_at', 'reviewed_by']
    fieldsets = (
        (None, {
            'fields': ('name', 'status',)
        }),
        ('Approval', {
            'classes': ('wide',),
            'description': mark_safe(
                "<h1>Author Submission Approval Form</h1>"
                "<h3>Please ensure the following:</h3>"
                "<h4>• The author name is correct and no duplicates exist.</h4>"
                "<h4>• The nationality is accurate.</h4>"
                "<h4>• The portrait image is clear and appropriate.</h4>"
                "<h3>Saving this form will generate a proper Author object.</h3>"
            ),
            'fields': ('nationality', 'portrait'),
        }),
        ('Audit Trail', {
            'classes': ('collapse',),
            'fields': ('submitted_by', 'created_at', 'reviewed_by', 'updated_at')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.status != 'pending':
            readonly.append('name')
        return readonly

    def get_fieldsets(self, request, obj=None):
        all_fs = super().get_fieldsets(request, obj)
        if obj and obj.status != 'pending':
            return [
                fs for fs in all_fs
                if fs[0] != 'Approval'
            ]
        return all_fs

    def save_model(self, request, obj, form, change):

        if obj.status == 'pending':        
            with transaction.atomic(): 
                author = models.Author.objects.create(
                    name = obj.name,
                    portrait = form.cleaned_data['portrait'],
                    nationality = form.cleaned_data['nationality'],
                )

                models.QuoteSubmission.objects.filter(
                    new_author_submission=obj
                ).update(
                    author=author,
                    new_author_submission=None
                )

                obj.status = 'approved'
                obj.author_obj = author
                obj.reviewed_by = request.user

                self.message_user(request, f'Author {author.name!r} successfully created from submission {obj.pk}.', level=messages.SUCCESS)

        else:
            self.message_user(request, f'Submission {obj.pk} is already approved. No new Author created.', level=messages.WARNING)

        return super().save_model(request, obj, form, change)
