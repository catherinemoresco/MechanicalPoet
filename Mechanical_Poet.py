# MechanicalPoet, a program which generates poetry in varying meters based on a source text.
# Copyright (C) 2014 Catherine Moresco
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

# The author can be contacted at catherine.moresco@gmail.com

import random

alphabet = map(chr, range(ord('A'), ord('Z')+1) + [ord("'")])
dictionary = {'A':{}, 'B':{}, 'C':{}, 'D':{}, 'E':{}, 'F':{}, 'G':{}, 'H':{}, 'I':{}, 'J':{}, 'K':{}, 'L':{}, 'M':{}, 'N':{}, 'O':{}, 'P':{}, 'Q':{}, 'R':{}, 'S':{}, 'T':{}, 'U':{}, 'V':{}, 'W':{}, 'X':{}, 'Y':{}, 'Z':{}, "'":{},}
wordlist = []
pdic = {}


def get_stresses(entry): # from a line in the dictiory, isolates the string that represents the pronounciation of the word on that line
	nums = ''
	for char in entry:
		if char == "0" or char == "1" or char == "2":
			nums = nums + char
	return nums

def build_dictionary_w2p(): # builds a dictionary of letter keys associated with dictionaries of words associated with that letter with their pronounciations
	cmu = open("textfiles/cmu.txt", "r")
	for line in cmu:
		word = line.split(' ')[0]
		if ord(word[0]) in range(ord('A'), ord('Z') + 1) or word[0] == "'": # checks if line starts with capital letter or apostrophe
			dictionary[word[0]][word] = get_stresses(line)
	cmu.close()


def build_dictionary_p2w(): # buils a dictionary associating pronounciation patterns with their corresponding words
	ps = []
	cmup = open("textfiles/cmup.txt", "r")
	for line in cmup:
		pronounciation = get_stresses(line)
		ps.append(pronounciation)
	cmup.close()
	cmup = open("textfiles/cmup.txt", "r")
	for p in list(set(ps)):
		pdic[p] = []
	for line in cmup:
		pronounciation = get_stresses(line)
		pdic[pronounciation].append(line.split(' ')[0])
	cmup.close()

def build_wordlist(): # lists all words in pronounciation dictionary
	cmu = open("textfiles/cmu.txt", "r")
	for line in cmu:
		word = line.split(' ')[0]
		if ord(word[0]) in range(ord('A'), ord('Z') + 1) or word[0] == "'":
			wordlist.append(word)
	cmu.close()

def build_model(string): # builds a dictionary associating each word with words that follow it in the sample
	model = {"Break":[]}
	sample = "Break " + string + " Break"
	words = sample.split(" ")
	for word in words: 
		if word not in wordlist:
			word == ""
		model[word] = []
	for i in range(0, len(words)-1):
		model[words[i]].append(words[i+1])
	return model


def write_poem(model): # generates text without regard to meter or rhyme
	lines = 0
	poem = ""
	word = "Break"
	while True:
		newword = model[word][random.randint(0, len(model[word])-1)]
		if newword == "Break":
			if lines == 5:
				return poem
			poem = poem + '\n'
			lines += 1
			word = newword
		else:
			poem = poem + newword + " "
			word = newword

def selectwords(pattern, wordlist): # selects the longest word in a list that follow given pattern
	wordsinpdic = []
	for p in get_subpatterns(pattern):
		if pattern in pdic:
			wordsinpdic = wordsinpdic + pdic[p]
	if wordsinpdic != []:
		words = list(set(wordsinpdic)&set(wordlist))
	else: 
		words = []
	if pattern == '':
		return []
	if words == []:
		newpattern = pattern[:len(pattern)-2]
		words = selectwords(newpattern, wordlist)
	return words


def match_line(linepattern, lastword, model): # creates a string of words to match a pattern
	if linepattern == "":
		return ""
	else: 
		line = ""
		if selectwords(linepattern, model[lastword]) == []:
			word = random.choice(list(set(match_multiple_patterns(get_subpatterns(linepattern)))&set(flatten(model.values()))))
		else:
			word = random.choice(selectwords(linepattern, model[lastword]))
		word_pattern = dictionary[word[0]][word]
		linepattern = linepattern[len(word_pattern):]
		return line + " " + word  + match_line(linepattern, word, model)


def get_subpatterns(pattern): # given a stress pattern, returns all subpatterns that can be formed by taking stresses off the beginning
	patterns = []
	for i in range(0,(len(pattern))):
		patterns.append(pattern[i:])
	return patterns

def match_multiple_patterns(patternlist): # given a list of patterns, will return all the words that match any of them
	wordlist = []
	for pattern in patternlist:
		if pattern in pdic:
			words = pdic[pattern]
			for word in words:
				wordlist.append(word)
	return wordlist


def flatten(x): # concatenates a list of lists into a single list
	flattened = []
	for a in x:
		for b in a:
			flattened.append(b)
	return flattened

def get_last_word(line):
	return line.split(' ')[-1]

def make_couplet():
	x = match_line("0101010101", flatten(model.values())[0], model)
	y = match_line("0101010101", get_last_word(x), model)
	return x + "\n" + y + "."

def make_ballad():
	x = match_line("01010101", flatten(model.values())[0], model)
	y = match_line("010101", get_last_word(x), model)
	return x + "\n" + y + "."

def print_current_source(model):
	print "Current source text is",
	if model == smodel:
		print "song lyrics of Ke$ha."
		return 0
	if model == cmodel: 
		print "the inaugural address of Barack Obama."
		return 0
	if model == momodel:
		print "the sonnets of William Shakespeare."
	else: 
		print "custom text."

def change_source():
	textchoice = raw_input("To select Ke$ha, enter (K). To select Shakespeare, enter (S). To select Obama, enter (O). Or, enter (C) to enter custom text.\n")
	if textchoice == "K":
		return smodel
	if textchoice == "S":
		return momodel
	if textchoice == "O":
		return cmodel
	if textchoice == "C":
		custom = raw_input("Enter your custom text now. It is recommended that you enter as much souce text as possible.\n")
		if len(list(set(custom.split(' '))&set(flatten(pdic.keys())))) < 25:
			print "That isn't enough text for me to work with. Please enter at least fifty English words separated by spaces. Please try again."

		formatted = custom.upper().replace('\n', ' Break ').replace('.', ' Break ').replace('!', ' Break ').replace('?', ' Break ')
		model = build_model(formatted)
	print_current_source(model)
	return model

def print_poem(mode):
	if mode == "blank verse":
		print make_couplet()
	if mode == "ballad":
		print make_ballad()
	if mode == "free verse":
		print write_poem(model)


def is_valid_pattern(pattern): # check a stress pattern to make sure that is is valid.
	for x in pattern:
		if x != "0" and x != "1":
			return False
	return True

def make_custom_line():
	pattern = raw_input("Please enter your desired stress pattern as a string of 1s and 0s, with 1 representing a stressed syllable and 0 representing an unstressed syllable.\n")
	if is_valid_pattern(pattern):
		print match_line(pattern, "A", model) + "."
	else:
		helpinput = raw_input("I'm sorry, that is not a valid pattern. Please enter only 1s and 0s, or enter (R) to return to the main menu.")
		if helpinput == "R":
			return None
		else: 
			make_custom_line()



def change_mode(mode):
	modechoice = raw_input("Enter (B) for ballad meter, (F) for free verse, or (I) for blank verse (iambic pentameter). Or, enter (C) to make a line with custom meter!\n")
	if modechoice == "F":
		mode = "free verse"
	if modechoice == "B":
		mode = "ballad"
	if modechoice == "I":
		mode = "blank verse"
	if modechoice == "C":
		make_custom_line()

	return mode



print "Opening program files..."
kesha = open("textfiles/kesha.txt", "r")
obama = open("textfiles/obama.txt", "r")
shakespeare = open("textfiles/shakespeare.txt", "r")
print "Analyzing text sample..."
sh = (kesha.read()).upper().replace('\n', ' Break ').replace('.', ' Break ').replace('!', ' Break ').replace('?', ' Break ')
co = (obama.read()).upper().replace('\n', ' Break ').replace('.', ' Break ').replace('!', ' Break ').replace('?', ' Break ')
mo = (shakespeare.read()).upper().replace('\n', ' Break ').replace('.', ' Break ').replace('!', ' Break ').replace('?', ' Break ')
# models of word frequency, forwards and backwards:
smodel = build_model(sh)
cmodel = build_model(co)
momodel = build_model(mo)
print "Building dictionaries..."
# dictionaries of words in models, sorted by final letters:	
build_dictionary_w2p()
build_dictionary_p2w()
build_wordlist()
model = cmodel
mode = "blank verse"
print "Here's some blank verse:"
print_poem(mode)
while True:
	action = raw_input("Another? Enter (A)! To change source text, enter (S). To change meter pattern, enter (M). Or, enter (Q) to quit.\n")
	if action == "M":
		print "Current meter is " + mode + "."
		mode = change_mode(mode)
	if action == "S":	
		print_current_source(model)
		model = change_source()
		print_poem(mode)
	if action == "A":
		print_poem(mode)
	if action == "Q":
		quit()
