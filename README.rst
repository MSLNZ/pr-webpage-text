===============
PR-WebPage-Text
===============
Update and view text on a web page.

This packages allows one to send text to a web server so that a web browser
can display the text. The motivation for creating this package comes from
wanting to view data (e.g., data that is acquired from a digital multimeter)
on a tablet, phone or another computer by simply opening a web browser and
entering the appropriate URL.

The web server runs on Python. However, any program that can send a PUT_
message can update the text on the web browser and any browser can be used
to view the text.

Installation
------------
You only need to install this package on the computer that you want to be
the web server.

To install the web server run

.. code-block:: console

   pip install https://github.com/MSLNZ/pr-webpage-text/archive/master.zip

Alternatively, using the `MSL Package Manager`_

.. code-block:: console

   msl install pr-webpage-text

This will create a ``webpage-text`` executable in the ``<python>/Scripts`` directory.

Dependencies
++++++++++++
* Python 2.7, 3.5+
* Flask_
* gevent_

Configuration File
------------------
The following options can be specified in a configuration file. The ``values`` in the
``[endpoints]`` section is the only key-value pair that is mandatory. All other key-value
pairs will be set to a default value if they are not specified in the configuration file.

.. code-block:: ini

   [server]
   # The hostname or IP address of the server.
   host=0.0.0.0

   # The port to run the server on.
   port=1683

   # Whether to use Flask's built-in server (also enables debug mode).
   # Otherwise gevent's WSGI server is used.
   use_flask_server=false

   [defaults]
   # The initial text to display on each web page.
   text=Send some data!

   # The font size (in px) of the text.
   size=200

   # The number of seconds for the client's web browser to
   # wait before it performs an automatic Refresh.
   refresh=1.0

   [endpoints]
   # Endpoints can be any text you want (e.g. they can be the name of
   # a lab or a person). For example, if the following values were
   # defined then the URL's to enter in a web browser would be
   # (assuming that the web server is running on the local computer):
   # http://127.0.0.1:1683/spectrophotometer
   # http://127.0.0.1:1683/joe
   values=spectrophotometer, joe

Usage
-----
To start the web server run

.. code-block:: console

   webpage-text --config my_config.ini

If a file named ``config.ini`` exists in the current working directory then
you do not have to specify it since it will automatically be loaded

.. code-block:: console

   webpage-text

When you start the web server you will see the value of the ``host`` and ``port``
that it is running on (i.e., ``http://host:port/``). You will need to know these
values when you send text to the web server or when you visit a web page.

Start the web server using the above configuration file (copy and paste to create the
``config.ini`` file). Open a web browser and enter the following URL
``http://127.0.0.1:1683/spectrophotometer``. You will see the text ``Send some data!``
and the page will automatically refresh every second.

The text on the web page won't change unless someone sends a PUT_ message to the
``/spectrophotometer`` endpoint on the server. The ``body`` of a PUT_ must be a JSON_
string with the following structure

.. code-block:: text

   {
     'text': string,    # the text to display in the web page
     'size': integer,   # the font size (in px)
     'refresh': float,  # how often the browser will automatically refresh
   }

There are examples_ in the ``examples`` directory for sending a PUT_ message to a
web server. Download_ and extract the package to run one of the examples to see the
text on the ``/spectrophotometer`` or ``/joe`` web page change.

.. _PUT: https://tools.ietf.org/html/rfc7231#section-4.3.4
.. _MSL Package Manager: https://msl-package-manager.readthedocs.io/en/latest/
.. _Flask: https://pypi.org/project/Flask/
.. _gevent: https://pypi.org/project/gevent/
.. _JSON: https://www.json.org/json-en.html
.. _examples: https://github.com/MSLNZ/pr-webpage-text/tree/master/examples
.. _Download: https://github.com/MSLNZ/pr-webpage-text/archive/master.zip
