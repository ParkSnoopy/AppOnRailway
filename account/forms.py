from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm, UsernameField

from .models import User, Profile

# Create your forms here.



class UserCreationForm(forms.ModelForm):
    username = UsernameField(label="Username", max_length=50)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ("username", "email", )
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and ( password1 != password2 ):
            raise forms.ValidationError("Passwords don't match!")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password( self.cleaned_data['password1'] )
        if commit:
            user.save()
        return user
    
    
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ("username", "email", "password", "is_leadership", "is_active", "is_admin", "register_date", )
        
    def clean_password(self):
        return self.initial['password']




class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = User
        fields = ('username', 'password', )
    
    
    _base_attrs = {
        'class': 'form-control', 
        'placeholder': '', 
    }
    
    # username = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs=_base_attrs
    #     )
    # )
    username = UsernameField(
        widget=forms.TextInput(
            attrs=_base_attrs
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs=_base_attrs
        )
    )




class UserSignupForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )
    
    _base_attrs = {
        'class': 'form-control', 
        'placeholder': '', 
    }
    
    username = forms.CharField(
        widget=forms.TextInput(
            attrs=_base_attrs
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs=_base_attrs
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=_base_attrs
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs=_base_attrs
        )
    )
    
    
    
class ProfileChangeForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ("nickname", "userimage", )
        
    def clean_userimage(self):
        self.initial['userimage']
        
    username = forms.CharField(
        max_length=100, 
        widget=forms.TextInput(), 
    )
    
    userimage = forms.ImageField(
        widget=forms.FileInput(), 
    )
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    