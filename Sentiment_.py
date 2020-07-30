'''
A couple of helper functions for the text preprocessing 
'''
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk import pos_tag
import re


def conversion_logic(dictionary):
	Reviews = dictionary['Reviews']
	Movie_N = dictionary['_id'] 
	Genre   = dictionary['genre']
	All_in  = {i:{} for i in range(len(Reviews))}

	for i,review in enumerate(Reviews):
		All_in[i]['Movie_N']= Movie_N
		All_in[i]['Genre']  = Genre
		#print(Reviews[i])
		All_in[i]['Review'] = Reviews[str(i)][0]
		All_in[i]['Stars']  = Reviews[str(i)][1] 
	return All_in


def preprocess(text):
	# For noise removal
	removals   = '(^[0-9A-Za-z])|^rt|http.+?'
	stop_words = stopwords.words('english')
	word_lemmatizer = WordNetLemmatizer()

	#Remove unnecessary characters
	text = re.sub(removals,' ',text)
	text = text.lower()

	# First step is tokenizing the text
	tokens = word_tokenize(text)
 
	# Second is converting words to their roots
	words  = [word_lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
	return words

def part_of_speech(text):
	return nltk.pos_tag(text)












	

