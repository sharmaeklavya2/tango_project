from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category, Page
from form_models import CategoryForm, PageForm

def index(request):
	context = RequestContext(request)
	category_list = Category.objects.all()
	for cat in category_list:
		cat.enc_name = cat.name.replace(' ','_')
	context_dict = {'categories': category_list}
	return render_to_response('rango/index.html', context_dict, context)

def category(request, category_enc_name):
	context = RequestContext(request)
	category_name = category_enc_name.replace('_',' ')
	context_dict = {}
	
	try:
		cat = Category.objects.get(name=category_name)
		pages = Page.objects.filter(category=cat)
		context_dict['pages']=pages
		context_dict['category']=cat
	except Category.DoesNotExist:
		return HttpResponse(category_name + " is an invalid category")
	
	return render_to_response("rango/category.html",context_dict,context)

def add_category(request):
	context = RequestContext(request)
	
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit=True)
			return index(request)
		else:
			print form.errors
			#return HttpResponse(form.errors)
	else:
		form = CategoryForm()
	
	return render_to_response("rango/add_category.html", {'form':form}, context)
