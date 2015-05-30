from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	likes = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=64)
	views = models.IntegerField(default=0)
	url = models.URLField()
	
	def __unicode__(self):
		return self.title

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	website = models.URLField(blank=True)
	picture = models.ImageField(blank=True, upload_to='profile_images')
	
	def __unicode__(self):
		return self.user.username	
