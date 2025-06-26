from django.urls import path, include
from quotes import views

app_name = 'quotes'

urlpatterns = [
    # Public-facing routes (browse, cards, authors, etc.)
    path('',    include('quotes.urls.public')),  
    # User-scoped routes
    path('user/', include(('quotes.urls.user_module', 'quotes'), namespace='user')), 
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