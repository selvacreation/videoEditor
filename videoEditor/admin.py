from django.contrib import admin
from .models import Video
from .models import BubbleVideos
# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'parent_video', 'name', 'videofile')
class BubbleVideosAdmin(admin.ModelAdmin):
    list_display = ('id','template_video_id','bubble_video_id','category','videofile')
admin.site.register(Video,VideoAdmin)
admin.site.register(BubbleVideos,BubbleVideosAdmin)