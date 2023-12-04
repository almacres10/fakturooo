from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)

    groups = models.ManyToManyField('auth.Group', related_name='user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_permissions')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_pegawai = models.CharField(max_length=100)

    def __str__(self):
        return self.nama_pegawai