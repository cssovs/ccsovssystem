from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html

from .forms import *
from .models import *


@admin.register(Program)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    form = ProgramForm

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    form = CourseForm
    
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('pk','student_no', 'lastname', 'firstname','email')
    form = StudentForm
    change_list_template = "admin/student/change_list.html"

# @admin.register(StudentAccount)
# class StudentAccountAdmin(admin.ModelAdmin):
#     list_display = ('pk','student','account')
