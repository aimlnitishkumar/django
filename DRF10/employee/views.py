from django.shortcuts import render

from .models import Employee

# Create your views here.

def home(request):
    employees = Employee.objects.all()
    return render(request, 'employee.html', {'employees': employees})