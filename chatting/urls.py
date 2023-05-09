from django.urls import path
from django.shortcuts import redirect

from .views import chat_home,  get_file, new_chatlog, new_filelog, json_chat_logs, json_room_data, json_annm_data



urlpatterns = [
    # REDITECT TO PK=1 PAGE (MAIN)
    path('home/', lambda request: redirect('chat_home', id=1) ),
    
    path('home/<int:id>/', chat_home, name="chat_home"),
    
    path('home/<int:id>/chat/<int:frompk>/data.json', json_chat_logs, name='json_chat_logs'),
    
    path('home/<int:id>/media/filecontent/<str:filename>', get_file, name='get_file'),
    
    path('home/<int:id>/input/message/', new_chatlog, name='new_chatlog'),
    path('home/<int:id>/input/file/', new_filelog, name='new_filelog'),
    
    path('home/<int:id>/room/data.json'             , json_room_data, name='json_room_data'),
    path('home/<int:id>/announcement/data.json'     , json_annm_data, name='json_annm_data'),
        
]
