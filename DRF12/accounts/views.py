from django.shortcuts import render
from rest_framework import viewsets
from .models import Account
from .serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    lookup_field = 'account_number'

def account_page(request):
    return render(request, 'accounts/account.html')