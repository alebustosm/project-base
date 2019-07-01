from django.db import models
from apps.core.models import BaseModel, Person


class Borrower(Person):
    user = models.OneToOneField('user.User', related_name='borrower', on_delete=models.PROTECT, null=True)
    cuit = models.CharField(max_length=100, blank=True,unique=True, null=True)
    dni = models.CharField(max_length=100, blank=True,unique=True, null=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)