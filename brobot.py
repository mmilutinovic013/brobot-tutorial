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
GREETING_RESPONSES = ["sup bruh", "suh dude", "swag", "yo", "yanny or laurel, bruh"]

# Create function to check for the user's input sentence
def check_for_greeting(sentence):
    # if any of the words in the user input is in the user input list - give a response.
    for word in sentence.words:
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)


def respond(sentence):
    # Parse the user sentence to find candidate "best response" sentences
    cleaned = preprocess_text(sentence)
    parsed = TextBlob(cleaned)

    # Loop through all sentences. This will help with noun extraction
    pronoun, noun, adjective, verb = find_candidate_parts_of_speech(parsed)

    # If we said something about the bot and used a direct noun...construct sentence around that noun.
    resp = check_for_comment_about_bot(pronoun, noun, adjective)

    # If the user greeted the bot - we will use a greeting response.
    if not resp:
        check_for_greeting(parsed)
    
    # If we don't override the final sentence - we try to construct a new one.
    if not pronoun:
        resp = random.choice(NONE_RESPONSES)
        elif pronoun == 'I' and not verb:
            resp = random.choice(COMMENTS_ABOUT_SELF)
        else:
            resp = construct_response(pronoun, noun, verb)

    # If none of that works - use a random response:
    if not resp:
        resp = random.choice(NONE_RESPONSES)
    
    # Log the response so we have history (can potentially use for later training)
    logger.info("Returning phrase '%s'", resp)

    # Filter response so we aren't saying bad stuff...
    filter_response(resp)

    # Return our response
    return resp

# Given the parsed input - find the best pronoun, direct noun, and verb
# to match the user's input. Returns a tuple of pronoun, noun, adj, verb, or None (if no good match)
def find_candidate_parts_of_speech:
    pronoun = None
    noun = None
    adjective = None
    verb = None
    
    # Go through and find all pronouns, nouns, adjectives, and verbs in sentence.
    for sent in parsed.sentences:
        pronoun = find_pronoun(sent)
        noun = find_noun(sent)
        adjective = find_adjective(sent)
        verb = find_verb(sent)
    
    # Log the pronouns, nouns, adjectives, and verbs for later use.
    logger.info("Pronoun=%s, noun=%s, adjective=%s, verb=%s", pronoun, noun, adjective, verb)

    # return tuple
    return pronoun, noun, adjective, verb

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