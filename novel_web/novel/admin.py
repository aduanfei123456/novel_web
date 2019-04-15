from django.contrib import admin
from .models import  Novel
from .models import UserProfile
# Register your models here.
admin.site.register(Novel)
admin.site.register(UserProfile)