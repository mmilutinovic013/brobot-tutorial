# Mark Milutinovic - mmilutinovic1313
# Last Updated: June 7, 2018
# Bro Bot
from __future__ import print_function, unicode_literals
import random
import logging
import os

os.environ['NLTK_DATA'] = os.getcwd() + '/nltk_data'

from textblob import TextBlob

# User responses we accept
GREETING_KEYWORDS = ("hello", "hi", "greetings", "yo", "what's up", "sup", "suh dude")

# Responses from the bot
GREETINGS_RESPONSES = ["sup bruh", "suh dude", "swag", "yo", "yanny or laurel, bruh"]

# Create function to check for the user's input sentence
def check_for_greeting(sentence):
    # if any of the words in the user input is in the user input list - give a response.
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETINGS_RESPONSES)

# If none of the special 1:1 cases match - we try to construct our own response
def construct_response(pronoun, noun, verb):
    resp = []
    
    # We want to pass the pronoun through and include it in the response.
    if pronoun:
        resp.append(pronoun)

    # Some comment about verbs
    if verb:
        verb_word = verb[0]
        if verb_word in ('be', 'am', 'is') # Some comment about lemmas!
            if pronoun.lower() == 'you':
                # Bot responds that the bot isn't what they say the user says they are.
                resp.append("aren't really")
            else:
                resp.append(verb_word)
    
    # Some comment about nouns
    if noun:
        pronoun = "an" if starts_with_vowel(noun) else "a"
        resp.append(pronoun + " " + noun)
    
    # Add a random bro-like word to the end of the sentence.
    resp.append(random.choice(("tho", "bro", "lol", "bruh", "smh", "gg", "glhf", "doe" ,"")))

    return " ".join(resp)

# Create function to filter out unwanted words, chars, or phrases
def filter_response(resp):
    tokenized = resp.split(' ')
    for word in tokenized:
        if '@' in word or '#' in word or '!' in word:
            raise UnacceptableUtteranceException()
    for s in FILTER_WORDS:
        if word.lower().starts_with(s):
            raise UnacceptableUtteranceException()