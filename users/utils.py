from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

from .forms import CustomUserCreationForm,ProfileForm,SkillForm
from . import models

# user defined file to filter the main code

# paginate projects
def paginateProfile(request ,profiles ,results):
    # create paginator
    # on 1 page give 2 results
    page = request.GET.get('page')


    # paginate the results for project
    paginator = Paginator(profiles ,results)

    # what page to get ?
    try : 
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages # get the number of pages
        profiles = paginator.page(page) # display the last page

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex) 

    return profiles,custom_range


# search query
def searchProfile(request):
    '''Search by name or short intro or skills'''
    search_query = ''

    # get search_query from form input data
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    ''' 
    models_fields__icontains ( __icontains tells not be case sensitive)
     __contains (case sensitve)
    '''
    # get by skills
    skills = models.Skill.objects.filter(name__icontains=search_query)

    # send back the search_query with results
    '''add distinct to avoid duplication of instance tabel'''
    profiles = models.Profile.objects.distinct().filter(
        Q(name__icontains = search_query) |
        Q(short_intro__icontains = search_query) |
        # skill__in = skills allow to search in child model
        # profile have skill in skills models.name
        Q(skill__in = skills)
        )
    
    return profiles ,search_query