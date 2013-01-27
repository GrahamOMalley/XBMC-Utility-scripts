#! /usr/bin/env python
import json
import httplib, urllib
import sys


# this script currently just handles the first item in the playlist, this is incorrect wont work for playlists > 1 item

url = 'http://localhost:8888'
jsonrpcurl = url + '/jsonrpc'

#player_data = json.dumps({'jsonrpc': "2.0", 'method': "Player.GetActivePlayers", 'id': "1"})
player_data = json.dumps({ "jsonrpc": "2.0", "method": "Player.GetItem", "params": { "playerid": 1, "properties": ["showtitle"] }, "id": 1 })

respdata = urllib.urlopen(jsonrpcurl, player_data).read()
respdata = respdata.replace("false", "False").replace("true", "True")
respdict = eval(respdata)

print "DEBUG: ", respdict

#if (not respdict['result']['video']):
if (not respdict['result']):
    print "Nothing playing..."
else:
    print "Now Playing: "
    print respdict['result']['item']['showtitle'] + ":\t" + respdict['result']['item']['label']
