from django import forms
from models import Category, Page, UserProfile
from django.contrib.auth.models import User

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
	
#	def clean(self):
#		print("TODO: implement Page URL cleaning")

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website','picture')
