from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home ,name='home'),
    # path('elect/',views.elect_officials,name='elect'),
    path('login/', views.login_auth , name='login'),
    path('logout/', views.logout_auth , name='logout'),
    path('candidates/',views.candidates,name="candidates"),
    path('vote/',views.vote,name='vote'),
    path('vote/profile/',views.profile_view,name='profile'),
    path('viewpost/',views.view_post,name='viewpost'),
    path('elected/',views.elected,name='elected'),
    path('register/', views.register_student_account, name='registration'),
]