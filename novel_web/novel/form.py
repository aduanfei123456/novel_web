from django import forms
from .models import Novel,UserProfile,User

class NovelForm(forms.ModelForm):
    title=forms.CharField(max_length=150,initial="无名",help_text="Title Name")
    novel_id=forms.CharField(max_length=150,initial="1111_00",help_text="title_id")
    category = forms.CharField(max_length=150, initial="玄幻",help_text="category")
    writer = forms.CharField(max_length=150, initial="佚名",help_text="writer")
    img_url = forms.CharField(max_length=150, initial="test.jpg",help_text="img_url")

    #fields 想显示的字段   exclude 想隐藏的字段
    class Meta:
        model=Novel
        exclude={}
class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),max_length=150)

    class Meta:
        model=User
        fields=('username','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=('picture',)