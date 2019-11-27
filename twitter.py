from bs4 import BeautifulSoup
import requests


def get_twitter_info(username):

   
    temp = requests.get('https://twitter.com/'+username)
    bs = BeautifulSoup(temp.text,'lxml')
    try:
        follow_box = bs.find('li',{'class':'ProfileNav-item ProfileNav-item--followers'})
        tweets_box = bs.find('li',{'class':'ProfileNav-item ProfileNav-item--tweets is-active'})
        likes_box = bs.find('li',{'class':'ProfileNav-item ProfileNav-item--favorites'})

        num_followers = follow_box.find('a').find('span',{'class':'ProfileNav-value'}).get('data-count')
        num_tweets = tweets_box.find('a').find('span',{'class':'ProfileNav-value'}).get('data-count')
        num_likes = likes_box.find('a').find('span',{'class':'ProfileNav-value'}).get('data-count')

        return num_followers,num_tweets,num_likes

    except Exception as e:
        print(str(e))




if __name__ == "__main__":
    print(get_twitter_info('tastynetwork'))