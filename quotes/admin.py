from django.contrib import admin
from . import models

# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at', 'likes', 'mood', 'author']
    list_editable = ['mood', 'likes']

"""     @admin.display(description="Author's Country")
    def authors_country(self, obj):
        return obj.author.get_nationality_display() """
    
    # list_filter = ['author__nationality']
    # search_fields = ['sentence', 'author__name']
        

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'id']
    search_fields = ['name']
    list_editable = ['nationality']

class QuoteSubmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'created_at', 'submitted_by', 'updated_at', 'reviewed_by', 'author', 'new_author_submission']

class AuthorSubmissionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status', 'created_at', 'submitted_by', 'updated_at', 'reviewed_by', 'name']

class NationalityAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(models.Quote, QuoteAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.QuoteSubmission, QuoteSubmissionAdmin)
admin.site.register(models.AuthorSubmission, AuthorSubmissionAdmin)
admin.site.register(models.Nationality)
