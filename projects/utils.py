from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


from .models import Project,Tag

# utils to reduce the code view in views.py

# search projects
def searchProjects(request):
    '''Search by Project or Name or Tag'''

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
    
    # get tag that container search_query
    tag = Tag.objects.filter(name__icontains = search_query)
        
    # avoid duplicating instance tabel value using distinct
    projects = Project.objects.distinct().filter(
        Q(title__icontains = search_query) |
        # query in parent child (search by user name)
        Q(owner__name__icontains = search_query) |
        Q(tags__in = tag)
    )

    return projects ,search_query



# paginate projects
def paginateProjects(request ,projects ,results):
    # create paginator
    # on 1 page give 2 results
    page = request.GET.get('page')

    # paginate the results for project
    paginator = Paginator(projects ,results)

    # what page to get ?
    try : 
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages # get the number of pages
        projects = paginator.page(page) # display the last page

    leftIndex = (int(page) - 4)

    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)

    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects