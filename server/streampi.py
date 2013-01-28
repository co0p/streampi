#!/usr/bin/python

from bottle import route, run, error
import cPickle, json
import pygst
pygst.require("0.10")
import gst, gobject



#----------------------------------------------
# settings 
#----------------------------------------------

#TODO - use config file - http://gotofritz.net/blog/weekly-challenge/restful-python-api-bottle/
PORT = 8000
DEBUG = True
PATH = "streamlist.p"
streamlist = None

#creates a playbin (plays media form an uri) 
player = gst.element_factory_make("playbin", "player")



#----------------------------------------------
# load / save stream list to file
#----------------------------------------------
def loadStreamsFromFile(path):
	global streamlist

	# init ... streamlist = {'key':'value'}
	# writeStreamToFile(PATH)

	streamlist = cPickle.load(open(path, 'rb'))
	print "loaded " + path
#def


def writeStreamToFile(path):
	cPickle.dump(streamlist, open(path, 'wb')) 
	print 'saved.'



#----------------------------------------------
# json response helper
#----------------------------------------------
# every response is a json object
def response(code, message, data = None):
	if data is None:
		return {'status':code, 'message':message}
	else:
		jsondata = json.dumps(data)
		return {'status':code, 'message':message, 'data':jsondata}




#----------------------------------------------
# data manipulation 
#----------------------------------------------

# returns a list of streams
@route('/get')
def getList():
	return response(200, "", streamlist)


# returns a list of streams
@route('/get/<name>')
def getList(name):

	if name is not None and len(name) > 0:

		if name in streamlist:
			return response(200, "", streamlist[name])
		
	return response(500, "couldn't find stream")



# adds a station to the list, overrides existing entries
@route('/add/<name>/<url:re:.+>')
def add(name=None, url=None):

	if name is None or len(name) < 1:
		return response(500, "name missing")

	if url is None or len(url) < 1:
		return response(500, "url missing")

	streamlist[name] = url
	writeStreamToFile(PATH)
	return response(200, "added stream '" +name+ "' to list")



# removes a station from the list
@route('/delete/<name>')
def delete(name):

	if name is not None and name in streamlist:
		del streamlist[name]
		return response(200, "deleted '" +name+ "'stream")

	return response(500, "couldn't delete stream")


#----------------------------------------------
# playing the stream
#----------------------------------------------

# play a stream
@route('/play')
def play():
	return response("500", "missing name of stream")

@route('/play/<name>')
def play(name):

	if name in streamlist:

		#our stream to play
		music_stream_uri = streamlist[name]
		#music_stream_uri = 'http://dradio_mp3_dlf_m.akacast.akamaistream.net/7/249/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_m'

		global player


		#set the uri
		player.set_property('uri', music_stream_uri)

		#start playing
		player.set_state(gst.STATE_PLAYING)
		return response("200", "start playing")

	else:
		return response(500, "missing stream")



# stop playing stream
@route('/stop')
def stop():

	global player
	player.set_state(gst.STATE_NULL)
	if state is gst.STATE_NULL:
		return response("200", "stop playing")
	else:
		return response(500), "failed to stop stream"


#----------------------------------------------
# main
#----------------------------------------------

def main() :
	# parse resourcelist
	loadStreamsFromFile(PATH)

	# run webserver
	run(host='localhost', port=PORT, debug=DEBUG)

#
if __name__ == '__main__':
	main()