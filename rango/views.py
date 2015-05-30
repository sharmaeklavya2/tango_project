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
	context_dict  = {}
	
	if request.method == "POST":
		form = CategoryForm(request.POST)
		if form.is_valid():
			newcat = form.save(commit=False)
			if len(Category.objects.filter(name=newcat.name))==0:
				newcat.save()
				context_dict["add_success"] = "Category "+newcat.name+" added successfully"
			else:
				context_dict["exists_error"] = "Category already exists"
				print("Category already exists")
	else:
		form = CategoryForm()
	
	context_dict['form']=form
	return render_to_response("rango/add_category.html", context_dict, context)
	
def add_page(request, category_enc_name):
	context = RequestContext(request)
	category_name = category_enc_name.replace('_',' ')
	context_dict = {'category_name':category_name, 'category_enc_name':category_enc_name}
	
	try:
		cat = Category.objects.get(name=category_name)
		if request.method=="POST":
			form = PageForm(request.POST)
			if form.is_valid():
				page = form.save(commit=False)
				page.category=cat
				page.save()
				context_dict["add_success"]="The page "+page.title+" was successfully added"
		else:
			form = PageForm()
		context_dict['form']=form
	except Category.DoesNotExist:
		pass
		# form is not added to context_dict when category is invalid
		# the add_page template depends on this behavior to determine if category is invalid
	
	return render_to_response("rango/add_page.html", context_dict, context)
