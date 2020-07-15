"""
Example script to put messages on a web server at a particular endpoint.

This example assumes that a `spectrophotometer` endpoint is available
on the web server.

Make sure the web server is running on the same computer and then open
a web browser and go to http://127.0.0.1:1683/spectrophotometer

Run this example script and watch the messages appear on the web page.
"""
from time import sleep

from webpage_text import put

# the messages to send
messages = [
    '1.23456789',
    'Multi\nline\nmessage',        # you can use \n for a new line
    'Hello<br>World!',             # or use the <br> HTML tag for a new line
    '-9.73&plusmn;0.05 &micro;V',  # you can use HTML characters
    'Goodbye... &#128542;',        # and HTML symbols
    '',
]

# the name of the endpoint on the server to send the messages to
endpoint = 'spectrophotometer'

# send each message
for message in messages:
    put(message, endpoint)
    sleep(5)
