from django.db import models

class Category(models.Model):
	name = models.CharField(max_length=128)
	
	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=64)
	views = models.IntegerField(default=0)
	url = models.URLField()
	
	def __unicode__(self):
		return self.title

