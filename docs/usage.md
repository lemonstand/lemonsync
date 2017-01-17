Once configured, LemonSync is ready for use.

In essence, LemonSync will wait in the background, listening for files you add, change, or delete in the folder you specified as your `watch_dir`.

When a change is detected, it will push to the store theme marked for **Editing**. Refreshing the page while previewing the theme will show the changes you made locally.

To start LemonSync, go to your `lemonstand_projects` folder in a terminal|cmd instance and type `lemonsync`.

When you call LemonSync, it will look for a `lemonstand.cfg` in the directory you are currently in. You can specify a config via the following command:

```
$ lemonsync --config=path/to/your/config.cfg
```

If you named your config file `lemonsync.cfg`, and are in the same directory as the config file, you can omit the --config flag from the command:

```
$ lemonsync
```

## Pages

Any new pages that you add are automatically registered with LemonStand when uploaded. You can set properties on the page such as the `url` and `name` of the page, by adding a header to the top of the page. See below for an example.

```
---
template: inner
protocol: all
published: true
name: About
url: /about
---
```

Pages also need to be named following a specific structure. The filename must begin with `page-` and end with `.htm`. Pages without this format will be ignored by your LemonStand store. See below for an example.

```
page-contact.htm
```

## Templates

Similar to pages, you can set the properties on a template by adding a header to the of the template. See below for example.

```
---
content_type: ‘application/xml; charset=utf-8'
description: 'Used for XML sitemap'
---
```

Templates do not require the `page-` prefix, but end with `.htm`. See below for example.

```
sitemap.htm
```

***

## Advanced Options


If you need to reset your theme you can pass the `--reset` argument to `LemonSync`. There are two
options for this argument, `local` and `remote`.

```
 $ lemonsync --config=path/to/your/config.cfg --reset=local
```

This will completely replace the contents of `watch_dir` set in `path/to/your/config.cfg` with the contents of your remote theme. All files and folders except `/.git*` will be removed. **This is an advanced feature and should be used with caution!**

```
$ lemonsync --config=path/to/your/config.cfg --reset=remote
```

This will completely replace the contents of your remote theme with the content in `watch_dir`, set in `path/to/your/config.cfg`.

**This is an advanced feature and should be used with caution! If not careful, you could end up deleting your entire remote theme!**
