"""
Produces a string of random text based on an input corpus. Useful for comedic or creative applications.

The statistical structure of the input corpus is analyzed and transition probabilities between each n-gram in the input are calculated. The random text is generated in the form of a Markov chain, whereby an initial n-gram in the corpus is randomly selected, and then all subsequent n-grams in the output are chosen based on transition probabilities calculated earlier.

The user specifies the path of the input corpus, the length of the n-grams to analyze, and the length of the output.

Only a single .txt files formatted in UTF-8 is accepted as input.

The larger the corpus, the better the results, however the program will still function with smaller inputs. For an input the length of a typical news article, n-grams of length 6 appear to offer the best trade-off between syntatical coherency and the originality of the output. Shorter n-grams tend to produce gibberish, whereas longer ones tend to yield long word runs identical to the input.
"""

import os,random
from nltk import tokenize

"""Imports the corpus."""
def import_corpus(corpus_path):
	corpus_file=open(corpus_path,"r",encoding="utf8")
	corpus=corpus_file.read().strip()
	corpus_file.close()
	return corpus

"""Tokenizes the corpus."""
def tokenize_corpus(corpus):
	words=tokenize.word_tokenize(corpus)
	words=[word for word in words if word.isalnum()]
	return words

"""Calculates n-gram frequencies."""
def calculate_n_gram_frequencies(words,n):
	n_gram_frequencies={}
	#Counts the occurrence of each n-gram.
	word_index=n
	while word_index<len(words):
		n_gram=tuple(words[word_index-n:word_index])
		if n_gram in list(n_gram_frequencies.keys()):
			n_gram_frequencies[n_gram]+=1
		else:
			n_gram_frequencies[n_gram]=1
		word_index+=1
	#Calculates the frequency of each n-gram.
	unique_n_grams=len(n_gram_frequencies)
	for n_gram in n_gram_frequencies:
		n_gram_frequencies[n_gram]/=unique_n_grams
	return n_gram_frequencies

"""Calculates the transitional probabilities of each n-gram given the occurrence of its inital word in the corpus."""
def calculate_n_gram_probabilities(n_gram_frequencies,word_frequencies):
	transitional_n_gram_probabilities=[]
	for n_gram in n_gram_frequencies:
		n_gram_frequency=n_gram_frequencies[n_gram]
		initial_word=tuple([n_gram[0]])
		initial_word_frequency=word_frequencies[initial_word]
		transitional_n_gram_probability=n_gram_frequency/initial_word_frequency
		transitional_n_gram_probabilities.append([n_gram,transitional_n_gram_probability])
	return transitional_n_gram_probabilities

"""Generates a string of random text based on the transition probabilities of each n-gram in the corpus."""
def generate_random_string(transitional_n_gram_probabilities,maximum_length):
	generated_words=[]
	#Randomly selects the initial n-gram.
	initial_n_gram=list(random.choice(transitional_n_gram_probabilities)[0])
	generated_words+=initial_n_gram
	#Randomly adds additional n-grams to the sequence given their transitional probabilities, until maximum length is reached.
	generated_words_index=len(generated_words)
	while len(generated_words)<=maximum_length:
		#Identifies all candidate n-grams to continue the sequence.
		preceding_word=generated_words[-1]
		candidate_n_grams=[]
		for i in range(0,len(transitional_n_gram_probabilities)):
			n_gram=transitional_n_gram_probabilities[i][0]
			transitional_n_gram_probability=transitional_n_gram_probabilities[i][1]
			if preceding_word==n_gram[0]:
				candidate_n_grams.append([i,transitional_n_gram_probability])
		#Randomly selects one of the candidate n-grams according to transition probability given the preceding word.
		chosen_n_gram=random.choices([row[0] for row in candidate_n_grams],[row[1] for row in candidate_n_grams])
		#Appends chosen n-gram to the sequence.
		generated_words+=transitional_n_gram_probabilities[chosen_n_gram[0]][0][1:]
	#Converts the generated sequence to a string.
	generated_string=" ".join(generated_words).lower()
	return generated_string

"""Validates all input. Returns False if an error is encountered, otherwise returns True."""
def validate_input(corpus_path,n,maximum_length):
	#Ensures corpus_path exists.
	if not os.path.exists(corpus_path):
		print("Error. Corpus file path does not exist.")
		return False
	#Ensures n is an integer greater than 0.
	if type(n)!=int:
		print("Error. n must be an integer.")
		return False
	elif n<=1:
		print("Error. n must be greater than 1.")
		return False
	#Ensures maximum_length is an integer greater than 0.
	if type(maximum_length)!=int:
		print("Error. maximum_length must be an integer.")
		return False
	elif maximum_length<=0:
		print("Error. maximum_length must be greater than 0.")
		return False
	#Returns True if all input is valid.
	return True

"""Main. Define arguments here, then run in the command line: python ./markov_text_generator.py"""
def main():
	corpus_path="./input.txt"
	n=2
	maximum_length=50
	#Validates input.
	if not validate_input(corpus_path,n,maximum_length):
		return -1
	#Loads and tokenizes the corpus.
	corpus=import_corpus(corpus_path)
	words=tokenize_corpus(corpus)
	#Calculates transition probabilities between each n-gram in the corpus.
	n_gram_frequencies=calculate_n_gram_frequencies(words,n)
	word_frequencies=calculate_n_gram_frequencies(words,1)
	transitional_n_gram_probabilities=calculate_n_gram_probabilities(n_gram_frequencies,word_frequencies)
	#Generates random text.
	generated_string=generate_random_string(transitional_n_gram_probabilities,maximum_length)
	print(generated_string)
	return 0

if __name__=="__main__":
	main()
