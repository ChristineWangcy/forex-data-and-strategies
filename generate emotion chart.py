import pandas as pd

USDEUR = '/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/forex daily data/newUSEU.csv'
news = '/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/cleaned news.csv'

headlinedata = pd.read_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/cleaned news.csv',names=['DATE','title'])
tradedata = pd.read_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/forex daily data/newUSEU.csv')
headlinedata = headlinedata.set_index('DATE')
tradedata = tradedata.set_index('DATE')
data = pd.concat([headlinedata,tradedata],axis=1,join='inner')
data['profit'] = data['close']/data['close'].shift(1)-1
data['label'] = 0
data.loc[data['profit'] >= 0.005, 'label'] = 1
data.loc[data['profit'] <=0,'label'] = -1
#print(data.head())
data = data[1:]
data.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/merged data.csv')

headlines = []
for row in range(0, len(data.index)):
    headlines.append(str(data['title'][row]))

print(headlines[0])
print(headlines[1])

n = int(len(headlines)/3)
traindata = headlines[:2*n]
testdata = headlines[2*n:]
train = data[:2*n]
test = data[2*n:]

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier

# implement BAG OF WORDS
countvector = CountVectorizer(ngram_range=(2,2))
print(traindata)
traindataset = countvector.fit_transform(traindata)
print((traindataset))
print(train['label'])

# implement RandomForest Classifier
randomclassifier = RandomForestClassifier(n_estimators=200, criterion='entropy')
randomclassifier.fit(traindataset,train['label'])

# Predict for the Test Dataset
testdataset = countvector.fit_transform(testdata)
predictions = randomclassifier.predict(testdataset)

# Import library to check accuracy
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
matrix = confusion_matrix(test['label'],predictions)
print(matrix)
score = accuracy_score(test['label'],predictions)
print(score)
report = classification_report(test['label'],predictions)
print(report)
