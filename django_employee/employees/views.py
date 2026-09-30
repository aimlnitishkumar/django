from django.shortcuts import render, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def employee_detail(request, id):
    employee = get_object_or_404(Employee, id = id)
    
    context = {
       "employee": employee
    }
    return render(request, 'employee_detail.html', context)

@login_required
def add_employee(request):
   if request.method == 'POST':
      form = EmployeeForm(request.POST, request.FILES)
      if form.is_valid():
         form.save()
      else:
         print(form.errors)
   form = EmployeeForm
   context = {
      'form': form,
   }
   return render(request, 'add_employee.html', context)