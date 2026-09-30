from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from blog.models import Article
from .serializers import ArticleSerializer
# Create your views here.

class ArticleListAPIView(ListAPIView):
    queryset = Article.objects.filter(status=True).order_by('-published')
    serializer_class = ArticleSerializer