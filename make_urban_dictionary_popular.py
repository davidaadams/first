import csv
import urllib2
from bs4 import BeautifulSoup
from unidecode import unidecode

def MakeUrbanDictionaryPopular():
	print "Making Urban Dictionary List..."
	letters = [ "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]
	all_words = list()
	for letter in letters:
		words = FindWords("http://www.urbandictionary.com/popular.php?character=" + letter)
		for w in words:
			all_words.append(w)
	#print all_words
	f = open("urban_dictionary.csv", "wb")
	for w in all_words:
		f.write(w + "\n")
	f.close()

def FindWords(url):
	try:
		url_data = urllib2.urlopen(url)
	except urllib2.HTTPError:
		return None
	soup = BeautifulSoup(url_data.read(), "lxml")
	#print(soup.prettify())
	body = soup.find("div", { "class" : "span9" }).find_all("li")
	words = list()
	for w in body:
		words.append(unidecode(w.get_text()).lower())
	return words

if __name__ == "__main__":
	MakeUrbanDictionaryPopular()
