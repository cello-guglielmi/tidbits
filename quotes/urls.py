from django.urls import path
from quotes import views

app_name = 'quotes'

urlpatterns = [
    path('daily/', views.daily_page, name='daily_page'),
	path('author/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('<int:pk>/', views.QuoteDetailPartial.as_view(), name='quote_detail'),
    path('browse/', views.BrowseList.as_view(), name='browse'),
    path('list/', views.quoteListView, name='quote_list'),
    path('author/add/', views.AuthorCreateView.as_view(), name='author-add'),
    path('author/<int:pk>/update', views.AuthorUpdateViewFunc, name='author-update'),
    path('author/<int:pk>/delete', views.AuthorDeleteView.as_view(), name='author-delete'),
    path('submit/', views.submitQuote, name='submit_quote'),
    path('submit/success', views.submitQuoteSuccess, name='submit_success'),
    path('quote/<int:pk>/update', views.QuoteUpdateView.as_view(), name='quote-update'),
    path('quote/<int:pk>/delete', views.QuoteDeleteView.as_view(), name='quote-delete'),
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