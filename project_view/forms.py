from django import forms
from project_view.models import Client, Project, Module, Part, Fixing, Fix, Topic, Picture

from django.core.files.uploadedfile import InMemoryUploadedFile
from project_view.humanize import naturalsize
from django.core.exceptions import ValidationError
from django.core import validators


class CreateFixingForm(forms.ModelForm):
    class Meta:
        model = Fixing
        fields = ['name']

class CreateFixForm(forms.ModelForm):
    class Meta:    
        model = Fix
        fields = ['fixing', 'number_of_elements', 'part']

class CreatePartForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ['name', 'description', 'module', 'supplier', 'thickness', 'minimal_draft_angle']  # Picture is manual


# Create the form class.
class CreateProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'client']

class CreateModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'project']

class CreateTopicForm(forms.ModelForm):
    
    class Meta:
        model = Topic
        fields = ['title', 'part']

class UpdateTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['description']

class CreatePictureForm(forms.ModelForm):

    picture = forms.FileField(required=False)
    upload_field_name = 'picture'

    class Meta:
        model = Picture
        fields = ['topic', 'content_type', 'picture']

    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('picture')
    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreatePictureForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.picture   # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance