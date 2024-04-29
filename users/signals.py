from .models import User,Profile

# the below imports perform same functionalty
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

# Django db signals
"""
    sender is the user who sends a request
    instance is the users instance (username is returned)
    created only returns either true or false
      if the new user is created 'created value is true'
      if the user is just updated 'created value in false'
"""
# @receiver(post_save,sender='users.Profile')
def createProfile(sender ,instance ,created ,**kwargs):
    '''
    if newuser is created alongside create profile wright with user
    Cautions : if condition set to created or not created it will try to-
        create profile for present user aslo
    '''
    if created:
        # create user with instance
        user = instance
        profile = Profile.objects.create(
            user=user,
            username = user.username,
            email = user.email,
            name = user.first_name,
            # can add any other related field when the USER is created
            # (when new USER is created with some credentails the same info ,
            # is saved in profile where the above fields are provided)
        )
        
        '''send email when profile is created'''
        subject = 'Welcome to Devsearch'
        message = 'We are glad to have you here!'

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email], # send to user
            fail_silently=False,
        )




# delete user
def deleteUser(sender ,instance ,**kwargs):
    '''On profile delete also delete user'''
    user = instance.user # name refered from profile model
    user.delete()


# update user
'''
the method will receieve the instance of Profile model
reason the sender='Profile' is specified
'''
@receiver(post_save ,sender='users.Profile')
def updateUser(sender ,instance ,created ,**kwargs):
    profile = instance 
    # get user (same as request.user.get.all())
    # instance is current user
    user = profile.user 

    if not created :
        user.first_name = profile.name
        user.email = profile.email       
        user.username = profile.username
        user.save() 


# post_save tells when a user is fully update/created then trigger the function
post_save.connect(createProfile ,sender=User)

# post_delete
post_delete.connect(deleteUser ,sender=Profile)