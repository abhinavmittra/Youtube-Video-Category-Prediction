import numpy as np
import pandas as pd
from textblob import Word
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
data = pd.read_csv('dataset.csv',encoding='utf-8', quotechar='"', delimiter=',')
data1=pd.DataFrame(data=data)
num=data.isnull().sum().sum()
data = data1.replace(np.nan, '', regex=True)
print("Replaced {} nan values".format(num))
#Remove urls
data['description']=data['description'].str.replace(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ")
data['description']=data['description'].str.replace(r'@[A-Za-z0-9]+','') # Remove @ signs
data['description'] = data['description'].apply(lambda x: " ".join(x.lower() for x in str(x).split())) # Change to lower
data['title']=data['title'].str.replace(r'''(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', " ")
data['title']=data['title'].str.replace(r'@[A-Za-z0-9]+','')
data['title'] = data['title'].apply(lambda x: " ".join(x.lower() for x in str(x).split()))

data['description'] = data['description'].str.replace('[^\w\s]','') # Replace whitespaces
data['title'] = data['title'].str.replace('[^\w\s]','')

stop = stopwords.words('english')

data['description'] = data['description'].apply(lambda x: " ".join(x for x in str(x).split() if x not in stop))
data['title'] = data['title'].apply(lambda x: " ".join(x for x in str(x).split() if x not in stop))

freq2 = pd.Series(' '.join(data['description']).split()).value_counts()[-50:] # remove top 50 rare words
freqtitle = pd.Series(' '.join(data['title']).split()).value_counts()[-50:]
freq = list(freq2.index)
data['description'] = data['description'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))
freq = list(freqtitle.index)
data['title'] = data['title'].apply(lambda x: " ".join(x for x in x.split() if x not in freq))

# from textblob import TextBlob
# data['description'].apply(lambda x: str(TextBlob(x).correct()))
# data['title'].apply(lambda x: str(TextBlob(x).correct()))
st = PorterStemmer()
data['description'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))
data['title'].apply(lambda x: " ".join([st.stem(word) for word in x.split()]))

data['description'] = data['description'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))
data['title'] = data['title'].apply(lambda x: " ".join([Word(word).lemmatize() for word in x.split()]))

data.to_csv('processed1.csv')