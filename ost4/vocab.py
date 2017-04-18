#! /usr/bin/python

import random
import os
import cgi, cgitb

cgitb.enable()
form = cgi.FieldStorage()

# Load data
f = open('/Users/tzh/PycharmProjects/wse2017/ost4/vocab.dat')
file_list = f.readlines()

numWords = len(file_list)

# dictionaries of nouns, verbs and adjs
nouns = {}
verbs = {}
adjs = {}

for i in range(0, numWords):
	line = file_list[i].split('|')
	# nouns
	if line[1] == 'n.':
		nouns[line[0]] = line[2]
	# verbs
	elif line[1] == 'v.':
		verbs[line[0]] = line[2]
	# adjectives
	elif line[1] == 'adj.':
		adjs[line[0]] = line[2]

nouns_key = nouns.keys()
verbs_key = verbs.keys()
adjs_key = adjs.keys()
random.shuffle(nouns_key)
random.shuffle(verbs_key)
random.shuffle(adjs_key)

# parameters
numQuestions = 1
numOptions = 4
numNouns = 1
numVerbs = 1
numAdjs = 1

# choose first random batch of vocabularies as questions
chosenNounsKey = []
chosenVerbsKey = []
chosenAdjsKey = []
for i in range(0, numNouns*numOptions):
	chosenNounsKey.append(nouns_key[i])
for j in range(0, numVerbs*numOptions):
	chosenVerbsKey.append(verbs_key[j])
for k in range(0, numAdjs*numOptions):
	chosenAdjsKey.append(adjs_key[k])

# Method used to split keys according to number of options
def generateKeySet(keys, num):
	keySets = []
	for i in range(0, num):
		keySet = []
		for j in range(0, numOptions):
			keySet.append(keys[j+i*numOptions])
		keySets.append(keySet)
	return keySets

nounsKeySets = generateKeySet(chosenNounsKey, numNouns)
verbsKeySets = generateKeySet(chosenVerbsKey, numVerbs)
adjsKeySets = generateKeySet(chosenAdjsKey, numAdjs)

# Method used to generate html list for every question
def generateQuestion(dic, keySet, questionNum):
	random.shuffle(keySet)
	answerNum = random.randint(0, 3)
	word = keySet[answerNum]
	
	# layout
	print "<p><li><b>" + keySet[answerNum] + "</b>: <br>"
	print "<input type=hidden name=a" + str(questionNum) + " value=" + str(answerNum) + ">"
	print "<input type=hidden name=w" + str(questionNum) + " value=" + str(word) + ">"
	
	for i in range(0, numOptions):
		print "<input type=radio name=q" + str(questionNum) + " value=" + str(i) + ">" + dic[keySet[i]] + "<br>"
	
	print "</li>"

# Print header
print "Content-type:text/html\n\n"

if os.environ['REQUEST_METHOD'] == 'GET':
	print "<html>"
	print "<body>"
	print "<h2>Vocabulary Quiz</h2><FORM ACTION=vocab.cgi METHOD=POST><OL>"

	for i in range(0, numNouns):
		generateQuestion(nouns, nounsKeySets[i], i)
	# for j in range(0, numVerbs):
	# 	generateQuestion(verbs, verbsKeySets[j], j+numNouns)
	# for k in range(0, numAdjs):
	# 	generateQuestion(adjs, adjsKeySets[k], k+numNouns+numVerbs)

	print "</OL><INPUT TYPE=SUBMIT VALUE=Grade></FORM>"
	print "</body>"
	print "</html>"

if os.environ['REQUEST_METHOD'] == 'POST':
	numCorrect = 0
	numWrong = 0
	correctAnswers = []
	wrongAnswers = []
	for i in range(0, numQuestions):
		if form["q"+str(i)].value == form["a"+str(i)].value:
			numCorrect += 1
			correctAnswers.append(form["w"+str(i)].value)
		else:
			numWrong += 1
			wrongAnswers.append(form["w"+str(i)].value)

	# layout
	print "<html>"
	print "<body>"
	print "You got <b>" + str(numCorrect) + " of " + str(numCorrect+numWrong) + "</b> answers correct."
	print "<p><table border=1>"
	print "<tr>"
	print "<th>Correct</th>"
	print "<th>Incorrect</th>"
	print "</tr>"
	print "<tr>"
	print "<td valign=top><font color=green>"
	for i in range(0, len(correctAnswers)):
		print correctAnswers[i] + " <br>"
	print "</font></td>"
	print "<td valign=top><font color=red>"
	for j in range(0, len(wrongAnswers)):
		print wrongAnswers[j] + " <br>"
	print "</font></td></tr></table>"
	print "</body>"
	print "</html>"
	

