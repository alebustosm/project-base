from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models.deletion import ProtectedError
from django.urls import reverse

from .utils import normalize_text


class ExcludeDeletedManager(models.Manager):
    def get_queryset(self):
        return super(ExcludeDeletedManager, self).get_queryset().filter(_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    _deleted = models.BooleanField(default=False)

    objects = ExcludeDeletedManager()
    admin_manager = models.Manager()

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def delete(self, using=None):
        try:
            super(BaseModel, self).delete(using)
        except ProtectedError:
            self._deleted = True
            self.save()


def content_image_name(instance, filename):
    return '/'.join(['profile', instance.__class__.__name__.lower(), filename])


class Person(BaseModel):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    full_name = models.CharField(max_length=61, null=True,blank=True, editable=False)
    email = models.EmailField(blank=True, null=True)
    sex = models.CharField(max_length=1,
                           blank=True,
                           default='',
                           choices=(('f', 'Femenino'), ('m', 'Masculino'), ('o', 'Otros')))
    birthday = models.DateField(blank=True,null=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    # country = models.ForeignKey("cities.Country", null=True)
    # province = models.ForeignKey("cities.Region", null=True)
    # locality = models.ForeignKey("cities.City", null=True)
    image = models.ImageField(upload_to=content_image_name,
                              blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        self.full_name = normalize_text("%s %s" % (self.first_name if self.first_name else "",
                                                   self.last_name if self.last_name else ""))
        if not getattr(self, 'email') and getattr(self, 'user'):
            self.email = self.user.email
        super(Person, self).save(*args, **kwargs)


