import os
import sys
import csv
import urllib
import hashlib
import lxml.html
 
if not os.path.exists('.cache'):
	os.makedirs('.cache')
 
def get(url):
	filename = '.cache/' + hashlib.sha1(url).hexdigest()
	if not os.path.exists(filename):
		urllib.urlretrieve(url, filename)
	return lxml.html.parse(filename)


baseURL = "http://www.wr.indianrailways.gov.in/accident_wr.jsp?lang=0&id=0%2C6&m1=MONTH&y1=YEAR&submit1=submit"

months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

years = ["2009","2010","2011","2012"]

data = open("wr_accidents_data.csv","wb")

out = csv.writer(data, lineterminator='\n')

for yr in years:
	for mn in months:
		URL = baseURL.replace("MONTH",mn).replace("YEAR",yr)
		tree = get(URL)
		rows = tree.xpath('.//table[17]//tr')[1:]
		if len(rows)>1:
			for row in rows:
				cells = row.findall('.//td')[1:]
				record = []
				for cell in cells:
					record.append(cell.text_content().strip())
				print record		
				out.writerow(record)

data.close()			