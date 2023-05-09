from django.urls import path

from . import views

# Create your urls here.


urlpatterns = [
    path('home/', views.home, name="liargame_home"),
    path('join/', views.join, name="liargame_join"),
    path('unjoin/', views.unjoin, name="liargame_unjoin"),
    
    path('set-word/', views.set_word_setter, name="liargame_set_word"),
    path('set-word/result/', views.set_word_result, name="liargame_set_word_result"),
    path('set-word/result/confirm/', views.set_word_result_confirm, name="liargame_set_word_result_confirm"),
    
    path('choose-liar/', views.choose_liar, name="liargame_choose_liar"),
    path('check-my-word/', views.check_my_word, name="liargame_check_my_word"),
    
    path('reset/', views.reset, name="liargame_reset"),
    
]
