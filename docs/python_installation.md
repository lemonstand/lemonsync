Installation
=========

We **highly** recommend using `virtualenv` to install lemonsync.

You must have python 2.7.x or higher for ``LemonSync`` to work. If you 
have `pip`_ already installed on your system you can run the following
command to install `LemonSync`:

```
    $ [sudo] pip install lemonsync   
```

If you do not have pip installed, you can install it from source:  

```
    $ git clone git://github.com/lemonstand/LemonSync.git
    $ cd LemonSync
    $ python setup.py install   
```

**There are some issues when compiling some of the needed dependencies with Xcode on Mac OSX.**
To fix this you can upgrade XCode command line tools to the latest version and install 
lemonsync by passing some extra arguments

```
    $ [sudo] ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install lemonsync
```
