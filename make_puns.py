import csv
import sys
import copy

def MakePuns(movie_file, dirty_file):
	print("Puns it is...")
	phones = LoadPhoneTypes()
	movie_phrases = LoadWordsAndPhones(movie_file)
	dirty_phrases = LoadWordsAndPhones(dirty_file)
	for title in movie_phrases:
		movie_phones = title[1:]
		movie_words = title[0].split()
		if ShouldCreatePuns(movie_words):
			print
			all_words = list()
			all_matches = list()
			found_match = False
			for idx in range(len(movie_phones)):
				matches = FindRhyme(movie_words[idx], movie_phones[idx], dirty_phrases, phones)
				all_words.append(movie_words[idx])
				all_matches.append(matches)
				if len(matches) > 0:
					found_match = True
				#print(movie_words[idx], matches)
			if found_match:
				print(title[0])
				for idx in range(len(all_words)):
					print(all_words[idx], all_matches[idx])

def ShouldCreatePuns(words):
	w = copy.copy(words)
	if 'the' in w:
		w.remove('the')
	return len(w) > 1

def FindRhyme(movie_word, movie_phones, dirty_phrases, phones):
	last_vowel = -1
	for ph in range(len(movie_phones)):
		if phones[movie_phones[ph]] == 'vowel':
			last_vowel = ph
	# Find the last phone that wasn't a stop or a vowel
	if last_vowel == -1:
		print("uanble to find vowel: ", single_word)
		return None
	else:
		tmp_vowel = -1
		for ph in range(last_vowel):
			if phones[movie_phones[ph]] == 'vowel' or phones[movie_phones[ph]] == 'stop':
				tmp_vowel = ph+1
		if tmp_vowel == -1:
			last_vowel_new = 0
		else:
			last_vowel_new = tmp_vowel
		movie_phone = movie_phones[last_vowel_new:] 
		# print(movie_phone)
		matches = FindDirtyWordsThatRhyme(movie_word, movie_phone, dirty_phrases)
		if len(matches) == 0:
			movie_phone = movie_phones[last_vowel:]
			if len(movie_phone) > 1:
				matches = FindDirtyWordsThatRhyme(movie_word, movie_phone, dirty_phrases)
		if len(matches) > 10:
			movie_phone = movie_phones
			if len(movie_phone) > 1:
				matches = FindDirtyWordsThatRhyme(movie_word, movie_phone, dirty_phrases)
		return matches

def FindDirtyWordsThatRhyme(movie_word, movie_phones, dirty_phrases):
	all_matches = list()
	for phrase in dirty_phrases:
		for i in range(1,len(phrase)):
			if len(phrase[i]) >= len(movie_phones): # needed?
				# print(phrase[i][-len(movie_phones):])
				if phrase[i][-len(movie_phones):] == movie_phones:
					if not (movie_word in phrase[0]):
						all_matches.append(phrase[0])
	return all_matches

def LoadPhoneTypes():
	phones = dict()
	with open('cmudict.0.7a.phones.csv', 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			phones[row[0]] = row[1]
	return phones

def LoadWordsAndPhones(file):
	words = list()
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			word = list([row[0]])
			for i in range(1,len(row)):
				phones = row[i].split()
				for ph_idx in range(len(phones)):
					ph_char = phones[ph_idx][-1]
					if ph_char == '0' or ph_char == '1' or ph_char == '2':
						phones[ph_idx] = phones[ph_idx][0:-1]
				word.append(phones)
			words.append(word)
	return words


if __name__ == "__main__":
	argv = sys.argv
	if len(argv) < 3:
		print("pass two args: the movie file and the dirty word file")
		sys.exit(1)
	MakePuns(argv[1], argv[2])
