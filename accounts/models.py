from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class MyBaseUserManager(BaseUserManager):
    def create_user (self, email, password = None, **kwargs):
        # Checking if email is provided
        if not email:
            # raise value error if email not provided
            raise ValueError ('Email must be provided for registering')
        # Normalizing the email
        email = self.normalize_email(email)
        # Creating the user of the given email
        user = self.model(email=email, **kwargs)
        # Set the password to this user
        user.set_password(password)
        # Save the user to the database after assign the password
        user.save(using=self._db)
        # Return the user
        return user
    
    def create_superuser (self, email, password=None, **kwags):
        # Creating the superuser by calling the create_user()
        # Setting the attributes is_staff and is_superuser to true
        kwags.setdefault('is_staff', True)
        kwags.setdefault('is_superuser', True)
        # Return the user
        return self.create_user(email, password, **kwags)


class CustomUser (AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=250, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Specifying the custom manager for creating a user
    objects = MyBaseUserManager()

    # Defining the username field the admin will be prompted to fill when created by interacting
    USERNAME_FIELD = 'email'
    # After user prompted to fill email if there is other required field will be defined here
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
