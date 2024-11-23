## importing libraries and dataset
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import random
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import json
import pickle
intents_file = open('intents1.json', encoding='utf-8').read()
intents1 = json.loads(intents_file) 
intents1

##preprocessing ==> NLP
words=[]
classes = []
documents = []
ignore_letters = ['!', '?', ',', '.','\n','-']
for intent in intents1['intents']:
    for pattern in intent['patterns']:
        List=intent['patterns']
        for i in List:
            word= nltk.word_tokenize(i)
            
            words.extend(word)
    
            documents.append((word, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
            #print(word)
print(set(words))
#print(documents)
#print(classes)
from nltk.corpus import stopwords
stop_words = set(stopwords.words('french'))
print(list(stop_words))
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_letters and w not in stop_words]
words = sorted(list(set(words)))
print(words)
print (len(words), "unique lemmatized words", words)
pickle.dump(words,open('words.pkl2','wb'))
pickle.dump(classes,open('classes.pkl2','wb'))

##encoding
training = []
testing = []  # create an empty list for testing data
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    word_patterns = doc[0]
    print(word_patterns)
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1
    
# Split the data into training and testing based on a ratio (e.g., 80% for training, 20% for testing)
    if np.random.rand() < 0.8:  # 80% for training
        training.append([bag, output_row])
    else:
        testing.append([bag, output_row])  # 20% for testing
        # Shuffle the training data
random.shuffle(training)
training = np.array(training)

# Create training and testing lists for X (patterns) and Y (intents)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Convert testing list to numpy array
testing = np.array(testing)

# Create testing lists for X (patterns) and Y (intents)
test_x = list(testing[:, 0])
test_y = list(testing[:, 1])
print("Training and testing data are created")
## FNN model
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))
 # Compiling model. SGD with Nesterov accelerated gradient gives good results for this model
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
 #Training and saving the model 
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1 ,validation_data=(test_x,test_y))
model.save('chatbot_model.h10', hist)
print("model is created")
score = model.evaluate(test_x, test_y, batch_size=32)
print(score)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
acc = hist.history['accuracy']
loss = hist.history['loss']
val_acc = hist.history['val_accuracy']
val_loss = hist.history['val_loss']
epochs = range(len(acc))

plt.plot(epochs, acc, 'r', 'training accuracy')
plt.plot(epochs, val_acc, 'g', 'val accuracy')
plt.title('Training_Valid_acc')
plt.savefig('Training_Valid_acc.png')
plt.figure()
plt.show()

plt.plot(epochs, loss, 'r', 'training loss')
plt.plot(epochs, val_loss, 'g', 'val loss')
plt.title('Training_Valid_loss')
plt.savefig('Training_Valid_loss.png')
plt.figure()
plt.show()