
# from django.utils import timezone
from django.conf import settings

from .models import Profile, User

from datetime import timedelta
import json


# USER_VARS = settings.LIARGAME_USER_VARS
# USER_VARS.set(
#     last_send_user = -1, 
#     last_send_time = timezone.now() + timedelta( weeks = -2 ), 
#     not_first = False, 
# )

def chatlogs_to_json(request, chatlogs, is_first):
    resultlogs = []
    if is_first and chatlogs:
        head = dict(**chatlogs[0])
        resultlogs.append(
            {
                "id": head['id'],
                "text_content": "",
                "file_content": "<<<TYPE::SEPARATOR>>>",
                "isText": False,
                "sentAt": head['sent_at'].strftime(settings.SEPARATOR_FORMAT),
            }
        )
        head.pop('user_id')
        head.pop('sent_at')
        head.pop('chatroom_id')
        resultlogs.append(
            head
        )
        
    for index, chatlog in enumerate(chatlogs[1:]):
        index += 1
        chatlog = dict(**chatlog)
        
        user_obj = User.objects.get(pk=chatlogs[index]['user_id'])
        
        chatlog['isText'] = True if ( not chatlogs[index].get('file_content') ) else False
        
        chatlog['fromSelf'] = True if ( request.user == user_obj ) else False
        chatlog['username'] = Profile.objects.get( user=user_obj ).nickname
        
        chatlog['sentAt'] = chatlogs[index]['sent_at'].strftime(settings.STRFTIME_FORMAT)
        
        chatlog['sameuser'] = chatlogs[index-1]['user_id'] == chatlogs[index]['user_id']
        
        timediff = chatlogs[index]['sent_at'] - chatlogs[index-1]['sent_at']
        
        if timedelta(hours=1) > timediff > timedelta(minutes=5):
            chatlogs[index]['sameuser'] = False
            
        if timediff > timedelta(hours=1):
            resultlogs.append(
                {
                    "id": chatlog['id'],
                    "text_content": "",
                    "file_content": "<<<TYPE::SEPARATOR>>>",
                    "isText": False,
                    "sentAt": chatlog['sent_at'].strftime(settings.SEPARATOR_FORMAT),
                }
            )
            chatlog['sameuser'] = False
        else:
            chatlog['sameuser'] = False
        
        
        chatlog.pop('user_id')
        chatlog.pop('sent_at')
        chatlog.pop('chatroom_id')
        resultlogs.append(chatlog)
    
    resultlogs = resultlogs[::-1]
    
    return json.dumps(resultlogs, indent=2)


def convlist_to_json(request, convlist):
    return json.dumps(convlist)


def roominfo_to_json(request, roominfo):
    
    roominfo['announcement'] = roominfo['announcement'].split('\r\n')
    
    return json.dumps(roominfo)















































