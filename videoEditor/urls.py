from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('trim/', views.trim, name='trim'),
    path('bubble/',views.bubble, name='bubble'),
    path('tts/',views.textToSpeech, name='textToSpeech')
]