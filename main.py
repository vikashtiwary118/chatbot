# -*- coding: utf-8 -*-
from chatterbot import ChatBot #import chatbot

from chatterbot.trainers import ListTrainer#Method to train chatbot
import os

bot=ChatBot('Test') #create the chatbot

#conv=open('chat.text','r').readlines()

bot.set_trainer(ListTrainer)#set the trainer

#bot.train(conv)#train the bot
for _file in os.listdir('files'):
    chats=open('files/'+_file,'r').readlines()
    bot.train(chats)
while(True):
     request=input('You:')
     response=bot.get_response(request)
     print('bot:',response)
    

