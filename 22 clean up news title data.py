import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn import preprocessing
import numpy as np

# clean data
data = pd.read_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/news.csv',header=0)

dates = data['time']
new_dates = []
for d in dates:
    pos = d.find('-')
    new_dates.append(d[pos-4:pos+6])
data['date'] = new_dates
data = data.drop(['time'], axis = 1)

data = data.groupby('date')['title'].agg(lambda  x:' '.join(x))

# make all str lower case
data = data.str.lower()
data.replace(':','') 

data.columns = ['date','title']
print(data)
data.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/cleaned news.csv')
print(data.iloc[1])   


