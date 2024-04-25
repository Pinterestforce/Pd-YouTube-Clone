from django.contrib import admin
from django.urls import path
from youtube.views import *
from youtube import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', HomeView.as_view()),
    path('',views.getstarted),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('new_video', NewVideo.as_view()),
    path('video/<int:id>', VideoView.as_view(),name="video"),
    path('favourite_video/<int:id>/', views.favourite_video,name="favourite_video"),
    path('accounts/login/?next=/favourite_video/<int:id>/', views.favourite_video,name="favourite_video"),
    path('video_favourite_list/', views.video_favourite_list,name="video_favourite_list"),
    path('comment', CommentView.as_view()),
    path('get_video/<file_name>', VideoFileView.as_view()),
    path('logout', LogoutView.as_view()),
    path('home/', HomeView.as_view()),
    path('search/',views.search),
    path('createchannel', CreateChannelView.as_view()),
    path('<user>/channel', ChannelView.as_view()),
    path('youtube/',views.youtube),
    path('videoplay/<int:id>/', views.videoplay, name='videoplay'),
    path('favourite_ytvideo/<int:id>/', views.favourite_ytvideo,name="favourite_ytvideo"),
    path('ytvideo_favourite_list/', views.ytvideo_favourite_list,name="ytvideo_favourite_list"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
