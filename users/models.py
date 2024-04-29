from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


# Profile
class Profile(models.Model):
    # user per profile (one user - one profile)
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    name = models.CharField(max_length=200 ,null=True ,blank=True)
    email = models.EmailField(max_length=100 ,null=True ,blank=True)
    username = models.CharField(max_length=200 ,null=True ,blank=True)
    short_intro = models.CharField(max_length=200 ,null=True ,blank=True)
    location = models.CharField(max_length=200 ,null=True ,blank=True)
    bio = models.TextField(null=True ,blank=True)
    profile_image = models.ImageField(blank=True ,null=True ,
                                      upload_to='profiles/' ,
                                      default='profiles/user-default.png')
    social_github = models.CharField(max_length=200 ,null=True ,blank=True)
    social_instagram = models.CharField(max_length=200 ,null=True ,blank=True)
    social_linkedin = models.CharField(max_length=200 ,null=True ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 ,unique=True ,primary_key=True ,
                          editable=False)
    
    def __str__(self):
        return self.username
    

# Skill
class Skill(models.Model):
    # one-many (one profile can have multiple skills)
    owner = models.ForeignKey(Profile ,null=True ,blank=True 
                              ,on_delete=models.CASCADE)
    name = models.CharField(max_length=200 ,null=True ,blank=True)
    description = models.TextField(null=True ,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4 ,unique=True ,primary_key=True 
                          ,editable=False)
    
    def __str__(self):
        return self.name


# Message
class Message(models.Model):
    # '''Send and Receive messages'''
    sender = models.ForeignKey(Profile ,on_delete=models.SET_NULL ,null=True ,blank=True)
    # 'related_name' connect with profile model 
    # rather than typing the submodel query (profile.message_set.all) we can type directly 'messages'
    recipient = models.ForeignKey(Profile ,on_delete=models.SET_NULL ,null=True ,blank=True 
                                  ,related_name='messages')
    name = models.CharField(max_length=200 ,null=True ,blank=True)
    email = models.EmailField(max_length=200 ,null=True ,blank=True)
    subject = models.CharField(max_length=200 ,null=True ,blank=True)
    body = models.TextField(null=True ,blank=True)
    is_read = models.BooleanField(default=False ,null=True)
    created_at = models.DateTimeField(auto_now_add=True )
    id = models.UUIDField(default=uuid.uuid4 ,unique=True 
                              ,primary_key=True ,editable=False)
    
    class Meta:
        # '''Sort message by unread order'''
        ordering = ['is_read' ,'-created_at']
    
    def __str__(self):
        return self.subject
    