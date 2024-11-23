from flask import Flask, render_template, request ,jsonify 
from flask_cors import CORS
import nltk
from spellchecker import SpellChecker
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
from keras.models import load_model
import json
import random
                                              
app=Flask(__name__, template_folder='template')

CORS(app)
from chat import initialize_chatbot

@app.route('/',methods=["GET"])
def index_get():  
   return  render_template('base.html')

@app.route('/predict',methods=["POST"])
def predict():
       
    text=request.get_json("message")
    chatbot = initialize_chatbot()
   # user_input = input("User: ")
    response = chatbot(str(text))
    message={"answer":response}

    return jsonify(message)
if __name__ == '__main__':
 app.run()


