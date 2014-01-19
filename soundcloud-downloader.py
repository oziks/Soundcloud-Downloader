#!/usr/bin/python2
import urllib2, sys, re
import urllib

from xml.dom.minidom import parseString

if len(sys.argv) <= 1:
	exit("You need to enter a user to download from")

def get_tag(element, name):
	# retrieve a name tag on the element structure
	tagXml = element.getElementsByTagName(name)[0].toxml();

	return tagXml.replace('<' + name + '>', '').replace('</' + name + '>', '')

def get_title(track):
	# retrieve the title of the song
	title = "%s.mp3" % get_tag(track, 'title')

	return title.replace('/', '-')

def get_url(track):
	# regular expression for the string we will search for in waveform-url tag
	regexp = 'https://w1.sndcdn.com/(.*?)_m.png'

	# find the song ID, if any
	match = re.search(regexp, get_tag(track, 'waveform-url'))

	if match:
		# create a new stream hyperlink with the song ID
		url = "http://media.soundcloud.com/stream/%s" % match.group(1)
	else:
		print "No song ID found for the %s user. Exiting." % sys.argv[1]
		sys.exit()

	return url

def main():
        failedTracks = []
	print "Getting Information... "

	# retrieve the user of the songs to download
	user = sys.argv[1]

	# retrieve type to download (tracks or favorites)
	type = sys.argv[2]

	if type != "tracks" and type != "favorites":
		type = "tracks"

	# retrieve the client_id from the final command-line argument
	client_id = sys.argv[-1]

	# retrieve the URL of the song to download from the final command-line argument
	soundcloud_api = "https://api.soundcloud.com/users/%s/%s?client_id=%s&limit=9999" % (user, type, client_id)

	try:
		# open api URL for reading
		xml = urllib2.urlopen(soundcloud_api)
	except ValueError:
		# the user supplied URL is invalid or could not be retrieved
		exit("Error: The user '%s' can not be retrieved" % user)

	# store the contents (source) of our song's URL
	xmlsource = xml.read()
	xml.close()

	# parse xml datasource
	data = parseString(xmlsource)
	tracks = data.getElementsByTagName('track')

	print "Ready to download the %s %s of the %s user... " % (len(tracks), type, user)

	# download songs for each track for the user
	for track in tracks:
		title = get_title(track)
		url   = get_url(track)

		print "Downloading File '%s'" % title
                try:
                    urllib.urlretrieve(url, title)
                except IOError as e:
                    failedTracks.append(title)
                    print 'Connection to SoundCloud Failed, unable to download:\n '+title+'\n continuing to next song'

	print "Download Complete"
        if len(failedTracks)>0:
            print 'Failed Tracks:\n'
            for t in failedTracks:
                print t+'\n'

if __name__ == '__main__':
	main()
