import django
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager, User

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    stars = models.IntegerField(default=0)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Ajoutez vos champs personnalisés ici

    def __str__(self):
        return self.reading_customuser.email

    def update_stars(self, num_stars):
        self.stars += num_stars
        self.save()

"""class Progress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='progress')
    #user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='progress')
    #user = models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    level = models.IntegerField()
    stars = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'level')"""


LEVEL_1_SOUNDS = ['ta', 'do', 'at', 'bi', 'ma', 're', 'su', 'py', 'fa', 'vi']
LEVEL_2_SOUNDS = ['far', 'por', 'dim', 'mes', 'son', 'cri', 'bal', 'cur', 'moi', 'rud']
LEVEL_3_SOUNDS = ['balle', 'chat', 'mois', 'dans', 'donc', 'très', 'mais', 'belle', 'mars', 'lire']
class Sound(models.Model):
    # Champ pour enregistrer le mot ou le son à lire
    text = models.CharField(max_length=255)
    # Champ pour enregistrer l'état du mot ou du son (correctement lu ou non)
    correct = models.BooleanField(default=False)
    
    def generate_sound_for_level(self, level):
        if level == 1:
            self.text = random.choice(LEVEL_1_SOUNDS)
        elif level == 2:
            self.text = random.choice(LEVEL_2_SOUNDS)
        elif level == 3:
            self.text = random.choice(LEVEL_3_SOUNDS)
        # Ajoutez d'autres conditions pour chaque niveau
        self.save()



