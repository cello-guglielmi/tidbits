import random
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import RegexValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields): # Helper function
        if not email:
            raise ValueError('Email must be set.')
        email = self.normalize_email(email)
        username = random_username()
        extra_fields.setdefault('nickname', username) # Keeping non-mandatory fields flexible
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuse', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)

ADJECTIVES = ["Nifty", "Silly", "Lucky", "Fancy", "Jolly",]
NOUNS = ["Reader", "Scholar", "Pupil", "Observer", "Learner",]

def random_username():
    ''' # probability of having a duplicate in 100.000 users is 0.000000012, do I really need this?
        for _ in range(5):
            adjective = random.choice(ADJECTIVES)
            noun = random.choice(NOUNS)
            suffix = uuid.uuid4().hex[:6]
            usrname = f"{adjective}{noun}{suffix}"
            if not CustomUser.objects.filter(username=usrname).exists():
                return usrname
        return uuid.uuid4().hex
    '''
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    suffix = uuid.uuid4().hex[:6]
    return f'{adj}{noun}-{suffix}'



nickname_validator = RegexValidator(
    regex=r'^[\w.\-]+$',
    message="Nicknames may contain letters, numbers, '.', '-' and '_' only.",
)

class CustomUser(AbstractUser):
    username = models.CharField('Internal username', max_length=50, unique=True, default=random_username)
    nickname = models.CharField('Display name', max_length=50, validators=[nickname_validator], help_text="This is what's displayed on your profile!")
    email = models.EmailField('Email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.nickname