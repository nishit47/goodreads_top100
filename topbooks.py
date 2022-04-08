from bs4 import BeautifulSoup
import requests
from csv import writer

import pandas as pd
from pandas_profiling import ProfileReport

url="https://www.goodreads.com/list/show/13086.Goodreads_Top_100_Literary_Novels_of_All_Time"
page=requests.get(url)

soup= BeautifulSoup(page.content, 'html.parser')
lists=soup.find_all('tr')

with open('goodreads_top100.csv', 'w', encoding='utf8', newline='') as f:
    thewriter=writer(f)
    heading=["Rank", "Name", "Author", "Rating"]
    thewriter.writerow(heading)

    for list in lists:
        ranking=list.find('td', class_="number").text
        title=list.find('a', class_="bookTitle").span.text
        author=list.find('a', class_="authorName").span.text
        ratingString=(list.find('span', class_="minirating").text[1:5])
        try:
            rating=float(ratingString)
        except:
            rating=4
        data=[ranking, title, author,rating]
        print(data)
        thewriter.writerow(data)

df=pd.read_csv("goodreads_top100.csv")

profile=ProfileReport(df)
profile.to_file(output_file="GoodreadsReport.html")