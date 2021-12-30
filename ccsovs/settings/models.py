from django.conf import settings
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

class Program(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, unique=True)
    program = models.ForeignKey(
            Program,
            on_delete=models.DO_NOTHING
        )

    def __str__(self):
        return self.name

class Student(models.Model):
    student_no = models.CharField(max_length=50, unique=True)
    firstname = models.CharField(max_length=50, unique=False)
    lastname = models.CharField(max_length=50, unique=False)
    middlename = models.CharField(max_length=50, unique=False)
    email = models.EmailField(unique=True)
    # profile = models.ImageField(upload_to='profile_image/',blank=True,null=True,verbose_name="profile")
    course = models.ForeignKey(
            Course,
            on_delete=DO_NOTHING
        )

    def __str__(self):
        return self.lastname + ',' + self.firstname + ' ' + self.middlename


@receiver(post_save, sender=Student)
def send_registration_link(sender,instance,created,**kwargs):
    if created:
        email = instance.email
        id = instance.pk
        send_email_registration(email,id)

class StudentAccount(models.Model):
    student = models.OneToOneField(
            Student,
            on_delete=models.DO_NOTHING
        )
    account = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            on_delete=models.DO_NOTHING,
        )


def send_email_registration(email, id):
    if email != 'None':
        subject = 'Online Voting Registration'
        message = 'Registration Link = ' + settings.HOST + '/register/?sid=' + str(id)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        print('Sending email for registration')

        send_mail(subject, message, email_from, recipient_list)