import tweepy
import re
from time import time, sleep
from datetime import datetime
import os
import glob

auth = tweepy.OAuthHandler('CONSUMERKEY','CONSUMERSECRET')
auth.set_access_token('ACCESSTOKEN', 'ACCESSTOKENSECRET')

#evil_tweets=['690681645905477632']

api = tweepy.API(auth)

me = api.me()

friendship_limit = api.rate_limit_status()['resources']['friendships']['/friendships/show']
number_of_friendship_requests = friendship_limit['limit'] - friendship_limit['remaining']


number_of_blocked = 0
j = 0;
blocked = []
if (os.path.exists("data")):
    files = glob.glob("data/*.csv")
else:
    os.makedir("data")
    files = []

def do_exception (e, twerp_type='Tweeter'):
    print str(e)
    print 'Exception: {}'.format(twerp_type)
    sleep(60 * 5)
    print 'Recovering'
    dump_blocks()
    #files = glob.glob("data/*.csv")
    check_limit(True)
    return


def dump_blocks ():
    global blocked
    if len(blocked) > 0:
        try:
            f = file('data/block_list'+ str(time())+'.csv', 'w')
            for item in blocked:
                f.write(item+'\n')
            f.close()
            blocked = []
            files = glob.glob("data/*.csv")
        except Exception, e:
            do_exception('file writing')

def check_duplicate ( id_str ):

    duplicate = False

    if id_str in blocked:
        duplicate = True

    if not duplicate:
        for csv_file in files:
            with open(csv_file, 'r') as losers:
                for twerp in losers:
                    twerp = twerp.rstrip()
                    #print twerp + ' ' + id_str

                    if twerp == id_str:
                        duplicate = True
                        break
            if duplicate:
                break
    return duplicate



def check_limit (force=False):
    global number_of_friendship_requests, api

    number_of_friendship_requests += 1
    try:
        if (number_of_friendship_requests >= 175) or force: # rate limit is 180 per 15 minutes
            reset = api.rate_limit_status()['resources']['friendships']['/friendships/show']['reset']
            continue_time = datetime.fromtimestamp(reset).strftime('%H:%M:%S')
            print 'waiting for rate limit... (will continue at {})'.format(continue_time)
            sleep(reset - time() + 1)
            number_of_friendship_requests = 0
    except Exception, e:
        do_exception(e, 'api limit')
    return



def block_twerp ( twerp, type_str, i=0 ):

    global number_of_friendship_requests, number_of_blocked, api, me



    print '{} #{}: {}'.format(type_str, i+1, twerp.screen_name)

    if check_duplicate(twerp.id_str):
        print '---duplicate'
    else:

        check_limit()
        friendship = api.show_friendship(source_screen_name=twerp.screen_name,
                                 target_screen_name=me.screen_name)
        if friendship[0].followed_by:
            print '------Spared!'
        else:
                number_of_blocked += 1
                #print 'blocked ({} already)'.format(number_of_blocked)
                api.create_block(screen_name=twerp.screen_name)
                blocked.append(twerp.id_str)
                blocked.sort()


    return i+1

def block_followers ( twerp ):
    try:
        for i, follower in enumerate(tweepy.Cursor(api.followers, screen_name=twerp.screen_name).items()):

            try:
                block_twerp(follower, 'Follower',  i)
            except Exception, e:
              do_exception(e, 'follower')
            check_limit()
    except Exception, e:
        do_exception(e, 'follower')
    return

##################




while True:

    try:
        for m, message in enumerate(tweepy.Cursor(api.direct_messages).items()):
            try:
                friendship = api.show_friendship(source_screen_name=message.sender_screen_name,
                                                     target_screen_name=me.screen_name)
                if friendship[0].followed_by:

                    if message.text.isdigit():

                        #print message.text
                        tweet = message.text

                        check_limit(True)
                        try:
                            api.update_status('Now blocking tweet {}'.format(tweet))
                        except Exception, e:
                            print str(e)

                        number_of_blocked = 0
                        j = 0;

                        status = api.get_status(tweet)
                        #print status
                        twerp = status.user  #.screen_name
                        #print twerp
                        block_twerp(twerp, 'Original',  0)
                        check_limit()
                        block_followers(twerp )

                        check_limit()
                        try:
                            for retweet in api.retweets(tweet, 500):
                                twerp = retweet.user #.screen_name
                                j = block_twerp(twerp, 'RTer',  j)
                                check_limit ()
                                block_followers(twerp)
                        except Exception, e:
                            do_exception(e, 'rewteeter')

                        check_limit()
                        api.update_status('blocked {} accounts from tweet {}'.format(number_of_blocked, tweet))
            except Exception, e:
                do_exception(e)
    except Exception, e:
        do_exception(e)

    print 'Finished my queue'
    dump_blocks()
    sleep(60*20) # sleep for 20 minutes
