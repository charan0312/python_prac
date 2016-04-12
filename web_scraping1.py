#!python3

import webbrowser, sys, pyperclip, requests
#webbrowser.open('http://bookmyshow.com')

#if len(sys.argv) > 1:
#	address = ' '.join(sys.argv[1:])
#else:
#	address = pyperclip.paste()

#webbrowser.open('https://www.google.com/maps/place/' + address)
res = requests.get('http://www.gutenberg.org/cache/epub/1112/pg1112.txt')

try:
	res.raise_for_status()
	playFile = open('RomeoAndJuliet.txt', 'wb')
	for chunk in res.iter_content(100000):
		playFile.write(chunk)
	playFile.close()
except Exception as exc:
	print 'There was a problem: %s' % (exc)
