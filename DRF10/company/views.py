from django.shortcuts import render
from .models import Company
# Create your views here.
def home(request):
    companies = Company.objects.all()
    return render(request, 'company.html', {'companies': companies})