from django import forms
from project_view.models import Client, Project, Module, Part, Fixing, Fix, Topic, Picture, Entry, Participant, Participation

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
        fields = ['name', 'description', 'module', 'supplier', 'thickness', 'minimal_draft_angle']


# Create the form class.
class CreateProjectForm(forms.ModelForm):
    choice_opts=Participant.objects.all()
    print(choice_opts)
    choice_list=list()
    for choice in choice_opts:
        print(choice.name)
        choice_list.append(choice.name)
    print(choice_list)
    
    #participant = forms.MultipleChoiceField(choices=Participant.objects.all())
    
    class Meta:
        model = Project
        fields = ['name', 'client', 'participant']


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

#----------------------------------------------------------------------
# for the calendar widget you need to change
# the input type of the inherited DateInput class 
# to date (instead of text):
class DateInput(forms.DateInput):
    input_type='date'

#class PersonInput(forms.MultipleChoiceField):


class CreateEntryForm(forms.ModelForm):
    # when form specific:
    #deadline = forms.DateField(widget=DateInput)

    #responsible = forms.MultipleChoiceField()
    
    class Meta:
        model = Entry
        fields = ['solution', 'responsible', 'involved', 'agreed_with', 'deadline']
        widgets = {'deadline': DateInput}
#----------------------------------------------------------------------

class CreateParticipantForm(forms.ModelForm):
    
    class Meta:
        model = Participant
        fields = ['name']

class CreateParticipationForm(forms.ModelForm):
    
    class Meta:
        model = Participation
        fields = ['participant', 'project']