"""
Activate Particular Ffmpeg Version
export PATH=/home/digital/Downloads/version_ff/ffmpeg-4.4-amd64-static:$PATH
ffmpeg -i /home/digital/Downloads/sajan2.mp4 -i /home/digital/Downloads/sajan1.mp4 -i /home/digital/Downloads/circle.png  -filter_complex "[0:v]scale=1920x1080[base];[1:v]scale=480x360[1v];[2:v]scale=-1:360,pad=480:360:(ow-iw)/2:color=#000000@1,format=rgb24[mask];[1v][mask]alphamerge[over];[base][over]overlay=x=1500:y=750" -t 5 /home/digital/Downloads/bubble2.mp4
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Video
from .models import BubbleVideos
from .forms import VideoForm
import subprocess
from django.core.files import File
from django.core.files.base import ContentFile
import base64


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
                video = BubbleVideos(category="bubbleVideo",template_video_id = templateVideoId, bubble_video_id = bubbleVideoId)
                video.videofile.save(relative_file_path, ContentFile(file_content))

                context = {
                     "bubbleVideo": video.videofile,
                     "BubbleEditorr": False,
                     "showEditor": True
                }

    return HttpResponse(template.render(context,request))

def textToSpeech(request):
     template = loader.get_template('textToSpeech.html')
     context = {
          "success": True
     }
     if request.method == "POST":
          Gender = request.POST.get("Gender")
          Accent = request.POST.get("Accent")
          Text = request.POST.get("Text")

          print(f"Gender is - {Gender}")
          print(f"Accent is - {Accent}")
          print(f"Text is - {Text}")
           
          des,resp = elevenLabsTtsApi(Gender,Accent,Text)

          audio_data = resp.content
          audio_base64 = base64.b64encode(audio_data).decode('utf-8')
          context = {
               "success": True,
               "audio_base64": audio_base64
          }
          return HttpResponse(template.render(context,request))
     return HttpResponse(template.render(context,request))

def merge(request):
    template = loader.get_template('mergeVideo.html')
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
                firstAudio = request.POST.get("firstAudio",True)
                print("bubbleVideoFile-->",bubbleVideoFile)
                print("templateVideoFile----->",templateVideoFile)

                mergeVideo1 = f"{base_dir}/media/{templateVideoFile}"
                mergeVideo2 = f"{base_dir}/media/{bubbleVideoFile}"
                output_file = "/home/digital/webApp/webApp/media/videos/tempMerge.mp4"
                if(firstAudio):
                    ffmpeg_command = [
                        'ffmpeg',
                        '-y',
                        '-i', mergeVideo1,
                        '-i', mergeVideo2,
                        '-filter_complex', '[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[v0][v1]hstack=inputs=2[v];[0:a][1:a]amerge=inputs=2[a]',
                        '-map', '[v]',
                        '-map', '[a]',
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-crf', '23',
                        '-preset', 'veryfast',
                        '-r', '30',  # Adjust the frame rate as needed
                        '-b:v', '2M',
                        output_file
                    ]
                else:
                    ffmpeg_command = [
                        'ffmpeg',
                        '-y',
                        '-i', mergeVideo1,
                        '-i', mergeVideo2,
                        '-filter_complex', '[0:v]scale=1920:1080[v0];[1:v]scale=1920:1080[v1];[v0][v1]hstack=inputs=2[v];[1:a]amerge=inputs=1[a]',
                        '-map', '[v]',
                        '-map', '[a]',
                        '-c:v', 'libx264',
                        '-c:a', 'aac',
                        '-crf', '23',
                        '-preset', 'veryfast',
                        output_file
                    ]

                subprocess.run(ffmpeg_command, check=True)

                print("firstAudio--->",firstAudio)
                print("mergeVideo1--->",mergeVideo1)
                print("mergeVideo2-->",mergeVideo2)
                with open(output_file, 'rb') as file:
                    file_content = file.read()
                
                relative_file_path = 'videos/tempBubble.mp4'
                video = BubbleVideos(category="mergedVideo",template_video_id = templateVideoId, bubble_video_id = bubbleVideoId)
                video.videofile.save(relative_file_path, ContentFile(file_content))

                context = {
                     "bubbleVideo": video.videofile,
                     "BubbleEditorr": False,
                     "showEditor": True
                }

    return HttpResponse(template.render(context,request))

def elevenLabsTtsApi(Gender,Accent,Text):
    import requests
    import json

    availableMaleVoiceIds = {
         "American": "pNInz6obpgDQGcFmaJgB",
         "British": "Yko7PKHZNXotIFUBG7I9",
         "Australian": "IKne3meq5aSn9XLyUdCD",
         "Italian": "zcAOhNBS3c14rBihAFp1"
    }
    availableFemaleVoiceIds = {
         "American": "EXAVITQu4vr4xnSDxMaL",
         "British": "ThT5KcBeYPX3keUQqHPh",
         "Australian": "XB0fDUnXU5powFXDhCwa",
         "Italian": "oWAxZDx7w5VEj9dCyTzz"
    }
    if Gender in ["Male"]:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{availableMaleVoiceIds[Accent]}" 
        print("url->",url)
    elif Gender in ["Female"]:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{availableFemaleVoiceIds[Accent]}" 
        print("female url -> ",url)

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": "3f70c9f5a84bfaf732d13c9846727f05"
    }

    data = {
        "text": Text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 1,
            "similarity_boost": 1
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    desPath = "/home/digital/webApp/webApp/media/videos/temp1.mp3"
    # if response.status_code in [200]:
    #     with open(desPath, "wb") as f:
    #         f.write(response.content)
    return desPath,response

def features(request):
     template = loader.get_template('features.html')
     return HttpResponse(template.render())