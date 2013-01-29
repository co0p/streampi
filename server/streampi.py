#!/usr/bin/python

from bottle import route, run, error, hook, response
import cPickle, json, ConfigParser
import pygst
pygst.require("0.10")
import gst, gobject



#----------------------------------------------
# settings 
#----------------------------------------------

# holds the settings
config = None

# this is the gstreamer playbin
player = gst.element_factory_make("playbin", "player")




# we need this hook for 'Access-Control-Allow-Origin'
@hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'




#----------------------------------------------
# load / save stream list to file
#----------------------------------------------

# load settings from cfg file
def loadConfigFromFile(path):

	global config
	config = ConfigParser.ConfigParser()
	
	#  if failed, use defaults
	try:
		config.readfp(open(path))
		print "loaded '" +path+ "'"

	except IOError:
		print "couldn't load 'streampi.cfg', using defaults."
		config.add_section("streampi")
		config.set("streampi", "port", "8000")
		config.set("streampi", "debug", "True")
		config.set("streampi", "path", "streamlist.p")

		print "writing '" +path+ "' file"
		config.write(open(path, 'wb'))
	#if
#def

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
def jsonResponse(code, message, data = None):
	if data is None:
		return {'status':code, 'message':message}
	else:
		jsondata = json.dumps(data)
		return {'status':code, 'message':message, 'data':jsondata}


#----------------------------------------------
# data manipulation 
#----------------------------------------------

# returns a list of streams
@route('/get', method='GET')
def getList():
	return jsonResponse(200, "", streamlist)


# returns a list of streams
@route('/get/<name>')
def getList(name):

	if name is not None and len(name) > 0:

		if name in streamlist:
			return jsonResponse
	(200, "", streamlist[name])
		
	return jsonResponse(500, "couldn't find stream")



# adds a station to the list, overrides existing entries
@route('/add/<name>/<url:re:.+>')
def add(name=None, url=None):

	if name is None or len(name) < 1:
		return jsonResponse(500, "name missing")

	if url is None or len(url) < 1:
		return jsonResponse(500, "url missing")

	streamlist[name] = url
	writeStreamToFile(PATH)
	return jsonResponse(200, "added stream '" +name+ "' to list")



# removes a station from the list
@route('/delete/<name>')
def delete(name):

	if name is not None and name in streamlist:
		del streamlist[name]
		return jsonResponse(200, "deleted '" +name+ "'stream")

	return jsonResponse(500, "couldn't delete stream")


#----------------------------------------------
# playing the stream
#----------------------------------------------

# play a stream
@route('/play')
def play():
	return jsonResponse("500", "missing name of stream")

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
		return jsonResponse(200, "start playing")

	else:
		return jsonResponse(500, "missing stream")



# stop playing stream
@route('/stop')
def stop():

	global player
	player.set_state(gst.STATE_NULL)
	return jsonResponse("200", "stop playing")


#----------------------------------------------
# main
#----------------------------------------------

def main() :

	# load config
	loadConfigFromFile("streampi.cfg")

	# parse resourcelist
	loadStreamsFromFile(config.get("streampi", "path"))

	# run webserver
	run(host='localhost',  
		port=config.get("streampi","port"),  
		debug=config.get("streampi", "debug"))

#
if __name__ == '__main__':
	main()

