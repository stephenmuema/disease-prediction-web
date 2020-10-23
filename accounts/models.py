from __future__ import unicode_literals

from enum import Enum

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from rest_framework.authtoken.models import Token

from djangoHealthAnalytics import settings
from djangoHealthAnalytics.extras import encrypt_string


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_staff=False, is_admin=False, is_active=True, is_company=False,
                    is_superuser=False, user_type='rest'):
        if not email:
            raise ValueError("user requires an email")
        if not password:
            raise ValueError("user requires a password")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.is_company = is_company
        user_obj.set_password(password)
        user_obj.is_staff = is_staff
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_superuser = is_superuser
        user_obj.user_type = user_type
        user_obj.save(using=self._db)
        return user_obj

    #     create accounts for access to statistical panel
    def create_staffuser(self, email, password=None, is_staff=True, is_admin=False, is_active=True):
        user = self.create_user(email, password=password, is_staff=is_staff, is_admin=is_admin, is_active=is_active,
                                is_company=False, is_superuser=False, user_type='staff'
                                )
        return user

    #     create admin account for site admins
    def create_superuser(self, email, password=None, is_staff=True, is_admin=True, is_active=True):
        user = self.create_user(email, password=password, is_staff=is_staff, is_admin=is_admin, is_active=is_active,
                                is_company=False, is_superuser=True, user_type='admin'
                                )
        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    class UserAccount(Enum):
        admin = ('admin', 'admin account')
        rest = ('rest', 'rest account')
        health = ('health', 'health official account')
        devs = ('dev', 'devs account')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    # [...]
    # status = models.CharField(
    #     max_length=32,
    #     choices=[x.value for x in STATUS],
    #     default=STATUS.get_value('available'),
    # )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_status = models.CharField(max_length=20, null=False, default="active")
    timestamp = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=32,
                                 choices=[x.value for x in UserAccount],
                                 default=UserAccount.get_value('rest'))
    email_confirmed = models.BooleanField(default=False)
    hash = models.TextField()
    USERNAME_FIELD = 'email'  # make email username field
    objects = UserManager()

    class Meta:
        db_table = "Users"
        verbose_name_plural = "Users"

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def user_is_admin(self):
        return self.is_admin

    @property
    def user_is_staff(self):
        return self.is_staff

    @property
    def user_is_active(self):
        return self.is_active

    def save(self, *args, **kwargs):
        self.hash = encrypt_string(
            '{}{}{}{}{}'.format(self.pk, self.first_name, self.last_name, self.password, self.timestamp))
        super(User, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=200, null=True)

    # alternative_phone_number = models.CharField(null=True, max_length=20, blank=True)
    # mobile_money_phone_number = models.CharField(null=True, max_length=20)
    # location = models.CharField(max_length=32)

    class Meta:
        db_table = 'User Profile'
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
