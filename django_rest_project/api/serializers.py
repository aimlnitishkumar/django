from rest_framework import searializers
from students.models import Student


class StudentSerializer(searializers.ModelSerializer):
    class Meta:
        model = Student 
        fields = "__all__"