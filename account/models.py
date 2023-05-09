from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("[Error from <UserManager.create_user>] Users must have an username")
        
        user = self.model(
            username=username, 
            email=self.normalize_email(email), 
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username, 
            email=email, 
            password=password, 
        )
        user.is_admin = True
        user.save(using=self._db)
        
        return user
    


class User(AbstractBaseUser):
    
    username = models.CharField(
        max_length=50, 
        unique=True, 
    )
    email = models.EmailField(
        verbose_name="email", 
        max_length=80, 
        unique=True, 
    )
    is_leadership = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    register_date = models.DateTimeField(default=timezone.now)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True #? self.is_admin
    
    def has_module_perms(self, app_label):
        return True #?
    
    @property
    def is_staff(self):
        return self.is_admin
    



class Profile(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    nickname  = models.CharField(max_length=20, blank=True, default="")
    userimage = models.ImageField(default='defaults/userimage.jpg', upload_to='profile/userimages')
    
    
    def __str__(self):
        return self.nickname
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, nickname=instance.username)

models.signals.post_save.connect(
    create_user_profile, 
    sender=User, 
)
    
    
    
    
    
    
    
    
    
    
    
    
    