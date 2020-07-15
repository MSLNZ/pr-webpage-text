===============
PR-Webpage-Text
===============
Update and view text on a web page.

This packages allows one to send text to a web server so that a web browser
can display the text. The motivation for creating this package comes from
wanting to view data (e.g., data that is acquired from a digital multimeter)
on a tablet, phone or another computer by simply opening a web browser and
entering the appropriate URL.

The web server runs on Python; however, any program that can send a PUT_
request can update the text that is displayed on the web page and any web
browser can be used to view the text.

A single server instance can handle requests for multiple URL endpoints.

Installation
------------
You only need to install this package on a computer that you want to be the
web server or if you want to send a PUT_ request to the web server. You do
not need to install it on the device that is displaying the text through a
web browser.

To install the package run

.. code-block:: console

   pip install https://github.com/MSLNZ/pr-webpage-text/archive/master.zip

Alternatively, using the `MSL Package Manager`_

.. code-block:: console

   msl install pr-webpage-text

This will create a ``webpage-text`` executable that is available to the Python
interpreter.

Dependencies
++++++++++++
* Python 3.5+
* Flask_
* gevent_
* requests_

Usage
-----
When you start the web server the value of the ``host``, ``port`` and ``endpoint``
will be displayed in the terminal (e.g., ``http://host:port/endpoint``). You will
need to know these values when you send a PUT_ request to the web server or when
you want to view the text in a web browser.

To start the web server you must, at the very least, specify the URL endpoints
that you want to be available. For example,

.. code-block:: console

   webpage-text --endpoints spectrophotometer joe

This will start the web server using the default settings. Open a web browser and
enter the following URL ``http://127.0.0.1:1683/spectrophotometer`` or
``http://127.0.0.1:1683/joe``.

The text on the web page won't change unless a PUT_ request is made to the
``spectrophotometer`` or the ``joe`` endpoint on the server. The ``body`` of a PUT_
request must be a JSON_ object with the following structure

.. code-block:: text

   {
     'text': string,    # the text to display in the web page
     'size': integer,   # the font size (in px)
     'refresh': float,  # how often the web browser will automatically refresh
   }

For a description of all supported command line arguments run

.. code-block:: console

   webpage-text --help

There are examples_ in the ``examples`` directory for sending a PUT_ request to the
web server. Download_ and extract the package to run one of the examples to see the
text on the ``spectrophotometer`` or ``joe`` endpoint to change.

Configuration File
------------------
You can also save the web-server settings in an INI-type configuration file and
load the settings from the terminal

.. code-block:: console

   webpage-text --config my_web_server_settings.ini

The following options can be specified in the configuration file. The ``endpoints``
key in the ``[server]`` section is the only key-value pair that is mandatory. All
other key-value pairs will be set to a default value if they are not specified
in the configuration file.

.. code-block:: ini

    [server]
    # The hostname or IP address of the server
    host=0.0.0.0

    # The port to run the server on
    port=1683

    # Endpoints can be any text you want (e.g. they can be the name of
    # a lab or a person). For example, if the following values were
    # defined then the URL's to enter in a web browser would be
    # (assuming that the web server is running on the local computer):
    # http://127.0.0.1:1683/spectrophotometer
    # http://127.0.0.1:1683/joe
    endpoints=spectrophotometer, joe

    # Whether to use the built-in server of flask (which runs in debug mode)
    # or to use the WSGI server of gevent
    use_flask=false

    # Whether to enable INFO log messages from the gevent WSGI server
    enable_log=false

    [text]
    # The initial text to display at each endpoint
    initial=Hello world!

    # The font size (in px) of the text
    size=500

    # The number of seconds for a web browser to wait before automatically
    # refreshing the web page
    refresh=0.1

.. _PUT: https://tools.ietf.org/html/rfc7231#section-4.3.4
.. _MSL Package Manager: https://msl-package-manager.readthedocs.io/en/latest/
.. _Flask: https://pypi.org/project/Flask/
.. _gevent: https://pypi.org/project/gevent/
.. _requests: https://pypi.org/project/requests/
.. _JSON: https://www.json.org/json-en.html
.. _examples: https://github.com/MSLNZ/pr-webpage-text/tree/master/examples
.. _Download: https://github.com/MSLNZ/pr-webpage-text/archive/master.zip
