from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone

from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .models import Message, Profile
from .utils import searchProfiles, paginateProfiles

LOGIN_URL = 'login'
NEW_MSG_COUNT = None

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account' )
        else:
            messages.error(request,'Username or Password is incorrect')
    return render(request,'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,"User was logged out!")
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method=="POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"User account was created!")
            login(request,user)
            return redirect('edit-account')
        else:
            messages.error(request,'An error has occured during registration')
    context={'page':page,'form':form}
    return render(request, 'users/login_register.html',context )


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_paginator, profiles = paginateProfiles(request,profiles,6)
    context = {"profiles":profiles, "search_query":search_query, 'custom_paginator':custom_paginator}

    if request.user.is_authenticated:
        try:
            new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
            context['unreadCount'] = new_msg_count
        except:
            context['unreadCount'] = ""
    return render(request,'users/profiles.html',context)


def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = Profile.objects.get(id=pk).skill_set.filter(description="")
    context= {'profile':profile, 'topSkills':topSkills, 'otherSkills':otherSkills}

    if request.user.is_authenticated:
        try:
            new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
            context['unreadCount'] = new_msg_count
        except:
            context['unreadCount'] = ""
    return render(request,'users/user-profile.html',context)



@login_required(login_url=LOGIN_URL)
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all()
    projects = profile.project_set.all()
    context={'profile':profile,'skills':skills,'projects':projects}
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
        context['unreadCount'] = new_msg_count
    except:
        context['unreadCount'] = ""
    return render(request,'users/account.html',context)


@login_required(login_url=LOGIN_URL)
def editAccout(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context={'form':form,'unreadCount':new_msg_count}
    return render(request, 'users/profile_form.html',context)


@login_required(login_url=LOGIN_URL)
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill was added successfully!")
            return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context = {'form':form,'unreadCount':new_msg_count}
    return render(request,'users/skill_form.html',context)


@login_required(login_url=LOGIN_URL)
def updateSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    form = SkillForm(instance=skill)
    
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill was updated!")
            return redirect('account')
    context = {'form':form, 'unreadCount':new_msg_count}
    return render(request,'users/skill_form.html',context)


@login_required(login_url=LOGIN_URL)
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    
    if request.method == "POST":
        skill.delete()
        messages.success(request,'Skill was deleted successfully')
        return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context = {'object':skill, 'unreadCount':new_msg_count}
    return render(request,'delete.html',context)

from django.db.models import Q
@login_required(login_url=LOGIN_URL)
def inbox(request):
    profile = request.user.profile
    # userMessages = profile.messages.all()
    # userMessages = Message.objects.filter(Q(sender=request.user.profile) | Q(recipient=request.user.profile))
    userMessages = Message.objects.filter(Q(recipient=request.user.profile))
    try:
        unreadCount = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        unreadCount = ""
    context = {'userMessages':userMessages,'unreadCount':unreadCount}
    return render(request, "users/inbox.html",context)



# messages functions

@login_required(login_url=LOGIN_URL)
def viewMessage(request,pk):
    profile = request.user.profile
    message = Message.objects.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.msg_read = timezone.now()
        message.save()
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context={'message':message,'unreadCount':new_msg_count}
    return render(request,'users/message.html',context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()
    try:
        sender = request.user.profile
    except:
        sender = None
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.sender_name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "You message was successfully sent!")
            return redirect('user-profile',pk=recipient.id)
    context = {'recipient':recipient, 'form':form}
    if request.user.is_authenticated:
        try:
            new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
        except:
            new_msg_count = ""        
        
        context = {'recipient':recipient, 'form':form,'unreadCount':new_msg_count}
    return render(request,'users/message_form.html',context)