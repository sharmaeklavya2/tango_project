from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category, Page, UserProfile
from form_models import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

def index(request):
	context = RequestContext(request)
	category_list = Category.objects.all()
	for cat in category_list:
		cat.enc_name = cat.name.replace(' ','_')
	context_dict = {'categories': category_list}
	return render_to_response('rango/index.html', context_dict, context)

def to_be_made(request):
	context = RequestContext(request)
	context_dict = {'base_body': "This page is yet to be implemented"}
	return render_to_response("rango/base.html", context_dict, context)

def category(request, category_enc_name):
	context = RequestContext(request)
	category_name = category_enc_name.replace('_',' ')
	context_dict = {}
	
	try:
		cat = Category.objects.get(name=category_name)
		cat.views+=1
		cat.save()
		pages = Page.objects.filter(category=cat).order_by('-views')
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
#	register_success = True
	
	if request.method=="POST":
		uform = UserForm(request.POST)
		upform = UserProfileForm(request.POST)
		if uform.is_valid() and upform.is_valid():
			user = uform.save(commit=False)
			user.set_password(user.password)
			if user.email=="":
				context_dict["reg_error"]="Email address is required"
			elif User.objects.filter(email=user.email).count() > 0:
				context_dict["reg_error"]="This email address is already in use"
			else:
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
		
		#if username is invalid, treat it as email and try to get real username
		if User.objects.filter(username=username).count()==0:
			emails = User.objects.filter(email=username)
			if emails.count()==1:
				username = emails[0].username
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
	
	if request.method=="POST":
		query = request.POST["query"].strip()
		if query:
			result_list = run_query(query)
			context_dict["result_list"] = result_list
	
	return render_to_response("rango/search.html", context_dict, context)

def goto_page_url(request):
	context = RequestContext(request)
	context_dict = {}
	
	url="/rango/"
	try:
		if request.method=="GET" and ('page_id' in request.GET):
			page_id = request.GET["page_id"]
			page = Page.objects.get(id=page_id)
			page.views+=1
			page.save()
			url = page.url
			
	except Page.DoesNotExist:
		pass
			
	return HttpResponseRedirect(url)

def view_all_users(request):
	context = RequestContext(request)
	context_dict = {}
	users = User.objects.all()
	context_dict["users"] = users
	context_dict["no_of_users"] = len(users)
	return render_to_response("rango/view_all_users.html", context_dict, context)

def view_user(request, username):
	context = RequestContext(request)
	context_dict = {'username':username}
	
	try:
		cuser = User.objects.get(username=username)
		context_dict['cuser'] = cuser
		cuprofile = UserProfile.objects.get(user=cuser)
		context_dict['cuprofile'] = cuprofile
		img_src = cuprofile.picture.name
		if img_src:
			img_src = (settings.MEDIA_URL+img_src)
		context_dict["img_src"] = img_src
	except User.DoesNotExist:
		pass
	
	return render_to_response("rango/view_user.html", context_dict, context)

def edit_profile(request):
	context_dict = {}

	if not request.user.is_authenticated():
		context_dict['base_title'] = "Rango - not logged in"
		context_dict['base_body'] = "You must log in to edit your profile."
		return render_to_response("rango/base.html", context_dict, context)

	user = User.objects.get(username=request.user.username)
	uprofile = UserProfile.objects.get(user=user)
	context_dict["uprofile"] = uprofile
	
	if request.method=="POST":
		#set name
		user.first_name = request.POST["first_name"]
		user.last_name = request.POST["last_name"]
		user.save()
		request.user=user
		#set email
		email = request.POST["email"]
		if not email:
			context_dict["reg_error"]="Email cannot be blank"
		elif email!=user.email and User.objects.filter(email=email).count()>0:
			context_dict["reg_error"]="The email address "+email+" is already in use"
		else:
			user.email=email
			user.save()
			request.user=user
		
		upform = UserProfileForm(request.POST, instance=uprofile)
		if upform.is_valid():
			uprofile = upform.save(commit=False)
			if 'picture' in request.FILES:
				uprofile.picture = request.FILES['picture']
			uprofile.save()
		upform = UserProfileForm(request.POST, instance=uprofile)
	else:
		#get current user's secondary data
		upform = UserProfileForm(instance=uprofile)

	img_src = uprofile.picture.name
	if img_src:
		img_src = (settings.MEDIA_URL+img_src)
	context_dict["img_src"] = img_src
	
	context_dict['upform']=upform;
	return render_to_response("rango/edit_profile.html", context_dict, RequestContext(request))

def change_password(request):
	context = RequestContext(request)
	context_dict={}
	
	if not request.user.is_authenticated():
		context_dict['base_title'] = "Rango - not logged in"
		context_dict['base_body'] = "You must log in to change your password."
		return render_to_response("rango/base.html", context_dict, context)
	
	if request.method=="POST":
		pass1 = request.POST["pass1"]
		pass2 = request.POST["pass2"]
		if pass1!=pass2:
			context_dict["pass_error"] = "Passwords do not match"
		elif pass1=="":
			context_dict["pass_error"] = "Password can't be empty"
		else:
			request.user.set_password(pass1)
			request.user.save()
			context_dict["base_title"] = "Rango - password changed"
			context_dict["base_body"] = "Your password has been changed successfully."
			return render_to_response("rango/base.html", context_dict, context)

	return render_to_response("rango/change_password.html", context_dict, context)

def like_category(request):
	#returning 0 means error
	if request.user.is_authenticated() and request.method=="GET" and 'category_id' in request.GET:
		category_id=request.GET['category_id']
		try:
			category = Category.objects.get(id=int(category_id))
			category.likes+=1
			category.save()
			return HttpResponse(category.likes)
		except Category.DoesNotExist:
			pass
	return HttpResponse(0)
