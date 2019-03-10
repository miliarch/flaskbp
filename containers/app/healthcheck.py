import urllib.request
import json
import sys

try:
    response = urllib.request.urlopen('http://localhost:5000/status')
    response_json = json.loads(response.read().decode('utf-8'))
    if not response_json['status'] == 'healthy':
        sys.exit(1)
except:
    sys.exit(1)
