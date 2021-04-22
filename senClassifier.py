import joblib
from string import digits
from nltk.stem.porter import PorterStemmer
import re
import nltk

#Define potter stemmer object using NLTK library
stemmer = PorterStemmer() 

#Function to find the root word
def StemTokens(tokens):
    s=""
    for token in tokens:
        if len(token)<900:
            s=s+stemmer.stem(token)+" "
    return s[:-1]

#Function that accept a text and return if it contains bad words or not
def pred(textt):
    t=[]
    vectorizer = joblib.load('vectorizers.joblib')
    model = joblib.load('classifier.joblib')
    temp = textt.translate(str.maketrans('', '', digits))
    temp = re.sub(r'[^\w\s]','',temp)
    temp = temp.lower()
    temp= StemTokens(nltk.word_tokenize(temp))
    t.append(temp)
    x= model.predict(vectorizer.transform(t))
    return x[0]
