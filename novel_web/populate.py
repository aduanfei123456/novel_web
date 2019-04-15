import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','novel_web.settings')
import random
import django
django.setup()
from novel.models import Novel
import re
import asyncio
from bs4 import BeautifulSoup
from aiohttp import ClientSession
import pymysql
import urllib.request

async def getnovels(url,novelurls):

    async with ClientSession() as session:


            async with session.get(url,ssl=False) as response:
                response=await response.text(encoding='gb18030')
                web_content=BeautifulSoup(response,"lxml")

                dt1=web_content.find(id="hotcontent").find_all("dt")
                for d in dt1:
                    novelurls.append(d.a["href"])
                ncs=web_content.find(id="newscontent").find_all("li")
                print(len(ncs))
                for l in ncs:
                   novelurls.append(l.a["href"])


novel_categories={"玄幻":"https://www.biquyun.com/xuanhuan/",
                  "修真":"https://www.biquyun.com/xiuzhen/",
                  "都市":"https://www.biquyun.com/dushi/",
                  "历史":"https://www.biquyun.com/lishi/",
                   "网游":"https://www.biquyun.com/wangyou/",
                  "科幻":"https://www.biquyun.com/kehuan/",}
novelIds={}
tasks=[]
for c,u in novel_categories.items():
    novelIds[c]=[]
    tasks.append(getnovels(u,novelIds[c]))
loop=asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

catemap={"玄幻":"xuanhuan","修真":"xiuzhen","都市":"dushi","历史":"lishi",
         "网游":"wangyou","科幻":"kehuan",
         }
async def ncrawler(category,cateurls):
   main_url="https://www.biquyun.com"
   writere = re.compile(r"：([\w]+)")
   conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='',db='test',charset='utf8')
   cursor=conn.cursor()
   counter=0
   introductions = {}
   async with ClientSession() as session:
      for cateurl in cateurls:
           introductions={}
           async with session.get(cateurl, ssl=False) as response:
                   #May raise SSLError
               html=(await response.text(encoding='gb18030'))
              # print(html)
               web_content = BeautifulSoup(html, "lxml")
               introductions["category"]=category
               introductions["id"]=re.search(r'https://www.biquyun.com/(\d+_\d+)',cateurl).group(1)
               introductions["title"]=web_content.find(id="info").h1.get_text()
               info = web_content.find(id="info")
               introductions["writer"]=writere.search(info.p.get_text()).group(1)

               introductions["brief_content"]=web_content.find(id="intro").get_text()
               try:
                  htmlimg=main_url+web_content.find(id="fmimg").img["src"]
               except Exception:
                  htmlimg=None

               if(htmlimg):
                  save_path=os.path.join(os.path.abspath('..'),'static','images','{}'.format(catemap[category]),'{}.jpg'.format(counter))
                  if not(os.path.exists(save_path)):
                      async with session.get(htmlimg,ssl=False) as img:
                          imgcode=await img.read()
                          with open(save_path,'wb') as f:
                              f.write(imgcode)
                              f.close
                  introductions["img_url"]=os.path.join(catemap[category],'{}.jpg'.format(counter))
               else:
                   introductions["img_url"]="test.jpg"

               sql="insert into novel_novel(title,novel_id,img_url,category,writer,brief_content)" \
                            "values(%s,%s,%s,%s,%s,%s)"
               cursor.execute(sql,(introductions["title"],introductions["id"],introductions["img_url"],introductions["category"],
                                           introductions["writer"],introductions["brief_content"]))
               conn.commit()
               print(introductions)
               counter=counter+1

   cursor.close()
   conn.close()
   print(introductions)
tasks2=[]
for c,ids in novelIds.items():
    tasks2.append(ncrawler(c,ids))
loop = asyncio.new_event_loop()
loop.run_until_complete(asyncio.wait(tasks2))
loop.close()

#add some test examples

'''class Populate(object):
    def __init__(self):

        self.dict=[]
        self.numdict={}
        for i in range(0,10):
            s=str(i)
            self.numdict[i]=s
        with open("Chinese_Dice",'r',encoding='utf-8') as f:
            text=f.read()
        for s in text:
            if s!=" ":
                self.dict.append(s)
        print(self.dict)
    def populate(self):
        novel_pages=[]
        for i in range(100):
            novel_name=""

            for j in range(random.randint(3,8)):
                    index=random.randint(0,len(self.dict)-1)
                    novel_name+=self.dict[index]

            novel_id=""
            for i in range(4):
                novel_id+=self.numdict[random.randint(0,9)]
            novel_id+="_"
            for i in range(3):
                novel_id += self.numdict[random.randint(0, 9)]
            img_url="./img.jpg"
            temp_novel={}
            temp_novel["name"]=novel_name
            temp_novel["id"]=novel_id
            temp_novel["img_url"]=img_url
            novel_pages.append(temp_novel)

        for n in novel_pages:
            p=Novel.objects.get_or_create(novel_id=n["id"])[0]
            p.title=n["name"]
            p.img_url=n["img_url"]
            p.save()

#Novel.objects.create(title="三寸人间",writer="耳根",novel_id="14_14055",img_url="static/images/14_14055.jpg",category="修真")
novels=Novel.objects.get(novel_id="14_14055")
n=novel_crawler(novel_id="14_14055")
novels.brief_content=n.introductions["brief_content"].replace(' ','')
print(novels.brief_content)
novels.save()

#delete the test models
#Novel.objects.filter().delete()

#p=Populate()
#p.populate()
#print(Novel.objects.get())
'''