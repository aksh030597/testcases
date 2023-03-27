from django.contrib import admin

# Register your models here.

from .models import Student, Marks



admin.site.register(Student)
admin.site.register(Marks)


