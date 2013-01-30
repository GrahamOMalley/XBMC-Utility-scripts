#! /usr/bin/env python
import MySQLdb
import argparse
from gomXBMCTools import formatNoAsStr
    # code...
parser = argparse.ArgumentParser(description='Prints most recently watched episodes and/or movies')
parser.add_argument('-e', '--episode', action="store_true", default=False, required=False, help='Scan episodes')
parser.add_argument('-m', '--movies', action="store_true", default=False, required=False, help='Scan movies')
parser.add_argument('-f', '--file_path', action="store_true", default=False, required=False, help='Print out file path')
parser.add_argument('-n', '--num', type=int, default=25, required=False, help='number of items to print')
parser.add_argument('-p', '--padding', type=int, default=35, required=False, help='column padding value')
args = parser.parse_args()

mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "xbmc_video60")

mc = mysql_con.cursor()
if args.episode:
    sortedEpList = []
    # (@)> - sql to get most recent episodes where playCount is not null order by lastPlayed
    mc.execute("select lastPlayed, strTitle, c12, c13, c00 from episodeview where playCount is not null order by lastPlayed desc limit %d" % args.num)
    print "Recently watched episodes:"
    for m in mc:
        # stupid hack this is a clunky POS
        timestamp = "%s:    " % (m[0])
        showname = m[1]
        showname = showname.ljust(args.padding)
        ep ="s%se%s:" % (formatNoAsStr(m[2]), formatNoAsStr(m[3]))
        ep = ep.ljust(args.padding/2)
        prstr = timestamp + showname + ep + m[4]
        sortedEpList.append(prstr)
    sortedEpList.sort()
    for i in sortedEpList: print i

if args.movies:
    movieList= []
    # (@)> - sql to get most recent movies
    mc.execute("select lastPlayed, c00 from movieview order by lastPlayed desc limit %d" % args.num)
    print "\nRecently Watched Movies:"
    for m in mc:
        timestamp = "%s:\t" % (m[0])
        prstr = "%s:    %s" % (m[0], m[1])
        movieList.append(prstr)
    movieList.sort()
    for i in movieList: print i
