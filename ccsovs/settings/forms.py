from django import forms
from .models import Course, Program, Student
 
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name','description','program')

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ('name','description')
        
# class PartyForm(forms.ModelForm):
#     class Meta:
#         model = Party
#         fields = ('name','description','member')

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('student_no', 'lastname', 'firstname', 'middlename','email','course')

class UploadForm(forms.Form):
    file = forms.FileField()