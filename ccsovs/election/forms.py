from django import forms
from django.forms.widgets import HiddenInput
from party.models import Party
from settings.models import Student, StudentAccount
from election.models import Candidate, Election, Position
import datetime

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ('vote_period_from','vote_period_to','position')

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('name','description')

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ('student','position','image','profile','election','party')
    
    def clean_election(self):
        return self.current_election();

    def clean_party(self):
        return self.get_party()

    def __init__(self,*args, **kwargs):
        instance = kwargs.get('instance', None)
        
        super(CandidateForm, self).__init__(*args, **kwargs)

        self.fields['election'].initial= self.current_election()
        self.fields['election'].widget = HiddenInput()
        
        self.fields['party'].initial= self.get_party()
        self.fields['party'].widget = HiddenInput()

        self.fields['student'].queryset=self.eligable_student_to_elect()
        self.fields['position'].queryset=self.position_available()
        
        
        if instance is not None:
            # edit mode
            self.fields['student'].empty_label = instance.student
            self.fields['position'].empty_label = instance.position
        else:
            pass
        
    def eligable_student_to_elect(self):
        candidates = Candidate.objects.filter(election=self.current_election()).values_list('student__id',flat=True)
        return Student.objects.exclude(id__in=candidates)

    def position_available(self):
        party = self.get_party()
        positions = Candidate.objects.filter(election=self.current_election(),party=party).values_list('position__id',flat=True)
        return Position.objects.exclude(id__in=positions)

    def get_party(self):
        user = self.current_user
        student = StudentAccount.objects.get(account__pk=user.id).student
        return Party.objects.get(leader=student)
    
    def current_election(self):
        today = datetime.datetime.now()
        e = Election.objects.get(created_at__year=today.year)
        return e
    