# what is soup object ->

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import csv,re

url = 'http://103.222.20.150/ftpdata/Movies/Hollywood/2020/'
webpage = requests.get(url)

## convert to beautiful soup object

soup = BeautifulSoup(webpage.content,'lxml')   ## A data structure representing a parsed HTML or XML document.

#  print(soup.prettify()) ## to see the html content in proper indendation we use prettify

movies_box = soup.find_all('a')
movies_link = [eachLink['href'] for eachLink in movies_box if not eachLink['href'] == '../']

movies_title = []
for titles in soup.find_all('a'):
    if not titles['href'] == '../':
        words = titles.text.split(' ')
        words.pop(len(words)-1)
        string = ' '
        string = string.join(words)
        movies_title.append(string)

print(movies_title)


movies = []
movies_size = []

count = 0
print(movies_link[0])
for innerLink in tqdm(movies_link):
    innerPage = requests.get(url + innerLink)
    parser = BeautifulSoup(innerPage.content,'lxml')
    movie_size_box = parser.find('pre').text
    fetch_size = movie_size_box.split(" ")
    file_in_GBs = re.findall("[1-3]G",movie_size_box)
    file_in_MBs = re.findall("[1-9][1-9][1-9]M", movie_size_box)
    if file_in_GBs:
        print(f"file in GB {file_in_GBs}")
        movies_size.append(file_in_GBs[0])
    elif file_in_MBs:
        print(f"file in MB {file_in_MBs}")
        movies_size.append(file_in_MBs[0])
    if count >= 19:
        break
    directDownloadLink = parser.find_all('a')
    directDownloadLink.pop(0)
    movies.append(url + innerLink + directDownloadLink[0]['href'])
    count += 1
    requests.get(url)

print(movies)
print(movies_size)

with open('movies_list.csv','w',newline='') as movies_details:
    feildNames = ['title','link','size']
    writer = csv.DictWriter(movies_details,fieldnames=feildNames)
    writer.writeheader()
    for counting in range(count):
        writer.writerow({'title' : movies_title[counting],'link' : movies[counting],'size':movies_size[counting]})

