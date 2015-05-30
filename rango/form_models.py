from django import forms
from models import Category, Page

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text="Enter category name")
	
	class Meta:
		model = Category
		fields = ('name',)

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=64, help_text="Enter title")
	url = forms.URLField(max_length=128, help_text="Enter URL")
	
	class Meta:
		model = Page
		fields = ('title','url')
