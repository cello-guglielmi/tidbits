from django.contrib import admin
from .models import Quote, Author

# Register your models here.

class QuoteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'likes', 'mood', 'author', 'authors_country']
    list_editable = ('mood', 'likes')

    @admin.display(description="Author's Country")
    def authors_country(self, obj):
        return obj.author.get_nationality_display()
    
    list_filter = ['author__nationality']
    search_fields = ['sentence', 'author__full_name']
        

class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'nationality', 'id']
    search_fields = ['full_name']
    list_filter = ['nationality']

admin.site.register(Quote, QuoteAdmin)
admin.site.register(Author, AuthorAdmin)
