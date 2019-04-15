import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'novel_web.settings')

import django
django.setup()
from novel import models.Novel

if __name__=='__main__':
    print("Starting Novel populate")


class Populate(object):
    def __init__(self):
        self.dict=[]
        with open(".\Chinese_Dice.txt",'r') as f:
            str=f.read()
            str.replace(" ","")
        for s in str:
            self.dict.append(s)
        print(self.dict)
    def populate(self):
        novel_pages=[
            {"title":"a"}


        ]
p=Populate()