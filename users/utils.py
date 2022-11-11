from django.db.models import Q
from .models import Profile,Skill
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

from devsearch import settings

def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles,results)
    
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(int(page))

    # range paginator
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1 
    
    rightIndex = (int(page) + 2)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_paginator = range(leftIndex,rightIndex)


    return custom_paginator, profiles, 


def searchProfiles(request):
    search_query = ""
    if request.GET.get('search_query'):
        search_query = str(request.GET.get('search_query')).strip(' ')
    
    skills = Skill.objects.filter(name__icontains=search_query)
    
    if settings.mongoDB:
        profiles = Profile.objects.filter(
            Q(name__icontains=search_query) |
            Q(short_intro__icontains=search_query) |
            Q(social_github__icontains=search_query) 
        )
    else:
        profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(short_intro__icontains=search_query) |
        Q(skill__in=skills)
        )
    return profiles, search_query