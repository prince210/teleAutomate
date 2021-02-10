from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import csv, time
import os
import requests
from tqdm import tqdm

root = Tk()

root.title("Tele@utomate")
root.iconbitmap("automate.ico")
root.resizable(False,False)

appendedMaterials = []

img = PhotoImage(file='gradient_wallpaper.png')
header = Label(root, image=img)
header.grid(row = 0,column = 0,columnspan = 3)
isRunning = True

## setting up button for conforming the selected movies

def confirmMovieSelection():
    for items in listboxMovies.curselection():  ## items are index
        listboxContents.insert(END,listboxMovies.get(items))

def confirmSerieSelection():
    for items in listboxSeries.curselection():  ## items are index
        listboxContents.insert(END,listboxSeries.get(items))

def confirmGameSelection():
    for items in listboxGames.curselection():  ## items are index
        listboxContents.insert(END,listboxGames.get(items))

button_movie = Button(root,text = "SELECT MOVIE",command = confirmMovieSelection)

button_series = Button(root,text = "SELECT SERIES",command = confirmSerieSelection)

button_game = Button(root,text = "SELECT GAMES",command = confirmGameSelection)



##      list_box with scroll bar for series
extFrameSeries = Frame(root)
scrollBarSeries = Scrollbar(extFrameSeries,orient=VERTICAL)  ## Scrollbar widget which displays a slider at a certain position.

listboxSeries = Listbox(extFrameSeries,width = 30,yscrollcommand = scrollBarSeries.set,selectmode = EXTENDED)  ## yscrollcommand sets the scroll bar

listboxSeries.insert(0,"series unavailable")
listboxSeries.insert(1,"Updated Soon")
# for count in range(50):
#     listboxSeries.insert(count,"series {}".format(count))

def selectSeries():
    scrollBarSeries.config(command=listboxSeries.yview)  ## yview => Query and change the vertical position of the view.
    scrollBarSeries.pack(side=RIGHT, fill=Y)
    extFrameSeries.grid(row = 1,column = 1)
    listboxSeries.pack(padx=15, side=RIGHT)




##      list_box with scroll bar for games
extFrameGames = Frame(root)
scrollBarGames = Scrollbar(extFrameGames,orient=VERTICAL)  ## Scrollbar widget which displays a slider at a certain position.

listboxGames = Listbox(extFrameGames,width = 30,yscrollcommand = scrollBarGames.set,selectmode = EXTENDED)  ## yscrollcommand sets the scroll bar


## To download games we have file divided into parts
## To download all parts of game we use dictonary with key as game title and value as list of part links
part_links = []
game_link = {}
games_size = []

with open('games_list.csv','r') as games_details:
    reader = csv.DictReader(games_details)
    index = 0
    for game_name in reader:
        if game_name['title'] not in game_link.keys():
            part_links = []
            part_links.append(game_name['link'])
            games_size.append(game_name['size'])
            game_with_size = game_name['title'] + ' ' + '[' + games_size[index] + 'GB' + ']'
            game_link[game_with_size] = part_links
            index += 1
            # game_link[game_name['title']] = part_links
        else:
            part_links.append(game_name['link'])
            game_with_size = game_name['title'] + ' ' + '[' + games_size[index] + 'GB' + ']'
            game_link[game_with_size] = part_links
            # game_link[game_name['title']] = part_links
    games_details.close()

# for keys in game_link.keys():
#     print(keys + ' ' + str(game_link[keys]),end = '\n')
index = 0
for games_title in game_link.keys():
    game_with_size = games_title + ' ' + '[' +  games_size[index] + 'GB' + ']'
    listboxGames.insert(index, games_title)
    index += 1


def selectGames():
    scrollBarGames.config(command=listboxGames.yview)  ## yview => Query and change the vertical position of the view.
    scrollBarGames.pack(side=RIGHT, fill=Y)
    extFrameGames.grid(row = 1,column = 1)
    listboxGames.pack(padx=15, side=RIGHT)


##      list_box with scroll bar for movies
extFrameMovies = Frame(root)
scrollBarMovies = Scrollbar(extFrameMovies,orient=VERTICAL)  ## Scrollbar widget which displays a slider at a certain position.

listboxMovies = Listbox(extFrameMovies,width = 30,yscrollcommand = scrollBarMovies.set,selectmode = EXTENDED)  ## yscrollcommand sets the scroll bar


## movie link will contain key as movie title and value as movie link
movie_link = {}
movies_size = []
with open('movies_list.csv','r') as movies_title:
    reader = csv.DictReader(movies_title)
    index = 0
    for movie_name in reader:
        movies_with_size = movie_name['title'] + ' ' + '[' +  movie_name['size'] + 'B' + ']'
        listboxMovies.insert(index,movies_with_size)
        # movie_link[movie_name['title']] = movie_name['link']
        movie_link[movies_with_size] = movie_name['link']
        index += 1
    movies_title.close()



def selectMovies():
    scrollBarMovies.config(command=listboxMovies.yview)  ## yview => Query and change the vertical position of the view.
    scrollBarMovies.pack(side=RIGHT, fill=Y)
    extFrameMovies.grid(row = 1,column = 1)
    listboxMovies.pack(padx=15, side=RIGHT)


##  aditional list box for displaying selected contents

extFrameContents = Frame(root)
scrollBarContents = Scrollbar(extFrameContents,orient=VERTICAL)  ## Scrollbar widget which displays a slider at a certain position.

listboxContents = Listbox(extFrameContents,width = 30,yscrollcommand = scrollBarContents.set,selectmode = EXTENDED)  ## yscrollcommand sets the scroll bar



scrollBarContents.config(command=listboxContents.yview)  ## yview => Query and change the vertical position of the view.
scrollBarContents.pack(side=RIGHT, fill=Y)
extFrameContents.grid(row = 1,column = 2)
listboxContents.pack(padx=15, side=RIGHT)


## creating out the text box to show the downloading files

extFrameDownDis = Frame(root,borderwidth = 2)
scrollBarDownDisY = Scrollbar(extFrameDownDis,orient=VERTICAL)
scrollBarDownDisX = Scrollbar(extFrameDownDis,orient=HORIZONTAL)

down_dis = Text(extFrameDownDis,width = 38,height = 8,undo = True,wrap = "none")

down_dis.config(yscrollcommand=scrollBarDownDisY.set, xscrollcommand=scrollBarDownDisX.set)
scrollBarDownDisY.config(command=down_dis.yview)  ## yview => Query and change the vertical position of the view.
scrollBarDownDisX.config(command=down_dis.xview)

scrollBarDownDisX.pack(side=BOTTOM, fill=X)
scrollBarDownDisY.pack(side=RIGHT, fill=Y)
down_dis.pack()
extFrameDownDis.grid(row = 4,column = 1,pady = 30)


## setting up display for different types of options selected
def optionsAvail(value):
    if value == "Series":

        scrollBarSeries.pack_forget()
        extFrameSeries.grid_forget()
        listboxSeries.pack_forget()

        scrollBarMovies.pack_forget()
        extFrameMovies.grid_forget()
        listboxMovies.pack_forget()

        scrollBarGames.pack_forget()
        extFrameGames.grid_forget()
        listboxGames.pack_forget()

        button_movie.grid_forget()
        button_game.grid_forget()
        button_series.grid_forget()

        selectSeries()
        button_series.grid(row=2, column=1,pady = 20)

    if value == "Movies":

        scrollBarSeries.pack_forget()
        extFrameSeries.grid_forget()
        listboxSeries.pack_forget()

        scrollBarMovies.pack_forget()
        extFrameMovies.grid_forget()
        listboxMovies.pack_forget()

        scrollBarGames.pack_forget()
        extFrameGames.grid_forget()
        listboxGames.pack_forget()

        button_movie.grid_forget()
        button_game.grid_forget()
        button_series.grid_forget()

        selectMovies()
        button_movie.grid(row=2, column=1,pady = 20)

    elif value == "Games":

        scrollBarSeries.pack_forget()
        extFrameSeries.grid_forget()
        listboxSeries.pack_forget()

        scrollBarMovies.pack_forget()
        extFrameMovies.grid_forget()
        listboxMovies.pack_forget()

        scrollBarGames.pack_forget()
        extFrameGames.grid_forget()
        listboxGames.pack_forget()

        button_movie.grid_forget()
        button_game.grid_forget()
        button_series.grid_forget()

        selectGames()
        button_game.grid(row=2, column=1,pady = 20)

selectOptionsVar = StringVar()
selectOptionsVar.set("Movies")
selectMovies()
button_movie.grid(row=2, column=1,pady = 20)

dropDown = OptionMenu(root, selectOptionsVar, "Movies", "Games", "Series",command=optionsAvail)
dropDown.grid(row = 1,column = 0,padx = 10,pady=2)

#####  remove the selected items button #####
def deleteMultiple():
    response = messagebox.askokcancel("Remove Files", "Do you want to perform the action?")
    for items in reversed(listboxContents.curselection()):
        if response:
            listboxContents.delete(items)

remove_butt = Button(root,text = "REMOVE",command = deleteMultiple)
remove_butt.grid(row = 2,column = 2)

#### Download button  ######

def saveToLocation():
    root.filename = filedialog.askdirectory(initialdir = r"C:\Program Files",title = "Download To Path")
    for item in listboxContents.get(0,END):  ## items are index
        # item = listboxContents.get(items)
        print(item)
        if item in movie_link.keys():
            download_movies(movie_link[item],root.filename,item)
        if item in game_link.keys():
            download_games(game_link[item],root.filename,item)
    # print(root.filename)
    down_dis.insert(END,'Downloading Files Finished ')
    print('Downloading Files Finished')


## Downloading File using requests ##

def download_movies(url,filepath,title):
    global isRunning

    print('Downloading started for {} to path {}'.format(title,filepath))
    down_dis.insert(END,'Downloading started for {} to path {} \n'.format(title,filepath))
    os.chdir(filepath)
    increment = 0

    with requests.get(url, stream=True) as r:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        print(type(progress_bar))
        with open('{}'.format(title)+'.mp4', 'wb') as f:
            for chunck in r.iter_content(chunk_size=block_size):
                if chunck:
                    f.write(chunck)
                    progress_bar.update(len(chunck))
                    down_dis.delete('1.0',END)
                    down_dis.insert(END, 'Downloading started for {} to path {} \n'.format(title, filepath))
                    down_dis.insert(END,progress_bar)
                    root.update()
            increment += 1
        progress_bar.close()
    down_dis.insert(END, 'Downloading for {} finished'.format(title, filepath))



## A single game has multiple parts or a game is divided into multiple files for download each of which is in url_list
def download_games(url_list,filepath,title):
    print('Downloading started for {} to path {}'.format(title,filepath))
    down_dis.insert(END,'Downloading started for {} to path {} \n'.format(title,filepath))
    os.chdir(filepath)
    increment = 0
    for url in url_list:
        with requests.get(url, stream=True) as r:
            with open('{}'.format(title)+'.rar', 'wb') as f:
                for chunck in r.iter_content(chunk_size=1024):
                    if chunck:
                        f.write(chunck)
                increment += 1
    down_dis.insert(END, 'Downloading for {} finished'.format(title, filepath))

download_butt = Button(root,text = "DOWNLOAD",command = saveToLocation,padx = 30)
download_butt.grid(row = 3,column = 1,pady = 20)


root.mainloop()