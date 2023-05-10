from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.forms.models import model_to_dict

from .models import Chatlog, Chatroom

from .jsonmaker import chatlogs_to_json, convlist_to_json, roominfo_to_json

from .fetchfile_handler import generate_filename, save_file

import json

# Create your views here.


@login_required
def chat_home(request, id):
    
    try:
        chatroom = Chatroom.objects.get(pk=id)
        
    except:
        chatroom = Chatroom.objects.create()
        
        return redirect( 'chat_home', id=chatroom.id )
    
    return render(request, "chatting/index.html", {
        "roomname": chatroom.roomname, 
    })
    
@login_required
def new_chatlog(request, id):
    if request.method == "POST":
        postdata = json.load(request)
        chatlog = postdata.get('data')
        
        if chatlog:
            Chatlog.objects.create(
                chatroom=id, 
                user=request.user, 
                text_content=chatlog, 
                sent_at=timezone.now(), 
            )
    
            return HttpResponse(status=200)
        return HttpResponse(status=204)
    return HttpResponse(status=405)




@login_required
def new_filelog(request, id):
    if request.method == "POST":
        
        for fileobj in request.FILES.values():
            filename = generate_filename(fileobj.name)
            
            if save_file(filename, fileobj) == True:
                
                Chatlog.objects.create(
                    chatroom=id, 
                    user=request.user, 
                    file_content=filename, 
                    sent_at=timezone.now(), 
                )
    
            return HttpResponse(status=200)
        return HttpResponse(status=204)
    return HttpResponse(status=405)

@login_required
def json_chat_logs(request, id, frompk):
    
    chatlogs = Chatlog.chatlogRetriever.get_logs_from_to(roompk=id, frompk=frompk, topk=256+frompk)
    
    json_chatlogs = chatlogs_to_json( request, chatlogs, is_first=(frompk==0) )
    
    return HttpResponse( json_chatlogs, content_type="application/json" )


@login_required
def json_room_data(request, id):
    
    convlist = list( Chatroom.objects.all().values() )
    
    json_convlist = convlist_to_json( request, convlist )
    
    return HttpResponse( json_convlist, content_type="application/json" )
    

@login_required
def json_annm_data(request, id):
    
    roominfo = Chatroom.objects.get(pk=id)
    roominfo = model_to_dict( roominfo, fields=tuple( field.name for field in roominfo._meta.fields ) )
    
    json_roominfo = roominfo_to_json( request, roominfo )
    
    return HttpResponse( json_roominfo , content_type="application/json" )
    
    
@login_required
def get_file(request, id, filename):
    return redirect('get_files', a='filecontent', b=filename)
    


































