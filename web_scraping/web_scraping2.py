#!python3

import requests, bs4, time

#res = requests.get('http://nostarch.com')
#res.raise_for_status()
#noStarchSoup = bs4.BeautifulSoup(res.text)
#type(noStarchSoup)

exampleFile = requests.get('http://www.engadget.com/')
exampleSoup = bs4.BeautifulSoup(exampleFile.text)
#type(exampleSoup)
#elems = exampleSoup.select('#author')
#print type(elems)
#print len(elems)
#print type(elems[0])
#print elems[0].getText()
#print str(elems[0])
#print elems[0].attrs

pElems = exampleSoup.select('p')
#print str(pElems[0])
#print pElems[0].getText()
#print str(pElems[1])
#print pElems[1].getText()
#print str(pElems[2])
#print pElems[2].getText()
i = 0
for elms in pElems:
	print pElems[i].getText()
	print pElems[i].attrs
#	time.sleep(2)
	i = i + 1
