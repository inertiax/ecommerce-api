from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """creates and saves new users"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, password):
        """creates and saves a new staff user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)

    def create_superuser(self, email, password):
        """creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def get_name(self):
        return self.name
    
    def get_surname(self):
        return self.surname
    
    @property
    def is_active(self):
        return self.active
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.superuser
