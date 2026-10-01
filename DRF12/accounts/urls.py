from django.urls import path
from . import views

urlpatterns = [
    path('page/', views.account_page, name='account-page'),
    path(
        '',
        views.AccountViewSet.as_view({
            'get': 'list',
            'post': 'create'
        })
    ),

    path(
        '<int:account_number>/',
        views.AccountViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy'
        })
    ),
]