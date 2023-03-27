
import uuid
from django.db import models
from django.core.validators import  validate_email
from django.forms import ValidationError

from django.core.exceptions import ValidationError

def custom_validator(value):
    if "example.com" in value:
        raise ValidationError("Email addresses from example.com are not allowed.")


class Student(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    div = models.CharField(max_length=5)
    mail = models.EmailField(unique=True, validators=[validate_email, custom_validator])
    mobile = models.CharField(max_length=20)

    def clean(self):
        return super(Student, self).clean()
    
    def __str__(self):
        return f"{self.name} {self.div} {self.mail} {self.mobile}"

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phisics = models.IntegerField
    math = models.IntegerField
    chemestry = models.IntegerField


