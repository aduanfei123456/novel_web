"""novel_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from django.conf.urls import url
#from novel.views import MyRegistrationView
'''❏ 注册 → /accounts/register/
❏ 注册完成 → /accounts/register/complete/
❏ 登录 → /accounts/login/
❏ 退出 → /accounts/logout/
❏ 修改密码 → /password/change/
❏ 重设密码 → /password/reset/'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')), #include urls from other apps
    path('novel/',include('novel.urls')),
  #  url(r'^accounts/register/$',MyRegistrationView.as_view(),name='registration_register'),
  #  url(r'^accounts/',include('registration.backends.simple.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
