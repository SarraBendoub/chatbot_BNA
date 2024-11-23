import nltk
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
lemmatizer = WordNetLemmatizer()

def initialize_chatbot():
    lemmatizer = WordNetLemmatizer()
    model = load_model('chatbot_model.h10')
    intents = json.loads(open('intents1.json', encoding='utf-8').read())
    words = pickle.load(open('words.pkl2', 'rb'))
    classes = pickle.load(open('classes.pkl2', 'rb'))
    
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        spell = SpellChecker(language='fr')
        misspelled = spell.unknown(sentence_words)
        corrected_sentence_words = []
        for word in sentence_words:
            if word in misspelled:
                corrected_word = spell.correction(word)
                corrected_sentence_words.append(corrected_word)
            else:
                corrected_sentence_words.append(word)
        corrected_sentence = []
        for word in corrected_sentence_words:
            corrected_sentence.append(lemmatizer.lemmatize(word.lower()))
        return corrected_sentence
    
    def bag_of_words(sentence, words, show_details=True):
        sentence_words = clean_up_sentence(sentence)
        bag = [0] * len(words)
        for s in sentence_words:
            for i, word in enumerate(words):
                if word == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % word)
        return np.array(bag)
    
    def predict_class(sentence):
        p = bag_of_words(sentence, words, show_details=True)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list
    
    def get_response(ints, intents):
        tag = ints[0]['intent']
        list_of_intents = intents['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result
    
    def chatbot_response(user_input):
        ints = predict_class(user_input)
        response = get_response(ints, intents)
        return response
    
    return chatbot_response
chatbot = initialize_chatbot()
user_input = input("User: ")
response = chatbot(user_input)
print("Chatbot:", response)
