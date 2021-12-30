from django.db import transaction
from post.models import Announcement
from party.models import Party
from election.models import Candidate, Election, Position, Vote
from settings.models import Student, StudentAccount
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import datetime

#get user party for leader
def get_user_leader_party(user):
    student = StudentAccount.objects.get(account__pk=user.id).student
    return Party.objects.get(leader=student)
    
# method to see if the user is a party leader
# if party leader - then check if the party has elected an officer for the
# current election period.
def party_leader_task(user):
    # check if there is an ongoing election for this year
    today = datetime.datetime.now()
    try:
        election = Election.objects.get(created_at__year=today.year)
        pos = election.position
        # check if student login is a party leader
        try:
            party = get_user_leader_party(user)     
            if party is not None:
                #check if the party has elected an officer already
                candidates = Candidate.objects.filter(election=election,party=party)
                if len(candidates) > 0:
                    return 'Your party has elected ' + str(len(candidates)) + '/' + str(pos.all().count()) + ' candidate(s)'
                else:                          
                    # return 'Election ' + str(election.created_at.year) + ' has started. Please Nominate ' + str(pos.all().count()) + ' position(s)'
                    return 'Nomination has started for election ' + str(election.created_at.year) + '.<br/> Please nominate ' + str(pos.all().count()) + ' position(s) if you have not done so.'
        except Party.DoesNotExist and Student.DoesNotExist and Party.DoesNotExist:
            pass
    except Election.DoesNotExist:
        return 'No Upcomming Election'

    return None

# method to elect official
@transaction.atomic
def elect_official(request,election,positions,party):
    for position in positions.iterator():
        selected_official = str(request.POST.get(str(position.pk)))
        if not(not selected_official.strip()):
            student = Student.objects.get(pk=selected_official)
            Candidate.objects.create(student=student,election=election,position=position,party=party)

# Notification to vote
def user_vote_notification(request):
    user= request.user
    student_user = StudentAccount.objects.get(account__pk=user.id).student

    # check if there is an ongoing election for this year
    today = datetime.datetime.now()
    current = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    try:
        election = Election.objects.get(created_at__year=today.year)
        efrom = str(election.vote_period_from.strftime("%m/%d/%Y, %H:%M:%S"))
        eto = str(election.vote_period_to.strftime("%m/%d/%Y, %H:%M:%S"))

        # check if already voted
        vote = Vote.objects.filter(election=election,voter=student_user)
        if election.vote_period_from.strftime("%m/%d/%Y, %H:%M:%S") <= current <= election.vote_period_to.strftime("%m/%d/%Y, %H:%M:%S"):
            if len(vote) > 0:
                return 'You vote has been casted for election <strong>' + str(election) + '</strong>'
            else:
                return 'Voting is on going and will end on <strong>' + eto + '</strong><br/><br/><a class="btn btn-primary" href="/vote" role="button">Vote Now</a>'
        else:
            if election.vote_period_from.strftime("%m/%d/%Y, %H:%M:%S") <= current >= election.vote_period_to.strftime("%m/%d/%Y, %H:%M:%S"):
                return 'Election ' + str(election) + ' has ended. Here is the <a href="/elected?eid='+str(election.id)+'">list of elected officials</a>'
            else: 
                return 'Voting period starts from ' + efrom + ' until ' + eto                
    except Election.DoesNotExist:
        return 'No Upcomming Election'

# method to count vote
@transaction.atomic
def count_vote(request,election,positions):
    user= request.user
    voter = StudentAccount.objects.get(account__pk=user.id).student

    for position in positions.iterator():
        candidate_voted = request.POST.get(str(position.name))
        if candidate_voted is not None:
            voted = Student.objects.get(pk=candidate_voted)
            Vote.objects.create(vote_for=voted,election=election,position=position,voter=voter)

# display newsfeed
def fetch_newsfeed(request):
    announcment_list = Announcement.objects.all().order_by('-updated_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(announcment_list, 5)

    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)

# fetch candidate info
def fetch_candidate_info(candidate_id,election_id,party_id):
    student = Student.objects.get(id=candidate_id)
    election = Election.objects.get(id=election_id)
    party = Party.objects.get(id=party_id)
    
    candidate = Candidate.objects.get(election=election,party=party,student=student)
    return candidate

