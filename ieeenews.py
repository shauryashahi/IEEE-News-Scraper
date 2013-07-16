from lxml.html import parse
import sys
import codecs

def main():
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	url = 'http://www.ieee.org/about/news/index.html'
	page = parse(url).getroot()
	thediv = page.cssselect('div.box-lc-indent')[1][1]
	#Prints the Recent Headlines from IEEE
	for r in thediv.cssselect('p>strong'):
		heading = r.text_content().split()
		if not heading:
			continue
		else:
			print ' '.join(heading)
			print 
	#Prints the HyperLinks to Full Story
	for r in thediv.cssselect('p'):
		links = r.cssselect('a')
		for link in links:
			if link.text_content()[0] == 'R':
				link = link.attrib['href']
				if link[0] == '/':
					htt = 'http://www.ieee.org%s'
					htt = htt %(link)
				else:
					htt = link
				print htt
if __name__ == '__main__':
	main()
