
from django.utils import timezone
from django.conf import settings

from .models import User, Profile

from datetime import timedelta
import json


USER_VARS = settings.LIARGAME_USER_VARS
USER_VARS.set(
    last_send_user = -1, 
    last_send_time = timezone.now() + timedelta( weeks = -2 ), 
    not_first = False, 
)

def chatlogs_to_json(request, chatlogs, is_first):    
    
    idx = -1
    while idx+1 < len(chatlogs):
        idx += 1
        
        chatlog = chatlogs[ idx ]
        chatuser = User.objects.get( pk = chatlog.pop('user_id') )
        
        this_sent_time = chatlog.pop('sent_at')
        
        chatlog['isText'] = True if ( not chatlog.get('file_content') ) else False
        
        chatlog['fromSelf'] = True if ( request.user == chatuser ) else False
        chatlog['username'] = Profile.objects.get( user=chatuser ).nickname
        
        chatlog['sentAt'] = this_sent_time.strftime(settings.STRFTIME_FORMAT)
        
        chatlog['sameuser'] = True
        
        if ( not is_first or USER_VARS.get('not_first') ) and USER_VARS.get( 'last_send_time' ) > ( this_sent_time + timedelta( minutes = -5 ) ):
            chatlog['sameuser'] = USER_VARS.get('last_send_user') == chatuser
            
        elif is_first or USER_VARS.get( 'last_send_time' ) < ( this_sent_time + timedelta( hours= -1 ) ):
            if is_first: USER_VARS.set(not_first=True)
            chatlogs.insert(
                idx, 
                {
                    "id": chatlog['id']-1,
                    "chatroom_id": chatlog['chatroom_id'],
                    "text_content": None,
                    "file_content": "<<<TYPE::SEPARATOR>>>",
                    "isText": False,
                    "sentAt": this_sent_time.strftime(settings.SEPARATOR_FORMAT),
                }
            )
            idx += 1
            chatlog['sameuser'] = False
        else:
            chatlog['sameuser'] = False
                    
            
        USER_VARS.set(
            last_send_user = chatuser, 
            last_send_time = this_sent_time
        )
    
    chatlogs = chatlogs[::-1]
    if not is_first:
        chatlogs.pop()
    
    USER_VARS.set(not_first=False)
    return json.dumps(chatlogs)


def convlist_to_json(request, convlist):
    return json.dumps(convlist)


def roominfo_to_json(request, roominfo):
    
    roominfo['announcement'] = roominfo['announcement'].split('\r\n')
    
    return json.dumps(roominfo)















































