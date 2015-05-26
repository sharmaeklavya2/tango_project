from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
	context = RequestContext(request)
	context_dict = {
			'title':'Rango',
			'body': 'Get ready to Rango!'
		}
	return render_to_response('rango/index.html', context_dict, context)
