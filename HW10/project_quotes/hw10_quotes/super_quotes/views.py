from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Quote, Author, Tag

from .forms import AuthorForm, QuoteForm, TagForm


def home(request, page=1):
    quotes = Quote.objects.all()
    per_page = 5
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_tags = Quote.objects.values('tags__name').annotate(quote_count=Count('tags__name')).order_by('-quote_count')[:10]
    return render(request, "super_quotes/index.html", context={"quotes": quotes_on_page, 'top_tags': top_tags})


def author_about(request, _id):
    author = Author.objects.get(pk=_id)
    return render(request, 'super_quotes/author.html', context={'author': author})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save()
            return redirect(to='super_quotes:home')
        else:
            return render(request, 'super_quotes/add_quote.html',
                          context={'form': QuoteForm, 'message': "Форма невірна"})
    return render(request, 'super_quotes/add_quote.html', context={'form': QuoteForm()})


@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save()
            return redirect(to='super_quotes:home')
        else:
            return render(request, 'super_quotes/add_author.html',
                          context={'form': AuthorForm, 'message': "Форма невірна"})
    return render(request, 'super_quotes/add_author.html', context={'form': AuthorForm()})


@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            new_tag = form.save()
            return redirect(to='super_quotes:home')
        else:
            return render(request, 'super_quotes/add_tag.html',
                          context={'form': TagForm, 'message': "Форма невірна"})
    return render(request, 'super_quotes/add_tag.html', context={'form': TagForm})


def find_tag(request, _id):
    per_page = 5
    quotes = Quote.objects.filter(tags=_id).all()
    paginator = Paginator(list(quotes), per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    tag_name = Tag.objects.filter(pk=_id).first().name
    top_tags = Quote.objects.values('tags__id', 'tags__name').annotate(quote_count=Count('tags__name')).order_by('-quote_count')[:10]

    return render(request, 'super_quotes/find_tag.html',
                  context={'quotes': page_obj, 'tag_name': tag_name, 'top_tags': top_tags})


def search_quotes(request):
    query = request.GET.get('q')
    quotes = Quote.objects.filter(
        Q(author__fullname__icontains=query)
        # Q(tags__name__icontains=query) |
        # Q(quote__quote__icontains=query)
    )
    return render(request, 'super_quotes/search_quotes.html', context={'quotes': quotes, 'query': query})
