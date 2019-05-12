from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd

data = pd.read_csv('processed.csv')
names = ['Art&Music', 'Food', 'History', 'Manufacturing', 'Science&Technology', 'Travel']

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['title'], data['description'])
y = vectorizer.fit_transform(data['category'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.40, random_state=1)

y_train = y_train.nonzero()[1]
y_test = y_test.nonzero()[1]

svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X_train, y_train)
svm_predictions = svm_model_linear.predict(X_test)
print("SVM Accuracy :",accuracy_score(y_test,svm_predictions)*100)
print(classification_report(y_test,svm_predictions,labels=None,target_names=names))