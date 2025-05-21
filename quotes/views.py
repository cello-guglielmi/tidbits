from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Quote, Author
import random, datetime
from django.views import generic

# Create your views here.

def daily_page(request):
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

def quoteListView(request):
    quotes = Quote.objects.all()
    try:
        author = int(request.GET.get('author'))
    except (TypeError, ValueError):
        author = None
    if author:
        quotes = quotes.filter(author_id=author)
    search_query = request.GET.get('search', '')
    if search_query:
        quotes = quotes.filter(sentence__icontains=search_query)
    mood_tags = request.GET.getlist('mood[]')
    if mood_tags:
        quotes = quotes.filter(mood__in=mood_tags)

    sz = int(request.GET.get('BATCH_SIZE', 3))
    paginator = Paginator(quotes, sz)
    page_number = int(request.GET.get('page', 1))
    page_obj = paginator.get_page(page_number)
    
    context = {
        'quotes': page_obj.object_list,
        'page': page_number,
        'page_obj': page_obj,
        'listAuthor': author,
        'searchQuery': search_query,
        'moodTags': mood_tags,
        'nextPage': page_obj.next_page_number() if page_obj.has_next() else None,
    }
    
    initial = int(request.GET.get('initial'))

    if initial == 1:
        # For initial load, return the complete list with search bar
        #print("========INITIAL RENDER========>", initial, "<")
        return render(request, 'quotes/components/quote_list.html', context)
    else:
        # For pagination requests and searches, return just the quote items as HTML fragments
        return render(request, 'quotes/components/quote_items_wrapper.html', context)



class QuoteDetailPartial(generic.DetailView):
    model = Quote
    template_name = 'quotes/components/quote_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_author"] = self.request.GET.get('show_author') == '1'
        return context


class BrowseList(generic.ListView):
    model = Quote
    template_name = 'quotes/browse_list.html' # Default is <app name>/<model name>_list.html ('polls/question_list.html')
    context_object_name = 'browse_quote_list'


