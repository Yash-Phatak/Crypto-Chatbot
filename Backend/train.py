import json
import pickle 
import numpy as np
import random
import nltk
nltk.download('punkt')
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout,ReLU
from keras.optimizers import SGD

words = []
classes = []
documents = []
ignore_words =['?','!']

data = open('Krypto\Backend\intents.json').read()
intents = json.loads(data)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        #tokenisation of each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        #adding documents
        documents.append((w,intent['tag']))
        
        #adding classes to the class list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

lemmatizer = WordNetLemmatizer()
words = [lemmatizer.lemmatize(w.lower(),pos='v') for w in words if w not in ignore_words]
words = sorted(list(set(words)))

classes = sorted(list(set(classes)))
pickle.dump(words,open('words.pkl',mode='wb'))
pickle.dump(classes,open('classes.pkl',mode='wb'))

#building the dl model
training =[]
output_empty = [0]*len(classes)
for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words if word not in ignore_words]
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    training.append([bag,output_row])
#shuffle and conversion to np array
random.shuffle(training)
training = np.array(training)

#train split for patterns and tags
train_x = list(training[:,0]) #for patterns
train_y = list(training[:,1]) #intents or tags

# 3 layers - 128 neurons - 64 neurons - intents number
model =  Sequential()
model.add(Dense(128,input_shape=(len(train_x[0]),),activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]),activation='softmax'))
#Compile model.Stochastic gradient descent with Nesterov accelarated gradient gives good results for this model
sgd = SGD(learning_rate=0.01,weight_decay=1e-6,momentum=0.9,nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
#fitting and saving the model
hist = model.fit(np.array(train_x),np.array(train_y),epochs=200,batch_size=5,verbose=1)
model.save('krypto_model.h5', hist)
print("Model Created.GG!")