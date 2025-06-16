from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import Quote, Author, QuoteSubmission
from .forms import AuthorForm, QuoteSubmissionForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import random, datetime
from django.views import generic

# Create your views here.

def homepage(request):
    return render(request, 'homepage.html', {'user': request.user})

def daily_page(request):
    def get_daily_seed(today):
        seed = 0
        for i in str(today):
            if i.isdigit():
                seed += int(i)
        return seed
    
    num_vis = request.session.get('num_vis', 0)
    num_vis += 1
    request.session['num_vis'] = num_vis
    context = {}
    quote = None
    today = datetime.date.today()
    all_quotes = list(Quote.objects.all())
    if all_quotes:
        seed = get_daily_seed(today) % len(all_quotes)
        quote = all_quotes[seed]
    context['number_of_visits'] = num_vis
    context['quote'] = quote
    context['day'] = today.strftime('%d')
    context['weekday'] = today.strftime('%A')
    context['month'] = today.strftime('%B')
    context['year'] = today.strftime('%Y')
    template = 'quotes/daily_page.html'
    return render(request, template, context)

def quoteListView(request):
    trigger = request.headers.get('hx-trigger')
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
    sort = request.GET.get('sort_value', 'id')
    quotes = quotes.order_by(sort)
    
    batchSize = int(request.GET.get('batchsize', 5))
    page_number = int(request.GET.get('page', 1))
    # ", batchSize)" because on first page load, page_count input doesn't exist.
    page_count = int(request.GET.get('page_count', batchSize)) if page_number == 1 else batchSize
    paginator = Paginator(quotes, page_count)
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

    if trigger == 'list-container':
        # For initial load, return the complete list with search bar
        return render(request, 'quotes/components/quote_list/quote_list.html', context)
    else:
        # For pagination requests and searches, return just the quote items as HTML fragments
        return render(request, 'quotes/components/quote_list/component_updater.html', context)
    
class QuoteDetailPartial(generic.DetailView):
    model = Quote
    template_name = 'quotes/components/quote_detail/quote_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_author"] = self.request.GET.get('show_author') == '1'
        return context
    
class AuthorDetail(generic.DetailView):
    model = Author


class BrowseList(generic.ListView):
    model = Quote
    template_name = 'quotes/browse_list.html' # Default is <app name>/<model name>_list.html ('polls/question_list.html')
    context_object_name = 'browse_quote_list'

# /////////////

""" class QuoteSubmissionCreateView(LoginRequiredMixin, generic.CreateView):
    model = QuoteSubmission
    form_class = QuoteSubmissionForm
    template_name = 'quotes/submit_quote.html'
    success_url = '/thanks/'

    def form_valid(self, form):
        form.instance.submitted_by = self.request.user
        return super().form_valid(form) """

def submitQuote(request):
    if request.method == 'POST':
        form = QuoteSubmissionForm(request.POST)
        if form.is_valid():
            # instance = form.save(commit=False)
            # instance.submitted_by = request.user
            # instance.save()
            form.save(request.user)
            return redirect('quotes:submit_success')
    else:
        form = QuoteSubmissionForm()
    authorList = Author.objects.all().order_by('name')
    return render(request, 'quotes/submit_quote.html', {'form': form, 'authors': authorList})

def submitQuoteSuccess(request):
    return render(request, 'quotes/submit_success.html')


@login_required
@require_POST
def toggle_like(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)

    if request.user in quote.likes.all():
        quote.likes.remove(request.user)
        liked = False
    else:
        quote.likes.add(request.user)
        liked = True
    
    # if request.htmx:
    return render(request, 'quotes/components/quote_detail/like_button.html', {'quote': quote, 'liked': liked})
    
    # return redirect('quote_detail', pk=quote_id)


# /////////////

class AuthorListView(generic.ListView):
    model = Author

class AuthorCreateView(generic.CreateView):
    # model = Author
    # fields = ["name"]
    form_class = AuthorForm
    template_name = 'quotes/author_form.html'
    success_url = reverse_lazy('browse')

def AuthorUpdateViewFunc(request, pk):
    # 1️⃣ Look up the Author instance or return 404
    author = get_object_or_404(Author, pk=pk)
    if request.method == 'POST':
        # 2️⃣ Bind POST data *and* the instance to the form
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            # 3️⃣ Redirect to your browse page (use the correct URL name)
            return redirect('quotes:browse')
    else:
        # 4️⃣ For GET, instantiate the form with the existing instance
        form = AuthorForm(instance=author)
    # 5️⃣ Render the same template for both GET and invalid POST
    return render(request, 'quotes/author_form.html', {'form': form})

class AuthorDeleteView(generic.DeleteView):
    model = Author
    success_url = reverse_lazy("author-list")
    

class QuoteCreateView(generic.CreateView):
    model = Quote
    fields = ["sentence"]

class QuoteUpdateView(generic.UpdateView):
    model = Quote
    fields = ["sentence"]

class QuoteDeleteView(generic.DeleteView):
    model = Quote
    success_url = reverse_lazy("quote-list")




