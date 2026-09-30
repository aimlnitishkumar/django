from django.urls import path
from .views import ArticleListAPIView

app_name = 'blog'
urlpatterns = [ 
    path('', ArticleListAPIView.as_view(), name='article-list'),
]