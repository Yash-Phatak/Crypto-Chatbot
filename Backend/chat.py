from keras.models import load_model
model = load_model('krypto_model.h5')
import json
import random
import pickle
import numpy as np
data = open('intents.json').read()
intents = json.loads(data)
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower(),pos ='v') for word in sentence_words]
    return sentence_words

#return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence,words,show_details=True):
    #tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    #bag of words- matrix of N words,vocabulary matrix
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w==s:
                #assign 1 if the current word is in the vocabulary position
                bag[i]=1
                if show_details:
                    print("Found in bag: %s" % w)
    return (np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

#The `getResponse` function takes the output of the `predict_class` function as input (`ints`) and the `intents_json` as another input.
def getResponse(ints, intents_json): #takes output of predict class as ints
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            if(tag=="greeting"or tag=="goodbye"or tag=="thanks"or tag=="thanks"or tag=="noanswer"or tag=="options"):
                result = random.choice(i['response'])
                print(result)
                break
            else:
                result = i['response']
                print(result)
                break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    response = getResponse(ints, intents)
    print(response)
    output = {"answer":response}
    # return res #string returned
    return output
