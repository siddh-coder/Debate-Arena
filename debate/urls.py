from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_debate, name='create_debate'),
    path('join/', views.join_debate, name='join_debate_code'),  # For code entry
    path('join/<int:debate_id>/', views.join_debate, name='join_debate'),
    path('debate/<int:debate_id>/', views.debate_room, name='debate_room'),
    path('debate/<int:debate_id>/close/', views.close_debate, name='close_debate'),
    path('debate/<int:debate_id>/submit/', views.submit_argument, name='submit_argument'),
    path('history/', views.debate_history, name='debate_history'),
]
