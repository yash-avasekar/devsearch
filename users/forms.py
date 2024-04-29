from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User,Profile,Skill,Message

# Custom User Form
# inherit the default UserCreationForm to get all functionalty and customize it
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name' ,'username' ,'email' ,'password1' 
                  ,'password2']
        labels = {
            'first_name' : 'Name',
        }

    
     # provide default class name style
    def __init__(self ,*args ,**kwargs):
        super(CustomUserCreationForm ,self).__init__(*args ,**kwargs)
        
        for name,field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})


# Profile form
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image' ,'name' ,'email' ,'username' ,'bio' 
                  ,'short_intro' ,'social_github' ,'social_instagram' 
                  ,'social_linkedin' ,]
        
    def __init__(self ,*args ,**kwargs):
        super(ProfileForm ,self).__init__(*args ,**kwargs)
    
        for name,field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})


# Skill form
class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    
    def __init__(self ,*args ,**kwargs):
        super(SkillForm ,self).__init__(*args ,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



# Message form
class MessageFrom(ModelForm):
    class Meta:
        model = Message
        fields = ['name' ,'email' ,'subject' ,'body']
    
    def __init__(self ,*args ,**kwargs):
        super(MessageFrom ,self).__init__(*args ,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


