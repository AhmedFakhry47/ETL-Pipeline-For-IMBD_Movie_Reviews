from pymongo import MongoClient
from Sentiment_ import *
import pandas as pd
import pymongo
import shutil
import json
import nltk
import os

#Get size of terminal for printing 
columns = shutil.get_terminal_size().columns

class ETL_pipeline():
	'''
	This class is for an ETL pipeline that handles the following:
	1- Extract text data (movies) from mondoDB
	2- Clean and transform/preprocess the movies.
	3- Store the preprocessed texts and labels into Json File (our data warehouse) that can be fed later 
	into a deep learning model.
	'''
	def __init__(self,meta=None):
		if(isinstance(meta,dict) ==0 ):
			assert 'please pass a dictionary with the meta data including the mongoDB_url' 
		self.mongoDB_url = meta['mongoDB_url']
		self.fextension  = meta['extension']

	def operate(self):
		#First step of the ETL pipeline is to start connection with the database and start collecting data
		self.cluster = MongoClient(self.mongoDB_url)
		self.db      = self.cluster["Movie_Review"]
		self.collection = self.db["IMBD_Reviews"]	
		self.collected_text = self.__collect()
		self.__transform()
		self.__store()

	def __pprint(self,stri='',i=0):
		if(i==0):print(str('____'+'Started '+stri+'____').center(columns))
		else: 
			print('.\n'.center(columns))
			print('.\n'.center(columns))
			print('.\n'.center(columns))
			print(str('____'+'Finished '+stri+'____').center(columns))

	def __navigate(self):
		'''
		A genr expression to pass through the huge number of documents stored in the database
		'''
		num_movies = self.collection.count()
		i = 0
		while(True):
			for movie in self.collection.find({}):
				if(i==num_movies):
					yield None
				yield movie
				i += 1

	def __collect(self):
		'''
		This function does the following:
		1-start connection with mongoDB
		2-go through the documents and collect useful information
		3-returns the collected information as a dataframe
		'''	

		staging_db = pd.DataFrame(columns=["Movie_N","Genre","Review","Stars"])
		movies = self.__navigate()
		self.__pprint(stri='Collection',i=0)
		for movie in movies:
			if(movie == None):
				break
			#Filtering unnecessary columns and add the rest 
			temp = {i:v for i,v in movie.items() if i in ['_id','genre','Reviews','users_rating']}
			temp = conversion_logic(temp)
			temp = pd.DataFrame.from_dict(temp, orient='index')
			staging_db = staging_db.append(temp,ignore_index=True)

		self.__pprint(stri='Collection',i=1)
		return staging_db


	def __transform(self):
		'''
		A function that does the preprocessing and the sentiment analysis over the text data
		'''
		self.__pprint(stri='Transform',i=0)
		self.collected_text['Reviews_preprocessed'] = self.collected_text['Review'].apply(preprocess) 
		self.collected_text['Part_of_Speech'] = self.collected_text['Review'].apply(pos_tag)
		self.__pprint(stri='Transform',i=1)

	def __store(self):
		'''
		One command function to store the preprocessed text into a json file
		'''
		self.__pprint(stri='storage',i=0)
		if(self.fextension =='json'):self.collected_text.to_json(path_or_buf=os.getcwd()+'/data.json',orient="columns")
		elif(self.fextension =='csv'):self.collected_text.to_csv(path_or_buf=os.getcwd()+'/data.csv',index=False)
		self.__pprint(stri='storage',i=1)