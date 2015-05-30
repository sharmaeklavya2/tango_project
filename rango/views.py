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
			#by using commit=False, we are just creating an object of type Category,
			#we are not saving it to the database right now.
			#we'll do that later by calling newcat.save()
			if len(Category.objects.filter(name=newcat.name))==0:
				newcat.save()
				context_dict["add_success"] = "Category "+newcat.name+" added successfully"
				return index(request)
			else:
				context_dict["exists_error"] = "Category already exists"
				print("Category already exists")
		else:
			print(form.errors)
			#return HttpResponse(form.errors)
	else:
		form = CategoryForm()
	
	context_dict['form']=form
	return render_to_response("rango/add_category.html", context_dict, context)
	
#def add_page(request, category_enc_name):
#	return HttpResponse("Adding pages is not yet implemented")
