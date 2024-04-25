from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='Password', max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,widget=forms.TextInput(attrs={'placeholder':'Username'}))
    password = forms.CharField(label='Password', max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    cpassword = forms.CharField(label='cPassword', max_length=20,widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))
    email = forms.CharField(label='Email', max_length=20,widget=forms.TextInput(attrs={'placeholder':'E-Mail'}))

class CommentForm(forms.Form):
    text = forms.CharField(label='text', max_length=300)
    
class NewVideoForm(forms.Form):
    title = forms.CharField(label='Title', max_length=20)
    description = forms.CharField(label='Description', max_length=300)
    file = forms.FileField()
    thumbnail_image= forms.ImageField()

class ChannelForm(forms.Form):
    channel_name = forms.CharField(max_length=50, label='Channel')