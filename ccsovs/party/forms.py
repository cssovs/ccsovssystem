from django import forms
from .models import *

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ('name','description','leader')