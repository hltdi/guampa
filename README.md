guampa
======

The collaborative translation website from [HLTDI](http://hltdi.github.io).

## Installation for hacking on it
Make sure you have Python 3.3 or higher, with pip and virtualenv installed (Ubuntu package python-virtualenv).

  * check out the source
  * `$ scripts/setup_virtualenv.sh`
  * `$ source venv/bin/activate` 
  * `$ scripts/create_db.sh`
  * `$ scripts/devserver.sh`

Now you should be good to go!

## Deploying to a server
Please see [DeployingWithApache](https://github.com/hltdi/guampa/wiki/DeployingWithApache) -- should work with other WSGI-enabled web servers too -- if you run it on another one (nginx, say), let us know!

libraries and other people's code included
==========================================
* [angular-translate](http://pascalprecht.github.io/angular-translate), licensed under the [WTFPL](http://www.wtfpl.net/)
* [jQuery Form Plugin](http://jquery.malsup.com/form/), dual-licensed under the MIT and GPLv2 licenses
* [WikiExtractor.py](http://medialab.di.unipi.it/wiki/Wikipedia_Extractor) licensed under the GPLv3, modified by us to work with Python 3 and hacked up a bit
