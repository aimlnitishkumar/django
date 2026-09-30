from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, BookViewSet, MemberViewSet, LibraryViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='api-books')
router.register(r'members', MemberViewSet, basename='api-members')
router.register(r'operations', LibraryViewSet, basename='api-operations')

urlpatterns = [
    # Frontend Template Route
    path('', home, name='home'),

    # REST Framework API Routes
    path('api/', include(router.urls)),
]