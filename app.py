import os
import urllib2

from flask import request
from flask import Flask
from flask import Response

app = Flask(__name__)
SEED = ##seed##
APPGEN = 'http://appgen.me/'

querystring = '?seed=' + unicode(SEED)

@app.route('/favicon.ico')
def favicon():
    return Response(status = 404)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    if (len(path) >= 2 and path[:2] == 'js') or (len(path) >= 3 and path[:3] == 'css'):
        upstream_path = APPGEN + path
    else:
        upstream_path = APPGEN + 'a/' + path

    url = upstream_path + querystring
    try:
        f = urllib2.urlopen(url)
        response = f.read().decode('utf-8').replace(querystring, '') # remove seed
        status = f.getcode()
        headers = f.headers.dict
        content_type = headers.get('content-type', 'text/html')
        return Response(response=response, status=status, headers=headers, content_type=content_type)
    except:
        print 'Error at ' + url
        raise
        return Response(response = '', status = 404)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
