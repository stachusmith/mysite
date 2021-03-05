from django import forms
from project_view.models import Client, Project, Module, Part, Fixing, Fix, Topic, Picture, Entry, Participant, Participation, Todo

from django.core.validators import MinLengthValidator
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
        fields = ['name', 'material', 'module', 'supplier', 'thickness', 'minimal_draft_angle']


# Create the form class.
class CreateProjectForm(forms.ModelForm):
        
    class Meta:
        model = Project
        fields = ['name', 'client']

class UpdateProjectForm(forms.ModelForm):
        
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
        fields = ['description', 'status']

#----------------------------------------------------------------------
# for the calendar widget you need to change
# the input type of the inherited DateInput class 
# to date (instead of text):
class DateInput(forms.DateInput):
    input_type='date'

#class PersonInput(forms.MultipleChoiceField):


class CreateEntryForm(forms.ModelForm):
    # when not model form:
    #deadline = forms.DateField(widget=DateInput)

    #responsible = forms.MultipleChoiceField()

    class Meta:
        model = Entry
        fields = [ 'solution', 'responsible', 'involved', 'agreed_with', 'deadline']
        widgets = {
            'deadline': DateInput(attrs={'class':'form_control'}),
            'responsible': forms.SelectMultiple(attrs={'class':'form_control'}),
            'solution': forms.Textarea(attrs={'class':'form_solution'}),
            'involved': forms.SelectMultiple(attrs={'class':'form_control'}),
            'agreed_with': forms.SelectMultiple(attrs={'class':'form_control'}),
        }
        
#----------------------------------------------------------------------

class CreateTodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = [ 'status', 'app_user', 'description', 'deadline']
        widgets = {
            #'status': forms.SelectMultiple(attrs={'class':'form_control'}),
            #'app_user': forms.SelectMultiple(attrs={'class':'form_control'}),
            'description': forms.Textarea(attrs={'class':'form_description'}),
            'deadline': DateInput(attrs={'class':'form_control'}),
        }

class CreateParticipantForm(forms.ModelForm):
    works_for_choices = ((1, 'OEM'),
                        (2, 'Supplier'),
                        (3, 'Development provider'))
    works_for = forms.ChoiceField(choices=works_for_choices, initial=True)
    phone_number = forms.RegexField(regex=r'^\+\d*', error_messages={'invalid':'invalid phone number'})
    class Meta:
        model = Participant
        fields = ['name', 'phone_number', 'email', 'works_for' ]

class CreateParticipantForm2(forms.ModelForm):

    def __init__ (self,  pk_for, *args, **kwargs):
        super(CreateParticipantForm2, self).__init__(*args, **kwargs)
        if pk_for == 1:
            self.fields.pop('supplier')
            self.fields.pop('development_provider')
        elif pk_for == 2:
            self.fields.pop('client')
            self.fields.pop('development_provider')
        else:
            self.fields.pop('client')
            self.fields.pop('supplier')

        
    
    class Meta:
        model = Participant
        fields = ['client', 'supplier', 'development_provider', 'job_title', 'project']

class CreateParticipantForm2POST(forms.ModelForm):
    
    class Meta:
        model = Participant
        fields = ['client', 'supplier', 'development_provider', 'job_title', 'project']

class CreateParticipationForm(forms.ModelForm):
    
    class Meta:
        model = Participation
        fields = ['participant', 'project']

class GetInTouchForm(forms.Form):
    name = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required= True, max_length=200)
    company = forms.CharField(required= False, max_length=200, validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

class GetInTouchForm2(forms.Form):
    message = forms.CharField(required= True, widget=forms.Textarea(attrs={'class':'message_field'}))