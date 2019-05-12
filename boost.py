from sklearn.metrics import accuracy_score,classification_report
from xgboost import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
data = pd.read_csv('processed.csv')
names=['Art&Music','Food','History','Manufacturing','Science&Technology','Travel']

vectorizer = TfidfVectorizer()
X=vectorizer.fit_transform(data['title'],data['description'])
y=vectorizer.fit_transform(data['category'])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.40, random_state=48)

y_train=y_train.nonzero()[1]
y_test=y_test.nonzero()[1]

model = XGBClassifier()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
xg_predictions = [round(value) for value in y_pred]

print("Accuracy of XGBOOST: ",accuracy_score(y_test, xg_predictions)*100)
print(classification_report(y_test,xg_predictions,labels=None,target_names=names))