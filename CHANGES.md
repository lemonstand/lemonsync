CHANGELOG
=======

##Version 0.1.22
**October 3, 2017**

LemonSync Python is no longer available or supported by LemonStand.


##Version 0.1.21
**July 21, 2016**

- Make the connection error message more descriptive
- Introduce an executable version for people having problems building from source

##Version 0.1.20
**January 25, 2016**

- **Bug Fix** (minor) - Adds check for editing theme.

##Version 0.1.19
**May 27, 2015**

- Disable SSL verification.

##Version 0.1.18
**May 19, 2015**

- **Bug Fix** (minor) - Use `PUT` instead of `POST` for /resource/touch request

##Version 0.1.17
**May 19, 2015**

- Use "edit theme" instead of "active theme"

##Version 0.1.16
**June 21, 2014**

- **Bug Fix** (major): Windows file path seperators are now accounted for when uploading files to s3
- **Bug Fix** (minor): Use binary mode when calculating md5 checksums of files to avoid incorrectly marking a file as changed

##Version 0.1.15
**June 03, 2014**

- Lock down dependency versions
- Closes #9 (Assume config.cfg file exists locally)
- Closes #8 (Report the theme being synced to)

##Version 0.1.14
**May 30, 2014**

- Bug Fix: rename LemonSync to lemonsync

##Version 0.1.13
**May 29, 2014**

- Bug Fix: Files not being registered with LemonStand API

##Version 0.1.12
**May 29, 2014**

- Disable SSL verification.

##Version 0.1.11
**May 28, 2014**

- Bug Fix: Caching issue with resources.

##Version 0.1.10
**May 24, 2014**

- Standard naming convention

##Version 0.1.9
**May 21, 2014**

- **Bug Fix** (minor): Access tokens were not being regenerated correctly after expiration.

##Version 0.1.8
**May 20, 2014**

- Better handling of terminal colors
- Send keynames to LS when updated, to record the modified stamp
- Add cache control headers

##Version 0.1.7
**May 17, 2014**

- **Bug Fix** (minor): The `ignore_patterns` setting was being incorrectly referenced.
- Better error handling when connection to s3 can not be made.
- Function renaming in `Connector` class
- Change default watch settings
- Make windows compatible

##Version 0.1.6
**May 13, 2014**

- Add configuration values
	- `pattern_match`
		- Explicitly state what files LemonSync will listen for
	- `ignore_dirs`
		- Provide a pattern for ignoring files
- Show any files from LemonStand that are different than the local file system when `LemonSync` starts
- Add command line argument `--reset=local` to force overwriting local files with remote theme files
- Add command line argument `--reset=remote` to force overwriting the remote theme files with the local files

##Version 0.1.5
**May 1, 2014**

- Initial release (beta)
