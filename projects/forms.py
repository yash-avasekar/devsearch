from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Project,Review

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title' ,'featured_image' ,'description'
                  ,'tags' ,'demo_link' ,'source_link']
        
        # customize field (eg. created multiple checkbox)
        widgets = {
            'tags' : forms.CheckboxSelectMultiple,
        }

    # provide default class name style(css class_name)
    def __init__(self ,*args ,**kwargs):
        super(ProjectForm ,self).__init__(*args ,**kwargs)
        
        for name,field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})


# Review Form
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body' ,'value']
        labels = {
            'body':'Add a comment with your vote',
            'value':'Place you vote',
        }

    # provide default class name style
    def __init__(self ,*args ,**kwargs):
        super(ReviewForm ,self).__init__(*args ,**kwargs)
        
        for name,field in self.fields.items() :
            field.widget.attrs.update({'class' : 'input'})