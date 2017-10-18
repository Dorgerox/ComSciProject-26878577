import spacy
from datetime import datetime

nlp = spacy.load('en')

# This function handles extracting keywords from a tweet. Use both entity recognition and POS tagging
def extractingText(tweet):
    keyInfoList = []
    tempTweet = nlp(tweet)
    for ent in tempTweet.ents:
        if ent.label_ == 'LOC' or ent.label_ == 'GPE' or ent.label_ == 'EVENT' or ent.label_ == 'FACILITY' or ent.label_ == 'DATE' or ent.label_ == 'TIME':
            for i in ent.string.rstrip().split():
                if not checkList(i, keyInfoList):
                    keyInfoList.append(ent.string.rstrip())
    for token in tempTweet:
        if token.pos_ == 'PROPN' or token.pos_ == 'ADJ' or token.pos_ == 'NOUN':
            if token.string.lower().rstrip() == 'flood':
                pass
            elif checkList(token.string.rstrip(), keyInfoList):
                pass
            else:
                keyInfoList.append(token.string.rstrip())
    symbol = "~`!@#%^+={}[]>'<*|/?*-+"
    for i in keyInfoList:
        for j in i:
            if j in symbol:
                keyInfoList.pop(keyInfoList.index(i))
                break
    return keyInfoList

# This function handles creating the string that is ready for the user to read on the webpage
def getInformationReady(list, location):
    string = "Date of tweet: &nbsp" + str(datetime.now().strftime('%d:%b')) + "<br />Time of tweet: &nbsp" + str(datetime.now().strftime('%H:%M:%S')) + "<br /> Location of Tweet: &nbsp" + location + "<br /> Looks like someone has commented on a flood! Here's what we found: <br />"
    for i in list:
        if i == 'Flash' or i == 'flash':
            i += " flood"
        string += '&nbsp&nbsp \u2022' + i + '<br />'
    return string

# This function is used to check if a word is already in the keyword list
def checkList(word,list):
    for i in list:
        if ' ' in i:
            temp = i.split()
            for j in temp:
                if word == j:
                    return True
        else:
            if word == i:
                return True
    return False
