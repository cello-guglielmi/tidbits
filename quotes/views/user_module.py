from django.shortcuts import render, redirect, get_object_or_404
from quotes.models import Quote, Author, QuoteSubmission
from quotes.forms import QuoteSubmissionForm
from accounts.decorators import active_login_required
from django.views.decorators.http import require_POST

# Create your views here.

@active_login_required
def toggle_like(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    if request.user in quote.likes.all():
        quote.likes.remove(request.user)
    else:
        quote.likes.add(request.user)
    return render(request, 'quotes/user_module/components/like_button.html', {'quote': quote})

@active_login_required
@require_POST
def toggle_bookmark(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    if request.user in quote.bookmarked_by.all():
        quote.bookmarked_by.remove(request.user)
    else:
        quote.bookmarked_by.add(request.user)
    return render(request, 'quotes/user_module/components/bookmark_button.html', {'quote': quote})

@active_login_required
def submitQuote(request):
    if request.method == 'POST':
        form = QuoteSubmissionForm(request.POST)
        if form.is_valid():
            # instance = form.save(commit=False)
            # instance.submitted_by = request.user
            # instance.save()
            form.save(request.user)
            return redirect('quotes:user:submit_success')
    else:
        form = QuoteSubmissionForm()
    authorList = Author.objects.all().order_by('name')
    return render(request, 'quotes/user_module/submissions/submit_quote.html', {'form': form, 'authors': authorList})

@active_login_required
def submitQuoteSuccess(request):
    return render(request, 'quotes/user_module/submissions/submit_success.html')


@active_login_required
def myBookmarks(request):
    return render(request, 'quotes/user_module/user_bookmarks.html', {'user': request.user})

@active_login_required
def myEntries(request):
    return render(request, 'quotes/user_module/user_entries.html', {'user': request.user})

@active_login_required
def submissionList(request):
    user_subs = request.user.quote_submissions
    list_type = request.GET.get('list_type')
    print('TPYE IS:', list_type)
    qs = user_subs.filter(status='pending') if list_type == 'pending' else user_subs.exclude(status='pending')
    context = {
        'list_type': list_type,
        'submission_list': qs,
    }
    return render(request, 'quotes/user_module/submissions/submission_list.html', context)

@active_login_required
def submissionCards(request):
    user_subs = request.user.quote_submissions
    list_type = request.GET.get('list_type')
    qs = user_subs.filter(status='pending') if list_type == 'pending' else user_subs.exclude(status='pending')

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
        'past_quote_subs': visible_qs,
        'itemCounter': itemCounter,
        'batchSize': batchSize,
        'hasMore': hasMore,
    }
    return render(request, 'quotes/user_module/submissions/components/submission_cards.html', context)
