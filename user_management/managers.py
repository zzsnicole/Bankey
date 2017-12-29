from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_no, name, password, **extra_fields):
        """
        Creates and saves a User with the given name, phone_no and password.
        """
        if not name and not phone_no:
            raise ValueError('The given name and phone_no must be set')
            name = self.normalize_name(name)
        user = self.model(phone_no=phone_no, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_no, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_no, name, password, **extra_fields)

    def create_superuser(self, phone_no, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(phone_no, name, password, **extra_fields)