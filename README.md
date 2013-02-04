streampi
========

convert your raspberrypi to a budget sonos streaming machine, controlled by a website 



work in progress screenshot
---------------------------

![an image of the controlling website, work in progress](https://raw.github.com/co0p/streampi/master/doc/mobile.png "the controlling website")




Get started
---------

1. start the server : [server/] python ./streampi.py (will listen on 192.168.0.41:8000)
2. go to http://192.168.0.41:8000, push some buttons and listen to a stream


Warning
--------

This is work in progress, no security, no error handling what so ever ! Use at your OWN risk.


REST commands
-------------

* `/ add / name / url` -> adds the entry (name, url) to the streamlist
* `/ delete / name`  -> removes entry with key name from the streamlist
* `/ play / name` -> plays the stream found under name 
* `/ stop` -> stops the currently playing stream

