import urllib2
import urllib
import json
import gzip
import sys
import os

import babelInfo

from StringIO import StringIO

def disambiguate(text,info_arg):

	service_url = 'https://babelfy.io/v1/disambiguate'

	#print "String '" + text + "' to be disambiguated..."

	lang = 'EN'
	match = 'PARTIAL_MATCHING'
	key = 'c4acd5cc-8451-4a6c-b667-e376546f4866'

	params = {
		'text'  : text,
		'lang'  : lang,
		'match' : match,
		'key'   : key	
	}

	url = service_url + '?' + urllib.urlencode(params)

	print "Service URL: " + url

	request = urllib2.Request(url)
	request.add_header('Accept-encoding', 'gzip')
	response = urllib2.urlopen(request)

	if response.info().get('Content-Encoding') == 'gzip':

		buffer = StringIO(response.read())
		file = gzip.GzipFile(fileobj=buffer)
		data = json.loads(file.read())

		print "Babelnet synset IDs:"

		for result in data:
			synsetId = result.get('babelSynsetID')
                	print synsetId
		
			run = 'python babelInfo.py ' + synsetId + ' ' + info_arg
			os.system(run)

if __name__ == '__main__':

	mode = sys.argv[1]
	info_arg = sys.argv[2]

	if mode == '-s':
		
		while True:
			txt = raw_input("Input a sentence:  ")
			
			if txt == 'exit!':
			   print 'Bye.'
			   sys.exit(0)
			else:
			   print txt
			   disambiguate(txt)
		
	elif mode == '-a':
		sentence = sys.argv[3]
		#print sentence
		disambiguate(sentence,info_arg)
		
		sys.exit(0)
        else:
		print 'Option ' + mode + ' not found.  Exiting.'
		sys.exit(1) 
