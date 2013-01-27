#! /usr/bin/env python
import os
import MySQLdb

#
# customized version of Nathan Hoads missing-movie-viewer python script
# will only work on my main xbmc pc
#


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

physical = get_files('/media/oneTB/videos/movies')
physical.sort()
shares = []
mysql_con = MySQLdb.connect (host = "localhost",user = "xbmc",passwd = "xbmc",db = "xbmc_video60")
mc = mysql_con.cursor()
mc.execute("""select strPath, strFilename from movieview""")
for m in mc:
    shares.append("%s%s" % (m[0].replace("smb://MEDIA", "/media"), m[1]))

shares.sort()

print "Missing Movies:"
for p in physical:
    if p not in shares: 
        print p
print ""

shares = []
mc.execute("""select strPath, strFilename from episodeview""")
for m in mc:
    shares.append("%s%s" % (m[0].replace("smb://MEDIA", "/media"), m[1]))
shares = [s.lower() for s in shares]
shares.sort()

physical = get_files('/media/twoTB1/videos/tv')
physical += get_files('/media/tv2')
physical.sort()


print "\nMissing episodes:"
for p in physical:
    if p.lower() not in shares:
        print p
