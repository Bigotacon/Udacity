historyAnswers = ["cao", "warlord", "han", "three kingdom", "cao wei", "emperor wu of wei" ]
historyText = ""

#this function sets the difficulty for the quiz
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
#this prints the introduction text for this quiz
#------------------------------------------------------------------------------

#this function checks if the users has gotten a right or worng answer
def numberOfQuestions(difficulty):
#------------------------------------------------------------------------------
	attempt = 0
	for word in historyText:
		if replacement != None:
			if (i != 0):
				print " ".join(replaced)
			validAnswer = 0
			while (validAnswer == 0):
				attempt += 1
				user_input = raw_input("Fill in blank " + str(i + 1) + ".")
			i += 1