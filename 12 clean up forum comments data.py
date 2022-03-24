import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from sklearn import preprocessing
import numpy as np

# clean data
data = pd.read_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/emotion data/EURUSD date and view count.csv',header=0)
print(data.head())

dates = data['date']
new_dates = []
for d in dates:
    if 'Edited' in d:
        print(d)
        d = d[7:]
        print(d)
    new_dates.append(d)
data['date'] = new_dates
#data.rename(columns={'view number':'investors attention index'})

investors_attention = np.array(data['view number']).reshape(-1,1)
print(investors_attention)

max_min_scaler = preprocessing.MinMaxScaler()
x_scaled = max_min_scaler.fit_transform(investors_attention)
data['investors attention index'] = x_scaled
data = data[['date','investors attention index']]

data = data[data.date.map(len) > 10]
data['date'] = pd.to_datetime(data['date'])
print(data)
data.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/emotion data/cleaned EURUSD date and view count.csv')

data2 = data.groupby(['date']).sum()
print(data2)
data2.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/emotion data/cleaned EURUSD date and view count.csv')
data3 = data2[-200:].sort_values(by=['investors attention index'])
print('top 20 most attentioned: ', data3[-20:])

print_data = data2[-200:]

# plot data
fig, ax = plt.subplots(figsize=(15,7))

# annotate max and min investors paied attention data
y_data = list(print_data['investors attention index'])
x_data = list(print_data.index)

# investors paid most attention
y_max = max(y_data)
y_max_index = y_data.index(y_max)
x_max = x_data[y_max_index]
ax.plot([x_max],[y_max],'o',markersize = 7, color = 'red')
ax.annotate('investors pay most attention', xy=(x_max,y_max),xytext=(x_max,y_max+0.02), \
    color = 'red')
ax.annotate(str(x_max)[:10], xy=(x_max,y_max),xytext=(x_max,y_max-0.05), \
    color = 'blue',fontweight='bold')

# investors paid least attention
y_min = min(y_data)
y_min_index = y_data.index(y_min)
x_min = x_data[y_min_index]
ax.plot([x_min],[y_min],'o',markersize = 7, color = 'red')
ax.annotate('investors pay least attention', xy=(x_min,y_min),xytext=(x_min,y_min+0.02), \
    color = 'red')
ax.annotate(str(x_min)[:10], xy=(x_min,y_min),xytext=(x_min,y_min-0.05), \
    color = 'blue',fontweight='bold')

#set ticks every week
#axes.xaxis.set_major_locator(mdates.WeekdayLocator())
#set major ticks format
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
print_data.plot(ax=ax)
plt.title('recent EURUSD investors attention')
plt.savefig('EURUSD attention index')

plt.show()