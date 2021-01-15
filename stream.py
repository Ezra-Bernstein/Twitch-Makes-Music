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
score = stream.Score()
numNotes = 1
composers = []


STREAMER_NAME="ezra0110"

twitch.Chat(channel='#'+STREAMER_NAME, nickname=STREAMER_NAME, oauth=OAUTH_TOKEN).subscribe(
    lambda message: message_handler(message))

def message_handler(message):
    # global composers
    global score
    global composers
    message_text = message.text
    message_sender = message.sender
    print(message_sender, message_text)
    arr = message_text.split(',')
    lastNote=None
    # print(arr)
    try:
        if len(arr) == 2 and arr[0] != '' and arr[1] != '' and arr[0] == "join":
            if message_sender not in composers:
                part = stream.Part()
                part.insert(0, instrument.fromString(arr[1]))
                part.id = message_sender
                part.partName = message_sender
                score.insert(0,part)
                print(part)
                composers.append(message_sender)
        elif message_text == "join":
            if message_sender not in composers:
                part = stream.Part()
                part.id = message_sender
                part.partName = message_sender
                score.insert(0,part)
                print(part)
                composers.append(message_sender)
        elif message_text == "stop" and message_sender == STREAMER_NAME:
            # score.metadata.composer = "Ezra0110"
            # for composer in composers:
            #     score.metadata.composer = score.metadata.composer + ", " + composer
            
            score.show()
        elif message_text == "reset" and message_sender == STREAMER_NAME:
            score.clear()
            score.write('musicxml.png', 'musicxml.png')
        elif len(arr) == 2 and arr[0] != '' and arr[1] != '' and message_sender in composers:
            #lastNote=None
            if arr[0] == "key" and re.match("^-?\d+$", arr[1]):
                score.parts.stream()[message_sender].append(key.KeySignature(int(arr[1])))
                score.write('musicxml.png', 'musicxml.png')
            else:

                if re.match("^[a-gA-G](#{0,3}|-{0,3})\d*$", arr[0]):
                    note_name = arr[0]
                else:
                    raise Exception('Invalid Note Name!!!')
                #note_octave = arr[1]
                note_duration = float(arr[1]) if re.match("^(\d*\.\d+|\d+\.\d*|\d+)$",arr[1]) else arr[1]
                # add_composer(message_sender)
                lastNote = add_to_score(score, note_name, note_duration, message_sender)# note_octave,)
                score.write('musicxml.png', 'musicxml.png')
    except Exception as e:
        print(e)
    #   print("yikes")
        if lastNote != None:
            #stream=score.notesAndRests 
            # last=stream.getElementById(stream.streamLength-1) 
            score.remove(lastNote, shiftOffsets=True)
        



def add_to_score(score, note_name, note_duration, message_sender): # note_octave,
    global numNotes
    global composers
    numNotes += 1
    n = note.Note(note_name)# + note_octave)
    n.duration = duration.Duration(note_duration)
    # print(n)
    # print(n.name)
    # print(n.duration)
    last = n
    score.parts.stream()[message_sender].append(n)
    # score.append(n)
    return last
    
# def add_composer(message_sender, composers):
#     if message_sender not in composers:
#         composers.append(message_sender)
