from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.core.models import BaseModel


class User(AbstractUser):
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        error_messages={
            'unique': _("A user with that username already exists."),
        })
    email = models.EmailField(_('email address'), unique=True)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def save(self, *args, **kwargs):
        self.username = self.email
        return super(User, self).save(*args, **kwargs)


ROL_ADMIN = 'admin'
ROL_USER = 'user'


ROLE_TYPE_CHOICES = (
    (ROL_ADMIN, 'Admin'),
    (ROL_USER, 'User')
    )

class Role(BaseModel):
    user = models.ForeignKey(User, related_name='roles', on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=ROLE_TYPE_CHOICES)

    def __str__(self):
        return "user: %s, type: %s" % (self.user.username,self.get_type_display())

    class Meta:
        ordering = ['created_at']
