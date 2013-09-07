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

#the URL has hard coding for western route
baseURL = "http://mumbailifeline.com/timetable.php?sel_route=western&sfrom=SOURCE&sto=DESTINATION&time1=12%3A00+AM&time2=12%3A00+AM&Submit=Submit"

#Known source and destination routes
src = ["Churchgate","Churchgate","Churchgate","Churchgate","Churchgate","Churchgate","Churchgate","Virar","Virar","Virar","Virar","Virar","Borivali","Andheri","Bandra","Goregaon","Malad","Bhayandar","Dadar","Bandra","Andheri","Borivali","Churchgate","Mahalaxmi","Andheri","Dadar","Bandra","Andheri","Vasai","Vasai"]

dest = ["Virar","Borivali","Andheri","Bandra","Malad","Goregaon","Bhayandar","Churchgate","Borivali","Andheri","Bandra","Dadar","Churchgate","Churchgate","Churchgate","Churchgate","Churchgate","Churchgate","Virar","Virar","Virar","Virar","Vasai","Borivali","Borivali","Borivali","Borivali","Vasai","Churchgate","Andheri"]

data = open("data.csv","wb")

for station in range(len(src)):
	URL = baseURL.replace("SOURCE",src[station].upper()).replace("DESTINATION",dest[station].upper())
	tree = get(URL)
	trains = tree.findall('.//table[@id="gradient-style"]//tr')[1:]

	out = csv.writer(data, lineterminator='\n')

	for train in trains:
		fields = train.findall('.//td')
		number = fields[0].find('.//a').get('href')
		speed = fields[1].text
		coaches = fields[2].text
		origin = fields[3].text
		end = fields[4].text
		start_time = fields[5].text
		end_time = fields[-1].text
		out.writerow([number, speed, coaches, origin, end, start_time, end_time])	

data.close()