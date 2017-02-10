#! /usr/bin/env python3.5
# Script for extracting twitter followers for screenName (screenName is same as username)
# by Aleksandar Josifoski https://about.me/josifsk
# 2017 February 10
# It extracts 300 followers in about 15min due to twitter restrictions

# Depends on installed tweepy. Most easy way to install pip3 install -U tweepy
import tweepy
import time
import codecs
import re
import sys

#Change to desired screenName from which you want to extract followers
screenName = "amazingfacts"

# Change directory
dirf = '/data/twitter/'

#insert your Twitter keys here, from https://apps.twitter.com
consumer_key =''
consumer_secret=''
access_token=''
access_secret=''

auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

time1 = time.time()

g = codecs.open(dirf + screenName + '_followers.txt', 'w', 'utf-8')
l = []
if(api.verify_credentials):
    print('Login successful')
cycle = 0
users = tweepy.Cursor(api.followers, screen_name=screenName, include_entities=True, include_status=True).items()
while True:
    try:
        user = next(users)
        cycle += 1
        if cycle % 300 == 0: print(cycle)
        fine = True
    except tweepy.TweepError:
        print('sleep 3min')
        time.sleep(3 * 60)
        fine = False
    except StopIteration:
        break
    if fine:
        g.write('screen_name: ' + str(user.screen_name) + '\n')
        g.write('name: ' + str(user.name) + '\n')
        g.write('id_str: ' + str(user.id_str) + '\n')
        g.write('profile_image_url: ' + str(user.profile_image_url_https) + '\n')
        try:
            expanded_url = str(dict(user.entities.get('url', {}).get('urls', [])[0]).get('expanded_url', []))
        except:
            expanded_url = ''
        g.write('url: ' + expanded_url + '\n')
        desc = str(user.description)
        desc = desc.replace('\n', ' ').replace('\r', ' ').replace('\t', '    ')
        g.write('description: ' + desc + '\n')
        g.write('location: ' + str(user.location) + '\n')
        g.write('protected: ' + str(user.protected) + '\n')
        g.write('statuses_count: ' + str(user.statuses_count) + '\n')
        g.write('friends_count: ' + str(user.friends_count) + '\n')
        g.write('followers_count: ' + str(user.followers_count) + '\n')
        g.write('listed_count: ' + str(user.listed_count) + '\n')
        try:
            acd = str(user._json.get('created_at', []))
        except:
            acd = ''
        g.write('acc_creation_date: ' + str(acd) + '\n')
        try:
            last_tweet = str(user.status._json.get('text', []))
            last_tweet_cd = str(user.status._json.get('created_at', []))
            last_tweet = last_tweet.replace('\n', ' ').replace('\r', ' ').replace('\t', '    ')
        except:
            last_tweet = ''
            last_tweet_cd = ''
        g.write('last_tweet: ' + last_tweet_cd + ' ' + last_tweet + '\n')
        g.write('*' * 50 + '\n')

g.close()
time2=time.time()
difftimeinmin = (time2-time1)/60.
print("%.2f minutes" % difftimeinmin)
print('Done.')
