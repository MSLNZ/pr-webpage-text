"""
Example script to put text on the web server at a particular endpoint.
"""
import re
import requests           # Run: pip install requests

host = '127.0.0.1'         # hostname or IP address of the server
port = 1683                # port number of the server
lab = 'spectrophotometer'  # the name of the endpoint on the server to send the text to
text = 'Hello<br>World!'   # the text to display
size = 200                 # font size of the text
refresh = 0.5              # number of seconds for a web browser to wait before it automatically refreshes

reply = requests.put(f'http://{host}:{port}/{lab}', json={'text': text, 'size': size, 'refresh': refresh})
if not reply.ok:
    matches = re.findall(r'/(\w+)</p>', reply.content.decode())
    raise ValueError('Invalid endpoint {!r}. Must be one of: {}'.format(lab, ', '.join(matches)))
