#!/usr/bin/env python
import pandas as pd
from sklearn.model_selection import train_test_split
#pip install -U scikit-learn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
## for saving the model and vectorizer
import joblib
import pickle
import re
from sklearn.linear_model import SGDClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import sys
import nltk
import json



'''
#prepare the dataset
df1 = pd.read_csv('train.csv', encoding='latin-1')
df2 = pd.read_csv('test.csv', encoding='latin-1')

df1= df1[['text', 'sentiment']]
df2 = df2[['text', 'sentiment']]

df = pd.concat([df1, df2], ignore_index=True)
df = df.dropna()


#clean text in dataset
#Lowercasing all the letters
df['text'] = df['text'].str.lower()
#Removing hashtags and mentions and links
df['text'] = df['text'].replace(to_replace='#[A-Za-z0-9_]+', regex=True, value='')
df['text'] = df['text'].replace(to_replace='@[A-Za-z0-9_]+', regex=True, value='')
df['text'] = df['text'].replace(to_replace=r'http\S+', regex=True, value='')


df.to_csv('mysent.csv',index=False)
'''
'''
df = pd.read_csv('mysent.csv', encoding='latin-1')

#splitting the dataset into a training and test set
text = df['text'].values
sent = df['sentiment'].values
reviews_train, reviews_test, y_train, y_test = train_test_split(text, sent, test_size=0.2, random_state=1000)

#vectorize the data    
vectorizer = CountVectorizer()
vectorizer.fit(reviews_train)

X_train = vectorizer.transform(reviews_train)
X_test = vectorizer.transform(reviews_test)

#train
classifier = LogisticRegression(solver='lbfgs', max_iter=2000)
classifier.fit(X_train, y_train)


#accuracy = classifier.score(X_test, y_test)
#print("Accuracy (Logistic Regression):", accuracy)
y_pred = classifier.predict(X_test)

#print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))
'''
'''
# Naive Bayes
vectorizer = CountVectorizer()
vectorizer.fit(reviews_train)

X_train = vectorizer.transform(reviews_train).toarray()
X_test = vectorizer.transform(reviews_test).toarray()

classifier = MultinomialNB()
classifier.fit(X_train, y_train)

accuracy = classifier.score(X_test, y_test)
print("Accuracy (Naive Bayes):", accuracy)
y_pred = classifier.predict(X_test)

print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))


# Random Forest
vectorizer = CountVectorizer()
vectorizer.fit(reviews_train)

X_train = vectorizer.transform(reviews_train).toarray()
X_test = vectorizer.transform(reviews_test).toarray()

classifier = RandomForestClassifier(n_estimators=100)
classifier.fit(X_train, y_train)

accuracy = classifier.score(X_test, y_test)
print("Accuracy (Random Forest):", accuracy)
y_pred = classifier.predict(X_test)

print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))


# SVM
vectorizer = CountVectorizer()
vectorizer.fit(reviews_train)

X_train = vectorizer.transform(reviews_train)
X_test = vectorizer.transform(reviews_test)

classifier = SVC()
classifier.fit(X_train, y_train)

accuracy = classifier.score(X_test, y_test)
print("Accuracy (SVM):", accuracy)
y_pred = classifier.predict(X_test)

print("\nClassification Report:\n", metrics.classification_report(y_test, y_pred))
'''


#save the model
#create the folder and store it there
#joblib.dump(classifier, 'sentiment_model.pkl', compress=9)

# Save the vectorizer
#vec_file_en = 'sentiment_vectorizer.pickle'
#pickle.dump(vectorizer, open(vec_file_en, 'wb'))


#load the model

classifier = joblib.load('sentiment_model.pkl')
vectorizer = pickle.load(open("sentiment_vectorizer.pickle", 'rb'))

#test on data
#text_for_analysis=['In this post, we’ll go over how to write DataFrames to CSV files.']

text_for_analysis=[]
filename = sys.argv[1]
with open(filename, encoding="utf8") as myfile:
    text="".join(line.rstrip() for line in myfile)
    
text_for_analysis = nltk.sent_tokenize(text)

#print(text_for_analysis)
X_new = vectorizer.transform(text_for_analysis)
results = classifier.predict(X_new)
print(results)

# what to send    
output_dictionary = {"sentimentlist": results.tolist(),
                     "sentences": text_for_analysis
                    }  

json_results = json.dumps(output_dictionary, indent = 2)
print(json_results)

to_store = sys.argv[2]

f = open(to_store, "w", encoding='utf-8')
f.write(json_results)
f.close()

