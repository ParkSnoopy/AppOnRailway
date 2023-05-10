
# from django.utils import timezone
from django.conf import settings

from .models import Profile, User

from datetime import timedelta
import json


def is_sameuser(user0, user1, timediff):
    if timediff < timedelta(minutes=10):
        return user0 == user1
    return False

def process_chatlog(chatlog:dict, user0:int, user1:int, req_user, user_obj, timediff) -> dict:
    
    chatlog['isText'] = True if ( not chatlog.get('file_content') ) else False
    
    chatlog['fromSelf'] = True if ( req_user == user_obj ) else False
    
    chatlog['username'] = Profile.objects.get( user=user_obj ).nickname
    
    chatlog['sentAt'] = chatlog['sent_at'].strftime(settings.STRFTIME_FORMAT)
    
    chatlog['sameuser'] = is_sameuser( user0, user1, timediff )
    
    return chatlog

def add_separator(resultlogs:list, chatlog:dict, timediff:timedelta):
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

def pop_unused(chatlog:dict) -> dict:
    chatlog.pop('user_id')
    chatlog.pop('sent_at')
    chatlog.pop('chatroom_id')
    return chatlog

def add_header(resultlogs:list, head:dict):
    resultlogs.append(
        {
            "id": head['id'],
            "text_content": "",
            "file_content": "<<<TYPE::SEPARATOR>>>",
            "isText": False,
            "sentAt": head['sent_at'].strftime(settings.SEPARATOR_FORMAT),
        }
    )

def chatlogs_to_json(request, chatlogs, is_first):
    resultlogs = []
    if is_first and chatlogs:
        head = dict(**chatlogs[0])
        add_header(resultlogs, head)
        head['fromSelf'] = True if ( request.user == User.objects.get(pk=head['id']) ) else False
        head['isText'] = True if ( not head.get('file_content') ) else False
        head['sentAt'] = head['sent_at'].strftime(settings.STRFTIME_FORMAT)
        head = pop_unused(head)
        resultlogs.append(head)
        
    for index, chatlog in enumerate(chatlogs[1:]):
        index += 1
        
        chatlog = dict(**chatlog)
        
        timediff = chatlogs[index]['sent_at'] - chatlogs[index-1]['sent_at']
        user_obj = User.objects.get(pk=chatlogs[index]['user_id'])
        
        user0 = chatlogs[index-1]['user_id']
        user1 = chatlogs[ index ]['user_id']
        
        chatlog = process_chatlog(
            chatlog=chatlog, 
            user0=user0, 
            user1=user1, 
            req_user=request.user, 
            user_obj=user_obj, 
            timediff=timediff
        )
        add_separator(
            resultlogs=resultlogs, 
            chatlog=chatlog, 
            timediff=timediff
        )
        chatlog = pop_unused(chatlog)
        
        resultlogs.append(chatlog)
    
    resultlogs = resultlogs[::-1]
    
    return json.dumps(resultlogs, indent=2)


def convlist_to_json(request, convlist):
    return json.dumps(convlist)


def roominfo_to_json(request, roominfo):
    
    roominfo['announcement'] = roominfo['announcement'].split('\r\n')
    
    return json.dumps(roominfo)















































