from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView   
# Create your views here.

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(status=True).order_by('-published')