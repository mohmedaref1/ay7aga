from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/uploads/user_<id>/<filename>
    return 'uploads/user/{0}/{1}'.format(instance.user.pk, filename)

class Massages(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    replay = models.CharField(max_length=5000, blank=True, null=True)
    massages = models.CharField(max_length=5000,blank=True,null=True)
    time=models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=user_directory_path,blank=True,null=True)

    def __str__(self):
        return f"id of maseege is {self.pk} and the massage is {self.massages} sended at {self.time} "
