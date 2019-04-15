from django.conf.urls import url
from . import views

#'^$'匹配空字符串

#namespace
app_name="novel"
#name attribute for relative url in template
urlpatterns=[
    url(r'^$',views.HomePage,name='homepage'),
    url(r'^(?P<novel_id>\d+_\d+)(/)?$',views.NovelIntroduction,name='introduction'),
    url(r'^(?P<novel_id>\d+_\d+)/(?P<chapter_id>\d+)(/)?$',views.Chapter,name='chapter'),
    url(r'^add_novel/$',views.Add_Novel,name='add_novel'),
    url(r'^category/(?P<category_slug_name>(\w)+)',views.Category,name='category'),
    url(r'^register/$',views.register,name='register'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'homepage/$',views.user_page,name='userpage'),
    url(r'about/$',views.about,name='about'),
    url(r'search/(?P<search_name>(\w)+)',views.SearchNovel,name='searchnovel'),
    url(r'collect/',views.collect_novel,name='collectnovel'),

]