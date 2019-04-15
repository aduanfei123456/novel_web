from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
#slugify change "how do i create a slug in django"  into  "how-do-i-create-a-slug-in-django"。
class Novel(models.Model):
    title=models.CharField(max_length=150,default="无名")
    novel_id=models.CharField(max_length=150,default="1111_00")
    img_url=models.CharField(max_length=150,default="test.jpg")
    category=models.CharField(max_length=150,default="玄幻")
    writer=models.CharField(max_length=150,default="佚名")
    brief_content=models.CharField(max_length=400,default="不错不错")
    hot=models.IntegerField(default=0)
    #slug=models.SlugField(default="玄幻",blank=True)
    #for debug print
    def __str__(self):
        return self.title
    '''def save(self,*args,**kwargs):
        self.slug=slugify(self.category)
        super(Novel,self).save(*args,**kwargs)
    class Meta:
        verbose_name_plural='categories'''
class UserNovel(models.Model):
    novel_id=models.CharField(max_length=150,default="1111_00")
    user_name=models.CharField(max_length=150,default="anoymous")
    praise=models.BooleanField(default=False)
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)

    colnodels=models.CharField(max_length=150)

    #upload to media/profile_images/
    picture=models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username