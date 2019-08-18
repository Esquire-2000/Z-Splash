
# Z-Splash

import pyunsplash # https://github.com/salvoventura/pyunsplash
import requests
import sys
import getpass
from tqdm import tqdm # https://github.com/tqdm/tqdm
import colorama
import random
import os
import shutil
import subprocess
import time, threading
from colorama import Fore, Back, Style
colorama.init()


def get_key():
    api_file=open('api_key.txt','r')
    api_key=api_file.readline() # 50 requests per hour
    api_file.close()
    return api_key

def get_images():
    global filename  #make filename global so the program can delete the previous wallpaper from temp

    try:
        filename
    except NameError: #if filename is not defined then pass
        pass
    else:
        os.remove(filename) # remove previous wallpaper

    change_time=get_time() # get change time from change_time() as seconds
    print ("Change time set to: %d seconds"%(change_time))
    goal=get_goals() # get the query list from get_goals()
    srch=str(random.choice(goal)) # take a random query
    print(Fore.YELLOW+"Topic: ",srch+Style.RESET_ALL) # print query

    search = pu.photos(type_='random', count=1, featured=True,orientation='landscape', query=srch)

    for entry in search.entries:
        url=entry.link_download # get the download link
        filename=entry.id # get the id as filename

    r = requests.get(url, stream = True)
    total_size = int(r.headers['content-length'])
    filename = "temp\\"+filename+".jfif" # add path and extension to file name
    print(Fore.CYAN+"File Name: ",os.path.basename(filename)+Style.RESET_ALL) # print file name
    print ("Downloading....")
    with open(filename, 'wb') as f:
        for data in tqdm(iterable = r.iter_content(chunk_size = 1024), total = int(total_size/1024), unit = 'KB'): # set tqdm stuff
            f.write(data) # write contents
    print (Fore.GREEN+"Download complete. Setting wallpaper .... "+Style.RESET_ALL)
    subprocess.call("WallpaperChanger "+filename+" 4",shell=True) # set wallpaper using WallpaperChanger.exe https://github.com/philhansen/WallpaperChanger

    threading.Timer(int(change_time), get_images).start() # call function after change time has passed

def mk_dir(): #make folder if it doesn't exists
    if not os.path.exists('temp'):
        os.makedirs('temp')

def initiate(): # remove all files in temp folder
    if os.path.exists('temp'):
        filelist = [ f for f in os.listdir('temp') ]
        for f in filelist:
            try:
                os.remove(os.path.join('temp', f))
            except:
                pass
    else:
        pass

def get_goals(): # get the queries from goals.txt
    if (os.path.isfile('goals.txt')):
        if (os.stat("goals.txt").st_size == 0):
            return ['flower','forest','nature']
        else:
            goal_file = open('goals.txt', 'r')
            for line in goal_file:
                fields=line.split(',')
            return fields
            goal_file.close()
    else:
        return ['flower','forest','nature']

def get_time(): # get time as argument (optional)
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        return int(sys.argv[1])
    else:
        return 1800

def get_name ():
    name=getpass.getuser()
    name=name[:1].upper()+name[1:]
    return name

def check_conn (): # check internet connection
    try:
        response=requests.get ("https://www.google.com/")
        return True
    except requests.ConnectionError: pass
    return False

# instantiate PyUnsplash object
pu = pyunsplash.PyUnsplash(api_key=get_key())
print(Fore.MAGENTA+"Welcome "+get_name()+" to Z-Splash"+ Style.RESET_ALL)
# Call functions
initiate() # delete contents of temp if present
mk_dir() # make temp folder if not present
if not check_conn():
    print(Fore.RED+"No internet connection found. "+ Style.RESET_ALL)
    time.sleep(5)
else:
    get_images() # get the images from unsplash.com


