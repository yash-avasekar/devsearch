from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import CustomUserCreationForm,ProfileForm,SkillForm,MessageFrom
from . import models
from . import utils

# Create your views here.

# User Login
def loginUser(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.POST:
        username = request.POST['username'].lower()
        password = request.POST['password']

        # check if user exist
        try:
            user = models.User.objects.get(username=username)
            # authenticate user
            user = authenticate(request ,username=username ,password=password)
       
            # login user
            if user is not None:
                login(request ,user) # this creates user session (session_id)
                messages.info(request ,'Logged In')
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')  # redirect to profiles page
            else:
                messages.error(request ,'Incorrect Username or Password')
                print(user)
        except Exception:
            messages.error(request ,'Username does not exist')


    return render(request ,template_name='users/login-register.html')


# user logout
def logoutUser(request):
    logout(request)
    messages.info(request ,'Logged Out')
    return redirect('login')


# user register view
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm() # pre defined form to create user with validation

    if request.POST:
        # save all the credentials in form 
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # dont save in database (commit acts as database command)
            # used when you want to know whether the username already exists
            user = form.save(commit=False)  # hold the form
            user.username = user.username.lower() # can be done in forms
            user.save() # save to database

            messages.success(request , 'Account Successfully Created')

            '''you can login the user immediately after regisertion'''
            login(request ,user)
            return redirect('profiles')
        else:
            messages.error(request ,"Error occured while creating user."+
                           "Make sure you met requirements")

    context = {
        'page': page,
        'form': form,
    }
    return render(request ,template_name='users/login-register.html' ,
                  context=context)


# profile view
def profile(request):
    # get data from custom made funtcion
    profiles ,search_query = utils.searchProfile(request)
    profiles ,custom_range = utils.paginateProfile(request ,profiles ,3)
    context = {
        'profiles' : profiles,
        'search_query':search_query,
        'custom_range':custom_range,
    }
    return render(request , 'users/profiles.html' ,context=context)


# user profile view
def userProfile(request ,pk):
    profile = models.Profile.objects.get(id = pk)
    top_skills = profile.skill_set.exclude(description__exact = '')
    other_skills = profile.skill_set.filter(description = '')
    context = {
        'profile' : profile,
        'top_skills' : top_skills,
        'other_skills' : other_skills,
    }
    return render(request ,template_name='users/user-profile.html' ,context=context)


# user account view
@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all() # get child model object

    context = {
        'profile':profile,
        'skills':skills,
    }
    return render(request ,'users/account.html' ,context=context)


# edit profile view
@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile # get user profile instance
    form = ProfileForm(instance=profile)

    if request.POST:
        form = ProfileForm(request.POST ,request.FILES ,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request ,'Account Updated')

    context = {
        'form':form,
    }
    return render(request ,'users/edit-account.html' ,context=context)


# edit skills view
@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile  # get the current user profile instance
    form = SkillForm()

    if request.POST:
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request ,'Skill Added Successfully !')
            return redirect('account')
        
    context={
        'form':form
    }
    return render(request ,'users/skill-form.html' ,context=context)


# update skill view
@login_required(login_url='login')
def updateSkill(request ,pk):
    profile = request.user.profile  # get the current user profile instance
    skill = profile.skill_set.get(id = pk)
    form = SkillForm(instance = skill)

    if request.POST:
        form = SkillForm(request.POST ,instance = skill)
        if form.is_valid():
            skill.save()
            messages.success(request ,'Skill Updated')
            return redirect('account')
        
    context={
        'form':form
    }
    return render(request ,'users/skill-form.html' ,context=context)


# delete Skill view
@login_required(login_url='login')
def deleteSkill(request ,pk):
    profile = request.user.profile # get user profile instance
    skill = profile.skill_set.get(id = pk) # get current user instance

    if request.POST:
        skill.delete() # delete
        messages.info(request ,'A Skill is Deleted')
        return redirect('account')

    context = {
        'object':skill
    }
    return render(request ,'delete-form.html' ,context=context)



# inbox view
@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    # the child model is accessible for reason of adding 'related_name' in model
    messageRequest = profile.messages.all()
    # get unread messages count
    unreadCount = messageRequest.filter(is_read = False).count() 

    context ={
        'messageRequest':messageRequest,
        'unreadCount':unreadCount,
    }
    return render(request ,'users/inbox.html' ,context=context)


# message vie
@login_required(login_url='login')
def viewMessage(request ,pk):
    profile = request.user.profile
    # cause only one user if fetched
    # just grammerly thing lol
    message = profile.messages.get(id = pk)

    if not request.GET:
        message.is_read = True
        message.save()

    context = {
        'profile':profile,
        'message':message,
    }
    return render(request ,'users/message.html' ,context=context)


# create message veiw
# user can also send message to developer
def createMessage(request ,pk):
    recipient = models.Profile.objects.get(id = pk)
    form = MessageFrom()

    try : 
        '''if user is logged in'''
        sender = request.user.profile
    except : 
        sender = None
    
    if request.POST:
        form = MessageFrom(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                '''if user is logged in get the Name and Email'''
                message.name = sender.name
                message.email = sender.email

            message.save()
            messages.success(request, 'Message has been sent')
            return redirect('user-profile' ,pk = recipient.id)

    context = {
        'recipient':recipient,
        'form':form,
    }
    return render(request ,'users/message-form.html' ,context=context)
