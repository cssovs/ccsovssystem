import openpyxl
from django.contrib import messages
from django.db import IntegrityError
from django.forms import forms
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from .forms import UploadForm
from .models import Course, Student


def iterate_save(list):
    counter = 0
    for i in range(len(list)):
        if i > 0:
            obj = list[i]
            try:
                course = Course.objects.get(name__iexact=obj[5])
                student = Student(student_no=obj[0], lastname=obj[1], firstname=obj[2], middlename=obj[3], email=obj[4],course=course)
                student.save()
                counter+=1
            except IntegrityError as e:
                pass
    
    return counter
            
def upload_bulk(request):
    if request.method == 'GET':
        form = UploadForm()
        return render(request, 'admin/student/upload.html', {'uploadForm': form})
    else:
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # read excel file
            excel_file = form.cleaned_data.get('file')
            wb = openpyxl.load_workbook(excel_file)
            worksheet = wb["Sheet1"]

            excel_data = list()
            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                excel_data.append(row_data)

            total_inserted = iterate_save(excel_data)
            if total_inserted > 0:
                messages.add_message(request, messages.INFO, str(total_inserted) + ' Student(s) were saved!')
            else:
                messages.add_message(request, messages.WARNING, 'No student were saved. Please check the file and make sure that there is no duplicate')
        else:
            messages.add_message(request, messages.ERROR, 'Error in uploading file!Make sure you are uploading excel '
                                                          'file with proper values')
        return HttpResponseRedirect('/admin/settings/student')
