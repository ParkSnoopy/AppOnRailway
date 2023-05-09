from django.urls import path

from . import views



urlpatterns = [
    path('', views.home, name='home'),
    
    path('media/<str:a>', views.get_file, name='get_files'),
    path('static/<str:a>', views.get_static, name='get_statics'),
    
    path('media/<str:a>/<str:b>', views.get_file, name='get_files'),
    path('static/<str:a>/<str:b>', views.get_static, name='get_statics'),
    
    path('media/<str:a>/<str:b>/<str:c>', views.get_file, name='get_files'),
    path('static/<str:a>/<str:b>/<str:c>', views.get_static, name='get_statics'),
    
]