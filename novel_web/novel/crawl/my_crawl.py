from bs4 import BeautifulSoup
#from urllib.request import urlopen
import requests
from urllib.error import HTTPError
import re
from urllib.parse import  urlencode
class temp_search(object):
    def __init__(self,title,id,writer):
        self.title=title
        self.id=id
        self.writer=writer
class novel_id(object):
    main_url="http://www.biquyun.com/"
    def __init__(self,novel_name):
        self.novel_name=novel_name
        self.novels=self.get_novelid(self.novel_name)

    def get_novelid(self,searchname):
        #encoding=gb2312  using Get method
        headers = {'Content-type': "application/x-www-form-urlencoded",
                   'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
        params = {
            'searchkey': searchname,
        }
        data_gb2312 = urlencode(params, encoding='gb2312')

        main_url = "http://www.biquyun.com/modules/article/soshu.php?" + data_gb2312
       # print(main_url)
        try:
            # main_url+=novel_name
            html = requests.get(main_url,verify=False)
        except Exception as e:
            print(e)
        html.encoding = "gb18030"
        print(html.text)
        search_content = BeautifulSoup(html.text, 'lxml')
        #print(search_content)
        try:
            ns = search_content.find(id="content").findAll("tr")[1:]
           # print(ns)
            novels = []
            for n in ns:
                tds = n.findAll("td")
                novel_name = tds[0].get_text()

                href = tds[0].a.get("href")
               # print(href)
                id = re.search(r"/(\d+_\d+)/", href).group(1)
                title=novel_name
                id = id
                new_chapter = (tds[1].get_text(), tds[1].a.get('href'))
                writer = tds[2].get_text()
                novels.append(temp_search(title,id,writer))
               # print(novels[novel_name]["writer"])
        #page redirected
        except Exception as e:
            nurl=search_content.find(id="list").find("a")["href"]
            nid=re.search(r'/(\d+_\d+)/',nurl).group(1)
            writers=search_content.find(id="info").find("p").get_text()

            writer=writers[7:]
            print(nid)
            return [temp_search(searchname,nid,writer),]
        return novels
class novel_crawler(object):
   _main_url="http://www.biquyun.com/"
   writere = re.compile(r"：([\w]+)")
   def __str__(self):
       return str([self.introductions,self.chapters])
   def __init__(self,novel_id):
       self.novel_url=self._main_url+novel_id
       self.introductions = {}
       self.get_through()

       self.dialogs=[]
   def get_through(self):
       try:
           #May raise SSLError
           html=requests.get(self.novel_url,verify=False)
       except Exception as e:
           print(e)
       html.encoding = "gb2312"
       web_content = BeautifulSoup(html.text, "lxml")
       self.web_content=web_content
       self.introductions["title"]=web_content.find(id="info").h1.get_text()
       info = web_content.find(id="info")
       self.introductions["writer"]=self.writere.search(info.p.get_text()).group(1)
       self.introductions["newchapter"]=info.findAll("p")[3].find("a").get_text()
       self.introductions["brief_content"]=web_content.find(id="intro").get_text()
       self.chapters=[]
       self.get_chapters()
   def get_chapters(self):
        li=self.web_content.find(id="list")
        chapters=li.findAll("dd")
        indexre=re.compile("/.*/(\d+)")
        for c in chapters:
            cname=c.a.get_text()
            cindex=c.a.get('href')
            self.chapters.append((cname,indexre.search(cindex).group(1)))

class NovelPage(object):
    def __init__(self,page_url):
        self.page_url=page_url
        self.get_a_page()
    def get_a_page(self):
       try:
            html=requests.get(self.page_url,verify=False)
       except HTTPError  as e:
           print(e)
       html.encoding = "gb2312"
       web_content=BeautifulSoup(html.content,"lxml")
       self.web_content=web_content
       chapter_name=web_content.find("title").get_text().strip()
     #  print(chapter_name)
       self.chapter_name=re.search(r"(.+)_(.+)_",chapter_name,).group(1)
     #  self.title=web_content.find("div",class_="bookname").h1.string
       self.title=re.search(r'_(.+)_',chapter_name).group(1)
       self.content=web_content.find("div",id="content").get_text()
       last_href=web_content.find(class_="bottem2").find(lambda tag:tag.get_text()=="上一章").get('href')
       next_href = web_content.find(class_="bottem2").find(lambda tag: tag.get_text() == "下一章").get('href')
       try:
         self.lchapter=re.search(r"(.+)\.html",last_href).group(1)
       except(AttributeError):
           self.lchapter=None
       try:
          self.nchapter = re.search(r"(.+)\.html", next_href).group(1)
       except:
           self.nchapter=None




 #      print(title,content)

  # def sort_chapters(self):

