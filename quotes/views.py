from django.shortcuts import render
from .models import Quote, Author
import random, datetime

# Create your views here.

def index(request):

    def get_daily_seed(today):
        seed = 0
        for i in str(today):
            if i.isdigit():
                seed += int(i)
        return seed
    
    context = {}
    quote = None
    today = datetime.date.today()
    all_quotes = list(Quote.objects.all())
    if all_quotes:
        seed = get_daily_seed(today) % len(all_quotes)
        quote = all_quotes[seed]
    context['quote'] = quote
    context['day'] = today.strftime('%d')
    context['weekday'] = today.strftime('%A')
    context['month'] = today.strftime('%B')
    context['year'] = today.strftime('%Y')
    template = 'quotes/index.html'
    return render(request, template, context)



def homepage(request):
    return render(request, 'homepage.html', {'user': request.user})