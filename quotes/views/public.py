from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Count, Sum
from quotes.models import Quote, Author
from quotes.forms import QuoteSubmissionForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views import generic
from django.templatetags.static import static
import datetime
# from django.core.paginator import Paginator

# Create your views here.

class HelpSection(generic.TemplateView):
    template_name = 'help.html'

class AuthorDetail(generic.DetailView):
    model = Author

class BrowseAuthors(generic.TemplateView):
    template_name = 'quotes/browse_authors.html'

class BrowseQuotes(generic.TemplateView):
    template_name = 'quotes/browse_quotes.html'
    

def dailyPage(request):

    def get_daily_seed(day):
        seed = 0
        for i in str(day):
            if i.isdigit():
                seed += int(i)
        return seed
    
    def get_bg(mood, seed):
        idx = seed % 4
        filename = f'{mood}{idx}.png'
        filepath = static(f'images/bg/{filename}')
        bg_url = f'style="background-image: url(\'{filepath}\');"'
        return bg_url
    
    today = datetime.date.today()
    ql = list(Quote.objects.all())
    seed = get_daily_seed(today)
    idx = seed % len(ql)
    quote = ql[idx]
    context = {
        'quote': quote,
        'day': today.strftime('%d'),
        'weekday': today.strftime('%A'),
        'month': today.strftime('%B'),
        'year': today.strftime('%Y'),
        'backgroundURL': get_bg(quote.mood, seed),
    }
    template = 'quotes/daily_page.html'
    return render(request, template, context)


def quoteCards(request):
    qs = Quote.objects.all()
    author = request.GET.get('list_author')
    if author:
        qs = qs.filter(author__slug=author)
    search_query = request.GET.get('search', '')
    if search_query:
        qs = qs.filter(sentence__icontains=search_query)
    mood_tags = request.GET.getlist('mood[]')
    if mood_tags:
        qs = qs.filter(mood__in=mood_tags)
    user_contr = request.GET.get('contributions', '')
    user_bms = request.GET.get('bookmarks', '')
    if user_contr:
        qs = qs.filter(submitted_by=user_contr)
    elif user_bms:
        qs = qs.filter(bookmarked_by=user_bms)
    sort = request.GET.get('sort_value', 'id')
    qs = qs.order_by(sort)

    batchSize = int(request.GET.get('batch_size', 1))
    itemCounter = int(request.GET.get('item_counter', batchSize))

    #==================================================================================================
    # Decided to utilize list slicing for pagination over Django's paginator.
    # Cleaner implementation for my functonality, and removes the need for "pageNumber" (hidden input)
    #==================================================================================================
    # pageNumber = int(request.GET.get('page_number', 1))
    # paginator = Paginator(qs, itemCounter) if pageNumber == 1 else Paginator(qs, batchSize)
    # pageObj = paginator.get_page(pageNumber)
    # if request.headers.get('hx-trigger') == 'show-more-button':
    # itemCounter += batchSize

    if request.headers.get('hx-trigger') == 'show-more-button':
        start = itemCounter
        itemCounter += batchSize
        visible_qs = qs[start:itemCounter]
    else:
        visible_qs = qs[:itemCounter]
    hasMore = qs.count() > itemCounter

    context = {
        'quotes': visible_qs,
        'listAuthor': author,
        'batchSize': batchSize,
        'itemCounter': itemCounter,
        'hasMore': hasMore,
    }
    return render(request, 'quotes/components/quote_list/quote_cards.html', context)


def authorCards(request):
    qs = (Author.objects.all().annotate(
            num_quotes=Count('quotes'),
            total_likes=Sum('quotes__likes'),))
    search_query = request.GET.get('search', '')
    if search_query:
        qs = qs.filter(
            Q(name__icontains=search_query) |
            Q(nationality__name__icontains=search_query)
        )
    sort = request.GET.get('sort_value', 'id')
    qs = qs.order_by(sort)

    batchSize = int(request.GET.get('batch_size', 1))
    itemCounter = int(request.GET.get('item_counter', batchSize))

    if request.headers.get('hx-trigger') == 'show-more-button':
        start = itemCounter
        itemCounter += batchSize
        visible_qs = qs[start:itemCounter]
    else:
        visible_qs = qs[:itemCounter]
    hasMore = qs.count() > itemCounter

    context = {
        'authors': visible_qs,
        'itemCounter': itemCounter,
        'batchSize': batchSize,
        'hasMore': hasMore,
    }
    return render(request, 'quotes/components/author_list/author_cards.html', context)
