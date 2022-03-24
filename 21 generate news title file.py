# fetch forex news 
from bs4 import BeautifulSoup
import requests
import pandas as pd

#'https://www.fxempire.com/news/forex-news'
url_heads = ['https://www.forexlive.com/Headlines/1','https://www.dailyfx.com/market-news/articles']
all_news = pd.DataFrame(columns = ['title','time'])

# Fetch HTML content

for url in url_heads:

    # Parse max page number

    if url == 'https://www.dailyfx.com/market-news/articles':
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        numbers = []
        page_numbers = soup.find_all('a', class_ = "dfx-paginator__link mx-1 mx-md-2")
        for p in page_numbers:
            number = int(p.get_text().replace("\n",""))
            numbers.append(number)
        print(numbers)
        last_page = numbers[-1]
    else:
        if url == "https://www.forexlive.com/Headlines/1":
            last_page = 4000
        else:
            if url == 'https://www.fxempire.com/news/forex-news':
                last_page = 195

    # parse html content

    for page_number in range(1,last_page): # get link for every page
        if page_number == 1:
            urlp = url
        else:
            urlp = url + '/' + str(page_number) 
            if url == 'https://www.fxempire.com/news/forex-news':
                urlp = url + '?page=' + str(page_number)

        html_content = requests.get(urlp).text
        #print(html_content)
        # parse every page html content 
        soup = BeautifulSoup(html_content, 'lxml')
        print(soup)
        news = pd.DataFrame()
        titles = []
        times = []
        
        # search all news in current page to news.csv
        if url == 'https://www.dailyfx.com/market-news/articles':
            all_titles = soup.find_all('span', class_ = "dfx-articleListItem__title jsdfx-articleListItem__title font-weight-bold align-middle")
            all_times = soup.find_all('span', class_ = "jsdfx-articleListItem__date text-nowrap")
            
        else:
            if url == 'https://www.forexlive.com/Headlines/1':                
                #<a href="https://invst.ly/sijov" class="js-external-link title" title="USD/CAD dips lower on light data calendar" rel="nofollow" target="_blank">USD/CAD dips lower on light data calendar</a>
                #all_titles = soup.find_all('a', class_ = "js-external-link title")
                all_titles = soup.find_all('h3')
                print(soup)
                print(all_titles)
                exit()
                all_times = soup.find_all('span', class_ = "date")   
            else:
                if url == 'https://www.fxempire.com/news/forex-news':
                    '''
                    <h3 font-size="14,16" class="Titles-sc-1o1kplc-0 gCZNNl"><div class="Card-sc-1ib64vn-0 PlxkZ">A Quiet Economic Calendar Leaves U.S Politics, COVID-19, and Brexit in Focus</div></h3>
                    '''
                    print(soup)
                    all_titles = soup.find_all('h3')
                    all_times = soup.find_all('time')
                    print(all_titles)
                    print(all_titles)
        
        for t in all_titles:
            text = t.get_text()
            print(text)
            titles.append(text)

        for time in all_times:
            t2 = time.get_text()
            print(t2)
            times.append(t2)

        news['title'] = titles
        news['time'] = times
        all_news = pd.concat([all_news,news],sort=False)
        all_news.to_csv('/Users/chunyanwang/Christine documents/projects/Forex daily strategy/Data/news data/news.csv')
        print('page ' + str(page_number) + ' is done. total length of news file is: ' + str(len(all_news)))

        exit()