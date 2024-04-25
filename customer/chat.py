# WORKING PART 1:
# import random
# import json
# import torch 
# import numpy as np
# from customer.model1 import NeuralNet
# from customer.nltk_utils import bag_of_words, tokenize
# from langdetect import detect
# from googletrans import Translator

# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# with open("customer/intents.json", 'r') as f:
#     intents = json.load(f)

# FILE = "data.pth"
# data = torch.load(FILE)

# input_size = data["input_size"]
# hidden_size = data["hidden_size"]
# output_size = data["output_size"]
# all_words = data['all_words']
# tags = data['tags']
# model_state = data["model_state"]

# model = NeuralNet(input_size, hidden_size, output_size).to(device)
# model.load_state_dict(model_state)
# model.eval()

# bot_name = "Sam"

# def translate_message(msg, src_lang, dest_lang):
#     translator = Translator()
#     translated_msg = translator.translate(msg, src=src_lang, dest=dest_lang)
#     print("Translated message:", translated_msg.text)  # Add this line for debugging
#     return translated_msg.text

# def get_response(msg):
#     detected_lang = detect_language(msg)
#     if detected_lang == "de":
#         msg = translate_text(msg, source_lang="de", target_lang="en")
#     elif detected_lang == "en":
#         pass
#     else:
#         msg = translate_text(msg, source_lang="auto", target_lang="en")
#     msg = str(msg).strip()
#     sentence = tokenize(msg)
#     X = bag_of_words(sentence, all_words)
#     X = X.reshape(1, X.shape[0])
#     X = torch.from_numpy(X).to(device)

#     output = model(X)
#     _, predicted = torch.max(output, dim=1)

#     tag = tags[predicted.item()]

#     probs = torch.softmax(output, dim=1)
#     prob = probs[0][predicted.item()]

#     print("PROBABILITY for: ", msg, "is: ", prob.item())
#     if prob.item() > 0.75:
#         for intent in intents['intents']:
#             if tag == intent["tag"]:
#                 bot_value = random.choice(intent['responses'])
#                 if detected_lang == "de":
#                     bot_value = translate_text(bot_value, source_lang="en", target_lang="de")
#                 return bot_value 
#         else:
#             bot_value = f"Ich verstehe nicht..."
#         return bot_value
    
#     else:
#         bot_value = f"Ich verstehe nicht..."
#         return bot_value

# # Add functions for language translation and detection
# def translate_text(text, source_lang="auto", target_lang="en"):
#     translator = Translator()
#     translated_text = translator.translate(text, src=source_lang, dest=target_lang)
#     return translated_text.text

# def detect_language(text):
#     try:
#         lang = detect(text)
#     except:
#         lang = "unknown"
#     return lang



import random
import json
import torch
import numpy as np
from customer.model1 import NeuralNet
from customer.nltk_utils import bag_of_words, tokenize
from googletrans import Translator

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Load intents file
with open("customer/intents.json", 'r') as f:
    intents = json.load(f)

# Load trained model parameters
FILE = "data.pth"
data = torch.load(FILE, map_location=device)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

# Initialize and load the model
model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def translate_text(text, source_lang="auto", target_lang="en"):
    """Function to translate text from source language to target language."""
    translator = Translator()
    translated_text = translator.translate(text, src=source_lang, dest=target_lang)
    return translated_text.text

def detect_language(text):
    """Function to detect the language of the given text."""
    translator = Translator()
    try:
        detected_lang = translator.detect(text).lang
    except Exception as e:
        detected_lang = "unknown"
        print(f"Language detection error: {e}")
    return detected_lang

def get_response(msg, lang='en'):
    """Generate a response from the chatbot based on the user's input and language."""
    # Translate message to English if necessary
    if lang != 'en':
        msg = translate_text(msg, source_lang=lang, target_lang='en')
    
    # Processing user input
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    # Select response if confidence is high enough
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                # Translate response back to original language if necessary
                if lang != 'en':
                    response = translate_text(response, source_lang='en', target_lang=lang)
                return response
    return "I do not understand..."

