from django.db import models
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

# one to many:

class Client(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(
            max_length=200,
            unique=True,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)


    def __str__(self):
        return self.name

class Supplier(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])

    def __str__(self):
        return self.name

class Topic(models.Model):
    topic_title = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(1, "Title must be greater than 1 character")])
    
    topic_description = models.TextField(max_length=255, null=True)

    def __str__(self):
        return self.topic_title
        
class Fixing(models.Model):
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

    description = models.TextField()
    
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
          
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    
    fixing_element = models.ManyToManyField(Fixing, through='Fix', related_name='fixing_project_view')

    thickness = models.IntegerField(null=True)

    minimal_draft_angle = models.IntegerField(null=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# many to many:
    
class Fix(models.Model):
    number_of_elements = models.IntegerField(null=True)

    part = models.ForeignKey(Part, on_delete=models.CASCADE)
    fixing = models.ForeignKey(Fixing, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('part', 'fixing')


# admin:
    def __str__(self) :
        if self.number_of_elements > 1:
            self.fixing.name = f'{self.fixing.name}s' #plural
        #string in admin
        return '%s has %s %s'%(self.part, self.number_of_elements, self.fixing.name)











    

    
