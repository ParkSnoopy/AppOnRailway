from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User, Profile

# Register your models here.



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ("username", "email", "register_date", "is_leadership", "is_admin", "is_active", )
    list_filter = ("is_admin", "is_leadership", )
    
    fieldsets = (
        (None           , {"fields": ("email", "password", )}), 
        ("Personal info", {"fields": ("username", "is_leadership", )}), 
        ("Permissions"  , {"fields": ("is_admin", "is_active", )}), 
    )
    add_fieldsets = (
        (None           , {
            "classes": ("wide", ), 
            "fields" : ("username", "email", "password1", "password2", ), 
        }), 
    )
    
    search_fields = ("username", "email", )
    ordering = ("register_date", )
    filter_horizontal = ()
    

class ProfileAdmin(admin.ModelAdmin):
    
    list_display = ("nickname", "user", )
    fieldsets = (
        ("Profile info", {"fields": ("nickname", "userimage", )}), 
        ("User info"  , {"fields": ("user", )}), 
    )
    add_fieldsets = (
        (None           , {
            "classes": ("wide", ), 
            "fields" : ("nickname", "user", ), 
        }), 
    )
    
    search_fields = ("nickname", "user", )
    ordering = ("user", )

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)

admin.site.register(Profile, ProfileAdmin)
