import pandas as pd
import nltk 
from nltk.corpus import stopwords
import string
import re
from string import digits
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

data = pd.read_csv('clean_data.csv')
texts = data['text'].astype(str)
y = data['is_offensive']

cleaned_text=[]
# table = str.maketrans('', '', string.punctuation)
# stop_words = set(stopwords.words('english'))
# porter = PorterStemmer()
count=0

stemmer = PorterStemmer() 

def StemTokens(tokens):
    s=" "
    for token in tokens:
        if len(token)<900:
            s=s+" "+stemmer.stem(token)
    return s

# lemmer = nltk.stem.WordNetLemmatizer()

# def LemTokens(tokens):
#     s=" "
#     for token in tokens:
#         s=s+" "+lemmer.lemmatize(token)
#     return s


statement_training = []
for i in data['text'].to_list():
    try:
        temp = i.translate(str.maketrans('', '', digits))
        temp = re.sub(r'[^\w\s]','',temp)
        temp = temp.lower()
        temp= StemTokens(nltk.word_tokenize(temp))
        statement_training.append(temp)
        print(count)
        count+=1
    except:
        statement_training.append("None")
    print(statement_training[count-1])

print(statement_training)







# for i in range(0,len(texts)):
#     tokens = nltk.word_tokenize(texts[i])
#     tokens = [w.lower() for w in tokens]

#     stripped = [w.translate(table) for w in tokens]

#     # remove remaining tokens that are not alphabetic
#     words = [word for word in stripped if word.isalpha()]

#     # filter out stop words
#     words = [w for w in words if not w in stop_words]

#     stemmed = [porter.stem(word) for word in words]
    
#     cleaned_text.append(' '.join(stemmed))

#     print(count)
#     count +=1

# print(cleaned_text)