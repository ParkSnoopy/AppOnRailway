from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from datetime import timedelta
import os

# Create your models here.


PUBLIC_STORAGE = FileSystemStorage(
    location='public/', 
)

class PublicfileManager(models.Manager):
    
    def create(self, content, title=None):
        if title:
            publicfile = self.model(content=content, title=title)
            PUBLIC_STORAGE.save(name=title, content=content)
        else:
            PUBLIC_STORAGE.save(name=content.name, content=content)
            publicfile = self.model(content=content)
        publicfile.save(using=self._db)
        return publicfile
    
    def remove_expired_and_get_existing(self):
        self.filter(
            created_at__lt = timezone.now() - timedelta(days=3)
        ).delete()
        
        publicfiles = list(map(
            lambda path: path.replace('public/', ''), 
            self.values_list('content', flat=True)
        ))
        
        for file in os.listdir( settings.MEDIA_ROOT / "public/" ):
            if file not in publicfiles + ['.gitkeep', ]:
                os.remove( settings.MEDIA_ROOT / "public/" / file )
        
        titles = list(self.values_list('title', flat=True))
        for index, value in enumerate( titles ):
            if not value:
                titles[index] = publicfiles[index]
        
        return publicfiles, titles
    
    
class Publicfile(models.Model):
    
    title = models.CharField(max_length=100, null=True, blank=True)
    content = models.FileField(upload_to='public/')
    created_at = models.DateTimeField(default=timezone.now)
    
    
    objects = PublicfileManager()
    
    def __str__(self):
        return f"PublicFile : {self.content}"


