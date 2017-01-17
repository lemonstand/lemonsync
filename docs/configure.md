_In order for_ `lemonsync` _to run correctly, you need to configure your environment. Here we will discuss the requirements for configuring your local environment._

There are a few steps to successfully configure your LemonSync environment:

1. Download your stores theme locally
2. Generate an API token for LemonSync to securely connect to your stores
3. Setup a configuration file locally to tie everything together

### Download Store Theme
_In order to work on our theme locally, we need to have our theme available locally._

* Go to your stores admin page
  - ie. `YOUR_STORE.lemonstand.com/backend/cms/theme`
* Select the appropriate theme and click export

![Generate a new API key here](https://s3.amazonaws.com/ls-docs/lemonsync_export_theme.png)

* A zip file will be downloaded by your browser
* Extract the contents into the `lemonstand_projects` folder. See the example below

```
+--- lemonstand_projects
|   \--- downloaded_theme_1
|       \--- pages, etc.
|       *--- theme.yaml
|   \--- downloaded_theme_2
|       \--- pages, etc.
|       *--- theme.yaml
|   *--- lemonstand.cfg
```
* Notes
  - The `theme.yaml` is important for lemonsync. Your local theme must have this file.
  - `lemonstand.cfg` is the config file used by lemonsync. In it you will define which theme to sync.

### Generate API Token

_In order to establish a secure connection with your LemonStand Store, API key credentials provided by your Store must be added to your `lemonstand.cfg` configuration file. The following will show you how to generate an API key for your store._

* The API keys can be generated in your Stores Admin Page
  - ie. `YOUR_STORE.lemonstand.com/backend/system/api`
* Generate a new API key in the Integrations > API section
* Use the generated keys in your `lemonstand.cfg` configuration file.

![Generate a new API key here](https://s3.amazonaws.com/ls-docs/lemonsync_api_key.png)

### Setup Configuration File
* Create a file called `lemonsync.cfg` in your `lemonstand_projects` folder.
* Open the file in your favorite text editor.
* Copy the following contents into `lemonsync.cfg`

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

#### **[Advanced Configuration Options](Advanced Configuration)**

* Paste the credentials for the API keys as found in the `Generate API Keys` section.
* Set your `watch_dir` to the path of your theme you downloaded. The directory specified must contain the `theme.yaml` file.
* The default values for `file_patterns` and `ignore_patterns` can be left as is, as you become more familiar with LemonSync you can edit these to customize your workflow.
  - See the [Advanced Configuration](Advanced Configuration) guide for more information on these options

Once you've customized your `lemonstand.cfg` file, you're ready to [Start Using](Usage), or return [Home](Home).
