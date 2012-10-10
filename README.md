Used to download music files from SoundCloud.com even if the download button is not available.

___

### How to use

Just run the python script like:

```shell
$ soundcloud-downloader.py USER CLIENT_ID
```
* `USER`: the username like `bassenectar` (http://soundcloud.com/bassnectar)
* `CLIENT_ID`: the soundcloud Client ID (this script uses the soundcloud api)

### Get the client ID

Register your app on [http://soundcloud.com/you/apps/new](http://soundcloud.com/you/apps/new) and takes the `Client ID`.

### Integrate into the console

Edit your `.bashrc` file and paste the following code :

```shell
function soundcloud() {
    user=$1
    /path/to/soundcloud-downloader.py ${user} CLIENT_ID
}
```
And to download the all tracks at one time from Bassnectar user:
```shell
$ soundcloud bassnectar
```
___

HAVE FUN :-)