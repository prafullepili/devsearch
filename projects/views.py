from bs4 import Tag
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .utils import searchProjects, paginateProjects
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm



def projects(request):
    projects, search_query = searchProjects(request)
    custom_paginator, projects =  paginateProjects(request, projects,6)
    
    context = {'projects': projects, 'search_query':search_query, 'custom_paginator':custom_paginator}
    if request.user.is_authenticated:
        try:
            new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
            context['unreadCount'] = new_msg_count
        except:
            context['unreadCount'] = ""
    return render(request,'projects/projects.html',context)


def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    # add reviews
    if request.method == "POST":
        print(request.POST)
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj #which project person voting on.
        review.owner = request.user.profile #who did vote that person object
        review.save()

        projectObj.getVoteCount

        messages.success(request,'You review was successfully submitted!')
        return redirect('project',pk=projectObj.id)

    context = {'project':projectObj,'form':form}
    if request.user.is_authenticated:
        try:
            new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
            context['unreadCount'] = new_msg_count
        except:
            context['unreadCount'] = ""
        context = {'project':projectObj,'form':form, 'unreadCount':new_msg_count}
    return render(request,'projects/single-project.html',context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    
    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',',' ').split()
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile 
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request,f"Project '{project.title}' created successfully!")
            return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context = {'form':form, 'unreadCount':new_msg_count}
    return render(request,"projects/project_form.html", context)


@login_required(login_url='login')
def updateProject(request,pk):
    profile = request.user.profile
    try:
        project = profile.project_set.get(id=pk)
    except Project.DoesNotExist:
        return HttpResponse("<h3><code><em>You can't edit other project 😡</em></code></h3>")
    form = ProjectForm(instance=project)

    if request.method == "POST":
        newtags = request.POST.get('newtags').replace(',',' ').split()
        
        form = ProjectForm(request.POST,request.FILES,instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request,f"Project '{project.title}' updated successfully!")
            return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context = {'form':form, 'unreadCount':new_msg_count,'project':project}
    return render(request,"projects/project_form.html", context)


@login_required(login_url='login')
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        messages.success(request,f"Project '{project.title}' deleted successfully!")
        return redirect('account')
    try:
        new_msg_count = request.user.profile.messages.all().filter(is_read=False).count()
    except:
        new_msg_count = ""
    context = {'object':project, 'unreadCount':new_msg_count}
    return render(request, 'delete.html',context)     
