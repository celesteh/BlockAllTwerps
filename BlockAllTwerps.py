import tweepy
import re
from time import time, sleep
import datetime
import os
import glob
import Tkinter as tk
import sys
from PIL import Image, ImageTk
import urllib
import io
from math import floor
import setproctitle

setproctitle.setproctitle('BlockAllTwerps')

root = None
mainframe = None
egg = None
api = None
me = None
config = {}
number_of_friendship_requests = 0
number_of_blocked = 0
j = 0;
blocked = []
files = []
last_reset = 0

def init():
    global config, egg, root, mainframe, api, me, number_of_blocked, number_of_friendship_requests, files



    file_name = "BlockAllTwerps.config"
    config_file= open(file_name)

    for line in config_file:
        line = line.strip()
        if line and line[0] is not "#" and line[-1] is not "=":
            var,val = line.rsplit("=",1)
            config[var.strip()] = val.strip()
    config_file.close()

    #gui
    if (len(sys.argv) > 1):
        #print('has gui')
        root = tk.Tk()
        if (sys.argv[1] == '-fullscreen'):
            #print('is fullscreen')
            root.attributes('-fullscreen', True)
        #else:
            #print ('not fullscreen')
        root.title('BlockAllTwerps')
        root.configure(background='black')
        mainframe = tk.Frame(root)
        egg = Image.open('default_profile_5_400x400.jpg')

    #twitter
    auth = tweepy.OAuthHandler(config['consumer_key'], config['consumer_secret'])
    auth.set_access_token(config['access_token'], config['access_token_secret'])


    api = tweepy.API(auth)

    #check_limit(True) #testing
    #do_wait(5) # testing
    try:
        rls = api.rate_limit_status()['resources']
        friendship_limit = rls ['friendships']['/friendships/show']
        number_of_friendship_requests = friendship_limit['limit'] - friendship_limit['remaining']
        lookups = (rls['users']["/users/show/:id"]['limit'] - rls['users']["/users/show/:id"]['remaining'])
        #print('lookups', lookups)
        number_of_friendship_requests = max(number_of_friendship_requests, lookups)

        if (number_of_friendship_requests >= 100):
            check_limit(True)
        else:
            check_limit()

        me = api.me()
    except tweepy.RateLimitError:
        sleep(15*60)
        number_of_friendship_requests = 0
        me = api.me()


    if (os.path.exists("data")):
        files = glob.glob("data/*.csv")
    else:
        os.makedir("data")
        files = []

    #if root:
        #print ('start gui')

def touch ():
    global root
    if root:
      print ('touch')
      if not os.path.exists('/tmp/blockalltwerps'):
          open('/tmp/blockalltwerps', 'a').close()
    return

def update_gui ():
    global root
    if root:
        #print('update')
        root.update()
        root.after(500, update_gui)

#def display_wait ( wait):
#    global mainframe, root
#
#    if root:
#        try:
#            if mainframe:
#                mainframe.destroy()
#            mainframe = tk.Frame(root, bg="black")
#            mainframe.pack(padx=5, pady=5, fill="both", expand=True)
#            text = 'Waiting for rate limit... (Will continue in {})'.format(wait)
#            label = tk.Label(mainframe, text=text, font=("FreeSans", 40), fg="white", bg="black", height=2)
#            label.pack(fill=tk.BOTH, expand=1)
#            #label.pack(fill=tk.BOTH, expand=1)
#            root.update()
#        except Exception, e:
#            dump_blocks()
#            print('gui failed')
#            sys.exit(1)

def display_user (twerp, duplicate =False):
    global mainframe, root, config

    #name = twerp.name
    #handle = twerp.screen_name
    img = twerp.profile_image_url
    img = img.replace('normal', '400x400')
    size = 400, 400
    #print(img)
    should_continue = False

    if root:
        try:
            if mainframe:
                mainframe.destroy()
            mainframe = tk.Frame(root, bg="black")
            mainframe.pack(padx=5, pady=5, fill="both", expand=True)

            try:
                #look out for network errors
                fp = urllib.urlopen(img)
                data = fp.read()
                fp.close()

                image = Image.open(io.BytesIO(data))
                image = image.resize((400, 400),Image.ANTIALIAS)

                should_continue = True
            except Exception, e:
                do_exception('network', 'gui')
                image = egg
                should_continue = False

            #if (image.size() != size):
            if should_continue:

                photo = ImageTk.PhotoImage(image)
                #photo.resize(size)

                title =  tk.Label(mainframe, text="Blocking", font=("FreeSans", int(config['title_size'])), fg="white", bg="black", height=2).grid(row=0, sticky=tk.W)
                pic = tk.Label(mainframe, image=photo, height=440, bg="black").grid(row=1, rowspan=10)
                name = tk.Label(mainframe, text=twerp.name, font=("FreeSans", int(config['name_size'])), fg="white", bg="black").grid(row=5, column=2, sticky=tk.W)
                handle = tk.Label(mainframe, text='@'+twerp.screen_name, font=("FreeSans", int(config['name_size'])), fg="blue", bg="black").grid(row=6, column=2, sticky=tk.W)
                if duplicate:
                    tk.Label(mainframe, text='(Duplicate... already blocked)', font=("FreeSans", int(config['dup_size'])), fg="white", bg="black").grid(row=10, column=2, sticky=tk.W)
                root.update()
        except Exception, e:
            dump_blocks()
            print('gui failed')
            sys.exit(1)
    #print twerp
def calc_string(delta):
    if delta.seconds >= 1:
        #print('fuck you')
        minutes = int(floor(delta.seconds/60))
        seconds = delta.seconds % 60
        disp_time = '{:0>2d}:{:0>2d}'.format(minutes, seconds)
    else:
        #print('and the horse etc')
        disp_time = '0:00'
    return disp_time

def do_wait(sleep_time):
    global mainframe, config
    print('wait')
    if root:
        delta = datetime.timedelta(seconds=sleep_time)
        disp_time = calc_string(delta)
        v= tk.StringVar()

        #print(disp_time)
        try:
            if mainframe:
                mainframe.destroy()
            mainframe = tk.Frame(root, bg="black")
            print('newframe')
            mainframe.pack(padx=5, pady=5, fill="both", expand=True)
            print('mainframe')
            text = 'Waiting for rate limit... (Will continue in {})'.format(disp_time)
            print(text)
            v.set(text)
            label = tk.Label(mainframe, textvariable=v, font=("FreeSans", int(config['wait_size'])), fg="white", bg="black", height=2)
            label.pack(fill=tk.BOTH, expand=1)
            #label.pack(fill=tk.BOTH, expand=1)
            root.update()
            for i in xrange(int(floor(sleep_time))):
                disp_time = calc_string(delta)
                text = 'Waiting for rate limit... (Will continue in {})'.format(disp_time)
                label.text = text
                v.set(text)
                print(label.text)
                root.update()
                delta = delta - datetime.timedelta(seconds=1)
                sleep (1)
                if (i % 60 == 0): # once per minute
                    touch()
            text = 'Waiting for rate limit... (Will continue in {})'.format('00:00')
            label.text = text
            v.set(text)
            print(label.text)
            root.update()
        except Exception, e:
            dump_blocks()
            print('gui failed')
            sys.exit(1)

    else :
        sleep(sleep_time)

def do_exception (e, twerp_type='Tweeter'):
    sleep_time = 60 * 5
    print str(e)
    print 'Exception: {}'.format(twerp_type)
    do_wait(sleep_time)
    print 'Recovering'
    dump_blocks()
    #files = glob.glob("data/*.csv")
    #check_limit(True)
    check_limit()
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

def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            dump_blocks()
            #time.sleep(15 * 60)
            do_wait(15*60)



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
    global number_of_friendship_requests, api, last_reset

    number_of_friendship_requests += 1
    touch()
    try:
        if (number_of_friendship_requests >= 175) or force: # rate limit is 180 per 15 minutes
            reset = api.rate_limit_status()['resources']['friendships']['/friendships/show']['reset']

            # If we've gone on so long we're in a new period, don't bother to wait
            if (reset == last_reset) or (reset == 0) or force:
                print('')
                continue_time = datetime.datetime.fromtimestamp(reset).strftime('%H:%M:%S')
                print 'waiting for rate limit... (will continue at {})'.format(continue_time)
                #display_wait(continue_time)
                #sleep(reset - time() + 1)
                print(reset - time() + 1)
                do_wait(reset - time() + 1)
                number_of_friendship_requests = 0

            last_reset = api.rate_limit_status()['resources']['friendships']['/friendships/show']['reset']
    except Exception, e:
        do_exception(e, 'api limit')
    return



def block_twerp ( twerp, type_str, i=0 ):

    global number_of_friendship_requests, number_of_blocked, api, me



    print '{} #{}: {}'.format(type_str, i+1, twerp.screen_name)

    if check_duplicate(twerp.id_str):
        print '---duplicate'
        display_user(twerp, True)
    else:

        check_limit()
        friendship = api.show_friendship(source_screen_name=twerp.screen_name,
                                 target_screen_name=me.screen_name)
        if friendship[0].followed_by:
            print '------Spared!'
        else:
            display_user(twerp, False)
            number_of_blocked += 1
            #print 'blocked ({} already)'.format(number_of_blocked)
            api.create_block(screen_name=twerp.screen_name)
            blocked.append(twerp.id_str)
            blocked.sort()

    sleep(1)
    return i+1

def block_followers ( twerp ):
    global root

    last_i = 0
    this_i = 0
    unchanged = 0
    limit = 50
    if root:
        limit = 10

    try:
        #for i, follower in limit_handled(tweepy.Cursor(api.followers, screen_name=twerp.screen_name).items()):
        for i, follower in enumerate(tweepy.Cursor(api.followers, screen_name=twerp.screen_name).items()):

            try:
                this_i = block_twerp(follower, 'Follower',  i)

                # if we've had a lot of duplicates, we still need to be aware of API limits
                if (last_i == this_i):
                    unchanged +=1
                    if (unchanged >= limit):
                        check_limit()
                        unchanged = 0
                else: #we've blocked someone
                    unchanged = 0


            except Exception, e:
              do_exception(e, 'follower')
            check_limit()
    except Exception, e:
        do_exception(e, 'follower')
    return

##################

init()

if root:
    root.after(500, update_gui)


first = True

while True:
    try:
        for m, message in enumerate(tweepy.Cursor(api.direct_messages).items()):
            try:
                check_limit()
                friendship = api.show_friendship(source_screen_name=message.sender_screen_name,
                                                     target_screen_name=me.screen_name)
                if friendship[0].followed_by:

                    if message.text.isdigit():

                        #print message.text
                        tweet = message.text

                        if first:
                            first = False
                        else:
                            check_limit(True)
                        try:
                            api.update_status('Now blocking tweet {}'.format(tweet))
                        except Exception, e:
                            print str(e)
                            #do_exception (e, 'tweeting')

                        number_of_blocked = 0
                        j = 0;

                        status = api.get_status(tweet)
                        #print status
                        twerp = status.user  #.screen_name
                        #display_user(twerp)
                        block_twerp(twerp, 'Original',  0)
                        #check_limit()
                        block_followers(twerp )

                        #check_limit()
                        try:
                            for retweet in api.retweets(tweet, 500):
                                twerp = retweet.user #.screen_name
                                j = block_twerp(twerp, 'RTer',  j)
                                #check_limit ()
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
