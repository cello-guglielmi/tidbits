from django.urls import path
from quotes.views import public

urlpatterns = [
    path('daily/', public.dailyPage, name='daily_page'),
    path('browse_quotes/', public.BrowseQuotes.as_view(), name='browse_quotes'),
    path('browse_authors/', public.BrowseAuthors.as_view(), name='browse_authors'),
    path('quote_cards/', public.quoteCards, name='quote_cards'),
    path('author_cards/', public.authorCards, name='author_cards'),
	path('author/<slug:slug>/', public.AuthorDetail.as_view(), name='author_detail'),
    # path('quote/<int:pk>/', views.QuoteDetailPartial.as_view(), name='quote_detail'),
]