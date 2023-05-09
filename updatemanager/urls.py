from django.urls import path

from . import views


urlpatterns = [
    path('', views.update_home, name='update_home'),
    path('<int:id>/', views.update, name='update'),
    path('<int:id>/confirm/', views.update_confirm, name='update_confirm'),
]
