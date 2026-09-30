from django.shortcuts import render
from django.http import HttpResponse

from .models import user_detail
# Create your views here.


def home(request):
    users = user_detail.objects.all()  # Fetch all user details from the database
    return render(request, 'home.html', {'users': users})   