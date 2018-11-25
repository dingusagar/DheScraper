#Python 2.x


from bs4 import BeautifulSoup
import urllib 
import sys
import os
from pySmartDL import SmartDL

import requests


"""
scraper downloads all the pdf books in the website https://books.goalkicker.com/
and saves them to the current working directory

"""




root_url = "https://books.goalkicker.com/"


"""
returns a list containing links on the webpage pointed by @params: url 
if count argument is given, it retrieves only the first count number of links 
"""
def getLinks(url,count = sys.maxsize):
	r  = requests.get(url)

	data = r.text

	soup = BeautifulSoup(data)
	links = []
	c = 0
	for link in soup.find_all('a'):
		if c >= count:
			break 
		links.append(link.get('href'))
		c += 1

	return links


links = getLinks(root_url)
print('Fetched links from the root : ' + str(links))
links = links[:-1]  # removing the last link which points to some twitter page or sth
# print(links)

for i in range(len(links)):

	"""
	The final download link is of the form https://books.goalkicker.com/DotNETFrameworkBook/DotNETFrameworkNotesForProfessionals.pdf
	we get that by combining 
	root_url : https://books.goalkicker.com/
	links[i] : DotNETFrameworkBook/

	The DotNETFrameworkNotesForProfessionals.pdf/ link is present in the page : root_url + links[i] : https://books.goalkicker.com/DotNETFrameworkBook/


	"""

	suburl = root_url + links[i]
	bookname = links[i][:-1] + '.pdf' # remove the last character which is '/' 
	pdflink = suburl + getLinks(suburl,count=1)[0] # first link points to the pdf link

	if os.path.isfile(bookname):
		print(bookname +  ' file already exists')
		continue
	print('Downloading ' + pdflink  + ' ....')
	obj = SmartDL(pdflink,'./' + bookname) # download and save in the current working directory
	obj.start()


