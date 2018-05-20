# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 17:04:53 2017

@author: Avinash
"""

import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk.tokenize import word_tokenize

vectorizer = TfidfVectorizer(stop_words='english',analyzer='word',lowercase=True,max_features=1100)

data={
  "greet": {
	"examples" : ["hello","hey there","howdy","hello","hi","hey","hey ho"]
	
  },
  "coffee": {
	"examples" : [
	  "i would like to have coffee",
	  "i would like to have coffee with soy milk",
	  "can you please get me a coffee with almond milk",
	  "can you please get me a coffee",
	  "i need a coffee with soy milk",
	  "maybe coffee",
	  "coffee it is!!!!",
	  "what italian options do i have",
	  "i want coffee",
	  "can you please get me a coffee",
	  "i love to have coffee",
	  "i will go with coffee this time",
	  "coffee",
	  "need a coffee",
	  "need to order a cup coffee",
	  "can i get a coffee",
	  "get me a coffee",
	  "get me a coffee please"

	],
  },
  "cappuccino": {
	"examples" : [
	  "i would like to have cappuccino with soy milk",
	  "i will go with cappuccino this time",
	  "i like to go with cappuccino and soy milk",
	  "i want cappuccino with almond milk",
	  "i need a cappuccino with almond milk",
	  "can you please get me a cappuucino with soy milk",
	  "can you get me a cappuccino",
	  "nothing can beat cappuccino",
	  "i love to have cappuccino"
	  "cappuccino",
	  "can you get me a cappuccino",
	  "please get me a cappuccino",
	  "can you please get me a cappuccino",
	  "i like to have cappuccino",
	  "need to order a cappuccino",
	  "please can i have cappuccino",
	  "i like to have cappuccino",
	  "i want to have cappuccino"
	]
  },
  "update": {
	"examples": [
	   "actually go with soy milk",
	   "can you change it to coffee",
	   "can you change it to cappuccino",
	   "no i changed my mind.please go with coffee",
	   "no i changed my mind.please go with cappuccino",
	   "update it with almond milk",
	   "change it to almond milk",
	   "change it to soy milk",
	   "i want to update",
	   "can you please update my order",
	   "i want to change my order",
	   "updte with coffee",
	   "i want to update my order",
	   "i want to change it",
	   "update it with soy milk"
	]

  },
  "end": {
	"examples" : [
	  "thank you",
	  "i am pleased",
	  "you are best",
	  "i am happy"
	  "thanks is a small word for you",
	  "thanks",
	  "thank you",
	  "end",
	  "thank you for your service",
	  "thnk you",
	  "thank u",
	  "i am done",
	  "done",
	  "end",
	  "i want to end the order",
	  "i want to close it",
	  "thanks"
	]
  }

}


is_confirmed = 0
training_text = []



training_text = []
training_class = []

for label in data.keys():
	for text in data[label]["examples"]:
		training_class.append(label)
		training_text.append(text)



X_vector = vectorizer.fit_transform(training_text)

clf = MultinomialNB()
clf.fit(X_vector,training_class)



order_json = {}


def greeting_intent():
	print('Bot: Hey I am your Cafe Coffee Day Assistant.\nI can help you with booking coffee and cappuccino.')

def end_intent():
	print('It is pleasure having you here.')


def cleaning_message(message):
	tokens = word_tokenize(message)
	tokens_clean = [re.sub(r'[^a-zA-Z0-9]' ,'',each_word) for each_word in tokens]
	tokens_final = [each_word.lower() for each_word in tokens_clean if len(each_word)]
	return tokens_final


def intent_prediction(message):
	out_put = []
	message_tokens = cleaning_message(message)
	message_string = (' '.join(message_tokens))
	out_put.append(message_string)
	out_put_vector = vectorizer.transform(out_put)
	out_put_class = clf.predict(out_put_vector)
	return out_put_class[0]




def beverage_intent(message):
	message_tokens = cleaning_message(message)
	if 'coffee' in message_tokens:
		order_json['beverage_type'] = 'coffee'
	elif 'cappuccino' in message_tokens:
		order_json['beverage_type'] = 'cappuccino'
	else:
		order_json['beverage_type'] = None
	
	if order_json.get('beverage_type'):
		if 'soy' in message_tokens or 'almond' in message_tokens:
			order_json['milk_type'] = 'soy' if 'soy' in message_tokens else 'almond'
		else:
			milk_choice = input('Bot: Please enter your milk choice type Soy or Almond\nUser: ')
			milk_choice_tokens = cleaning_message(milk_choice)
			if 'soy' in milk_choice_tokens or 'almond' in milk_choice_tokens:
				order_json['milk_type'] = 'soy' if 'soy' in milk_choice_tokens else 'almond'
			else:
				milk_choice = input('Bot: Can you please restrain your self in entering to Soy or Almond\nUser: ')
				milk_choice_tokens = cleaning_message(milk_choice)
				if 'soy' in milk_choice_tokens or 'almond' in milk_choice_tokens:
					order_json['milk_type'] = 'soy' if 'soy' in milk_choice_tokens else 'almond'
				else:
					print('Bot:Sorry for not being able to serve you right now,I am still learning\n')
		if order_json.get('beverage_type') and order_json.get('milk_type'):
			print('Bot: Your order is %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
			update_choice = input('Bot: Your above Displayed order is final: Yes or No\nUser: ')
			if update_choice.strip().lower() == 'no':
				update_intent(input('Bot: Please enter your updated choice\nUser: '))
			elif update_choice.strip().lower() == 'yes':
				print('Bot: Great will be back with your order')
				global is_confirmed
				is_confirmed = 1
				time.sleep(3)
				print('Bot: Here is your order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
			else:
				order_json.clear()
				print('Bot: Sorry for it I am still learning.\n')
		else:
			order_json.clear()
	else:

		print('Bot: Sorry Seems like it was a wrong intent prediction.Sorry for it.\n')
		order_json.clear()

	




def update_intent(message):
	if len(order_json):
		message_tokens = cleaning_message(message)
		if any(x in message_tokens for x in ['coffee', 'cappuccino','soy','almond']):
			if any(x in message_tokens for x in ['coffee','cappuccino']):
				# print "Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['beverage_type'])
				order_json['beverage_type'] = 'coffee' if 'coffee' in message_tokens else 'cappuccino'
				if  any(x in message_tokens for x in ['soy','almond']):
					# print "Bot: Seems like you are not satisfied with %s milk will change it right away"%(order_json['milk_type'])
					order_json['milk_type'] = 'soy' if 'soy' in message_tokens else 'almond'
					print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
				else:
					milk_choice_assert = input('Bot: Are you satisfied with Milk Type\nUser: ')
					if milk_choice_assert.strip().lower() == 'no':
						print('Bot: I will change %s milk type right away'%(order_json['milk_type']))
						order_json['milk_type'] = 'soy' if 'almond' == order_json['milk_type'] else 'almond' 
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					elif milk_choice_assert.strip().lower() == 'yes':
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					else:
						print('Bot: Sorry for it I am still learning.Can you please type Yes or No\n')
						milk_choice_assert = input('User: ')
						if milk_choice_assert.strip().lower() == 'no':
							print('Bot: I will change %s milk type right away'%(order_json['milk_type']))
							order_json['milk_type'] = 'soy' if 'almond' == order_json['milk_type'] else 'almond' 
							print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
						elif milk_choice_assert.strip().lower() == 'yes':
							print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
						else:
							global is_confirmed
							if (is_confirmed):
								order_json['beverage_type'] = 'coffee' if order_json['beverage_type'] == 'cappuccino' else 'cappuccino'
							else:
								order_json.clear()
							print('Bot:Sorry for not being able to serve you right now,I am still learning\n')
			
			elif any(x in message_tokens for x in ['soy','almond']):
				print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['milk_type']))
				order_json['milk_type'] = 'soy' if 'soy' in message_tokens else 'almond'
				if  any(x in message_tokens for x in ['coffee','cappuccino']):
					print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['beverage_type']))
					order_json['beverage_type'] = 'coffee' if 'coffee' in message_tokens else 'cappuccino'
					print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
				else:
					beverage_choice_assert = input('Bot: Are you satisfied with beverage Type\nUser: ')
					if beverage_choice_assert.strip().lower() == 'no':
						print('Bot: I will change %s right away'%(order_json['beverage_type']))
						order_json['beverage_type'] = 'coffee' if 'cappuccino' == order_json['beverage_type'] else 'cappuccino'
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					elif beverage_choice_assert.strip().lower() == 'yes':
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					else:
						if (is_confirmed):
							order_json['milk_type'] = 'soy' if order_json['milk_type'] == 'almond' else 'soy'
						else:
							order_json.clear()
						print('Bot:Sorry for not being able to serve you right now,I am still learning\n')

		else:
			beverage_change = input('Bot: Do you want me to change the beverage,Please type Yes or No.\nUser: ')
			if beverage_change.strip().lower() == 'yes':
				print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['beverage_type']))
				order_json['beverage_type'] = 'coffee' if 'cappuccino' == order_json['beverage_type'] else 'cappuccino'
				milk_change = input('Bot: Do you want me to change the milk, Yes or No\nUser: ')
				if milk_change.strip().lower() == 'yes':
					print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['milk_type']))
					order_json['milk_type'] = 'soy' if 'almond' == order_json['milk_type'] else 'almond'
					print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
				elif milk_change.strip().lower() == "no":
					print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
				else:
					milk_change = input('Bot:Can you Please type Yes or no\nUser: ')
					if milk_change.strip().lower() == 'yes':
						print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['milk_type']))
						order_json['milk_type'] = 'soy' if 'almond' == order_json['milk_type'] else 'almond'
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					elif milk_change.strip().lower() == "no":
						print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
					else:
						if (is_confirmed):
							order_json['beverage_type'] = 'coffee' if order_json['beverage_type'] == 'cappuccino' else 'cappuccino'
						else:
							order_json.clear()
						print('Bot: Sorry for it I am still learning\n')
			elif beverage_change.strip().lower() == 'no':
				print("Bot: Seems like you are not satisfied with %s will change it right away"%(order_json['milk_type']))
				order_json['milk_type'] = 'soy' if 'almond' == order_json['milk_type'] else 'almond'
				print('Bot: this is your updated order %s with %s milk type'%(order_json['beverage_type'],order_json['milk_type']))
			else:
				if(is_confirmed):
					print('Bot: Sorry for it I am still learning.\n')
				else:
					order_json.clear()

					print('Bot: Sorry for it I am still learning.\n')
	else:
		print('Bot: Sorry Nothing to update\n')



if __name__ == '__main__':
	greeting_intent()
	while(1):
		user_response = input('User: ')
		if intent_prediction(user_response) == 'coffee' or intent_prediction(user_response) == 'cappuccino':
			beverage_intent(user_response)
		elif intent_prediction(user_response) == 'update':
			update_intent(user_response)
		elif intent_prediction(user_response) == 'end':
			end_intent()
			break
		elif intent_prediction(user_response) == 'greet':
			greeting_intent()
			continue
		if order_json.get('beverage_type'):
			print ('\nBot:Relishing it!!!.\nBot: For Modifying your order,Please type update.\nBot: Liked it try other combinations\n')
		else:
			greeting_intent()

	print ("Bot: Hope you had a seeming experience")

