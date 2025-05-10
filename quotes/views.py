from django.shortcuts import render
from .models import Quote, Author
import random, datetime
from django.views import generic

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

class AuthorDetail(generic.DetailView):
    model = Author

    # template_name = 'quotes/author_details.html'
    # Default is <app name>/<model name>_detail.html

    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quotes'] = self.object.quotes.all()
        return context
    # Manually passing related quotes allows for more flexibility & filtering:
    #    one_month_ago = timezone.now() - timedelta(days=30)
    #    context['quotes'] = self.object.quotes.filter(created_at__gte=one_month_ago)
    '''

class QuoteDetailPartial(generic.DetailView):
    model = Quote



