from pyexpat.errors import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.views.generic.base import View, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import string, random
from django.core.files.storage import FileSystemStorage
import os
import datetime
from wsgiref.util import FileWrapper




from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# from django.shortcuts import get_absolute_url

def getstarted(request):
    return render( request ,'getstarted.html')

class VideoFileView(View):

    def get(self, request, file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = FileWrapper(open(BASE_DIR+'/'+file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response

class HomeView(View):
    template_name = 'index.html'
    def get(self, request):
        most_recent_videos = Video.objects.order_by('-datetime')[:8]
        most_recent_channels = Channel.objects.filter()

        channel = False
        print(request.user.username)
        if request.user.username != "":
            try:
                channel = Channel.objects.filter(user__username = request.user)
                print(channel)
                channel = channel.get()
            except Channel.DoesNotExist:
                channel = False
        return render(request, self.template_name, {'menu_active_item': 'home', 'most_recent_videos': most_recent_videos, 'most_recent_channels': most_recent_channels, 'channel': channel})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/home')

class VideoView(View):
    template_name = 'video.html'

    def get(self, request, id):
        #fetch video from DB by ID
        video_by_id = Video.objects.get(id=id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_by_id.path = 'http://localhost:8000/get_video/'+video_by_id.path
        context = {'video':video_by_id}
        print(request.user)
        is_favourite = False

        if video_by_id.favourite.filter(id=request.user.id).exists():
            is_favourite = True
        context['is_favourite'] = is_favourite

        if request.user.is_authenticated:
            print('user signed in')
            comment_form = CommentForm()
            context['form'] = comment_form

        comments = Comment.objects.filter(video__id=id).order_by('-datetime')[:5]
        print(comments)
        context['comments'] = comments

        try:
            channel = Channel.objects.filter(user__username = request.user).get().channel_name != ""
            print(channel)
            context['channel'] = channel
        except Channel.DoesNotExist:
            channel = False
        return render(request, self.template_name, context)

def favourite_video(request,id):
    video=Video.objects.get(id=id)
    if video.favourite.filter(id=request.user.id).exists():
        video.favourite.remove(request.user)
    else:
        video.favourite.add(request.user)
    # return render(request,'video/%s',% id)
    return redirect('video',id=video.id)

@login_required
def like_post(request, post_id):
    # Your logic to handle liking the post goes here
    return JsonResponse({'message': 'Post liked successfully'})

@login_required
def like_button(request):
    # This view function is just for the like button click event
    # It doesn't do anything other than showing the popup if the user is not logged in
    return JsonResponse({'message': 'Please login first to like the post'})

def video_favourite_list(request):
    user=request.user
    favourite_video = user.favourite.all()
    channel = False
    print(request.user.username)
    if request.user.username != "":
        try:
            channel = Channel.objects.filter(user__username = request.user)
            print(channel)
            channel = channel.get()
        except Channel.DoesNotExist:
            channel = False
    context={'favourite_video':favourite_video,'channel':channel}
    return render(request,'video_favourite_list.html',context)

class LoginView(View):
    template_name = 'login.html'
    def get(self, request):
        if request.user.is_authenticated:
            #logout(request)
            return redirect('/home')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out HTML-Form from View to LoginForm()
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # create a new entry in table 'logs'
                login(request, user)
                print('success login')
                return redirect('/home')
            else:
                return redirect('/login')
        return HttpResponse('This is Login view. POST Request.')

class CommentView(View):
    template_name = 'comment.html'

    def post(self, request):
        # pass filled out HTML-Form from View to CommentForm()
        form = CommentForm(request.POST)
        if form.is_valid():
            # create a Comment DB Entry
            text = form.cleaned_data['text']
            video_id = request.POST['video']
            video = Video.objects.get(id=video_id)

            new_comment = Comment(text=text, user=request.user, video=video)
            new_comment.save()
            return redirect('/video/{}'.format(str(video_id)))
        return HttpResponse('This is Register view. POST Request.')

class RegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        if request.user.is_authenticated:
            print('already logged in. Redirecting.')
            print(request.user)
            return redirect('/home')
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # pass filled out HTML-Form from View to RegisterForm()
        form = RegisterForm(request.POST)
        if form.is_valid():
            # create a User account
            print(form.cleaned_data['username'])
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            cpassword = form.cleaned_data['cpassword']
            email = form.cleaned_data['email']
            if password==cpassword:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                new_user.save()
            else:
                return redirect('/register')           
            return redirect('/login')
        return HttpResponse('This is Register view. POST Request.')

class NewVideo(View):
    template_name = 'new_video.html'

    def get(self, request):
        if request.user.is_authenticated == False:
            return redirect('/register')
        try:
            channel = Channel.objects.filter(user__username = request.user).get().channel_name != ""
            if channel:
                form = NewVideoForm()
                return render(request, self.template_name, {'form':form, 'channel':channel})
        except Channel.DoesNotExist:
            return HttpResponseRedirect('/home')
        

    def post(self, request):
        # pass filled out HTML-Form from View to NewVideoForm()
        form = NewVideoForm(request.POST, request.FILES)

        if form.is_valid():
            # create a new Video Entry
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            file = form.cleaned_data['file']
            thumbnail_image=form.cleaned_data['thumbnail_image']
            random_char = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            path = random_char+file.name

            fs = FileSystemStorage(location = os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            print(fs)
            print(filename)
            print(file_url)

            new_video = Video(title=title,
                            description=description,
                            user=request.user,
                            path=path,
                            thumbnail_image=thumbnail_image)
            new_video.save()

            # redirect to detail view template of a Video
            return redirect('/video/{}'.format(new_video.id))
        else:
            return HttpResponse('Your form is not valid. Go back and try again.')

class ChannelView(View):
    template_name = "channelview.html"

    def get(self, request, user):
        if request.user.is_authenticated:
            videos = Video.objects.filter(user__username = user).order_by("-datetime")
            print(Channel.objects.filter(user__username = user).get())

            return render(request, self.template_name, {'channel':Channel.objects.filter(user__username = user).get(), 'videos': videos})

class CreateChannelView(View):
    template_name = "channel.html"

    def get(self, request):
        if request.user.is_authenticated:
            try:
                if Channel.objects.filter(user__username = request.user).get().channel_name != "":
                    return redirect('/home')
            except Channel.DoesNotExist:
                form = ChannelForm()
                channel = False
                return render(request, self.template_name, {'form': form, 'channel': channel})


    def post(self, request):
        # pass filled out HTML-Form from View to RegisterForm()
        form = ChannelForm(request.POST)
        if form.is_valid():
            # create a User account
            print(form.cleaned_data['channel_name'])
            channel_name = form.cleaned_data['channel_name']
            user = request.user
            subscribers = 0
            new_channel = Channel(channel_name=channel_name, user=user, subscribers=subscribers)
            new_channel.save()
            return redirect('/home')
        return HttpResponse('This is Register view. POST Request.')


def search(request):
    vname=request.GET.get("vname")
    data=Video.objects.all()
    ytvideos=YoutubeVideo.objects.all()
    channel = False
    print(request.user.username)
    if request.user.username != "":
        try:
            channel = Channel.objects.filter(user__username = request.user)
            print(channel)
            channel = channel.get()
        except Channel.DoesNotExist:
            channel = False
    for d in data:
        if d.title.lower()==vname.lower():
            return render(request,"search.html",{"data":d,'channel':channel})
    for yt in ytvideos:
        if yt.videoname.lower()==vname.lower():
            print(yt)
            return render(request,"ytsearch.html",{"ytd":yt,'channel':channel})
    return render(request,"search.html", {'channel':channel,"d":"Sorry, Video Not found"})

def youtube(request):
    ytvideos=YoutubeVideo.objects.all()
    channel = False
    print(request.user.username)
    if request.user.username != "":
        try:
            channel = Channel.objects.filter(user__username = request.user)
            print(channel)
            channel = channel.get()
        except Channel.DoesNotExist:
            channel = False
    return render(request,"youtube.html", {'channel':channel,'ytvideos':ytvideos})
# def videoplay(request, id):
#     ytvideos = YoutubeVideo.objects.filter(id=id)
#     yt = YoutubeVideo.objects.get(id=id)
#     # recomended = YoutubeVideo.objects.all()
#     now = datetime.datetime.now()
#     channel = False
#     is_favourite = False
#     if yt.favouriteyt.filter(id=request.user.id).exists():
#         is_favourite = True
#     print(request.user.username)
#     if request.user.username != "":
#         try:
#             channel = Channel.objects.filter(user__username = request.user)
#             print(channel)
#             channel = channel.get()
#         except Channel.DoesNotExist:
#             channel = False
#     link_params = {'ytvideos': ytvideos,'time':now,'channel':channel,'yt':yt,'is_favourite':is_favourite}
#     return render(request, 'videoplay.html', link_params)
def videoplay(request, id):
    try:
        yt = YoutubeVideo.objects.get(id=id)
    except YoutubeVideo.DoesNotExist:
        # Handle the case where the video with the given id does not exist
        # You can customize this error handling as per your requirement
        return redirect('home')  # Redirect to home or any appropriate page

    if request.user.is_authenticated:
        is_favourite = yt.favouriteyt.filter(id=request.user.id).exists()
    else:
        is_favourite = False
        # Display a message if the user is not logged in
        return redirect('login')  # Redirect to the login page

    # Retrieve channel information if the user is logged in
    now = datetime.datetime.now()
    channel = False
    if request.user.username:
        try:
            channel = Channel.objects.filter(user__username=request.user).get()
        except Channel.DoesNotExist:
            channel = False

    link_params = {'ytvideos': [yt], 'time': now, 'channel': channel, 'yt': yt, 'is_favourite': is_favourite}
    return render(request, 'videoplay.html', link_params)


def favourite_ytvideo(request,id):
    ytvideo=YoutubeVideo.objects.get(id=id)
    if ytvideo.favouriteyt.filter(id=request.user.id).exists():
        ytvideo.favouriteyt.remove(request.user)
    else:
        ytvideo.favouriteyt.add(request.user)
    # return render(request,'video/%s',% id)
    return redirect('videoplay',id=ytvideo.id)

def ytvideo_favourite_list(request):
    user=request.user
    favourite_ytvideo = user.favouriteyt.all()
    channel = False
    print(request.user.username)
    if request.user.username != "":
        try:
            channel = Channel.objects.filter(user__username = request.user)
            print(channel)
            channel = channel.get()
        except Channel.DoesNotExist:
            channel = False
    context={'favourite_ytvideo':favourite_ytvideo,'channel':channel}
    return render(request,'ytvideo_favourite_list.html',context)