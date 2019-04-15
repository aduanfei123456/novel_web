from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404
#from django.http import HttpResponse
#from .models import Question,Choice
from .crawl.my_crawl import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Novel,UserNovel
from .form import NovelForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import   login_required
from django.contrib.auth import logout
from datetime import datetime
from registration.backends.simple.views import RegistrationView

import json
import os
main_url="http://www.biquyun.com/"
novel_categories=["玄幻","修真","都市","历史","网游","科幻"]
class tempchapter(object):
    def __init__(self,name,href):
        self.name=name
        self.href=href
class tempnovels(object):
    def __init__(self,categtory,novels=None):
        self.category=categtory
        self.novels=novels

def HomePage(request):
    #request.session.set_test_cookie()
    Home_Novels=[]
    catemap = {"玄幻": "xuanhuan", "修真": "xiuzhen", "都市": "dushi", "历史": "lishi",
               "网游": "wangyou", "科幻": "kehuan",
               }
    for category in novel_categories:
        #get for one object,filter for objects
        c_novel=Novel.objects.filter(category=category)
        if (len(c_novel)>0):
            Home_Novels.append(tempnovels(category,c_novel[:7]))
        else:
            Home_Novels.append(tempnovels(category))
    displaynovels=Novel.objects.all()[12:17]

    hotnovels=Novel.objects.filter()[:10]
    for h in hotnovels:
        h.img_url="/".join(h.img_url.split("\\"))
    context_dict={'HomeNovels':Home_Novels,'categories':novel_categories,'hotnovels':hotnovels,'displaynovels':displaynovels}
    visitor_cookie_handler(request)
    context_dict['visits']=request.session['visits']
    response= render(request,'novels/homepage.html',context=context_dict)


    return response

def get_save(novel_id):
    _main_url = "http://www.biquyun.com/"
    novel_url=_main_url+novel_id
    # May raise SSLError
    html = requests.get(novel_url, verify=False)
    writere = re.compile(r"：([\w]+)")

    html.encoding = "gb2312"
    web_content = BeautifulSoup(html.text, "lxml")
    introductions={}

    introductions["id"] = novel_id
    introductions["title"] = web_content.find(id="info").h1.get_text()
    info = web_content.find(id="info")
    introductions["writer"] = writere.search(info.p.get_text()).group(1)

    introductions["brief_content"] = web_content.find(id="intro").get_text()
    try:
        htmlimg = main_url + web_content.find(id="fmimg").img["src"]
    except Exception:
        htmlimg = None

    if (htmlimg):
        img_name=re.search(r'/([\w\s]+)\.jpg',htmlimg).group(1)
        print(img_name)
        print(os.path.abspath('..'))
        save_path = os.path.join(os.path.abspath('.'), 'static', 'images', 'undefined', '{}.jpg'.format(img_name))
        print(save_path)
        if not (os.path.exists(save_path)):

            response=requests.get(htmlimg, verify=False)

            with open(save_path, 'wb') as f:
                f.write(response.content)
                f.close
        introductions["img_url"] = os.path.join('undefined', '{}.jpg'.format(img_name))
    else:
        introductions["img_url"] = "test.jpg"
    print(introductions)
    n=Novel.objects.create(novel_id=introductions["id"],title=introductions["title"],writer=introductions["writer"],brief_content=introductions["brief_content"],img_url=introductions["img_url"])
    n.save()
    return n
def NovelIntroduction(request,novel_id):

    n_crawler=novel_crawler(novel_id)
    searchn=Novel.objects.filter(novel_id=novel_id)
    if(len(searchn)>0):
        n_database=searchn[0]
    else:
        n_database=get_save(novel_id)

    clias=[]
    for chapter,href in n_crawler.chapters:
        clias.append(tempchapter(chapter,href))
    context_dict={'information':n_crawler.introductions,'clias':clias,'nbase':n_database,'imgurl':"images/"+n_database.img_url}
    if(request.user.is_authenticated):
        user_name=request.user.username
        collected=UserNovel.objects.filter(user_name=user_name,novel_id=novel_id)
        if(len(collected)>0):
            context_dict["collected"]=1
        else:
            context_dict["collected"]=0
    return render(request,'novels/detail.html',context=context_dict)
def Chapter(request,novel_id,chapter_id):
    page_url='/'+novel_id+'/'+chapter_id+'.html'
    n=Novel.objects.filter(novel_id=novel_id)[0]
    Apage=NovelPage(main_url+page_url)
    relative_novels=Novel.objects.filter(category=n.category)[:10]
    context_dict={
        'novel':n,
        'content':Apage.content,
        'chapter_name':Apage.chapter_name,
        'relative_novels':relative_novels,
    }
    if(Apage.nchapter!=None):
       context_dict['next_chapter']=Apage.nchapter
    if (Apage.lchapter != None):
       context_dict['last_chapter']=Apage.lchapter,

    return render(request,'novels/page.html',context=context_dict)

def Category(request,category_slug_name):
    context_dict={}
    try:
        novels=Novel.objects.filter(category=category_slug_name)
        context_dict['novels']=novels
        context_dict['category']=category_slug_name
    except Novel.DoesNotExist:
        context_dict['novels']=None
        context_dict['category']=None
    return render(request,'novels/category.html',context_dict)

def Add_Novel(request):
    form=NovelForm()

    if request.method=='POST':
        form=NovelForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return HomePage(request)
        else:
            print(form.errors)

    return render(request,'novels/add_novel.html',{'form':form})

def about(request):
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED")
        request.session.delete_test_cookie()
    return HttpResponseRedirect(reverse('novel:homepage'))
def register(request):
    registered=False

    if request.method=='POST':
        user_form=UserForm(data=request.POST)
        profile_form=UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()

            #set_password calculate the hashvalue of password
            user.set_password(user.password)
            user.save()

            #delay the save
            profile=profile_form.save(commit=False)
            profile.user=user

            if 'picture' in request.FILES:
                profile.picture=request.FILES['picture']

            profile.save()

            registered=True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    return render(request,
                  'novels/register.html',
                  {
                      'user_form':user_form,
                      'profile_form':profile_form,
                      'registered':registered
                  }
                  )

@csrf_exempt
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                #status code 302
                return HttpResponseRedirect(reverse('novel:homepage'))

            else:
                #not activiated,forbidden to log in
                return HttpResponse("Your account is disabled")
        else:
            print("Invalid login details:{0},{1}".format(username.password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'novels/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('novel:homepage'))
@login_required
def collect_novel(request):
    if(request.method=='POST'):
        uname=request.user.username

        nid=request.POST.get("novel_id")
        print(uname,nid)
        un,created=UserNovel.objects.get_or_create(novel_id=nid,user_name=uname)
        un.save()

        return HttpResponse("success")
@login_required
def user_page(request):
    novelids=UserNovel.objects.filter(user_name=request.user.username)
    novels=[]
    for ns in novelids:
        nid=ns.novel_id
        print(nid)
        tempn=Novel.objects.filter(novel_id=nid)[0]
        novels.append(tempn)
    return render(request,'novels/userpage.html',{"novels":novels})

#use session to save cookie so that the statics is in the server side
def get_server_side_cookie(request,cookie,default_val=None):
    val=request.session.get(cookie)
    if not val:
        val=default_val
    return val
def visitor_cookie_handler(request):
    visits=int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie=get_server_side_cookie(request,'last_visit',str(datetime.now()))

    last_visit_time=datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
    if(datetime.now()-last_visit_time).days>0:
        visits=visits+1
        request.session['last_visit']=str(datetime.now())
    else:
        request.session['last_visit']=last_visit_cookie
    request.session['visits']=visits
class MyRegistrationView(RegistrationView):
    def get_success_url(self,user):
        return '/novel/'

def SearchNovel(request,search_name):

    ns=novel_id(search_name)
    return render(request,'novels/searchresults.html',{'novels':ns.novels})