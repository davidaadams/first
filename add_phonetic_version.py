import csv
import sys

def AddPhonetic(input, output):
	print("Sounding it out...")
	print(input)
	print(output)
	phones = LoadPhones()
	lines = open(input, "r").readlines()
	total_complete = 0
	total_incomplete = 0
	all_output = list()
	for l in lines:
		line = l[:-1]
		missing_words = False
		word_phones = list([line])
		for word in line.split():
			if word in phones:
				word_phones.append(phones[word])
			else:
				missing_words = True
				word_phones.append("")

		if not missing_words:
			# print("found all phones:", word_phones)
			total_complete += 1
			all_output.append(word_phones)
		else:
			print("missing some phones:", word_phones)
			total_incomplete += 1
		
	print("totals:", total_complete, total_incomplete)
        with open(output, 'wb') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                writer.writerows(all_output)
		
def LoadPhones():
	lines = open("cmudict.0.7a_lower_no_dupes_plus.txt").readlines()
	# lines = open("head_cmudict.txt").readlines()
	phones = dict()
	for l in lines:
		split = l.find(' ')
		word = l[:split]
		phone = l[split+2:-1]
		phones[word] = phone
	return phones

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
	argv = sys.argv
	if len(argv) < 3:
		print("pass two args: the input and output file names")
		sys.exit(1)
	AddPhonetic(argv[1], argv[2])
