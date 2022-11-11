import uuid
from django.db import models
from django.contrib.auth.models import User
# from django.forms import ValidationError
import os
from django.conf import settings



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.SET_NULL,null=True,blank=True)
    name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=400,blank=False,null=True)
    bio = models.TextField(blank=True,null=True)
    username = models.CharField(max_length=200,blank=True, null=True)
    location = models.CharField(max_length=200,blank=True, null=True)
    short_intro = models.CharField(max_length=200,blank=True,null=True)
    profile_image = models.ImageField(blank=True,null=True,upload_to='profiles/',default="profiles/user-default.png")
    social_github = models.CharField(max_length=200,blank=True, null=True)
    social_twitter = models.CharField(max_length=200,blank=True, null=True)
    social_linkedin = models.CharField(max_length=200,blank=True, null=True)
    social_youtube = models.CharField(max_length=200,blank=True, null=True)
    social_website = models.CharField(max_length=200,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']
    def __str__(self):
        return str(self.user.username)
    
    def userProfile(self):
        if self.profile_image:
            p = os.getcwd()+f"/{'static' if settings.DEBUG else 'staticfiles' }/{self.profile_image.url}"
            if os.path.isfile(p):
                return self.profile_image.url
            else:
                return f"/images/profiles/user-default.png"
        return f"/images/profiles/user-default.png"

    # def userProfile(self):
    #     try:
    #         url = self.profile_image.url
    #     except:
    #         url = ''
    #     return url

class Skill(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(max_length=300,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)

    def __str__(self):
        return str(self.name)

    

class Message(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile,on_delete=models.SET_NULL,null=True,blank=True,related_name="messages")
    sender_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False,null=True)
    msg_read = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True, editable=False)
    

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read','-created']