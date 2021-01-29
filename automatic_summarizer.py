"""
This is an extractive text summarization script which implements the TextRank algorithm.

A statistical measure of the similarity of each sentence to every other is taken, then each sentence is ranked from most to least central. Those sentences with the highest average similiarity are presumed to be most central to the overall meaning of the text, and are included in the summary.

The user may specify a compression ratio from 0.0 to 1.0; the compression ratio corresponds to 1 - (length of summary/length of input); the closer to 1, the shorter the summary.

Only .txt files formatted in UTF-8 are accepted as input.

If the user has never used 'tokenize' in Python's NLTK module before, then this functionality will probably need to be installed first. Open a Python instance and type 'import nltk' > 'nltk.download("punkt")'. This only needs to be done once.

By default, NLTK's 'tokenize' supports English text, but appears to come with options supporting other languages too. Please see NLTK's documentation for details: https://www.nltk.org/api/nltk.tokenize.html
"""

import os
from nltk import tokenize
from scipy import spatial

"""Imports the source text."""
def import_source_text(source_text_path):
	source_text_file=open(source_text_path,"r",encoding="utf8")
	source_text=source_text_file.read().strip()
	source_text_file.close()
	return source_text

"""Identifies each sentence in the source text, returning them as a list."""
def tokenize_by_sentence(source_text):
	sentences=tokenize.sent_tokenize(source_text)
	return sentences

"""Identifies each unique word in the source text, returning them as a list."""
def identify_unique_words(source_text):
	words=tokenize.word_tokenize(source_text)
	words=[word for word in words if word.isalnum()]
	unique_words_in_source=list(set(words))
	return unique_words_in_source

"""Converts sentences into vectors."""
def vectorize_sentences(sentences,unique_words_in_source):
	sentence_vectors=[]
	#Iteratively vectorizes each sentence.
	for i in range(0,len(sentences)):
		#Tokenizes the current sentence.
		words_in_current_sentence=tokenize.word_tokenize(sentences[i])
		words_in_current_sentence=[word for word in words_in_current_sentence if word.isalnum()]
		#Initializes the sentence vector.
		sentence_vector=[]
		for j in range(0,len(unique_words_in_source)):
			sentence_vector.append(0)
		#Constructs the sentence vector by tallying up the occurrence of each unique source-text word within the current sentence.
		for j in range(0,len(words_in_current_sentence)):
			for k in range(0,len(unique_words_in_source)):
				if words_in_current_sentence[j]==unique_words_in_source[k]:
					sentence_vector[k]+=1
					break
		sentence_vectors.append(sentence_vector)
	#Returns the sentence vectors.
	return sentence_vectors

"""
Uses an implementation of the TextRank algorithm to identify key sentences.

The average cosine similarities of each sentence are calculated and ranked. Those with the highest average cosine similarities are presumed to be the most 'central' to the meaning of the text.
"""
def textrank(sentence_vectors):
	#Initializes the average similiarity list.
	average_similarities=[]
	for i in range(0,len(sentence_vectors)):
		average_similarities.append([i,0.0])
	#Populates the average similiarity list.
	for i in range(0,len(sentence_vectors)):
		for j in range(0,len(sentence_vectors)):
			if i==j:
				continue
			else:
				similarity=1.0-spatial.distance.cosine(sentence_vectors[i],sentence_vectors[j])
				average_similarities[i][1]+=similarity
	for i in range(0,len(average_similarities)):
		average_similarities[i][1]/=(len(sentence_vectors)-1)
	#Ranks the average similarity list in descending order.
	average_similarities=sorted(average_similarities,key=lambda l:l[1],reverse=True)
	#Returns the average similarity list.
	return average_similarities

"""Generates an extractive summary of the input text according to a user-specified compression ratio."""
def generate_summary(sentences,average_similarities,compression_ratio):
	summary=""
	sentences_to_keep=sorted(average_similarities[0:int(len(average_similarities)*(1-compression_ratio))],key=lambda l:l[0])
	for sentence in sentences_to_keep:
		summary+=sentences[sentence[0]]+" "
	summary=summary.strip()
	return summary

"""Validates all input. Returns False if an error is encountered, otherwise returns True."""
def validate_input(compression_ratio,source_text_path):
	#Ensures compression_ratio is a floating point.
	if type(compression_ratio)!=float:
		print("Error. compression_ratio must be a floating point.")
		return False
	#Ensures compression_ratio is between 0 and 1.
	if ((compression_ratio<0.0) or (compression_ratio>1.0)):
		print("Error. compression_ratio must be between 0.0 and 1.0, inclusive.")
		return False
	#Ensures source_text_path exists.
	if not os.path.exists(source_text_path):
		print("Error. Source text file path does not exist.")
		return False
	#Ensures source_text_path points to a text file.
	if source_text_path.split(".")[-1]!="txt":
		print("Error. Source text file path must be of type '.txt'.")
		return False
	#Returns True if all input is valid.
	return True

"""Main. Define arguments here, then run in the command line: python ./automatic_summarizer.py"""
def main():
	compression_ratio=0.9
	source_text_path="./input.txt"
	#Validates input.
	if not validate_input(compression_ratio,source_text_path):
		return -1
	#Imports the source text.
	source_text=import_source_text(source_text_path)
	if source_text=="":
		#Terminates if the source text is an empty string.
		return -1
	#Tokenizes the source text into its sentences and unique words.
	sentences=tokenize_by_sentence(source_text)
	if len(sentences)<2:
		#Terminates if sentence count is less than 2, since cosine similiarity cannot be calculated in this case.
		return -1
	unique_words_in_source=identify_unique_words(source_text)
	#Vectorizes the sentences.
	sentence_vectors=vectorize_sentences(sentences,unique_words_in_source)
	#Invokes TextRank.
	average_similarities=textrank(sentence_vectors)
	#Generates and prints the summary.
	summary=generate_summary(sentences,average_similarities,compression_ratio)
	print(summary)
	return 0

if __name__=="__main__":
	main()
