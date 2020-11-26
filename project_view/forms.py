from django import forms
from project_view.models import Client, Project, Module, Part 

from django.core.files.uploadedfile import InMemoryUploadedFile
from project_view.humanize import naturalsize
from django.core.exceptions import ValidationError
from django.core import validators


class CreatePartForm(forms.ModelForm):

    class Meta:
        model = Part
        fields = ['name', 'description', 'module', 'supplier', 'thickness', 'minimal_draft_angle']  # Picture is manual


# Create the form class.
class CreateProjectForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ['name', 'client']

#    def __init__(self, pk):
#        super(CreateProjectForm, self).__init__(pk)
#        client_name = Client.objects.get(id=pk)
#        client_id = pk
#        CLIENT_CHOICES = (
#            (client_id, (client_name))
#        )
#
#        self.fields['client'].choices = CLIENT_CHOICES
#        self.fields['client'].widget.choices = CLIENT_CHOICES
#        print (self.fields['client'].choices)



    #client = forms.ChoiceField(choices = CLIENT_CHOICES)
    #name = forms.CharField(required=True, max_length=500, min_length=3, strip=True)
    
#    def __init__(self, pk):
#        super(CreateProjectForm, self).__init__(pk)
#        client_name = Client.objects.get(id=pk)
#        client_id = pk
#        CLIENT_CHOICES = (
#            (client_id, (client_name))
#        )
#        client = forms.ChoiceField(choices = CLIENT_CHOICES)
#        print(self.fields['client'])
        
        
        
        #self.fields['client'].queryset = Project.objects.filter(client_id=client)
        #self.fields['client'].queryset = client
        #print(self.fields['client'].queryset)



    

class CreateModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['name', 'project']
    # Validate the size of the picture
    #def clean(self):
    #    cleaned_data = super().clean()
    #    pic = cleaned_data.get('picture')
    #    if pic is None:
    #        return
    #    if len(pic) > self.max_upload_limit:
    #        self.add_error('picture', "File must be < "+self.max_upload_limit_text+" bytes")

    # Convert uploaded File object to a picture
    #def save(self, commit=True):
    #    instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
    #    f = instance.picture   # Make a copy
    #    if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
    #        bytearr = f.read()
    #        instance.content_type = f.content_type
    #        instance.picture = bytearr  # Overwrite with the actual image data

    #    if commit:
    #        instance.save()

    #    return instance

# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other
