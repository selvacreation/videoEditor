from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Video
from .forms import VideoForm
import subprocess
from django.core.files import File
from django.core.files.base import ContentFile
import os


def members(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def trim(request):
    template = loader.get_template('editorTrim.html')
    context = {
        'showTrim': False
    }

    if request.method == 'POST':
        form_type = request.POST.get('form_type', None)
        print("form_type----------->",form_type)
        if form_type == 'form1':
            form = VideoForm(request.POST or None,request.FILES or None)
            if form.is_valid():
                form.save()
            lastvideo = Video.objects.last()
            print("1",lastvideo)
            videofile = lastvideo.videofile

            context= {'videofile': videofile,
                'form': form,
                'showTrim': True
                }
            return HttpResponse(template.render(context,request))
        elif form_type == 'form2':
            startSec = request.POST.get('startSec')
            stopSec = request.POST.get('stopSec')
            duration = int(stopSec) - int(startSec)
            output_file = '/home/digital/webApp/webApp/media/videos/temp.mp4'

            video = Video.objects.last()
            base_dir = '/home/digital/webApp/webApp'
            relative_file_path = 'videos/temp.mp4'
            source_video_path = f"{base_dir}/media/{video.videofile}"

            ffmpeg_command = [
                'ffmpeg',
                '-y',
                '-i', source_video_path,
                '-ss', str(startSec), 
                '-t', str(duration),
                '-c', 'copy',  
                output_file
            ]
            subprocess.run(ffmpeg_command, check=True)
            with open(output_file, 'rb') as file:
                file_content = file.read()

            video = Video(name="trimmedVideo")
            video.videofile.save(relative_file_path, ContentFile(file_content))
            lastvideo = Video.objects.last()
            trim_videofile = lastvideo.videofile
            context= {'videofile': trim_videofile,
                'showTrim': True,
                'download': True
                }
            return HttpResponse(template.render(context,request))
    return HttpResponse(template.render(context,request))