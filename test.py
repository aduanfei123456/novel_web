from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import HTTPError
import re
import requests
from urllib.parse import urlencode
writere=re.compile(r"：([\w]+)")
newchapter=writere

action="/modules/article/soshu.php"
main_url = "http://www.biquyun.com/modules/article/soshu.php"


def get_novelid(search_name):
    headers = {'Content-type': "application/x-www-form-urlencoded", 'Authorization': 'APP appid = 4abf1a,token = 9480295ab2e2eddb8'}
    params = {
        'searchkey': search_name,
    }
    data_gb2312=urlencode(params,encoding='gb2312')
    main_url = "http://www.biquyun.com/modules/article/soshu.php?"+data_gb2312
    try:
        #main_url+=novel_name
        html = requests.get(main_url)
    except Exception as e:
        print(e)
    html.encoding="gb2312"
    search_content=BeautifulSoup(html.text,'lxml')
    ns=search_content.find(id="content").findAll("tr")[1:]
    novels={}
    for n in ns:
        tds=n.findAll("td")
        novel_name=tds[0].get_text()
        novels[novel_name]={}
        href=tds[0].a.get("href")
        print(href)
        id=re.search(r"/(\d+_\d+)/",href).group(1)
        novels[novel_name]["id"]=id
        novels[novel_name]["new_chapter"]=(tds[1].get_text(),tds[1].a.get('href'))
        novels[novel_name]["writer"]=tds[2].get_text()

    print(novels)
novel_name="斗破"
get_novelid(novel_name)