"""
Activate Particular Ffmpeg Version
export PATH=/home/digital/Downloads/version_ff/ffmpeg-4.4-amd64-static:$PATH
ffmpeg -i /home/digital/Downloads/sajan2.mp4 -i /home/digital/Downloads/sajan1.mp4 -i /home/digital/Downloads/circle.png  -filter_complex "[0:v]scale=1920x1080[base];[1:v]scale=480x360[1v];[2:v]scale=-1:360,pad=480:360:(ow-iw)/2:color=#000000@1,format=rgb24[mask];[1v][mask]alphamerge[over];[base][over]overlay=x=1500:y=750" -t 5 /home/digital/Downloads/bubble2.mp4
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Video
from .forms import VideoForm
import subprocess
from django.core.files import File
from django.core.files.base import ContentFile


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
        base_dir = '/home/digital/webApp/webApp'
        print("form_type----------->",form_type)
        if form_type == 'form1':
            form = VideoForm(request.POST or None,request.FILES or None)
            if form.is_valid():
                saved_video = form.save()
                context= {'videofile': saved_video.videofile,
                    'form': saved_video,
                    'showTrim': True
                    }
                return HttpResponse(template.render(context,request))
        elif form_type == 'form2':
            startSec = request.POST.get('startSec')
            stopSec = request.POST.get('stopSec')
            video_id = request.POST.get('video_id')

            duration = int(stopSec) - int(startSec)
            output_file = '/home/digital/webApp/webApp/media/videos/temp.mp4'

            video = Video.objects.get(id=video_id)
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

            video = Video(name="trimmedVideo",parent_video = video_id)
            video.videofile.save(relative_file_path, ContentFile(file_content))
            context= {'videofile': video.videofile,
                'showTrim': True,
                'download': True
                }
            return HttpResponse(template.render(context,request))
    return HttpResponse(template.render(context,request))

def bubble(request):
    template = loader.get_template('bubbleEdit.html')
    context = {
        'showEditor': False
    }
    if request.method == 'POST':
        base_dir = '/home/digital/webApp/webApp'
        form_type = request.POST.get('form_type', None)
        if form_type == 'form1':
                form = VideoForm(request.POST or None,request.FILES or None)
                if form.is_valid():
                    saved_video = form.save()
                    context= {'videofile': saved_video.videofile,
                        'form': saved_video,
                        'showEditor': True,
                        'BubbleEditorr': True,
                        'showUploadBubble': True
                        }
                    return HttpResponse(template.render(context,request))
        elif form_type == 'form2':
                templateVideoId = request.POST.get("templateVideoId",None)
                templateVideo = Video.objects.get(id=templateVideoId)
                form = VideoForm(request.POST or None,request.FILES or None)
                if form.is_valid():
                    saved_video = form.save()
                    context= {'videofileBubble': saved_video.videofile,
                              'videofile': templateVideo.videofile,
                              'form': saved_video,
                              'templateVideo': templateVideo,
                              'showEditor': True,
                              "BubbleEditorr": True,
                              'showUploadBubble': False
                        }
                    return HttpResponse(template.render(context,request))
        elif form_type == "form3":
                templateVideoId = request.POST.get("templateVideoId",None)
                bubbleVideoId = request.POST.get("bubbleVideoId",None)
                bubbleVideoFile = request.POST.get("bubbleVideoFile",None)
                templateVideoFile = request.POST.get("templateVideoFile",None)
                print("bubbleVideoFile-->",bubbleVideoFile)
                print("templateVideoFile----->",templateVideoFile)

                templateVideoFile = f"{base_dir}/media/{templateVideoFile}"
                bubbleVideoFile = f"{base_dir}/media/{bubbleVideoFile}"
                circularImg = f"{base_dir}/videoEditor/static/images/circularBubble.png"
                output_file = "/home/digital/webApp/webApp/media/videos/tempBubble.mp4"

                command = [
                    'ffmpeg',
                    '-y',
                    '-i', templateVideoFile, '-i', bubbleVideoFile, '-i', circularImg,
                    '-filter_complex',
                    '[0:v]scale=1920x1080[base];[1:v]scale=480x360[1v];[2:v]scale=-1:360,pad=480:360:(ow-iw)/2:color=#000000@1,format=rgb24[mask];[1v][mask]alphamerge[over];[base][over]overlay=x=1500:y=750',
                    output_file
                ]

                subprocess.run(command, check=True)
                with open(output_file, 'rb') as file:
                    file_content = file.read()
                
                relative_file_path = 'videos/tempBubble.mp4'
                video = Video(name="bubbleVideo",parent_video = f"{templateVideoId}_{bubbleVideoId}")
                video.videofile.save(relative_file_path, ContentFile(file_content))

                context = {
                     "bubbleVideo": video.videofile,
                     "BubbleEditorr": False,
                     "showEditor": True
                }

    return HttpResponse(template.render(context,request))