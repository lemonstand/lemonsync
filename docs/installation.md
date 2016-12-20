## Installation

_LemonSync is a command-line python application. We recommend using [VirtualEnv](https://virtualenv.pypa.io/en/stable/) in combination with [pip](https://pip.pypa.io/en/stable/)._

### Install Dependencies
  * Install [pip](https://pip.pypa.io/en/stable/installing/)
  * Install [VirtualEnv](https://virtualenv.pypa.io/en/stable/installation/)

### Setup Environment
* Open a terminal/cmd instance
* Change directories to where you will keep your project(s)
* Create a python Virtual Environment:
  ```
  $ virtualenv lemonstand_projects
  ```
  - `lemonstand_projects` can be any name;
  - `lemonstand_projects` will be a folder, containing several subfolders which will contain a unique python instance.

### Install `LemonSync`
```
$ /path/to/lemonstand_projects/bin/pip install lemonsync
```
Activate the `lemonstand_projects` environment:
```
$ cd ./lemonstand_projects/bin/source activate
```
Test LemonSync is installed:
```
$ lemonsync
usage: lemonsync [-h] -c CONFIG [-r RESET]
```

If you see the `usage` message, your environment has been correctly installed and you are ready to configure LemonSync.

From here you are ready to [Configure Your Environment](Configuration) or return [Home](Home).
