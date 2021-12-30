import logging
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect, render
from django.db import transaction

from settings.models import StudentAccount

from .forms import *
from .service import *

logger = logging.getLogger('django')

# home page
@login_required
def home(request):
    user_detail = {
        'party_leader_task' : party_leader_task(request.user),
        'vote_notification' : user_vote_notification(request) 
    }
    newsfeed = fetch_newsfeed(request)
    return render(request,'index.html', {'user_detail' : user_detail,'newsfeed': newsfeed})

## Login function
def login_auth(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, "login.html")
    else:
        return render(request, "login.html")

@login_required
def logout_auth(request):
    logout(request)
    return redirect('home')

# function to register student account
@transaction.atomic
def register_student_account(request):
    sid = request.GET.get('sid')
    student = Student.objects.get(pk=sid)

    if request.method == "POST":
        form = RegistrationForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                account = form.save(commit=False)
                account.set_password(account.password)
                account.is_staff = False
                account.is_superuser = False
                account.is_active = True
                account.save()

                # student.profile = request.FILES["profile"]
                # student.save() #update student

                #create student account
                StudentAccount.objects.create(student=student,account=account)

                messages.success(request, 'You have been registered.')
                return redirect('home')
            else:
                messages.error(request, 'Password did not match')
                return render(request, "registration.html", {'form': form})
    else:
        if request.method == 'GET':
            form = RegistrationForm(initial={'email': student.email, 'first_name': student.firstname, 'last_name': student.lastname,'username':student.email})
    return render(request, "registration.html", {'form': form})

@login_required
def candidates(request):
    today = datetime.datetime.now()
    election = Election.objects.get(created_at__year=today.year)
    party = get_user_leader_party(request.user)
    candidates = Candidate.objects.filter(party=party,election=election)
    return render(request,'candidates.html',{'candidates':candidates})

## Elect official page
@login_required
def elect_officials(request):
    #get current election
    today = datetime.datetime.now()
    election = Election.objects.get(created_at__year=today.year)

    #get current user's party
    party = get_user_leader_party(request.user)

    #get party members to elect (only party member should be elected)
    members = party.member.all()

    #election positions
    positions = election.position.all()

    if request.method == 'POST':
        elect_official(request,election,positions,party)
        return render(request,'elect.html', {'positions': positions ,'party' : party, 'members': members})
    else:
        return render(request,'elect.html', {'positions': positions ,'party' : party, 'members': members})

# actual voting
@login_required
def vote(request):
    #get current election
    today = datetime.datetime.now()
    election = Election.objects.get(created_at__year=today.year)

    if request.method == 'POST':
        print(request.POST)
        #election positions
        positions = election.position.all()
        count_vote(request,election,positions)
        return redirect('/')
    else:
        candidates = Candidate.objects.filter(election=election)
        return render(request,'vote.html',{'candidates':candidates})

# check profile
@login_required
def profile_view(request):
    candidate_id = request.GET.get('id')
    party_id = request.GET.get('pid')
    election_id = request.GET.get('eid')

    candidate_detail = fetch_candidate_info(candidate_id,election_id,party_id)
    context = {
        'detail' : candidate_detail
    }
    
    return render(request,'profile.html',context)

# view election winners
@login_required
def elected(request):

    class StudentVoteInfo:
        def __init__(self,student,vote_count):
            self.student = student
            self.vote_count = vote_count

    eid = request.GET.get('eid')
    election = Election.objects.get(id=eid)
    
    tally_with_position = {}

    # get all positions from this election
    positions = election.position
    
    for position in positions.iterator():
        # get all candidates from this position
        candidates = Candidate.objects.filter(election=election,position=position)
        tally = []
        #get votes from each candidates
        for candidate in candidates.iterator():
            student_candidate = candidate.student
            votes = Vote.objects.filter(election=election,vote_for=student_candidate).count()

            # tally[student_candidate] = votes
            tally.append(StudentVoteInfo(student_candidate,votes))
            tally_with_position[position] = tally

    context = {
        "total" : tally_with_position,
        "election" : election
    }
    
    return render(request,'elected.html',context)

# view post
@login_required
def view_post(request):
    sid = request.GET.get('pid')
    post = Announcement.objects.get(pk=sid)
    context = {
        'post':post
    }
    return render(request,'post.html',context)