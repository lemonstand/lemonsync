When running, `LemonSync` will listen for changes in the folder you configure, and automatically push updates to your s3 store. This is helpful if you want to add your theme under local version control, or prefer to work in locally rather than in the LemonStand UI.

#Installation

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

Once you have cloned this repo onto your machine, you can simply run `python LemonSync.py` from your command line. To stop the program type `Ctrl-C`.

## TODO
- When the application starts up, check if the s3 folder is different. If it is, ask the user if they want to upload their local files to s3, or pull s3 to their local files.  
- API access to LemonStand2 for token access, AWS user credentials, store hash name, etc.
- Bundle as a `pip` package or use `pyinstaller` to create a cross platform executable.
- Make it easy for multiple developers to work on the same theme.
