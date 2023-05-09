from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, Http404
from django.conf import settings

from .models import Publicfile

import os

# Create your views here.
    

def filelist(request):
    
    publicfiles, titles = Publicfile.objects.remove_expired_and_get_existing()
    
    return render(request, 'publicshare/index.html', {"files_titles": zip(publicfiles, titles), })



def get_publicfile(request, filename:str):
    
    path = settings.MEDIA_ROOT / 'public' / filename
    
    if os.path.isfile(path):
        
        if str(path).split('.')[-1] != 'zip':
            return FileResponse( open( path, 'rb' ) )
        else:
            response = HttpResponse( open( path, 'rb' ), content_type='application/zip' )
            response['Content-Disposition'] = f'attachment; filename={filename}.zip'
            return response
    
    else:
        
        raise Http404()
    
def upload_publicfile(request):
    
    if request.method == "POST":
        
        if request.FILES:
            title = request.POST['title']
            
            publicfile = Publicfile.objects.create(
                content=request.FILES.get('file'), 
                title=(title if title else None), 
            )
            
            with open( settings.MEDIA_ROOT / str(publicfile.content) , "wb") as output:
                for chunk in request.FILES.get('file').chunks():
                    output.write(chunk)
            
            return redirect('publicshare')
    
    return render(request, 'publicshare/upload.html')