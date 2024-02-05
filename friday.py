
import pyttsx3 as p
import speech_recognition as sr
import pygame


engine = p.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
print(voices)


def speak(text):
    engine.say(text)
    engine.runAndWait()


r = sr.Recognizer()


def start_friday():
    greeting = f"Hello sir , My Name is Friday,Your Service Assistant ,How are You sir ?"
    speak(greeting)


start_friday()

with sr.Microphone() as source:
    r.energy_threshold = 400
    r.adjust_for_ambient_noise(source, 1.2)
    print("Listening to You sir : ")
    audio = r.listen(source)
    text2 = r.recognize_google(audio)
    print("You Told : "+text2)

if "Happy" in text2 or "good" in text2 or "you" in text2 or "fine " in text2:
    speak("I'm Happy you are doing good ,")
speak("What can I do For you ? ")


import google_trans
from google_trans import Translator
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound
import os


def trans():
  print(google_trans.LANGUAGES)

  # kn - kannada   en - english

  mic = sr.Microphone()
  r = sr.Recognizer()

  with mic as source:
         translator = Translator()
         input_language = (input("Select Language from : "))
         output_language = (input("Select your Language To : "))

         print("Speak the text that need to be translated ..")
         r.adjust_for_ambient_noise(source,duration=0.2)
         audio3 = r.listen(source)
         text3 = r.recognize_google(audio3)

         print("You told : "+text3)
         trans_to = translator.translate(text3,src=input_language,dest=output_language)
         transed_text = trans_to.text
         print("The translated meaning is : "+transed_text)
         speak = gTTS(text=transed_text, lang=output_language, slow=False)
         speak.save("captured_voice.mp3")
         #playsound('captured_voice.mp3')
         #os.remove('captured_voice.mp3')

         pygame.mixer.init()
         pygame.mixer.music.load('captured_voice.mp3')
         pygame.mixer.music.play()

         print(transed_text)

#last =trans()
#print(last)



from selenium import webdriver
import time

class Google():
    def __init__(self):
     self.driver=webdriver.Chrome()

    def gettext(self,query):
        self.query = query
        self.driver.get("https://www.google.co.in/")
        find = self.driver.find_element("xpath",'//*[@id="APjFqb"]')
        find.click()
        find.send_keys(query)
        enter = self.driver.find_element("xpath",'/html/body/div[1]/div[3]/form/div[1]/div[1]/div[2]/div[2]/div[6]/center/input[1]')
        enter.click()
        time.sleep(6)

#ob = Google()
#ob.gettext('Is the combination of vitamin c and vitamic b3 is possible without side effects ')


class toKnow():
    def __init__(self):
     self.driver=webdriver.Chrome()

    def getinfo(self,query):
        self.query = query
        self.driver.get("https://www.wikipedia.org//")
        search = self.driver.find_element("xpath",'//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element("xpath",'//*[@id="search-form"]/fieldset/button/i')
        enter.click()
        time.sleep(6)

#ob = toKnow()
#ob.getinfo('Thomas alva edison')

from selenium import webdriver
import time

class Review:
    def __init__(self):
      self.driver = webdriver.Chrome()

    def getreview(self , query):
        self.query = query
        self.driver.get("https://www.youtube.com/results?search_query="+query)
        search = self.driver.find_element("xpath",'//*[@id="dismissible"]/ytd-thumbnail')
        search.click()
        time.sleep(10)

#ob = Review()
#ob.getreview()

i = 0
while True:
    with sr.Microphone() as source:
        r.energy_threshold = 400
        r.adjust_for_ambient_noise(source, 1.2)
        print("After One task , Moving to new Task . Tell me Sir What do want again ...")
        audio_new = r.listen(source)
        text2 = r.recognize_google(audio_new)

    try:
        print("You Told: " + text2)

        if "Friday" in text2:
            speak("Yes sir! I am listening")

        elif "data" in text2 or "something" in text2 or "about this" in text2:

            speak("Tell me about which info do you need?")

            with sr.Microphone() as source3:
                r.energy_threshold = 450
                r.adjust_for_ambient_noise(source3, 1.2)
                print("Following your words with wiki...")
                audio1 = r.listen(source3)
                info = r.recognize_google(audio1)
                print("You told : " + info)
            speak("Searching for {} in Wiki".format(info))
            aut = toKnow()
            aut.getinfo(info)
            speak("Do you need something else, sir?")

        elif "product" in text2 or "review" in text2 or "video" in text2:
            speak("Mention the product name, sir?")
            with sr.Microphone() as source2:
                r.energy_threshold = 450
                r.adjust_for_ambient_noise(source2, 1.2)
                print("Following your words with product ...")
                audio2 = r.listen(source2)
                vid = r.recognize_google(audio2)
                print("You Told: " + vid)
                print("Playing this product review on YouTube ")
            ass = Review()
            ass.getreview(vid)
            time.sleep(2)
            speak("Do you need something else, sir?")

        elif "translate" in text2 or "language" in text2:
            speak("Providing you the necessary options to select languages ")

            d = trans()
            print(d)
            time.sleep(2)
            speak("Do you need something else, sir?")

        elif "Google" in text2 or "search" in text2:
            g = "What do you want me to google sir ?"
            speak(g)

            with sr.Microphone() as source3:
                r.energy_threshold = 450
                r.adjust_for_ambient_noise(source3, 1.2)
                print("Following your words with google ...")
                audio20 = r.listen(source3)
                info = r.recognize_google(audio20)
                print("You told : " + info)
            speak("Searching for {} in google".format(info))
            ser = Google()
            ser.gettext(info)
            speak("Do you need something else, sir?")

        elif "bye" or "see you later" in text2:
            b = "Thank you sir, Hope we meet soon and Have a Good Day Sir !! "
            speak(b)
            print("Bye, Sir, You can contact me whenever you need me to Assist you ")
            break

        else:
            break

    except sr.UnknownValueError:
        print("I am listening, sir...")

    i = i+1

print("Thank you sir, Hope we meet soon and Have a Good Day Sir !! ")





