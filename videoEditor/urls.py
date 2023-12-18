from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('trim/', views.trim, name='trim'),
    path('bubble/',views.bubble, name='bubble'),
    path('tts/',views.textToSpeech, name='textToSpeech'),
    path('merge/',views.merge, name='merge'),
    path('features/',views.features, name='features'),
    path('record/',views.record, name='record')
]