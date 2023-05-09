from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings


from account.models import Profile

# Create your views here.


def home(request):
    
    nickname = 'Err'
    if request.user.is_authenticated:
        nickname = Profile.objects.get( user=request.user ).nickname
    
    return render(request, 'homepage/home.html', {'nickname': nickname})



SLUG_SEQUENCE = 'abcdefghijklmnopqrstuvwxyz'

@login_required
def get_file(request, **paths):
    
    fullpath = settings.MEDIA_ROOT
    for slug in SLUG_SEQUENCE[:len(paths)]:
        fullpath /= paths.get(slug)
    
    return FileResponse( open( fullpath, 'rb' ) )

@login_required
def get_static(request, **paths):
    
    fullpath = settings.STATIC_ROOT
    for slug in SLUG_SEQUENCE[:len(paths)]:
        fullpath /= paths.get(slug)
    
    return FileResponse( open( fullpath, 'rb' ) )