from django.db import models
from django.utils import timezone

from datetime import timedelta

from account.models import User, Profile


# Create your models here.



class Chatroom(models.Model):
    
    roomname = models.CharField(max_length=100, default="Our Chatroom")
    
    announcement_title = models.TextField(max_length=200, default="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sagittis dictum tortor, sed mollis justo lacinia eget. ")
    announcement = models.TextField(max_length=1000, default="In pharetra volutpat eros, in tempus est pellentesque quis. Vivamus pretium sodales ex at suscipit. In porta libero turpis, sit amet mattis quam vestibulum vel. In non felis eu enim hendrerit fringilla ut in lacus. Quisque leo tortor, feugiat vitae sagittis eget, mattis quis dui. Cras bibendum luctus finibus. Mauris id neque nec nunc malesuada eleifend maximus et enim. \r\nDuis aliquam vestibulum cursus. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque elit nunc, eleifend a pulvinar eget, sodales ut lectus. Integer eu nibh velit. Phasellus maximus malesuada nisi in aliquam. In convallis orci id quam aliquam bibendum. Integer consectetur fermentum molestie. Cras id mi efficitur, porta quam et, laoreet neque.")
    
    
    def __str__(self):
        return f"{self.roomname}"
    



class ChatlogRetrieveManager(models.Manager):
    
    def get_queryset(self):
        currtime = timezone.now()
        return super().get_queryset().filter( sent_at__gte = currtime - timedelta(days=self.days_before) )
    
    def set_days_before(self, days_before=None):
        self.days_before = days_before if days_before else self.default_days_before
    
    def get_recent_n_logs(self, n=None, pk=None):
        if pk:
            recent_n = self.get_queryset() \
                .filter(chatroom=pk)
        else:
            recent_n = self.get_queryset() \
                .all()
        
        recent_n = recent_n.order_by('-id')
        
        return recent_n.values() [:n] [::-1]
    
    def get_logs_from_to(self, roompk, frompk=0, topk=65536):
        logs = self.get_queryset() \
            .filter( chatroom = roompk ) \
            .filter( pk__gte = frompk ) \
            .filter( pk__lt = topk )
        
        return list( logs.values() )
    
    default_days_before = 7
    days_before = default_days_before



class ChatlogManager(models.Manager):
    
    def create(self, chatroom, user, sent_at=None, text_content=None, file_content=None):
        if chatroom:
            chatroom = Chatroom.objects.get(pk=chatroom)
            
        if not chatroom:
            chatroom = Chatroom.objects.all().first()
            
        if file_content:
            
            chatlog = self.model(
                chatroom     = chatroom, 
                user         = user, 
                file_content = file_content, 
            )
            
        elif text_content:
            chatlog = self.model(
                chatroom     = chatroom, 
                user         = user, 
                text_content = text_content, 
            )
        
        chatlog.save(using=self._db)
        
        return chatlog



class Chatlog(models.Model):
    
    chatroom = models.ForeignKey(Chatroom, default=1, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text_content = models.TextField(max_length=512, blank=True, null=True)
    file_content = models.ImageField(upload_to='filecontent/', blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True, default=timezone.localtime)
    
    
    chatlogRetriever = ChatlogRetrieveManager()
    objects = ChatlogManager()    
    
    
    def __str__(self):
        nickname_len_lim = 20
        content_len_lim = 50
        
        profile = Profile.objects.get(user=self.user)
        
        if self.text_content:
            return f"at '{self.chatroom}' , {profile.nickname[:nickname_len_lim]}" + ("..." if len( profile.nickname )  > nickname_len_lim else "") + f" ~ {self.text_content[:content_len_lim]}" + ("..." if len( self.text_content )  > content_len_lim else "")
        return f"at '{self.chatroom}' , {profile.nickname[:nickname_len_lim]}" + ("..." if len( profile.nickname )  > nickname_len_lim else "") + f" ~ {self.file_content}"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    