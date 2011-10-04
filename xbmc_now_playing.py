#! /usr/bin/env python
import json
import httplib, urllib
import sys

url = 'http://localhost:8888'
jsonrpcurl = url + '/jsonrpc'

player_data = json.dumps({'jsonrpc': "2.0", 'method': "Player.GetActivePlayers", 'id': "1"})
respdata = urllib.urlopen(jsonrpcurl, player_data).read()
respdata = respdata.replace("false", "False").replace("true", "True")
respdict = eval(respdata)

if (not respdict['result']['video']):
    print "Nothing playing..."
else:
    v_data = json.dumps({'jsonrpc': "2.0", 'method': "VideoPlaylist.GetItems", 'id': "1"})
    vresp = urllib.urlopen(jsonrpcurl, v_data).read()
    vresp = vresp.replace("false", "False").replace("true", "True")
    vdict = eval(vresp)
    str_np = vdict['result']['items'][0]['label']
    str_file = vdict['result']['items'][0]['file']
    print "Now Playing: " + str_np + " (" + str_file + ")"
