## All Settings

* `api_host` [required]
   > Your full LemonStand domain

* `api_key` [required]
  > The  _Public Key_ of your LemonStand API key (created in your store administration panel)

* `api_access` [required]
  > The _API Token_ of your LemonStand API key (also available in your store administration panel)

* `watch_dir` [required]
  > This is the directory that `LemonSync` will listen to changes on.

* `store_host` [required]
  > The host name of your store.

* `file_patterns` [optional]
  > By default, `LemonSync` will listen to changes on all files, that are not specified in the `ignore_patterns` setting. Values need to be comma separated, and enclosed in square brackets.

* `ignore_patterns` [optional]
  > By default, `LemonSync` will ignore any `.tmp` and `git/` files. Patterns are matched based on Unix style "globbing". Values need to be comma separated, and enclosed in square brackets.

***

### `api_host` [required]

- `api_host` is the full URL of your store

#### Examples

1. `https://my-curios-shop.lemonstand.com` - if your store name is _my-curios-shop_ and does not use a custom domain.
2. `https://my-curios-shop.ca` - if you have a custom domain and have SSL configured.

**Note: LemonSync will only modify the theme marked as the _editing theme_ for the user who owns this API key. You can put a theme into _editing_ mode by using the theme settings in the LemonStand backend.**

***


### `watch_dir` [required]

The `watch_dir` should point to your local theme folder, which should have the `theme.yaml` file in it.

***

### `file_patterns` [optional]

#### Examples

   - Watch for changes only to `.js` and `.css` files.

      ```
      file_patterns = [ "*.js", "*.css" ]
      ```

   - Watch for changes in specific directories.

      ```
       file_patterns = [ "*/pages/*", "*/resources/*" ]
      ```
      This will match against all directories named `pages` and `resources` in your `watch_dir`. To watch on the root level `pages` and `resources` directories only, you need to specify the full path to the directories.

      ```
      file_patterns = [ "/full/path/to/pages/*", "/full/path/to/resources/*" ]
      ```

   - Watch for changes to specific files in directories.

      ```
      file_patterns = [ "*/pages/*.js", "*/resources/*.css" ]
      ```

***

### `ignore_patterns` [optional]


   - Ignore a specific file. This will ignore all occurrences of `file.ext` in any sub-directory.

      ```
      ignore_patterns = [ "*/file.ext" ]
      ```

      To match a file in a specific directory, the full path needs to be specified.

      ```
      ignore_patterns = [ "/full/path/to/file.ext" ]
      ```
   - Ignore directories.

      ```
      ignore_patterns = [ "*/directory/*" ]
      ```

      To match a specific directory you need to specify the full path.

      ```
      ignore_patterns = [ "/full/path/to/directory/*" ]
      ```
