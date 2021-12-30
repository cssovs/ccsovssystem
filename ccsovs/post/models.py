from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.contrib.auth.models import User
from tinymce import models as tinymce_models

class Announcement(models.Model):
    title = models.CharField(max_length=100, unique=True)
    videofile= models.FileField(upload_to='videos/', null=True,blank=True, verbose_name="Video")
    content = tinymce_models.HTMLField()
    banner = models.ImageField(upload_to='images/',blank=True,null=True,verbose_name="Image")
    created_by = models.ForeignKey(User, on_delete=DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title