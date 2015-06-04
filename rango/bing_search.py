#!/usr/bin/python2

import json
import urllib, urllib2
import os

def run_query(search_terms):
	root_url = 'https://api.datamarket.azure.com/Bing/Search/v1/'
	source = 'Web'
	
	results_per_page=10
	offset=0
	
	query = urllib.quote("'{0}'".format(search_terms))
	
	search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
		root_url,source,results_per_page,offset,query)
	
	username = ''
	keypath = os.path.join(os.path.dirname(__file__),"bing_api_key.txt")
	ifile = open(keypath)
	bing_api_key = ifile.read().strip()
	ifile.close()
	
	password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
	password_mgr.add_password(None, search_url, username, bing_api_key)
	
	results = []
	
	try:
		handler = urllib2.HTTPBasicAuthHandler(password_mgr)
		opener = urllib2.build_opener(handler)
		urllib2.install_opener(opener)
		
		response = urllib2.urlopen(search_url).read()
		json_response = json.loads(response)
		
		for result in json_response['d']['results']:
			results.append({
				'title':result['Title'],
				'link':result['Url'],
				'summary':result['Description']})
	
	except urllib2.URLError, e:
		print("Error when querying Bing API:")
		print(e)
	
	return results
