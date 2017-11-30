from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone_no, password, **extra_fields):
        """
        Creates and saves a User with the given email, phone_no and password.
        """
        if not email and not phone_no:
            raise ValueError('The given email and phone_no must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone_no, password, **extra_fields)

    def create_superuser(self, email, phone_no, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, phone_no, password, **extra_fields)