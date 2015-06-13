from django.contrib import admin
from models import Category, Page, UserProfile
from django.contrib.admin import ModelAdmin

class CategoryAdmin(ModelAdmin):
	list_display=('name','views','likes')

class PageAdmin(ModelAdmin):
	list_display=('title','category','url','views')

class UserProfileAdmin(ModelAdmin):
	list_display=('user','website')

admin.site.register(Category,CategoryAdmin)
admin.site.register(Page,PageAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
