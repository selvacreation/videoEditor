from django.db import models

# Create your models here.
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    parent_video = models.IntegerField(null=True)
    name = models.CharField(max_length=100)
    videofile = models.FileField(upload_to='videos/', null=True, verbose_name="")

class BubbleVideos(models.Model):
    id = models.AutoField(primary_key=True)
    template_video_id = models.IntegerField()
    bubble_video_id = models.IntegerField()
    category = models.CharField(max_length=100)
    videofile = models.FileField(upload_to='videos/')
