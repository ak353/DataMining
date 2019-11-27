import requests
from bs4 import BeautifulSoup
import re
import youtube_scraper as ytscrap
import instagram  
import twitter



def get_accounts(youtube_username):

    url = 'https://www.youtube.com/user/'+youtube_username+'/about'

    facebook_acc = 'NIL'
    instagram_acc = 'NIL'
    twitter_acc = 'NIL'

    print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
  
    for a in (soup.find_all('a', href=True)):

        if("facebook" in  a['href']):
            facebook_acc = get_facebook_username(str(a['href']))

        if("instagram" in  a['href']):
            instagram_acc = get_instagram_username(str(a['href']))
 

        if("twitter" in  a['href']):
            twitter_acc = get_twitter_username(str(a['href']))

    return facebook_acc,instagram_acc,twitter_acc



def get_facebook_username(url):
    try:
        a = url.split("facebook.com%2F")[1]
        b = a.split("&")[0]
        return b.strip('%2F')
    except: return 'NIL'

            
def get_twitter_username(url):
    try:
        a = url.split("twitter.com%2F")[1]
        b = a.split("&")[0]
        return b.strip('%2F')
    except: return 'NIL'


def get_instagram_username(url):
    try:
        a = url.split("instagram.com%2F")[1]
        b = a.split("&")[0]
        return b.strip('%2F')
    except: return 'NIL'
    
'''
Create a usernames table
0) Youtube
1) Facebook
2) Instagram
3) Twitter
'''

def write_dataset():

    f_count = 0
    i_count = 0
    t_count = 0
    at_least_2 = 0

    f_read = open("yt_dataset.txt", "r")
    f_write = open("social_media_usernames.txt", "w")
    lines = f_read.readlines()

    for l in lines:
        try:
            youtube = l.split(';')[1]
            facebook,insta,twit = get_accounts(youtube)
            f_write.writelines(youtube+";"+facebook+ ";" +insta + ";" + twit+"\n")

            if(facebook != 'NIL'): f_count+=1
            if(insta != 'NIL'): i_count+=1
            if(twit != 'NIL'): t_count+=1
            if( (facebook != 'NIL' and insta != 'NIL') or (facebook != 'NIL' and twit != 'NIL') or 
                (insta != 'NIL' and twit != 'NIL') ): 
                    
                    at_least_2+=1
        
        except: print("Error " + l)

    print("Facebook " + str(f_count))
    print("Insta " + str(i_count))
    print("Twitter " + str(t_count))
    print("At least 2 social media acc " + str(at_least_2))



'''
    Youtube_username
    Facebook_username
    Instagram_username
    Twitter_username
'''

def dataset_have_insta_and_twitter():
    count = 0
    f_read = open("social_media_usernames.txt", "r")
    # f_write = open("social_media_usernames_new1.txt", "w")
    lines = f_read.readlines()

    try:
        for l in lines:
            row = l.split(';')
            if(row[2]!='NIL' and row[3].strip()!='NIL' ):
                f_write.writelines(l)
                

    except Exception as e:
        print(str(e))


def build_twitter_dataset():

    f_read = open("social_media_usernames.txt", "r")
    f_write = open("twitter_dataset.txt", "w")

    lines = f_read.readlines()
    for l in lines:
        try:
            youtube_username = l.split(';')[0]
            twitter_username = l.split(';')[3].strip()
            num_followers,num_following,num_tweets,num_likes = twitter.get_twitter_info(twitter_username)
            
            f_write.writelines(youtube_username+";"+twitter_username+';'+num_followers+';'+num_following+";"+num_tweets+";"+num_likes+"\n")

        except Exception as e:
            print(str(e) + l)
            # f_write.writelines(twitter_username+';'+"NIL"+';'+"NIL"+";"+"NIL"+';'+"NIL\n")
            continue



def fix_twitter_dataset():

    f_read = open("twitter_dataset.txt", "r")
    f_write = open("twitter_dataset_new.txt", "a")

    lines = f_read.readlines()
    for l in lines:
        try:
            twitter_username = l.split(';')[3]
            num_followers,num_following,num_tweets,num_likes = twitter.get_twitter_info(twitter_username.strip())
            
            f_write.writelines(twitter_username+';'+num_followers+';'+num_following+";"+num_tweets+";"+num_likes+"\n")

        except Exception as e:
            print(str(e) + l)
            continue




def find_all_usernames(usr,lst,column):

    for l in lst:
        sp = l.split(";")
        if (sp[column] == usr.strip()):
            return l
    
    print("Error: " + usr)
    return 'NIL'



def remove_dup(name):

    lines_seen = set()
    outfile = open(name.strip('.txt')+"_no_duplicate.txt", "w")
    for line in open(name, "r"):
        if line not in lines_seen:
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()



def build_final__dataset():

    f_read_username = open("social_media_usernames.txt", "r")
    f_read_yt = open("yt_dataset.txt", "r")
    f_read_twitter = open("twitter_dataset.txt", "r")
    f_read_insta = open("instagram_dataset.txt", "r")

    f_write_dataset = open("Dataset.csv", "w")


    
    lines_insta = f_read_insta.readlines()
    lines_username = f_read_username.readlines()
    lines_yt = f_read_yt.readlines()
    lines_twit = f_read_twitter.readlines()


    for l in lines_insta:
        insta_um = l.split(';')[0]  
        username_table_row = find_all_usernames(insta_um,lines_username,2)
       
       
        yt = username_table_row.split(";")[0].strip()
        twit = username_table_row.split(";")[3].strip()  # In Usernmae Table, Twitter username at index 3
        twit_rec = find_all_usernames(twit,lines_twit,1) # In Twitter Table, username at index 1

        print(insta_um+ " " + twit_rec) 
        yt_rec = find_all_usernames(yt,lines_yt,1)  # In Youtube Table, username at index 1
    
        record = ""
        rec = ""

        record = (yt_rec.strip()+";"+l.strip()+";"+twit_rec)  # Merge All 
        record_split = record.split(";")

        record_split[3] = check_value(record_split[3])
      

        if(len(record_split) > 14):
            rec = (record_split[1]+";"+record_split[2]+";"+record_split[3]+";"
                    +record_split[4]+";"+record_split[6]+";"
                    + record_split[7]+";"+  record_split[8]+";"+ record_split[12]+";"
                    + record_split[13]+";"+ record_split[14])

        print(rec)

        f_write_dataset.writelines(rec)



def check_value(value):
    try:
        value = value.strip()
        if 'M' in value:
            value = value.strip('M')
            # print(value)
            value = float (value) * 1000000

            return str(value)

        else: return value

    except Exception as e:
        
        print("err:" + value)
        return 'NIL'



if __name__ == "__main__":
    build_final__dataset()