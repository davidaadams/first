import urllib2
from bs4 import BeautifulSoup

def ReadListOfWords(file_name):
	return open(file_name, "r").readlines()

def MakeDictionary():
	print "Making Dictionary..."
	all_words = ReadListOfWords("dictionary.txt")
	print "Read normal dictionary"
	index = 0
	for word in all_words:
		index += 1
		w = word[:-1]
		# print w
		spelling = FindPhoneticSpelling("http://www.merriam-webster.com/dictionary/" + w)
		if spelling:
			print str(index) + "," + w + "," + spelling
		else:
			print str(index) + "," + w + "," + "NA"



def FindPhoneticSpelling(url):
	try:
		url_data = urllib2.urlopen(url)
	except urllib2.HTTPError:
		return None
	soup = BeautifulSoup(url_data.read(), "lxml")
	# print(soup.prettify())
	headword = soup.find(id="headword")
	if not headword:
		return None
	spans = headword.find_all("span")
	if len(spans) < 2:
		return None
	else:
		return spans[1].get_text()


if __name__ == "__main__":
	MakeDictionary()
