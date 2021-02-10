from bs4 import BeautifulSoup
import requests
import csv

url = 'http://s7.bitdownload.ir/Game/'

response = requests.get(url)

soup = BeautifulSoup(response.content,'lxml')

games_box = soup.find('tbody').find_all('a')

game_size = []
games_title = []
count = 0

game_link = {}

for gamesCollection in games_box:
    if count >= 12:
        break
    if gamesCollection.text != 'Parent directory/' and 'Collection' in gamesCollection.text:
        innerUrl = gamesCollection['href']
        splittedText = gamesCollection.text.split('.')
        splittedText.pop(len(splittedText)-1)
        blankStr = ' '
        parentFolderName = blankStr.join(splittedText)
        # games_title.append(parentFolderName)

        innerPage = requests.get(url+innerUrl)
        parser = BeautifulSoup(innerPage.content,'lxml')
        print(parentFolderName)
        index = 0

        for game in parser.find('tbody').find_all('a'):
            if 'Parent' not in game.text and (('.rar' not in game.text) and ('nfo' not in game.text)):
                print(game.text)
                size_count_gb = 0
                size_count_mb = 0
                sum = 0
                entries = []
                name = game.text.replace("."," ")
                name = name.replace("/"," ")
                games_title.append(name)
                count += 1
                downloadPageUrl = game['href']
                downloadPage = requests.get(url+innerUrl+downloadPageUrl)
                downloadParser = BeautifulSoup(downloadPage.content,'lxml')
                for file_size in downloadParser.find('tbody').find_all('td',text=True):
                    if 'MiB' in file_size.text:
                        size_count_mb = file_size.text.split("MiB")[0]
                        val = 0.00097 * float(size_count_mb)
                        sum += val
                    elif 'GiB' in file_size.text:
                        size_count_gb = file_size.text.split("GiB")[0]
                        val = float(size_count_gb)
                        sum += val
                for downloadLink in downloadParser.find('tbody').find_all('a',text=True):
                    print('----------->'+downloadLink['href'])
                    if '.rar' in downloadLink['href']:
                        entries.append(url + innerUrl + downloadPageUrl + downloadLink['href'])

                index += 1
                game_link[games_title[len(games_title)-1]] = entries
                game_size.append(round(sum))
            requests.get(url+innerUrl)

        requests.get(url)

print(games_title)
print(game_size)

for entries in game_link.keys():
    print(f'{entries} ---> {game_link.get(entries)}',end='\n')

keys = sorted(game_link.keys())
with open('games_list.csv','w',newline='') as games_details:
    feildNames = ['title', 'link','size']
    writer = csv.DictWriter(games_details, fieldnames=feildNames)
    writer.writeheader()
    for index,games_name in enumerate(game_link.keys()):
        for eachLink in game_link[games_name]:
            writer.writerow({'title' :games_name ,'link' : eachLink,'size':game_size[index]})
