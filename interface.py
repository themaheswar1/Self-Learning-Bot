import random
import tkinter as tk
from tkinter import *
from subprocess import Popen
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import json
#import nlpbot

model = load_model("C:/Users/thema/Desktop/NLPassistant/NLP.h5")
with open("C:/Users/thema/Desktop/NLPassistant/train.json") as file:
    intents = json.load(file)

# Load words and classes from the pickle files
with open('words.pkl', 'rb') as f:
    words = pickle.load(f)

with open('classes.pkl', 'rb') as f:
    classes = pickle.load(f)

# create an object of WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
tokenizer = Tokenizer()
max_sequence_length = 49


def activate_mic():
    # Run your script (friday.py) using subprocess
    Popen(['python', 'friday.py'])


def clean_up_sentence(sentence):

    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)

    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words, show_details=True):

    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:

                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))


def predict_class(sentence, model):

    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    error = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>error]

    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []

    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(text):
    ints = predict_class(text,model)
    res = getResponse(ints,intents)
    return res


def send_msz(event=None):
    usr_input = message.get()
    usr_input = usr_input.lower()

    user_text_label = tk.Label(text_box_chat_history, text=f'You: {usr_input}', font=('Times New Roman', 10, 'bold'), bg='lightblue')
    user_text_label.pack(padx=10, pady=5, anchor='w')

    if usr_input == "end":
        text_box_chat_history.insert(tk.END, "NLPAssistant : Thank You sir, I hope I assisted you properly\n")
        root.destroy()
    else:
        response = chatbot_response(usr_input)
        assistant_text_label = tk.Label(text_box_chat_history, text=f'NLPAssistant: {response}', font=('Arial', 10), bg='lightgreen')
        assistant_text_label.pack(padx=10, pady=5, anchor='w')

        enter_msg_from_user_window.delete(0, tk.END)


def activate_mic_and_send():
    activate_mic()
    send_msz()


root = tk.Tk()
root.title("NLPAssistant")
root.geometry('800x600')
root.resizable(False, False)

message = tk.StringVar()

default_response ="Hi , This is Friday! Your Assistant"
default_Label = tk.Label(text=default_response, font=('Arial', 14),fg='Brown', wraplength=1000,padx=10, pady=10)
default_Label.pack()


text_box_chat_history = tk.Text(root, bd=1, bg='white', width=50, height=20)
text_box_chat_history.pack(fill="both", expand=True)

scrollbar = Scrollbar(root, command=text_box_chat_history.yview, cursor="heart",width=15)
text_box_chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")

enter_msg_from_user_window = tk.Entry(root, width=30, textvariable=message)
enter_msg_from_user_window .place(x=1, y=540, height=60, width=579)
enter_msg_from_user_window .focus()

text_box_chat_history.config(fg='black')
text_box_chat_history.tag_config('usr', foreground='black')
text_box_chat_history.config(fg='black')
text_box_chat_history.tag_config('usr', foreground='black', justify='right')
text_box_chat_history.tag_config('assistant', foreground='black', justify='left')


button_send = tk.Button(root, text='Send', bg='dark green', activebackground='grey', command=send_msz, width=12, height=5, font=('Arial'))
button_send.place(x=690, y=540, height=60, width=110)

mic_image = tk.PhotoImage(file="C:/Users/thema/Desktop/NLPassistant/mic.png").subsample(2, 3)
button_mic = tk.Button(root, image=mic_image, bg='blue', activebackground='white', command=activate_mic_and_send, width=12, height=2, font=('Arial'))
button_mic.place(x=580, y=540, height=60, width=110)

root.bind('<Return>', send_msz)
scrollbar.place(x=760,y=6, height=530,width=4)


root.mainloop()
