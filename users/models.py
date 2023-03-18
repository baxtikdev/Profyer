from parler.models import TranslatableModel, TranslatedFields

from .manager import CustomUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    username = None
    email = models.EmailField(_("Email address"), unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.get_full_name()


class UserType(models.IntegerChoices):
    CLIENT = 1, _('CLIENT')
    SPECIALIST = 2, _('SPECIALIST')


class UserVote(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    age = models.IntegerField(null=True, blank=True)
    vote_number = models.IntegerField(null=True, blank=True)
    language = models.ManyToManyField('Language', blank=True)
    country = models.ManyToManyField('Country', blank=True)
    services = models.ManyToManyField('Service', blank=True)
    type = models.IntegerField(choices=UserType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + ' ' + str(self.type)


class Service(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name of Service"), max_length=50)
    )

    def __str__(self):
        return self.name


class Country(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Name of Country"), max_length=50)
    )

    def __str__(self):
        return self.name


class Language(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Language"), max_length=50)
    )

    def __str__(self):
        return self.name
