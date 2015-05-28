def add_cat(name,views,likes):
	return Category.objects.get_or_create(name=name,views=views,likes=likes)[0]

def add_page(cat, title, url, views=0):
	return Page.objects.get_or_create(category=cat, title=title, url=url, views=views)[0]

def populate():
	cat_dict = {}
	
	ifile = open("rango_pop_data/category.txt")
	for line in ifile:
		views=0
		likes=0
		words=line.split('\t')
		if len(words) < 1:
			continue
		else:
			cat_name = words[0]
			if len(words) >=2:
				views = int(words[1])
			if len(words) >=3:
				likes = int(words[2])
		cat_dict[cat_name] = add_cat(cat_name,views,likes)
	ifile.close()
	
	ifile = open("rango_pop_data/page.txt")
	for line in ifile:
		views = 0
		words = line.split('\t')
		if len(words) < 3:
			continue
		else:
			cat_name, title, url = words[0:3]
			if url[-1]=='\n':
				url = url[:-1]
		if len(words) == 4:
			views = int(words[3])
		add_page(cat_dict[cat_name], title, url, views)
	ifile.close()
	
	for c in Category.objects.all():
		for p in Page.objects.filter(category=c):
			print "- {0} - {1}".format(str(c),str(p))

if __name__=='__main__':
	import os
	"Starting Rango Population script..."
	os.environ.setdefault('DJANGO_SETTINGS_MODULE','tango_project.settings')
	from rango.models import Category, Page
	populate()
