from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from chatting.models import Chatroom

# Create your views here.
USER_VARS = settings.LIARGAME_USER_VARS


@login_required
def update_home(request):
    chatrooms = list(Chatroom.objects.all().values())
    return render(request, 'updatemanager/index.html', {"chatrooms": chatrooms})

@login_required
def update(request, id):
    
    chatroom = Chatroom.objects.get(pk=id)
    
    if request.method == 'POST':

        USER_VARS.set(
            anncm_title = request.POST.get('title', ''), 
            anncm = request.POST.get('content', ''), 
        )
        
        return redirect('update_confirm', id=id)


    
    return render(request, 'updatemanager/update.html', {
        "roomname": chatroom.roomname, 
        "anncm_title": chatroom.announcement_title, 
        "anncm": chatroom.announcement, 
    })

@login_required
def update_confirm(request, id):

    chatroom = Chatroom.objects.get(pk=id)
    
    if request.method == 'POST':
        
        Chatroom.objects.filter(pk=id).update(
            announcement_title = USER_VARS.get("anncm_title", ""), 
            announcement = USER_VARS.get("anncm", ""), 
        )
        chatroom = Chatroom.objects.get(pk=id)
        
        return redirect('update_home')

    return render(request, 'updatemanager/update_confirm.html', {
        "roomname": chatroom.roomname, 
        "anncm_title": USER_VARS.get("anncm_title"), 
        "anncm": USER_VARS.get("anncm"), 
        "id": id, 
    })