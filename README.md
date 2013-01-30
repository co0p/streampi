streampi
========

convert your raspberrypi to a budget sonos streaming machine, controlled by a website 



work in progress screenshot
---------------------------

![an image of the controlling website, work in progress](https://raw.github.com/co0p/master/streampi/doc/mobile.png "the controlling website")




Get started
---------

1. start the server : [server/] python ./streampi.py (will listen on localhost:8000)
2. start the client: [client/] ./client.sh (will listen on port 8001)
3. go to http://localhost:8001, push some buttons

REST commands
-------------

* `/ add / name / url` -> adds the entry (name, url) to the streamlist
* `/ delete / name`  -> removes entry with key name from the streamlist
* `/ play / name` -> plays the stream found under name 
* `/ stop` -> stops the currently playing stream

