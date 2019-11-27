import requests
import json
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import html

def get_instagram_info(username):
    
    url = 'https://www.instagram.com/'+username+'/?__a=1'
    reply = requests.get(url).json()
    print(json_reply)


    if 'json' in reply.headers.get('Content-Type'):
        js = reply.json()
    else:
        print('Response content is not in JSON format.')
        # print(reply.content)
        

    number_followers =(str) (json_reply['graphql']['user']['edge_followed_by']['count'])
    number_following = (str)(json_reply['graphql']['user']['edge_follow']['count'])
    number_posts = (str)(json_reply['graphql']['user']['edge_owner_to_timeline_media']['count'])
    return number_followers,number_following,number_posts


def clear_dataset():
    f_read = open("instagram_dataset2.txt", "r")
    f_write = open("instagram_dataset2_new.txt", "w")

    lines = f_read.readlines()
    for l in lines:
        if(  ('Followers' in l) and ('Following' in l) and ('Posts' in l)):
            sp = l.split(";")
            
            row = (sp[0] + ";"+ sp[1].strip('Followers',).strip()+";"+ sp[2].strip('Following').strip()+";"+sp[3].strip('Posts').strip()+"\n")
            f_write.writelines(row)

    f_read.close()
    f_write.close()

def read_values():

    f_read = open("instagram_dataset2_new.txt", "r")
    f_write = open("instagram_dataset2.txt", "w")
    
    lines = f_read.readlines()
    for l in lines:
        sp = l.split(";")

        followers = sp[1]
        following = sp[2]
        posts = sp[3]

        followers = check_value(followers)
        following = check_value(following)
        posts = check_value(posts)

        f_write.writelines(sp[0]+";"+followers+";"+following+";"+posts+"\n")



def check_value(value):
    try:
        value = value.strip()
        if 'm' in value:
            value = value.strip('m')
            # print(value)
            value = float (value) * 1000000


        elif 'k' in value:
            value = value.strip('k')
            # print(value)
            value = float (value) * 1000
        
        return str(value)

    except Exception as e:
        
        print("err:" + value)
        return 'NIL'


if __name__ == "__main__":
    clear_dataset()
    read_values()




