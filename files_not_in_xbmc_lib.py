#! /usr/bin/env python
import os
import MySQLdb
import argparse

#
# customized version of Nathan Hoads missing-movie-viewer python script
# will only work on my main xbmc pc
#

parser = argparse.ArgumentParser(description='Prints most recently added episodes and/or movies')
parser.add_argument('-e', '--episode', action="store_true", default=False, required=False, help='Scan episodes')
parser.add_argument('-m', '--movies', action="store_true", default=False, required=False, help='Scan movies')
args = parser.parse_args()

FILE_EXTENSIONS = ['mpg', 'mpeg', 'avi', 'flv', 'wmv', 'mkv', '264', '3g2', '3gp', 'ifo', 'mp4', 'mov', 'iso', 'ogm']

def file_has_extensions(filename, extensions):
    # get the file extension, without a leading colon.
    name, extension = os.path.splitext(os.path.basename(filename))
    name = name.lower()
    extension = extension[1:].lower()
    extensions = [ f.lower() for f in extensions ]

    if extension == 'ifo' and name != 'video_ts':
        return False

    return extension in extensions

def get_files(path):
    results = []
    for root, sub_folders, files in os.walk(path):
        for f in files:
            if file_has_extensions(f, FILE_EXTENSIONS):
                f = os.path.join(root, f)
                results.append(f)

    return results

physical = get_files('/media/nasGom/video/movies/')
physical.sort()
shares = []
mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "MyVideos75")
mc = mysql_con.cursor()
mc.execute("""select strPath, strFilename from movieview""")
for m in mc:
    shares.append("%s%s" % (m[0].replace("smb://NAS/nas", "/media/nasGom"), m[1]))

shares.sort()


print "Missing Movies:"
for p in physical:
    if p not in shares: 
        print p
print ""

if args.episode:
    shares = []
    mc.execute("""select strPath, strFilename from episodeview""")
    for m in mc:
        shares.append("%s%s" % (m[0].replace("smb://NAS/nas", "/media/nasGom"), m[1]))
    shares = [s.lower() for s in shares]
    shares.sort()

    physical = get_files('/media/nasGom/video/tv')
    physical.sort()


    print "\nMissing episodes:"
    for p in physical:
        if p.lower() not in shares:
            print p
