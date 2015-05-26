def add_cat(name):
	return Category.objects.get_or_create(name=name)[0]

def add_page(cat, title, url, views=0):
	return Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]

def populate():
	cat_dict = {}
	
	ifile = open("pop_data.txt")
	for line in ifile:
		cat_name, title, url = line.split('\t')
		if cat_name in cat_dict:
			cat = cat_dict[cat_name]
		else:
			cat = add_cat(cat_name)
			cat_dict[cat_name] = cat
		add_page(cat, title, url)
	
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c),str(p))

if __name__=='__main__':
	import os
	"Starting Rango Population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_project.settings')
	from rango.models import Category, Page
	populate()
