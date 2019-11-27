import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"] 
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "secret.json"



class Channel:
    def __init__(self, channel_name,username ,uploads,subscribers,total_views):
        self.name = channel_name
        self.username = username
        self.uploads = uploads
        self.subscribers = subscribers
        self.total_views = total_views

    def print_all(self,channel):
        print(channel.name + ";" + channel.username+ ";" + channel.uploads + ";" + channel.subscribers + ";" + channel.total_views+"\n")
        return(channel.name + ";" + channel.username+ ";" + channel.uploads + ";" + channel.subscribers + ";" + channel.total_views+"\n")


url = 'http://socialblade.com/youtube/top/5000/mostsubscribed'

def get_list_youtube_channels():  

    youtube_channels = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'html.parser')
    channels = soup.find('div', attrs={'style': 'float: right; width: 900px;'}).find_all('div', recursive=False)[4:]

    for channel in channels:
        channel_name = channel.find('div', attrs={'style': 'float: left; width: 350px; line-height: 25px;'}).a.text.strip()
        uploads = channel.find('div', attrs={'style': 'float: left; width: 80px;'}).span.text.strip()
        subscribers = channel.find_all('div', attrs={'style': 'float: left; width: 150px;'})[0].text.strip()
        total_views = channel.find_all('div', attrs={'style': 'float: left; width: 150px;'})[1].span.text.strip()
        user_name = get_channel_username_scrape(channel_name)
        
        if(user_name != "NIL"):
            channel = Channel(channel_name,user_name,uploads,subscribers,total_views)
            youtube_channels.append(channel)

    return youtube_channels



def get_channel_username_scrape(name):

    user = "NIL"
    url = "https://www.youtube.com/results?search_query="
    channel_filter = "&sp=EgIQAg%253D%253D"

    page = requests.get(url+name+channel_filter)
    soup = BeautifulSoup(page.content, 'html.parser')

    print(url+name+channel_filter)
    for a in (soup.find_all('a', href=True)):

        if("/user/" in a['href']):
            user = a['href']
            user = user[6:]
            break
    
    return user


def get_channel_username_API(name):


    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.search().list(
        part="snippet",
        q=name,
        type="channel",
        maxResults=1,
    )
    response = request.execute()

    print(response)


def write_dataset():

    f = open("yt_dataset.txt", "w")
    channels = get_list_youtube_channels()
    for c in channels:
        f.write(c.print_all(c))
        
    f.close()


if __name__ == "__main__":
    get_channel_username_API('pewdiepie')