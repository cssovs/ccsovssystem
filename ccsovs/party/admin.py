from django.contrib import admin
from .forms import PartyForm

from .models import Party

# @admin.register(PartyLeader)
# class PartyLeaderAdmin(admin.ModelAdmin):
#     list_display = ('party','leader')

# @admin.register(StudentAccount)
# class StudentAccountAdmin(admin.ModelAdmin):
#     list_display = ('student','account')


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('name','leader')
    list_filter = ['leader']
    # filter_horizontal = ['leader', ]
    form = PartyForm
