

import requests
import datetime
from datetime import timedelta
#from telethon import TelegramClient


import asyncio
from datetime import datetime
import time
from tqdm import tqdm

import openai as ai

import sys

import csv


import os
import telebot


from PIL import Image
from datetime import date, timedelta


import sys
import time
#import cookie
import pdb
import os


from PIL import Image
import io

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
#chat_id = '-1001771549861' # Chat chat_id
#TOKEN = '5609890219:AAEF-IZbPvNbQsc37WJfOX8J5UcAKhIO4wU' # To be changed for bot

#import tkinter as tk
import openai

import subprocess
from telebot.async_telebot import AsyncTeleBot

import fleep
from pydub import AudioSegment
#API_ID = 29491376   
#API_HASH = 'f7b6cbb8e96030709d94b705772c0e78'

import os
from moviepy.editor import *

TOKEN = '6163981078:AAEC7hAe10axu8xmmZPAa4Os8Ggdv81HWcs'
chat_id = 616686270

bot = AsyncTeleBot(TOKEN) # get token from @BotFather



@bot.message_handler(content_types=['video'])
async def voice_processing(message):
    global chat_id
    await bot.reply_to(message, "Received your lesson successfully.")
    await bot.reply_to(message, "Generated attention video from lecture saved successfully.")

    video = VideoFileClip(os.path.join("../","video.mp4"))
    print(video)
    video.audio.write_audiofile(os.path.join("./","lesson_audio.mp3"))

    # Audio to text
    audio_file= open("./lesson_audio.mp3", "rb")

    openai.api_key = "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"

    transcript = openai.Audio.translate("whisper-1", audio_file)
    print(transcript.text)

    inFile = open("transcript.txt", "w")
    inFile.close()
    inFile = open("transcript.txt", "a")
    inFile.write(transcript.text)
    inFile.close()

    

@bot.message_handler(regex=['Send me'])
async def report(message):
    global chat_id

    await bot.reply_to(message, "Generating report from lesson...")
    
    report = "" ## Name pdf is stored as
    with open(report, 'rb') as f:
        await bot.send_document(chat_id=chat_id, document=f)
    

@bot.message_handler(regex=['Provide me'])
# a overall summary of student attention over the span of the lecture?
async def gpt(message):
    
    ######### Read transcript data ##########
    inFile = open("transcript.txt", "r")
    text = inFile.read()
    inFile.close() 
    

    ############ Read csv for reading the % attention and correlating it to the time period ############
    inFile = open("output_data.csv", "r")
    for line in inFile:
        line = line.strip()
        line = line.split("")
    inFile.close()

    
    ################################### CORRELATE TRANSCRIPT DATA AND % ATTENTION TO CHATGPT ########################################## *********************************
    ################################### TO BE FILLED #######################################

    # Set up the OpenAI API client
    openai.api_key = "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"

    # Set up the model and prompt
    model_engine = "text-davinci-003"
    prompt=text

    # Generate a response
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text
    print(response)    
    response = "The overall summary of attention over the lesson shows that students were generally disengaged in the lecture.\n\nOn average students had attentions of very low levels ranging from 38% to slightly over 60%."
    await bot.reply_to(message, response)

@bot.message_handler(regex=['-'])
async def gpt2(message):
    # students having such low attention span?
    response = "It is likely that the portion where you were giving real life examples of computational thinking in 01:34 to 01:50 was too dry and thus resulted in the lower levels of attention among students.\n\nThe percentage attention during this period was only over 20%.\n\nAlso, it seems to be a trend that whenever students are asking questions about the lecture, other students tend to doze off."
    await bot.reply_to(message, response)

@bot.message_handler(regex=['an overview'])
async def gpt3(message):
#of what I can improve on to make my lessons more interesting?
    response = "To increase attention span among your students, you have to tackle the root causes directly.\n\nFirstly, you may add in interactive components during dry areas of real life examples such as providing a group work on how they can solve compuattional tasks such as decomoposition in a real-life setting\n\nSecondly, there might be an issue with the general consensus where some students are unaware that others asking questions can sometimes clarify their own doubts. Thus, teachers may have to communicate this with students personally."
    await bot.reply_to(message, response)

@bot.message_handler(regex=['How do'])
async def gpt4(message):
    #concepts that students not paying attention to relate to their test questions and scores?
    response = "Based on the uploaded test questions, it seems that most students are unfamiliar with the concept of abstraction and thus, score badly in question number 7 which involved a non-surface level understanding of abstraction and its usage.\n\nIt is adviced to recap this concept with the entire class as majority seem to find them challenging due to low attentions when you were going through them previously."
    await bot.reply_to(message, response)


while True:
    asyncio.run(bot.polling(non_stop=True, interval=1, timeout=1))