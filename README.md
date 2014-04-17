#LemonSync

**LemonSync** will listen for changes in the folder you configure, and automatically push updates to your store theme. This is helpful if you want to add your theme under version control, or prefer to work locally rather than in the LemonStand UI.

##Installation

You must have python 2.7.x or higher for `LemonSync` to work. Also, please make sure you have the needed libraries installed. If you have `pip` already installed on your system you can run the following commands to install them.

`sudo pip install watchdog`  
`sudo pip install boto`

If you do not have pip installed, you can also install those libraries using `easy_install`. 

##Configuration

You need to set your configuration values, which are located in `config.cfg`. The settings below will be provided to you by LemonStand technical support.

- `aws_access_key`
- `aws_secret_key`
- `bucket`
- `name` 
- `theme`

You need to set the directory that will watch for changes.
- `watch` Remember to add a trailing slash.

##Usage

Once you have cloned this repository onto your machine, you can simply run `python LemonSync.py` from your command line. To stop the program type `Ctrl-C`.

##Getting Started

To get started using LemonSync, you should download the theme you will be editing from your LemonStand store. This can be down through the backend export option found at `/backend/cms/theme`. Once you have your theme unzipped on your local machine, you can set the full path to the theme folder as your `watch` directory. 

###Caching

By default, LemonStand caches all CMS objects (pages, partials, etc.). In order to use LemonSync, you will want to temporarily, disable caching.

1. Log into your store as the administrator.
2. Navigate to `/backend/cms/settings` and select **Disable CMS cache for backend users**. 

With this enabled, the cache will be skipped when a user is logged in to the backend, allowing you to always see the current versions of pages.

###Pages

Any new pages that you add need to be registered with LemonStand. As of now, this means logging into your stores `backend` and adding the page manually. This is where you set the `url` and other options such as `title` to the page.


## TODO
- Automatically register new pages, resources, etc.
- When the application starts up, check if the s3 folder is different. If it is, ask the user if they want to upload their local files to s3, or pull s3 to their local files.  
- API access to LemonStand2 for token access, AWS user credentials, store hash name, etc.
- Bundle as a `pip` package or use `pyinstaller` to create a cross platform executable.
- Make it easy for multiple developers to work on the same theme.
