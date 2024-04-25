from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=300)
    path = models.CharField(max_length=60)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False) #todo: auto_now=True
    thumbnail_image = models.ImageField(upload_to="thumbnail/",default="No thumbnail")
    favourite=models.ManyToManyField('auth.User',related_name='favourite',blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(max_length=300)
    datetime = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class Channel(models.Model):
    channel_name = models.CharField(max_length=50, blank=False, null=False)
    subscribers = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class YoutubeVideo(models.Model):
    videoname = models.CharField(max_length=150)
    videolink = models.CharField(max_length=150)
    videodisc = models.CharField(max_length=500)
    favouriteyt = models.ManyToManyField('auth.User',related_name="favouriteyt",blank=True)
    thumbnail_image = models.ImageField(upload_to="thumbnail/")

    def __str__(self):
        return self.videoname
