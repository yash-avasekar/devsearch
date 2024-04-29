from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .models import Project,Tag
from .forms import ProjectForm,ReviewForm
from .utils import searchProjects,paginateProjects

# Create your views here.


# All projects view
def projects(request):
    # get searchProjects
    projects ,search_query = searchProjects(request)
    custom_range ,projects  = paginateProjects(request ,projects ,9)

    context = {
        'projects' : projects,
        'search_query':search_query,
        'custom_range':custom_range,
    }
    return render(request ,'projects/projects.html' ,context=context)


# particaluar project view
def project(request ,pk):
    projectobj = Project.objects.get(id = pk)
    form = ReviewForm()

    if request.POST:
        form = ReviewForm(request.POST)
        if form.is_valid():
            # set current user for the review 
            review =  form.save(commit=False)
            review.project = projectobj # get current project
            # project owner
            review.owner = request.user.profile # set current user
            review.save()

            projectobj.getVoteCount # attribute from model

            messages.success(request ,"Your Review was added")
            # update project votes

            return redirect('single-project' ,pk = projectobj.id)

    context = {
        'project' : projectobj,
        'form':form,
    }
    return render(request ,'projects/single-project.html' ,context=context)


# create-form view
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile # get instance of user profile
    form = ProjectForm()

    if request.POST:
        form = ProjectForm(request.POST ,request.FILES)
        if form.is_valid:
            project = form.save(commit=False) # hold form 
            # set instance of owner with current profile
            project.owner = profile 
            project.save()
            messages.success(request ,'Project Created')
            return redirect('account')

    context = { 'form' : form}
    return render(request ,'projects/project-form.html' ,context=context)


# update-form view
@login_required(login_url='login')
def updateProject(request ,pk):
    # prevent from other user from updating the data of other user
    profile = request.user.profile # get the current user profile instance
    project = profile.project_set.get(id = pk)
    form = ProjectForm(instance=project)

    if request.POST:
        # update the image by request.FILES
        form = ProjectForm(request.POST ,request.FILES ,instance=project)
        if form.is_valid:
            form.save()
            messages.info(request ,'Project Updated')
            return redirect('account')

    context = { 'form' : form}
    return render(request ,'projects/project-form.html' ,context=context)


# delete-project view
@login_required(login_url='login')
def deleteProject(request ,pk):
    # prevent from other user from deleting the data of other user
    profile = request.user.profile # get current user profile instance
    project = profile.project_set.get(id = pk)

    if request.POST:    
        project.delete()
        messages.success(request ,'Project Deleted')
        return redirect('account')
    
    context = {
        'object':project,
    }
    return render(request ,'delete-form.html' ,context=context)