from bs4 import BeautifulSoup
#from urllib.request import urlopen
import requests
from urllib.error import HTTPError
import re
from urllib.parse import  urlencode
class novel_id(object):
    main_url="http://www.biquyun.com/"
    def __init__(self,novel_name):
        self.novel_name=novel_name
        self.get_novelid

    def get_novelid(search_name):
        #encoding=gb2312  using Get method
        headers = {'Content-type': "application/x-www-form-urlencoded",
                   'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
        params = {
            'searchkey': search_name,
        }
        data_gb2312 = urlencode(params, encoding='gb2312')
        main_url = "http://www.biquyun.com/modules/article/soshu.php?" + data_gb2312
        try:
            # main_url+=novel_name
            html = requests.get(main_url)
        except Exception as e:
            print(e)
        html.encoding = "gb2312"
        search_content = BeautifulSoup(html.text, 'lxml')
        ns = search_content.find(id="content").findAll("tr")[1:]
        novels = {}
        for n in ns:
            tds = n.findAll("td")
            novel_name = tds[0].get_text()
            novels[novel_name] = {}
            href = tds[0].a.get("href")
            print(href)
            id = re.search(r"/(\d+_\d+)/", href).group(1)
            novels[novel_name]["id"] = id
            novels[novel_name]["new_chapter"] = (tds[1].get_text(), tds[1].a.get('href'))
            novels[novel_name]["writer"] = tds[2].get_text()
        return novels
class novel_crawler(object):
   _main_url="http://www.biquyun.com/"
   writere = re.compile(r"：([\w]+)")

   def __init__(self,novel_id):
       self.novel_url=self._main_url+novel_id
       self.get_through()
       self.introductions={}
       self.dialogs=[]
   def get_through(self):
       try:
           html=requests.get(self.novel_url)
       except HTTPError as e:
           print(e)
       web_content = BeautifulSoup(html.text, "lxml")
       self.web_content=web_content
       self.introductions["title"]=web_content.find(id="info").h1.get_text()
       info = web_content.find(id="info")
       self.introductions["writer"]=self.writere.search(info.p.get_text()).group(2)
       self.introductions["newchapter"]=info.findAll("p")[3].find("a").get_text()
       self.chapters={}
       self.get_chapters()
   def get_chapters(self):
        li=self.web_content.find(id="list")
        chapters=li.findAll("dd")
        indexre=re.compile("/.*/(\d+)")
        for c in chapters:
            cname=c.a.get_text()
            cindex=c.a.get('href')
            self.chapters[cname]=indexre.search(cindex).group(1)
   def get_a_page(self,page_url=None):
       try:
            html=requests.get(page_url)
       except HTTPError  as e:
           print(e)
       web_content=BeautifulSoup(html.content,"lxml")
       title=web_content.find("div",class_="bookname").h1.string
       content=web_content.find("div",id="content").get_text()
       print(title,content)

