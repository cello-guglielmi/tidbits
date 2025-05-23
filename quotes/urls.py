from django.urls import path
from . import views

urlpatterns = [
    #
    #
    path('daily/', views.daily_page, name='daily_page'),
	path('author/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('<int:pk>/', views.QuoteDetailPartial.as_view(), name='quote_detail'),
    path('browse/', views.BrowseList.as_view(), name='browse'),
    path('list/', views.quoteListView, name='quote_list'),
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