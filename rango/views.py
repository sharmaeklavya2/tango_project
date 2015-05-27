from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Category

def index(request):
	context = RequestContext(request)
	context_dict = {'categories': Category.objects.all()}
	return render_to_response('rango/index.html', context_dict, context)
