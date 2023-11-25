from django.contrib import admin
from .models import Video
# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_video', 'name', 'videofile')
admin.site.register(Video,VideoAdmin)