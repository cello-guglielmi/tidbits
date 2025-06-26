from django.urls import path, include

app_name = 'quotes'

urlpatterns = [
    # Public-facing routes (browse, cards, authors, etc.)
    path('',    include('quotes.urls.public')),  
    # User-scoped routes
    path('user/', include('quotes.urls.user_module', namespace='user')), 
]