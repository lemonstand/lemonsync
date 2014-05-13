LemonSync
=========

lemonsync 0.1.5

Released: 1-May-2014

.. image:: https://pypip.in/download/LemonSync/badge.png
    :target: https://pypi.python.org/pypi//LemonSync/
    :alt: Downloads


**LemonSync** will listen for changes in the folder you configure, and
automatically push updates to your store theme. This is helpful if you
want to add your theme under version control, or prefer to work locally
rather than in the LemonStand UI.

Installation
------------

We **highly** recommend using `virtualenv` to install lemonsync.

You must have python 2.7.x or higher for ``LemonSync`` to work. If you 
have `pip`_ already installed on your system you can run the following
command to install `LemonSync`:

::

    $ [sudo] pip install lemonsync   

If you do not have pip installed, you can install it from source:  

::

    $ git clone git://github.com/lemonstand/LemonSync.git
    $ cd LemonSync
    $ python setup.py install   

**There are some issues when compiling some of the needed dependencies with Xcode on Mac OSX.**
To fix this you can upgrade XCode command line tools to the latest version and install 
lemonsync by passing some extra arguments

::

    $ [sudo] ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install lemonsync


Configuration
-------------

You need to create a configuration file, which can be named anything you
like, for example ``config.cfg``. See below for an example which can
be copied. Just be sure to change the values ``api_key``, ``api_access``, 
``watch_dir`` and ``store_host``. In order to obtain your ``api_key`` 
and ``api_access`` token, you will need to login to your store backend, 
and under the ``Settings`` tab is a section named ``API``, where you can 
generate a private API key for ``LemonSync``.

::

    [api]
    api_host = https://api.lemonstand.com
    api_key = YOUR_API_KEY
    api_access = YOUR_API_TOKEN

    [dir]
    watch_dir = /path/to/your/local/theme/

    [store]
    store_host = YOUR_STORE.lemonstand.com  


Usage
-----

Once installed, you can run ``lemonsync`` from the command line. 
To stop the program type ``Ctrl-C``.

::

    $ lemonsync --config=path/to/your/config.cfg   

Version `0.1.6` instroduced two new command line arguments.

::

    $ lemonsync --config=path/to/your/config.cfg --reset=local   

This will completely replace the contents of `watch_dir` set in `path/to/your/config.cfg`
with the contents of your remote theme. All files and folders except `.git*` will be removed.
**This is an advanced feature and should be used with caution!**

::

    $ lemonsync --config=path/to/your/config.cfg --reset=remote   

This will completely replace the contents of your remote theme with the content
in `watch_dir`, set in `path/to/your/config.cfg`.

**This is an advanced feature and should be used with caution! If not careful, you
could end up deleting your entire remote theme!** 

Getting Started
---------------

To get started using LemonSync, you should download the theme you will
be editing from your LemonStand store. This can be down through the
backend export option found at ``/backend/cms/theme``. Once you have
your theme unzipped on your local machine, you can set the full path to
the theme folder as your ``watch_dir`` directory in your configuration.

Caching
~~~~~~~

By default, LemonStand caches all CMS objects (pages, partials, etc.).
In order to use LemonSync, you will want to temporarily disable caching.

1. Log into your store as the administrator.
2. Navigate to ``/backend/cms/settings`` and select **Disable CMS cache
   for backend users**.

With this enabled, the cache will be skipped when a user is logged in to
the backend, allowing you to always see the current versions of pages.
**Note:** Caching will remain disabled only while the administrator is
logged in. Once logged out, caching will resume regardless of whether or
not the CMS cache has been disabled.

Pages
~~~~~

Any new pages that you add are automatically registered with LemonStand
when uploaded. You can set properties on the page such as the ``url``
and ``name`` of the page, by adding a header to the top of the page. See
below for an example.

::

    ---
    template: inner
    protocol: all
    published: true
    name: About
    url: /about
    ---

TODO
----

-  When LemonSync starts, check if the theme has been modified somewhere else.
   If it has, ask the user if they want to upload their local files, 
   or pull the remote theme to their local version.
-  Make it easy for multiple developers to work on the same theme.

.. _pip: http://www.pip-installer.org/