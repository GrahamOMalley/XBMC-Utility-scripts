#! /usr/bin/env python
import sys
import MySQLdb

EP = False
MOV = False
RESULT_NUMBER = 25

switch = ['-m', '-e', '-n']
for i in range(len(sys.argv)):
    if sys.argv[i] in switch:
        if sys.argv[i] == '-m':
            MOV = True
        if sys.argv[i] == '-e':
            EP = True
        if sys.argv[i] == '-n':
            try:
                RESULT_NUMBER = int(sys.argv[i+1])
            except:
                print "usage example: -n 5"
                sys.exit()

if((not EP) and (not MOV)):
    print "Usage: %s (-m) (-e) (-n int)" % sys.argv[0]
    print "\t-m: scan movies"
    print "\t-e: scan episodes"
    print "\t-n: number of items to display for each category"
    sys.exit()
mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "xbmc_video")

mc = mysql_con.cursor()
if EP:
    # (@)> - sql to get most recent episodes
    mc.execute("select strTitle, c12, c13, c00 from episodeview order by idEpisode desc limit %d" % RESULT_NUMBER)
    print "Recent Episodes:"
    for m in mc:
        print "%s s%se%s: %s" % (m[0], m[1], m[2], m[3])

if MOV:
    # (@)> - sql to get most recent movies
    mc.execute("select c00 from movieview order by idMovie desc limit %d" % RESULT_NUMBER)
    print "\nRecent Movies:"
    for m in mc:
        print "%s" % (m[0])
