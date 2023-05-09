from django.urls import path

from . import views


urlpatterns = [
    path('', views.filelist, name='publicshare'),
    
    path('shared/<str:filename>', views.get_publicfile),
    
    path('upload/', views.upload_publicfile)
    
]
