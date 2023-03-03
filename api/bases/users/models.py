import ast
import hashlib
import logging
import uuid
import random

from datetime import datetime
from collections import OrderedDict
from urllib.parse import ParseResult

from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin, AbstractUser
)
from django.db import models, utils
from django.apps import apps
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from rest_framework.authtoken.models import Token
from api.bases.users.choices import ProfileChoices

logger = logging.getLogger('django.server')


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username, request=None):
        if request and apps.is_installed('django.contrib.sites'):
            return self.get(
                **{'is_active': True, self.model.USERNAME_FIELD: username, 'site': get_current_site(request)})
        else:
            return self.get(**{'is_active': True, self.model.USERNAME_FIELD: username})

def get_default_site():
    try:
        return Site.objects.first().id
    except Exception as e:
        return None

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, auto_created=True, unique=True, primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_online = models.PositiveSmallIntegerField(default=0)
    last_password_change = models.DateTimeField(default=timezone.now, blank=True, null=True)
    site = models.ForeignKey(Site, default=get_default_site, on_delete=models.CASCADE, blank=True, null=True)
    deactivated_at = models.DateTimeField(null=True, blank=True, help_text='탈퇴일', editable=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def get_random_digit(self):
        """
        :return: 1~5
        """
        return (hash(self.id) % 5) + 1

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        unique_together = (('email', 'site', ),)
        ordering = ['email']

    def set_password(self, raw_password):
        super(User, self).set_password(raw_password)
        self.last_password_change = timezone.now()

class Image(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, auto_created=True, unique=True, primary_key=True,
                          help_text='자원 고유 ID')
    file = models.ImageField(upload_to='avatars', null=True, blank=True, help_text='이미지',
                             width_field='width', height_field='height')
    width = models.PositiveIntegerField(blank=True, null=True, help_text='이미지 넓이')
    height = models.PositiveIntegerField(blank=True, null=True, help_text='이미지 높이')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.file)

    @staticmethod
    def default_image(digit):
        filename = 'profile_{}.png'.format(digit)
        path = 'ums/media/avatars/{}'.format(filename)

        file = ParseResult(scheme='https',
                           netloc='cdn.backend.co',
                           path=path, params='', query='', fragment='').geturl()
        return {
            'file': file,
            'width': '360',
            'height': '360',
        }


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True, related_name='avatar')
    name = models.CharField(_('name'), max_length=30, blank=True, help_text='이름')
    nickname = models.CharField(max_length=30, null=True, blank=True, help_text='별명')
    phone = models.CharField(max_length=20, null=True, blank=True, help_text='휴대폰 번호')
    mobile_carrier = models.CharField(max_length=2, choices=ProfileChoices.MOBILE_CARRIER, null=True, blank=True,
                                      help_text='휴대폰 통신사')
    address = models.CharField(max_length=120, null=True, blank=True, help_text='주소')
    birth_date = models.DateField(null=True, blank=True, help_text='생년월일')
    gender_code = models.PositiveSmallIntegerField(choices=ProfileChoices.GENDER_TYPE, null=True, blank=True,
                                                   help_text='성별')

    class Meta:
        db_table = 'users_user_profile'


class ExpiringToken(Token):
    """Extend Token to add an expired method."""
    updated = models.DateTimeField(auto_now=True)

    def expired(self):
        """Return boolean indicating token expiration."""
        now = timezone.now()

        if self.user.is_active and self.expiry and self.updated < now - timezone.timedelta(seconds=self.expiry):
            return True
        return False

    @property
    def expiry(self):
        if self.user.is_staff:
            return None

        return settings.EXPIRING_TOKEN_LIFESPAN