import os
import random
from django.shortcuts import render, redirect
from django.conf import settings

def login_view(request):
    if request.method == 'POST':
        # Accept any username and password
        request.session['logged_in'] = True
        return redirect('feed')
    return render(request, 'feed/login.html')

def feed_view(request):
    if not request.session.get('logged_in'):
        return redirect('login')
    
    video_dir = os.path.join(settings.MEDIA_ROOT, 'videos')
    videos = []
    
    if os.path.exists(video_dir):
        for filename in os.listdir(video_dir):
            if filename.endswith(('.mp4', '.webm', '.ogg')):
                # Generamos ruta relativa web a media para usar en src del video
                videos.append(f"{settings.MEDIA_URL}videos/{filename}")
    
    # Randomizar los vídeos
    random.shuffle(videos)
    
    return render(request, 'feed/feed.html', {'videos': videos})
