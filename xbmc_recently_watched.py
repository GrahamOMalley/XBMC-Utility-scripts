#! /usr/bin/env python
import sys
import MySQLdb

EP = False
MOV = False
PRINT_FILE_PATH = False
RESULT_NUMBER = 25
PADDING = 35

switch = ['-m', '-e', '-n', '-f']
for i in range(len(sys.argv)):
    if sys.argv[i] in switch:
        if sys.argv[i] == '-m':
            MOV = True
        if sys.argv[i] == '-e':
            EP = True
        if sys.argv[i] == '-f':
            PRINT_FILE_PATH = True
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
    # (@)> - sql to get most recent episodes where playCount is not null order by lastPlayed
    mc.execute("select lastPlayed, strTitle, c12, c13, c00 from episodeview where playCount is not null order by lastPlayed desc limit %d" % RESULT_NUMBER)
    print "Recently watched episodes:"
    for m in mc:
        # stupid hack this is a clunky POS
        timestamp = "%s:\t" % (m[0])
        showname = m[1]
        showname = showname.ljust(PADDING)
        ep ="s%se%s:" % (m[2], m[3])
        ep = ep.ljust(PADDING/2)
        prstr = timestamp + showname + ep + m[4]
        print prstr

if MOV:
    # (@)> - sql to get most recent movies
    mc.execute("select lastPlayed, c00 from movieview order by lastPlayed desc limit %d" % RESULT_NUMBER)
    print "\nRecently Movies:"
    for m in mc:
        prstr = "%s: %s" % (m[0], m[1])
        print prstr
