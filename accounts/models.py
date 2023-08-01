from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def delete(self, *args, **kwargs):
        # Store the user ID before deleting
        user_id = self.id
        # Perform deletion of the user account
        super().delete(*args, **kwargs)
        # Perform additional actions to retain data or handle associated models
        # For example, you can mark the user's data as archived instead of deleting it
        UserProfile.objects.filter(user_id=user_id).update(archived=True)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
