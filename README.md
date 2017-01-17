![](https://travis-ci.org/lemonstand/lemonsync.png?branch=master)

_LemonSync allows local editing to be easily previewed on your store. Changes made locally are automatically picked up while LemonSync is running, and applied to your stores theme. This allows developers to improve their store themes quickly and safely._

# Quickstart

_This guide will help you get lemonsync up and running as quickly as possible. For more detailed instructions, see the [Installation](Installation), [Configuration](Configuration), or [Usage](Usage) links._

### Installation
There are several ways to install LemonSync. If you have pip install, the easiest way is to simply:

`pip install lemonsync`

If these options are not available to you, you can visit the [Installation Page](https://github.com/lemonstand/lemonsync/blob/master/docs/installation.md) or [Install the Executable](https://github.com/lemonstand/lemonsync/wiki/Prebuilt-executable).

**NOTE:** If on OSX, installing with the default python installation may cause issues. If you see the error message `Could not make connection to LemonStand!
` try reinstalling `lemonsync` using the `pip` easy-install method.  

### Configuration

Once installed, create a file called `lemonstand.cfg`. Copy the following into that file:

```
[api]
api_host = https://YOUR_STORE.lemonstand.com
api_key = YOUR_PUBLIC_API_KEY
api_access = YOUR_API_TOKEN

[dir]
watch_dir = /path/to/lemonstand_projects/downloaded_theme/
file_patterns = [ "*" ]
ignore_patterns = [ "*.tmp", "*.TMP", "*/.git*", "*.DS_Store", "*/node_modules/*" ]

[store]
store_host = YOUR_STORE.lemonstand.com
```

- [Find Your API Credentials](https://docs.lemonstand.com/api/lemonstand-rest-api/introduction#authentication)
- Set your watch_dir to where you want the local theme files to be

Once done, you can call `lemonsync` in a terminal instance. If you are in the directory `lemonstand.cfg` is, it will work immediately. Otherwise, you need to specify the directory:

```
$ lemonsync -c /path/to/lemonstand.cfg
```

# Additional Resources

* [Detailed Installation](https://github.com/lemonstand/lemonsync/blob/master/docs/installation.md)
* [Detailed Configuration](https://github.com/lemonstand/lemonsync/blob/master/docs/configure.md)
* [Detailed Usage](https://github.com/lemonstand/lemonsync/blob/master/docs/usage.md)
* How to [upgrade Python](Upgrading-Python) (including upgrading Python/SSL)
