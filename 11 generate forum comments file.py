# fetch EUR/USD forum discussion data 
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.forexfactory.com/thread/10372-eurusd'

# Fetch HTML content
html_content = requests.get(url).text

# Parse the html content
soup = BeautifulSoup(html_content, 'lxml')
#print(soup.prettify())  # print the parsed data of html
print(soup)
print(soup.find('a',class_='last'))
exit()
#last_page_number = int(soup.find('a',class_='last').string)
print(last_page_number)

data = []

forex_type = 'EURUSD'

if forex_type == 'EURUSD':
    url_head = 'https://www.forexfactory.com/thread/10372-eurusd'
elif forex_type == 'AUDUSD':
    url_head = 'https://www.forexfactory.com/showthread.php?t=95260'
elif forex_type == 'GBPUSD':
    url_head = 'https://www.forexfactory.com/showthread.php?t=10378'
elif forex_type == 'USD/JPY':
    url_head = 'https://www.forexfactory.com/showthread.php?t=5505'

for i in range(last_page_number,last_page_number-200,-1):
    last_page_url = url_head + '?page=' + str(i)
    html_content = requests.get(last_page_url).text
    soup = BeautifulSoup(html_content, 'lxml')
    dates_reviews = soup.find_all('span',class_='visible-mv')
    for d in dates_reviews:
        text1 = d.get_text()
        index1 = text1.find('m') 
        index11 = text1.find(',')
        index12 = text1.find(':')
        if index1 != -1 and index11 != -1:
            if index12 > index11 + 5:
                date = text1[text1.find('\n')+2:index11+6]
            else:
                date = text1[text1.find('\n')+2:index11]
            data.append([date,view_num])
        text2 = d.parent.get_text()
        index2 = text2.find('#')
        if index2 !=-1:
            view_num = text2[index2+1:]
    print('page ' + str(i) + ' is done.')
    df_data = pd.DataFrame(data,columns=['date','view number'])
    df_data.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data\
        /emotion data/' + forex_type + 'date and view.csv')
    df_data_count = df_data.groupby(['date']).count()
    df_data_count.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data\
        /emotion data/' + forex_type + 'date and view count.csv')
print(df_data_count)