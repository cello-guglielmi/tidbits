from django.urls import path
from quotes.views import user_module

app_name = 'user'

urlpatterns = [
    path('submit/', user_module.submitQuote, name='submit_quote'),
    path('submit/success', user_module.submitQuoteSuccess, name='submit_success'),
    path('like/<int:quote_id>', user_module.toggle_like, name='toggle_like'),
    path('save/<int:quote_id>', user_module.toggle_bookmark, name='toggle_bookmark'),
    path('bookmarks', user_module.myBookmarks, name='bookmarks'),
    path('entries', user_module.myEntries, name='entries'),
    path('submission_list', user_module.submissionList, name='submission_list'),
    path('submission_cards', user_module.submissionCards, name='submission_cards'),
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