from django.db import models
from django.contrib.auth.models  import User,AbstractUser

class User(AbstractUser):
  name=models.CharField(max_length=200,null=True)
  email=models.EmailField(null=True,unique=True)
  bio=models.TextField(null=True)


  avatar=models.ImageField(null=True,default="avatar.svg") # depends on Pillow package need install pillow package
  USERNAME_FIELD='email'
  REQUIRED_FIELDS=[]





class Topic(models.Model):
  name=models.CharField(max_length=200)

  def __str__(self):
     return self.name

# Create your models here.
class Room(models.Model):
  host=models.ForeignKey(User,on_delete=models.SET_NULL,null=True) # get all users data in user variable
  topic=models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True) # get all topic data in user variable
  name=models.CharField(max_length=1000)
  description=models.TextField(null=True,blank=True) 
  participants=models.ManyToManyField(User,related_name='participants',blank=True)
  updated=models.DateTimeField(auto_now=True) #take every snapshot every time 
  created=models.DateTimeField(auto_now_add=True)  #take (initial time) time  of creation only  snapshot every time means created time only

  class Meta:
    ordering = ['-updated','-created']    #ordering = ['created','updated'] without "-" new one and updated one will appear last 

  def __str__(self):
    return self.name


class Message(models.Model):
  user=models.ForeignKey(User,on_delete=models.CASCADE)  # get all users data in user variable
  room=models.ForeignKey(Room,on_delete=models.CASCADE)# depends on Room models and if room is deleted automatically this one also deletes
  body=models.TextField()
  updated=models.DateTimeField(auto_now=True) #take every snapshot every time 
  created=models.DateTimeField(auto_now_add=True)  #take (initial time) time  of creation only  snapshot every time means created time only

  class Meta:
    ordering = ['-updated','-created']    #ordering = ['created','updated'] without "-" new one and updated one will appear last 

  def __str__(self):
     return self.body[0:50]