from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category, Page
from form_models import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout

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
		context_dict['base_title'] = "Rango - invalid category"
		context_dict['base_body'] = category_name + " is an invalid category"
		return render_to_response("rango/base.html", context_dict, context)
	
	return render_to_response("rango/category.html",context_dict,context)

def add_category(request):

	context = RequestContext(request)
	context_dict  = {}
	
	if request.user.is_authenticated():
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

	else:
		context_dict['base_title'] = "Rango - not logged in"
		context_dict['base_body'] = "You can't add categories because you are not logged in"
		return render_to_response("rango/base.html", context_dict, context)
	
def add_page(request, category_enc_name):
	context = RequestContext(request)
	category_name = category_enc_name.replace('_',' ')
	context_dict = {'category_name':category_name, 'category_enc_name':category_enc_name}
	
	try:
		cat = Category.objects.get(name=category_name)
		if request.user.is_authenticated():
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
		else:
			context_dict['base_title'] = "Rango - not logged in"
			context_dict['base_body'] = "You can't add pages because you are not logged in"
			return render_to_response("rango/base.html", context_dict, context)
	except Category.DoesNotExist:
		context_dict['base_title'] = "Rango - invalid category"
		context_dict['base_body'] = category_name + " is an invalid category"
		return render_to_response("rango/base.html", context_dict, context)
	
	return render_to_response("rango/add_page.html", context_dict, context)
	
def register(request):
	context = RequestContext(request)
	context_dict = {}
	register_success = False
	
	if request.method=="POST":
		uform = UserForm(request.POST)
		upform = UserProfileForm(request.POST)
		if uform.is_valid() and upform.is_valid():
			user = uform.save()
			user.set_password(user.password)
			user.save()
			
			uprofile = upform.save(commit = False)
			uprofile.user = user
			if 'picture' in request.FILES:
				uprofile.picture = request.FILES['picture']
			uprofile.save()
			context_dict["reg_success"]="Registration successful"
	else:
		uform = UserForm()
		upform = UserProfileForm()
	context_dict['uform'] = uform
	context_dict['upform'] = upform
	return render_to_response("rango/register.html", context_dict, context)

def user_login(request):
	context = RequestContext(request)
	context_dict = {}
	if request.method=="POST":
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(username=username,password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect("/rango/")
			else:
				context_dict["login_error"]="Your account has been disabled."
		else:
			context_dict["login_error"]="Failed to authenticate. Check username and password."
	return render_to_response("rango/login.html", context_dict, context)

def user_logout(request):
	if request.user.is_authenticated():
		logout(request)
		return HttpResponseRedirect("/rango/")
	else:
		context = RequestContext(request)
		context_dict={
			"base_body":'You are already logged out.',
		}
		return render_to_response("rango/base.html", context_dict, context)

from bing_search import run_query

def search(request):
	context = RequestContext(request)
	context_dict = {}
	
#	context_dict['base_title']="Rango - Search"
#	context_dict['base_body']="Search is not yet implemented"
	
	if request.method=="POST":
		query = request.POST["query"].strip()
		if query:
			result_list = run_query(query)
			context_dict["result_list"] = result_list
	
	return render_to_response("rango/search.html", context_dict, context)
