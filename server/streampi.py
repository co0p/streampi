#!/usr/bin/python

from bottle import route, run, hook, response, static_file, error
import cPickle, ConfigParser
import pygst
pygst.require("0.10")
import gst

#----------------------------------------------
# settings 
#----------------------------------------------

# holds the settings
config = None
streamlist = None
prefix = '/api'


# this is the gstreamer playbin
player = gst.element_factory_make("playbin", "player")

# we need this hook for 'Access-Control-Allow-Origin'
@hook('after_request')
def enable_cors():
	response.headers['Access-Control-Allow-Origin'] = '*'



#----------------------------------------------
# load / save stream list to file
#----------------------------------------------

def resetStreamInFile(path):
	global streamlist

	streamlist = {'chillout':'http://listen.di.fm/public3/chillout.pls',
		'dradio':'http://dradio_mp3_dlf_m.akacast.akamaistream.net/7/249/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_m'}
	writeStreamToFile(path)
	loadStreamsFromFile(path)

#def


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
# data manipulation 
#----------------------------------------------


@route(prefix + '/reset')
def resetData():
	resetStreamInFile(config.get("streampi", "path"))
#def

# returns a list of streams
@route(prefix + '/get', method='GET')
def getList():
	return {'error':False, 'streams':streamlist}


# returns a list of streams
@route(prefix + '/get/<name>')
def getName(name):

	if name is not None and len(name) > 0:
		if name in streamlist:
			return {'error':False, 'stream':streamlist[name]}
		
	return {'error':True, 'message':"couldn't find stream"}



# adds a station to the list, overrides existing entries
@route(prefix + '/add/<name>/<url:re:.+>')
def add(name=None, url=None):

	if name is None or len(name) < 1:
		return {'error':True, 'message':"name missing"}

	if url is None or len(url) < 1:
		return {'error':True, 'message':"url missing"}

	streamlist[name] = url
	writeStreamToFile(config.get("streampi", "path"))
	return {'error':False, 'message':"added stream '" +name+ "' to list"}



# removes a station from the list
@route(prefix + '/delete/<name>')
def delete(name):

	if name is not None and name in streamlist:
		del streamlist[name]
		return {'error':False, 'message':"deleted '" +name+ "'stream"}

	return {'error':True, 'message':"couldn't delete stream"}


#----------------------------------------------
# playing the stream
#----------------------------------------------

# play a stream
@route(prefix + '/play')
def play():
	return {'error':True, 'message':"missing name of stream"}

@route(prefix + '/play/<name>')
def playName(name):

	if name in streamlist:

		#our stream to play
		music_stream_uri = streamlist[name]
		#music_stream_uri = 'http://dradio_mp3_dlf_m.akacast.akamaistream.net/7/249/142684/v1/gnl.akacast.akamaistream.net/dradio_mp3_dlf_m'

		global player


		#set the uri
		player.set_property('uri', music_stream_uri)

		#start playing
		player.set_state(gst.STATE_PLAYING)
		return {'error':False, 'message':"start playing"}

	else:
		return {'error':True, 'message':"missing stream"}



# stop playing stream
@route(prefix + '/stop')
def stop():

	global player
	player.set_state(gst.STATE_NULL)
	return {'error':False, 'message':"stop playing"}


#----------------------------------------------
# show the website
#----------------------------------------------
@route('/')
def showWebsite():
    return static_file('mobile.html', root='../client')

@error(500)
def onError500(code):
	return "Server failure"


@error(404)
def onError404(code):
	return "this page does not exists"

#----------------------------------------------
# main
#----------------------------------------------
loadConfigFromFile("streampi.cfg")
loadStreamsFromFile(config.get("streampi", "path"))

run(host='192.168.0.41',
		port=config.get("streampi","port"),  
		debug=config.get("streampi", "debug"),
		reloader=True)