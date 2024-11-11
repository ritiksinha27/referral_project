from django.db import models
from django.contrib.auth.models import AbstractUser# Create your models here.
from .manager import CustomUserManager
class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.EmailField(max_length=255, unique=True)
    mobile_no= models.CharField(max_length=255, unique=True)
    password= models.CharField(max_length=255)
    unique_id= models.CharField(max_length=255, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    objects= CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile_no',  'first_name', 'last_name', 'password']
    
    def __str__(self) -> str:
        return self.username
    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id =  self.mobile_no+'YEP'
        super().save(*args, **kwargs)
class UserStructure(models.Model):
    user_id= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ref_by_user_id= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='ref_by_user_id', blank=True, null=True)
    points= models.IntegerField(default=0)
    child_branch=models.ManyToManyField(CustomUser, related_name='child_branch', blank=True)

    def __str__(self) -> str:
        return self.user_id.username
    @property
    def child_count(self):
        return self.child_branch.count()
