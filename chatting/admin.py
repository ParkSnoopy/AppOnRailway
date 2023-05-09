from django.contrib import admin

from .models import Chatlog
from .models import Chatroom

# Register your models here.


admin.site.register(Chatlog)
admin.site.register(Chatroom)