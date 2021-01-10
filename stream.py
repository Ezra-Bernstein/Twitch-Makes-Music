import twitch
from dotenv import load_dotenv
import os
from music21 import *
import re

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")


helix = twitch.Helix(CLIENT_ID, CLIENT_SECRET)
score = stream.Stream()
numNotes = 1
# composers = []

twitch.Chat(channel='#ezra0110', nickname='Ezra0110', oauth=OAUTH_TOKEN).subscribe(
    lambda message: message_handler(message))

def message_handler(message):
    # global composers
    global score
    message_text = message.text
    message_sender = message.sender
    print(message_sender, message_text)
    arr = message_text.split(',')
    if message_text == "stop" and message_sender == "ezra0110":
        # score.metadata.composer = "Ezra0110"
        # for composer in composers:
        #     score.metadata.composer = score.metadata.composer + ", " + composer
        score.show()
    elif len(arr) == 2:
        note_name = arr[0]
        #note_octave = arr[1]
        note_duration = float(arr[1]) if re.match("^(\d*\.\d+|\d+\.\d*|\d+)$",arr[1]) else arr[1]
        # add_composer(message_sender)
        add_to_score(score, note_name, note_duration)# note_octave,)
        




def add_to_score(score, note_name, note_duration): # note_octave,
    global numNotes
    
    numNotes += 1
    n = note.Note(note_name)# + note_octave)
    n.duration = duration.Duration(note_duration)
    
    print(n)
    score.append(n)
    
# def add_composer(message_sender):
#     global composers
#     if message_sender not in composers:
#         composers.append(message_sender)
