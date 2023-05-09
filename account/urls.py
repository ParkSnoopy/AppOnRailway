from django.urls import path

from . import views

# from django.contrib.auth.views import LoginView


urlpatterns = [
    path('signup/', views.sign_up, name='account_signup'),
    
    path('login/', views.login_view, name='account_login'),
    path('logout/', views.logout_view, name='account_logout'),
    path('update/<int:id>/', views.update_profile, name='update_profile')
]
