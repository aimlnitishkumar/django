from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('employees', views.EmployeeViewSet, basename='employee')



urlpatterns = [
    path('students/', views.studentView),
    path('students/<int:pk>/', views.studentDetailView),

    # path('employees/', views.Employees.as_view()),
    # path('employees/<int:pk>/', views.EmployeeDetail.as_view()),


    path('', include(router.urls))


]