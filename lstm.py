import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, SpatialDropout1D
from sklearn.model_selection import train_test_split
import re
from sklearn.preprocessing import LabelBinarizer
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
from sklearn.metrics import classification_report,accuracy_score
df = pd.read_csv('processed.csv')
df.drop(['youID'],axis=1,inplace=True)
df.drop(['title'],axis=1,inplace=True)

df=df[df['description'].notnull()]
df = df.reset_index(drop=True)
#FURTHER PREPROCESSING FOR LSTM
REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def clean_text(text):
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text. substitute the matched string in REPLACE_BY_SPACE_RE with space.
    text = BAD_SYMBOLS_RE.sub('', text) # remove symbols which are in BAD_SYMBOLS_RE from text. substitute the matched string in BAD_SYMBOLS_RE with nothing.
    text = text.replace('x', '')
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # remove stopwords from text
    return text
df['description'] = df['description'].apply(clean_text)
df['description'] = df['description'].str.replace('\d+', '')
#max frequency of words
MAX_NB_WORDS = 1800
MAX_SEQUENCE_LENGTH = 2000
EMBEDDING_DIM = 100
tokenizer = Tokenizer(num_words=MAX_NB_WORDS, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
tokenizer.fit_on_texts(df['description'].values)
word_index = tokenizer.word_index
X = tokenizer.texts_to_sequences(df['description'].values)
X = pad_sequences(X, maxlen=MAX_SEQUENCE_LENGTH)
Y = pd.get_dummies(df['category']).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.20, random_state = 42)

model = Sequential()
model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=X.shape[1]))
model.add(SpatialDropout1D(0.2))
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(6, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

epochs = 5
batch_size = 64

#history = model.fit(X_train, Y_train, epochs=epochs, batch_size=batch_size,validation_split=0.1,callbacks=[EarlyStopping(monitor='val_loss', patience=3, min_delta=0.0001)])
#model.save_weights("lstmweightsnew.h5")

model.load_weights("lstmweightsnew.h5")
accr = model.evaluate(X_test,Y_test)
ypred_classes=model.predict_classes(X_test,verbose=0)
label_binarizer = LabelBinarizer()
label_binarizer.fit(range(max(ypred_classes)+1))
ypred = label_binarizer.transform(ypred_classes)
print("Accuracy : ",accuracy_score(Y_test,ypred))
print(classification_report(Y_test,ypred))

