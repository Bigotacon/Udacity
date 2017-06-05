historyAnswers = ["cao", "warlord", "han", "three kingdom", "cao wei", "emperor wu of wei" ]blankList = ["_1_", "_2_", "_3_", "_4_", "_5_", "_6_"]#quizDictionary = {'cao': '_1_', 'warlord': '_2_', 'han': '_3_', 'three kingdom': '_4_', 'cao wei':'_5_', 'emperor wu of wei':'6'}
historyText = ""replaced = []
#------------------------------------------------------------------------------
#this function sets the difficulty for the quiz#first a player is prompted for input#if they pick a valid response they break from the loop#the function then sets the text to be used and#then return the string named difficulty#------------------------------------------------------------------------------def difficultyFn(historyText, difficulty):
	while (True):
		difficulty = difficulty.lower()
		if (difficulty == "easy"):
			historyText = ('Cao _1_ was a Chinese _2_ and the penultimate Chancellor ' +
			'of the Eastern _3_ dynasty who rose to great power in the final years of the ' +
			'dynasty. As one of the central figures of the _4_ period, he ' +
			'laid the foundations for what was to become the state of cao wei and was ' +
			'posthumously honoured as Emperor Wu of Wei.')
			break
		elif (difficulty == "medium"):
			historyText = ('Cao _1_ was a Chinese _2_ and the penultimate Chancellor ' +
			'of the Eastern _3_ dynasty who rose to great power in the final years of the ' +
			'dynasty. As one of the central figures of the _4_ period, he ' +
			'laid the foundations for what was to become the state of _5_ and was ' +
			'posthumously honoured Emperor Wu of Wei.')
			break
		elif (difficulty == "hard"):
			historyText = ('Cao _1_ was a Chinese _2_ and the penultimate Chancellor' +
			'of the Eastern _3_ dynasty who rose to great power in the final years of the '+
			'dynasty. As one of the central figures of the _4_ period, he ' +
			'laid the foundations for what was to become the state of _5_ and was ' +
			'posthumously honoured as _6_.')
			break
		#continue looping
		else:
			print "It looks like you did not enter a valid option./n Please enter another value."
	return historyText
#this prints the introduction text for this quizdef introduction(historyText):	print "Dude and dudettes its time for a history pop quiz"	print "Please fill in the blanks for this paragraph."	print historyText
#------------------------------------------------------------------------------# Checks if a word in the blank line is a substring of the word passed in.#------------------------------------------------------------------------------def word_in_pos(word, blankList):    for pos in blankList:        if (pos in word):            return pos    return None
#------------------------------------------------------------------------------
#this function checks if the users has gotten a right or worng answer#if the user gets it right they will recieve a 1#else the user will recieve a 0#------------------------------------------------------------------------------def checkAnswers(word, historyAnswers, element):	if (word == historyAnswers[element].lower()):		score = 1		print "You got the correct answer!"	elif (word != historyAnswers[element].lower()):		score = 0		print "Please try again."	else:		print "If you got this line then there is an error"	return score
def numberOfQuestions(difficulty):	numberOfBlanks = 0	if (difficulty == "easy"):		numberOfBlanks = 4	elif (difficulty == "medium"):		numberOfBlanks = 5	elif (difficulty == "hard"):		numberOfBlanks = 6	return numberOfBlanks
#------------------------------------------------------------------------------#this is the main function#At first it asks the player what difficulty they would like#it then has a rolepalyying introduction#and then it splits the text#------------------------------------------------------------------------------difficulty = raw_input("Type desired difficulty...easy, medium, hard \n")historyText = difficultyFn(historyText, difficulty)introduction(historyText)historyText = historyText.split()#------------------------------------------------------------------------------#This function runs the game#at first it shows the user the entire paragraph#it loops through through the text until if finds a blank#the user is prompted to fill in the blank#if the user answerss correctly they can proceed#otherwise they must guess again#the user is told how well they did at the end#------------------------------------------------------------------------------def runGame(blankList, historyAnswers, historyText, replaced, difficulty):	i = 0
	attempt = 0
	for word in historyText:		replacement = word_in_pos(word, blankList)
		if replacement != None:
			if (i != 0):
				print " ".join(replaced)
			validAnswer = 0
			while (validAnswer == 0):
				attempt += 1
				user_input = raw_input("Fill in blank " + str(i + 1) + ".")				validAnswer = checkAnswers(user_input, historyAnswers, i)			word = word.replace(replacement, user_input)			replaced.append(word)
			i += 1		else:			replaced.append(word)	replaced = " ".join(replaced)	print replaced	numberOfBlanks = numberOfQuestions(difficulty)	print "You guessed the write answer " + str((numberOfBlanks/float(attempt)) * 100) + " % of the time."	grade = ((numberOfBlanks/float(attempt)))	if(grade == 100):		print "You did it boss. Amazing."	elif(grade >= 90):		print "That was amazing"	elif (grade >= 80):		print "Alright, that was good"	else:		print "At least you made it out alive."#------------------------------------------------------------------------------#run the main function#------------------------------------------------------------------------------runGame(blankList, historyAnswers, historyText, replaced, difficulty)