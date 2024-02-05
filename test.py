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
#import nlpbots

model = load_model("C:/Users/thema/Desktop/NLPassistant/NLP.h5")
with open("C:/Users/thema/Desktop/NLPassistant/train.json") as file:
    intents = json.load(file)

# Load words and classes from the pickle files
with open('C:/Users/thema/Desktop/NLPassistant/words.pkl', 'rb') as f:
    words = pickle.load(f)

with open('C:/Users/thema/Desktop/NLPassistant/classes.pkl', 'rb') as f:
    classes = pickle.load(f)

# create an object of WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
tokenizer = Tokenizer()
max_sequence_length = 49


def activate_mic():
    # Run your script (friday.py) using subprocess
          Popen(['python', 'C:/Users/thema/Desktop/NLPassistant/friday.py'])


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


def send(event = None):
    msg = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    text_length = len(msg)
    if msg != '':
        Chat_frame.config(state=NORMAL)

        Chat_frame.tag_config("user", foreground="#000000", background="light blue", font=("Courier",14, "bold"))
        Chat_frame.insert(END, f'YOU    : {msg} \n', "user")
        if msg == "end":
             Chat_frame.insert(tk.END, "FRIDAY : Thank You sir, I hope I assisted you properly\n")
             root.destroy()

        else:
             response = chatbot_response(msg)
             text_length1 = len(response)

             Chat_frame.tag_config("assistant", foreground="#000000", background="light green", font=("Courier", 14))
             Chat_frame.insert(tk.END, f'FRIDAY : {response} \n', "assistant")

        Chat_frame.config(state=DISABLED)
        Chat_frame.yview(END)


root = Tk()
root.title("NLP Assistant")
root.geometry('800x600')
root.resizable(width=FALSE, height=FALSE)
message = tk.StringVar()


intro_message = "Hello, I'm Friday, your Assistant. How can I help you today?\n\n"
Chat_frame = Text(root, bd=0, bg="white", height="8", width="50", font="Helvetica")
Chat_frame.insert(END, intro_message)
Chat_frame.config(state=DISABLED)
Chat_frame.pack(fill="both", expand=True)


scrollbar = Scrollbar(root, command=Chat_frame.yview, cursor="heart",width=8)
Chat_frame['yscrollcommand'] = scrollbar.set


SendButton = Button(root, font=("Verdana",12,'bold'), text="Send", width="12", height=5, bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff', command= send )


EntryBox = Text(root, bd=0, bg="white",width="29", height="5", font="Arial")


def activate_mic_and_send():
    activate_mic()
    send()


Chat_frame.tag_config('usr', foreground='black', justify='right')
Chat_frame.tag_config('assistant', foreground='black', justify='left')
button_send = Button(root, text="♾", bg='dark green', activebackground='grey', command=send, width=30, height=30, font=('Arial',50))
button_send.place(x=690, y=540, height=60, width=110)

mic_image = PhotoImage(file="C:/Users/thema/Desktop/NLPassistant/mic.png").subsample(2,3)
button_mic = Button(root, image=mic_image, bg='blue', activebackground='white', command=activate_mic_and_send, width=12, height=2, font=('Arial'))
button_mic.place(x=580, y=540, height=60, width=110)

EntryBox.bind('<Return>', send)


scrollbar.place(x=780,y=6, height=530,width=8)
Chat_frame.place(x=6,y=6, height=530, width=770)
EntryBox.place(x=1, y=540, height=60, width=580)

root.mainloop()
