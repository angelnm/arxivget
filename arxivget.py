import urllib.request as libreq
import xml.etree.ElementTree as ET
from pathlib import Path
import conf

def show_data(data):
	print(data)
	out_file.write('{}\n'.format(data))

def download_file(download_url, filename):
	response = libreq.urlopen(download_url)    
	file = open("papers/" + filename + ".pdf", 'wb')
	file.write(response.read())
	file.close()

def display_author(entry, params):
	show_data('* ID: \n{}'.format(entry.find('{http://www.w3.org/2005/Atom}id').text))
	show_data('* UPDATED: \n{}'.format(entry.find('{http://www.w3.org/2005/Atom}updated').text))
	title = entry.find('{http://www.w3.org/2005/Atom}title').text
	show_data('* TITLE: \n{}'.format(title))
	show_data('* SUMMARY: \n{}'.format(entry.find('{http://www.w3.org/2005/Atom}summary').text.rstrip("\n")))
	show_data('* AUTHORS:')
	for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
		show_data(author[0].text)
	link = entry.find('{http://www.w3.org/2005/Atom}id').text.replace('/abs/', '/pdf/')
	show_data('* LINK: \n{}.pdf'.format(link))
	if params['download']:
		download_file(link, title)
	show_data('')



Path("papers/").mkdir(parents=True, exist_ok=True)
params = conf.parameters

query=params['query']
query=query.replace(' ', '+')
query=query.replace('(', '%28')
query=query.replace(')', '%29')
query=query.replace('"', '%22')

url_str = 'http://export.arxiv.org/api/query?search_query={0}&start=0&max_results={1}&sortBy=lastUpdatedDate'.format(
																											query, 
																											params['numpapers'])
with libreq.urlopen(url_str) as url:
	req = url.read()
	root = ET.fromstring(req)

out_file = open('papers/info.txt', 'w')
for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
	display_author(entry, params)
out_file.close()