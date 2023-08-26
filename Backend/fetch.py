import requests
from bs4 import BeautifulSoup

url = "https://coinmarketcap.com/"
html_text = requests.get(url)
soup = BeautifulSoup(html_text.content,'lxml')
titles = soup.find('tbody').find_all('tr')
# print(titles[1].text)
i=1 
for title in titles:   
    print(i)
    print(title.text)
    i+=1