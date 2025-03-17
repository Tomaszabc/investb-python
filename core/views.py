from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
import logging
logger = logging.getLogger(__name__)


def index(request):
    articles = Article.objects.all().order_by('-created_at')  # Pobranie wszystkich artykułów
    return render(request, 'core/index.html', {'articles': articles})

def new_article(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ArticleForm()
    return render(request, 'core/new_article.html', {'form': form})

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Pobierz artykuł do edycji
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)  # Wypełnij formularz danymi artykułu
        if form.is_valid():
            form.save()  # Zapisz zmiany
            return redirect('index')  # Przekieruj na stronę główną
    else:
        form = ArticleForm(instance=article)  # Wypełnij formularz danymi artykułu
    return render(request, 'core/edit_article.html', {'form': form, 'article': article})


def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Pobierz artykuł na podstawie ID
    return render(request, 'core/article_detail.html', {'article': article})
