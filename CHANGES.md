CHANGELOG
=======

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