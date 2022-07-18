import speech_recognition as sr
from gtts import gTTS
from translate import Translator
import random
import playsound
import os   
import pyowm
from city import *

owm = pyowm.OWM('5d3ff5ff43be72d71e13cba6accf2337')

# Приветствие англ. вариант
priv = 'hello','Hello','hi','Hi','good morning','Good morning','good evening',\
    'Good evening','good night','Goof night','hey','Hey'
# Прощание англ. вариант
prosh = 'bye','Bye','good bye','Good bye','see you','See you'
# Знакомство англ. вариант
znak = 'how are you','How are you',"What's up","what's up",'How are you doing',\
    'how are you doing',"How's it going","how's it going","How's life","how's life"

def listen():
    voise_recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something: ')        
        audio = voise_recognizer.listen(source)

    try:
        voice_text = voise_recognizer.recognize_google(audio, language='en')
        print(f'You are said: ...{voice_text}')
        return voice_text
    except sr.UnknownValueError:
        return 'Ошибка распознания!'        
    except sr.RequestError:
        return 'Ошибка соединения!'
    text = input('Enter: ')
    print(f'Вы сказали {text}')

    return text

def say(text):
    voice = gTTS(text)
    unique_file = "audio_" + str(random.randint(0,100000)) + '.mp3'  # audio .mp3
    voice.save(unique_file)

    playsound.playsound(unique_file)    
    os.remove(unique_file)

    print(f'Assistent: {text}')

def weather(command):
    # listen()
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(command)
    w = observation.weather
    temp = w.temperature('celsius')['temp']

    say(f'In town {command} just {w.detailed_status}')
    say(f'Temperature in district {temp}')

def translate(trans):
    # listen()
    translator = Translator(to_lang="ru")
    translation = translator.translate(trans)
    say(translation)

def handle_command(command):
    if command in priv:
        say('Hi-hi')
    elif command in znak:
        say('Pretty good, and you?')
    elif command in prosh:
        stop()
    elif command in cities:
        weather(command)
    elif command in sities:
        weather(command)
    elif command == 'translate' or command == 'Translate':
        say('Say the word or proposal to translate!')
        trans = input('...: ')
        translate(trans) 
    else:   
        say('Sorry, can you repeat?')

def stop():
    say('See you later!')
    exit()

def start():
    print('Start assistent...')

    while True:
        command = listen()
        handle_command(command)

try:
    start()
except KeyboardInterrupt:
    stop()