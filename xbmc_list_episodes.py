#! /usr/bin/env python
import MySQLdb
import argparse
import gomXBMCTools

parser = argparse.ArgumentParser(description='Prints out all episodes for a given show')
parser.add_argument('-f', '--filename', action="store_true", default=False, required=False, help='print out path of episode too')
parser.add_argument('-s', '--show', type=str, required=True, help='the shows name')
parser.add_argument('-p', '--padding', type=int, default=60, required=False, help='column padding value')
args = parser.parse_args()

# globals
sortedEpList = []
actual_showname = ""

mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "xbmc_video60")

mc = mysql_con.cursor()
mc.execute("select strTitle, c12, c13, c00, strPath, strFilename from episodeview where strTitle like '%" + args.show + "%'" )
for m in mc:
    actual_showname = m[0]
    s = "s%se%s:\t\t" % (gomXBMCTools.formatNoAsStr( m[1]), gomXBMCTools.formatNoAsStr(m[2]))
    ept = str(m[3]).ljust(args.padding)
    s+= ept
    if args.filename: 
         s += "%s%s" % (m[4], m[5])
    sortedEpList.append(s)

print "Episodes in XBMC Library for: %s" % actual_showname
sortedEpList.sort()
for s in sortedEpList: print s
