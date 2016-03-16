import urllib2
import urllib
import json
import gzip
import sys


from StringIO import StringIO

def getSynset(id,mode):
    
    service_url = 'https://babelnet.io/v1/getSynset'
    key  = 'c4acd5cc-8451-4a6c-b667-e376546f4866'
    cands = 'TOP'

    params = {
        'id' 	: id,
        'key'  	: key
    }

    if mode == '-top':
	params['cands'] = cands	

    url = service_url + '?' + urllib.urlencode(params)
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip')
    response = urllib2.urlopen(request)

    if response.info().get('Content-Encoding') == 'gzip':
        
        buf = StringIO( response.read())
        f = gzip.GzipFile(fileobj=buf)
        data = json.loads(f.read())

        print '\n'

        senses = data['senses']
        for result in senses:

            #result = senses[i]
            lemma = result.get('lemma')
            language = result.get('language')

            if language == 'EN':
                print language.encode('utf-8') + "\t" + str(lemma.encode('utf-8'))
                break

        print '\n'

        # retrieving BabelGloss data
        glosses = data['glosses']
        for result in glosses:
            language = result.get('language')
            if language == 'EN':
                gloss = result.get('gloss')
                print language.encode('utf-8') + "\t" + str(gloss.encode('utf-8'))
                break
	print '\n'

if __name__ == '__main__':

    id = sys.argv[1]
    mode = sys.argv[2]
    getSynset(id,mode)
