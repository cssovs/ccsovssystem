from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from settings.models import Student, StudentAccount
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib import messages

class Party(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=50, unique=True)
    leader = models.ForeignKey(
            Student,
            on_delete=DO_NOTHING
        )

    def __str__(self):
        return self.name

@receiver(pre_save, sender=Party)
def update_leader_access(sender,instance,**kwargs):
    if instance.id is None:
        update_staff_status(instance.leader,True)
    else:
        # update
        old = Party.objects.get(id=instance.id)
        update_staff_status(old.leader,False)
        update_staff_status(instance.leader,True)

@receiver(post_delete, sender=Party)
def delete_leader_access(sender,instance,**kwargs):
    update_staff_status(instance.leader,False)

@transaction.atomic
def update_staff_status(student,status):
    try:
        student=StudentAccount.objects.get(pk=student.pk)
        account = student.account
        account.is_staff = status

        # for announcement
        add_announcement = Permission.objects.get(name='Can add announcement')
        change_announcement = Permission.objects.get(name='Can change announcement')
        delete_announcement = Permission.objects.get(name='Can delete announcement')
        view_announcement = Permission.objects.get(name='Can view announcement')

        # for electing officials
        add_candidate = Permission.objects.get(name='Can add candidate')
        change_candidate = Permission.objects.get(name='Can change candidate')
        delete_candidate = Permission.objects.get(name='Can delete candidate')
        view_candidate = Permission.objects.get(name='Can view candidate')

        if status:
            account.user_permissions.add(add_announcement,change_announcement,delete_announcement,view_announcement,add_candidate,change_candidate,delete_candidate,view_candidate)
        else:
            account.user_permissions.remove(add_announcement,change_announcement,delete_announcement,view_announcement,add_candidate,change_candidate,delete_candidate,view_candidate)

        account.save()
    except StudentAccount.DoesNotExist:
        pass