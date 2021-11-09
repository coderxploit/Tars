from gtts import gTTS
import speech_recognition as sr
import re
import time
import webbrowser
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import requests
import pygame
import urllib.request
import urllib.parse
import bs4
from pygame import mixer



def talk(audio,count):
    print(audio)
    for line in audio.splitlines():
        text_to_speech = gTTS(text = audio, lang = 'en-US')
        text_to_speech.save('audio{}.mp3'.format(count))
        mixer.init()
        mixer.music.load('audio{}.mp3'.format(count))
        mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        mixer.stop()

def myCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('Tars is listening')
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration = 1)
        audio = r.listen(source)
        print("analyzing...")

    try:
        command = r.recognize_google(audio).lower()
        talk('You said:', random.random())
        talk(command, random.random())
    
    
    except sr.UnknownValueError:
        print('Please Repeat!!')
        command = myCommand() 

    return command

def tars(command):
    errors = [
        "I don't Know What you mean",
        "Excuse me",
        "Will You Please Repeat?"
    ]

    if 'google' in command:
        talk("What should I search for you", random.random())
        command = myCommand()
        reg_ex = re.search('search(.*)',command)
        search_for = command.split('search',1)[1]
        print(search_for)
        url = 'https://www.google.com/'
        if reg_ex:
            subgoogle = reg_ex.group(1)
            url = url + 'r/' + subgoogle
            talk('okay!',random.random())
            driver = webdriver.Firefox(executable_path='C:\\Users\\Bae_wada\\Desktop\\rto\\geckodriver.exe')
            driver.get('http://www.google.com')
            search = driver.find_element_by_name('q')
            search.send_keys(str(search_for))
            search.send_keys(Keys.RETURN)


    elif 'email' in command:
        talk('What is the subject?',random.random())
        time.sleep(3)
        subject = myCommand()
        talk('What should I say?',random.random())
        message = myCommand()
        content = 'Subject: {}\n\n{}'.format(subject, message)

        #init gmail SMTP
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('pblexample21', '!2e45678')
        mail.sendmail('pblexample21','shubhamparmar1107@gmail.com', content)

        mail.close()
        talk('Email sent',random.random())
    
    elif 'youtube' in command:
        talk('Ok!',random.random())
        reg_ex = re.search('youtube (.+)', command)
        if reg_ex:
            domain = command.split("youtube",1)[1] 
            query_string = urllib.parse.urlencode({"search_query" : domain})
            html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
            search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
            #print("http://www.youtube.com/watch?v=" + search_results[0])
            webbrowser.open("http://www.youtube.com/watch?v={}".format(search_results))
            pass

    elif 'hello' in command:
        talk('Hello! I am TARS. How can I help you?',random.random())
        time.sleep(3)
    elif 'who are you' in command:
        talk('I am one of four former U.S. Marine Corps tactical robots',random.random())
        time.sleep(3)
    else:
        error = random.choice(errors)
        talk(error,random.random())
        time.sleep(3)





talk("Hello I'am Tars!", random.random())
while True:
    time.sleep(2)
    audio = "Hello I'am Tars"
    tars(myCommand())
