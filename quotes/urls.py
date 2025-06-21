from django.urls import path
from quotes import views

app_name = 'quotes'

urlpatterns = [
    path('daily/', views.daily_page, name='daily_page'),
    path('browse_quotes/', views.BrowseQuotes.as_view(), name='browse_quotes'),
    path('browse_authors/', views.BrowseAuthors.as_view(), name='browse_authors'),
    path('quote_list/', views.quoteListView, name='quote_list'),
    path('author_list/', views.authorListView, name='author_list'),
    # path('quote/<int:pk>/', views.QuoteDetailPartial.as_view(), name='quote_detail'),
	path('author/<slug:slug>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('submit/', views.submitQuote, name='submit_quote'),
    path('submit/success', views.submitQuoteSuccess, name='submit_success'),
    path('like/<int:quote_id>', views.toggle_like, name='toggle_like'),
    path('favorite/<int:quote_id>', views.toggle_favorite, name='toggle_favorite'),
]

'''
app_name = 'polls'
urlpatterns = [
	# ex: /polls/
    path('', views.IndexView.as_view(), name='index'),
	# ex: /polls/5/
	path('<int:pk>/', views.DetailView.as_view(), name='detail'),
	# ex: /polls/5/results/
	path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
	# ex: /polls/5/vote/
	path('<int:question_id>/vote/', views.vote, name='vote')

]
'''