from django.db import models
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

# one to many:

class Participant(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(
            max_length=200,
            unique=True,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    participant = models.ManyToManyField(Participant, through='Participation', related_name='participation_project_view')

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    def __str__(self):
        return self.name

class Fixing(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    def __str__(self):
        return self.name


    

# main model:

class Part(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")])

    material = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")],
            blank=True)
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
          
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, blank=True, null=True)
    
    fixing_element = models.ManyToManyField(Fixing, through='Fix', related_name='fixing_project_view')

    thickness = models.FloatField(null=True)

    minimal_draft_angle = models.FloatField(null=True)

    my_parts = models.ManyToManyField(settings.AUTH_USER_MODEL, through='My_part', related_name='my_parts_project_view')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    
    description = models.TextField(max_length=255, null=True, blank=True)

    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=True)

    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    date_of_creation = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    date_of_entry = models.DateField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    deadline = models.DateField()
    problem_description = models.TextField()
    solution = models.TextField()
    responsible = models.ManyToManyField(Participant, through='Responsibility', related_name='responsible_participants')
    #responsible = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='responsible_participants')
    involved = models.ManyToManyField(Participant, related_name='involved_participants')
    agreed_with = models.ManyToManyField(Participant, related_name='agreed_with_participants')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Picture(models.Model):
    picture = models.BinaryField(null=True, blank=True, editable=True)

    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    session = models.IntegerField(null=True)

# many to many:

class Participation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Responsibility(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)


class Fix(models.Model):
    
    number_of_elements = models.IntegerField(null=True)
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    fixing = models.ForeignKey(Fixing, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('part', 'fixing')


# admin:
    def __str__(self) :
        if self.number_of_elements > 1:
            self.fixing.name = f'{self.fixing.name}s' #plural
        #string in admin
        return '%s has %s %s'%(self.part, self.number_of_elements, self.fixing.name)

class My_part(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('part', 'user')










    

    
