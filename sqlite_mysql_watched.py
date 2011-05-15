#! /usr/bin/env python

# After creating a mysql db, switching, mounting sources as smb shares, and scanning items to library
# use this script tp scan through the default sqlite db that xbmc uses, and update the mysql db with watched tv episodes
# 
# assumes same episode title and base filename (NOT fully qualified filename)

import sqlite3
import MySQLdb

sqlite_db_file = "backupvids.db"

msh = "localhost"
msu = "xbmc"
msp = "xbmc"
msdb = "xbmc_video"

sqlite_con = sqlite3.connect(sqlite_db_file)
mysql_con = MySQLdb.connect (host = msh,user = msu,passwd = msp,db = msdb)

mc = mysql_con.cursor()
sqlitec = sqlite_con.cursor()

# update TV SHOWS
sqlitec.execute("""select strFilename, c00, playCount from episodeview where playCount > 0""")
for row in sqlitec:
	print "file: " + row[0] + " will have its playcount incremented"
	mc.execute ("""UPDATE episodeview SET playCount = 1 WHERE strFilename = %s and c00 = %s""", (row[0], row[1]))

# update MOVIES
sqlitec.execute("""select strFilename, c00 from movieview where playCount > 0""")
for row in sqlitec:
	print row
	mc.execute ("""UPDATE movieview SET playCount = 1 WHERE strFilename = %s and c00 = %s""", (row[0], row[1]))

sqlitec.close()
mc.close()
