from django.http import QueryDict
from .models import Project,Tag
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from devsearch import settings

def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects,results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # range paginator
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1 
    
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_paginator = range(leftIndex,rightIndex)


    return custom_paginator, projects, 

def searchProjects(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = str(request.GET.get('search_query')).strip(' ')
    
    tags = Tag.objects.filter(name__icontains=search_query)
    if settings.mongoDB:
        projects = Project.objects.filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) 
        )
    else:
        projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(owner__name__icontains=search_query) |
        Q(tags__in=tags)
        )
    return projects, search_query