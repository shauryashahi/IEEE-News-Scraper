from lxml.html import parse
import sys
import codecs
import sqlite3

def main():
	headings = []
	htt = []
	conn = sqlite3.connect('./database/news.db')
	c = conn.cursor()
	c.executescript(
	"""DROP TABLE IF EXISTS news;
	CREATE TABLE IF NOT EXISTS `news`(
	headings text not null,
	hlink text not null
	);""")
	sys.stdout = codecs.getwriter('utf8')(sys.stdout)
	url = 'http://www.ieee.org/about/news/index.html'
	page = parse(url).getroot()
	thediv = page.cssselect('div.box-lc-indent')[1][1]
	#Prints the Recent Headlines from IEEE
	for r in thediv.cssselect('p>strong'):
		heading = r.text_content().strip()
		if not heading:
			continue
		else:
			headings.append(heading)
	#Prints the HyperLinks to Full Story
	for r in thediv.cssselect('p'):
		links = r.cssselect('a')
		for link in links:
			if link.text_content()[0] == 'R':
				link = link.attrib['href']
				if link[0] == '/':
					http = 'http://www.ieee.org%s'
					htt.append(http %(link))
				else:
					htt.append(link)
	for i in xrange(14):
		print headings[i], htt[i]
		a = headings[i]
		b = htt[i]
		c.execute('insert into news (headings,hlink) values (?,?)',(a,b))
		conn.commit()
if __name__ == '__main__':
	main()
