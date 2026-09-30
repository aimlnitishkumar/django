from django.contrib import admin
from .models import Department, Employee

class EmployeeAdmin(admin.ModelAdmin): # this is for make admin pannel editable and view proper, using this the admin override over model that is created by django

    list_display = ['id','full_name', 'email', 'designation', 'salary', 'joining_date','manager','is_active']
    list_filter = ['manager']
    search_fields = ['full_name', 'email']
    list_editable = ['is_active']
    list_display_links = ['full_name', 'email']
    ordering = ['id']

# Register your models here.
admin.site.register(Department)
admin.site.register(Employee, EmployeeAdmin)