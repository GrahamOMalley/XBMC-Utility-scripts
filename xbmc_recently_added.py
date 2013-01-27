#! /usr/bin/env python
import sys
import MySQLdb

# globals
EP = False
MOV = False
PRINT_FILE_PATH = False
RESULT_NUMBER = 25
EP_FILTER = "idEpisode"

switch = ['-m', '-e', '-n', '-f', '-a']
for i in range(len(sys.argv)):
    if sys.argv[i] in switch:
        if sys.argv[i] == '-m':
            MOV = True
        if sys.argv[i] == '-e':
            EP = True
        if sys.argv[i] == '-f':
            PRINT_FILE_PATH = True
        if sys.argv[i] == '-a':
            EP_FILTER = 'c05'
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
    print "\t-f: also print file path for each item"
    print "\t-a: print/sort by date aired instead of date added"
    sys.exit()
mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "xbmc_video60")

mc = mysql_con.cursor()
if EP:
    # (@)> - sql to get most recent episodes
    mc.execute("select strTitle, c12, c13, c00, strPath, strFilename from episodeview order by %s desc limit %d" % (EP_FILTER, RESULT_NUMBER))
    print 'Using ep filter: ', EP_FILTER
    print "Recent Episodes:"
    for m in mc:
        prstr = "%s s%se%s: %s" % (m[0], m[1], m[2], m[3])
        if PRINT_FILE_PATH: 
            prstr = "%s s%se%s: %s\n\t%s/%s" % (m[0], m[1], m[2], m[3], m[4], m[5])
        print prstr

if MOV:
    # (@)> - sql to get most recent movies
    mc.execute("select c00, strPath, strFileName from movieview order by idMovie desc limit %d" % RESULT_NUMBER)
    print "\nRecent Movies:"
    for m in mc:
        prstr =  "%s" % (m[0])
        if PRINT_FILE_PATH: 
            prstr = "%s\n\t%s/%s" % (m[0], m[1], m[2])
        print prstr
