from django.contrib import admin
from party.models import Party
from settings.models import StudentAccount
from election.forms import CandidateForm, ElectionForm, PositionForm
import datetime
from election.models import Candidate, Election, Position, Vote
    
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('vote_for','election','position','voter')

@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ('created_at','vote_period_from','vote_period_to')
    list_filter = ['position', ]
    filter_horizontal = ['position', ]
    form = ElectionForm

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    form = PositionForm

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('student','election','position','party')
    form = CandidateForm
       
        
    def get_queryset(self, request):
        qs = super(CandidateAdmin, self).get_queryset(request)
        user =  request.user
        student = StudentAccount.objects.get(account__pk=user.id).student
        party = Party.objects.get(leader=student)
        return qs.filter(party=party)

    def get_form(self, request, *args, **kwargs):
        form = super(CandidateAdmin, self).get_form(request, **kwargs)
        form.current_user = request.user
        return form

    def has_module_permission(self, request):
        today = datetime.datetime.now()
        try:
            election = Election.objects.get(created_at__year=today.year)
            is_not_super = request.user.is_superuser
            has_election_ongoing = election is not None
            return not is_not_super and has_election_ongoing
        except Election.DoesNotExist:
            return False
