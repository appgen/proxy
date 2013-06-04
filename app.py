import os
import urllib2

from flask import request
from flask import Flask
from flask import Response

app = Flask(__name__)
SEED = ##seed##
CANONICAL = 'http://appgen.me/a/'

querystring = '?seed=' + unicode(SEED)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = CANONICAL + path + querystring
    f = urllib2.urlopen(url)
    response = f.read().replace(querystring, '') # remove seed
    status = f.getcode()
    headers = f.headers.dict
    content_type = headers.get('content-type', 'text/html')
    return Response(response=response, status=status, headers=headers, content_type=content_type)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
