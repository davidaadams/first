import csv
import urllib2
from bs4 import BeautifulSoup
from unidecode import unidecode

def MakeImdbTop1000():
	print "Making IMDB List..."
	all_movies = list()
	for index in range(1,1001,100):
		movies = FindMovies("http://www.imdb.com/search/title?at=0&groups=top_1000&sort=user_rating,desc&view=simple&start=" + str(index))
		for m in movies:
			all_movies.append(m)
	print len(all_movies)
	with open('top_1k.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		writer.writerows(all_movies)
	
def FindMovies(url):
	try:
		url_data = urllib2.urlopen(url)
	except urllib2.HTTPError:
		return None
	soup = BeautifulSoup(url_data.read(), "lxml")
	# print(soup.prettify())
	body = soup.find_all("tr")
	movies = list()
	for index in range(2,len(body)-2):
		title = unidecode(body[index].find("a").get_text()).lower()
		year = int(body[index].find_all("td")[1].find("span").get_text()[1:-1])
		votes = int(body[index].find_all("td")[3].get_text().strip().replace(",", ""))
		movies.append([title, year, votes])
	return movies

if __name__ == "__main__":
	MakeImdbTop1000()
