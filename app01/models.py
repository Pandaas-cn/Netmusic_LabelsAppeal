from django.db import models

# Create your models here.

class info(models.Model):
    musiclink = models.CharField(max_length=50,blank=True)
    system_label = models.CharField(max_length=10,blank=True)
    user_label = models.CharField(max_length=10,blank=True)
    userid = models.CharField(max_length=20,blank=True)
    username = models.CharField(max_length=20,blank=True)
    imgfile = models.CharField(max_length=50,blank=True)
    checklabel = models.CharField(max_length=5,blank=True)
    status = models.CharField(max_length=5,default='申诉提交')
    correct = models.CharField(max_length=8,default='')
    submit_time = models.DateField(auto_now_add=True)

class admins(models.Model):
    username = models.CharField(max_length=10,blank=True,unique=True)
    password = models.CharField(max_length=20,blank=True)