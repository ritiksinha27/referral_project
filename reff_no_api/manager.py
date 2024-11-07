from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom user manager to handle user creation with email as username
    and additional custom fields.
    """

    def create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email, password and extra fields.
        """
        if not username:
            raise ValueError('Users must have an email address')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Creates and saves a SuperUser with the given email, password and extra fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)


        if password is None:
            raise ValueError('Superusers must have a password')

        user = self.create_user(username, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user