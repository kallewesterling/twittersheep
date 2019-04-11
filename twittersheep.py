__version__ = "beta 1"
__author__ = 'Kalle Westerling'
__license__ = 'MIT'


# Settings
try: from config import *
except: raise RuntimeError("An error occurred when importing the settings. Make sure the `config.py` file exists in the same directory as twittersheep.py.") from None

# Imports

## From python's standard library
import time, json, os
from pathlib import Path

## Special imports
try: import tweepy
except: raise RuntimeError("TwitterSheep requires tweepy. You must install the package: Run `pip install tweepy` from your terminal.") from None
    
try: from wordcloud import WordCloud, STOPWORDS
except: raise RuntimeError("TwitterSheep requires wordcloud. You must install the package: Run `pip install wordcloud` from your terminal.") from None

try: import progressbar
except: raise RuntimeError("TwitterSheep requires progressbar. You must install the package: Run `pip install progressbar` from your terminal.") from None

try: import matplotlib.pyplot as plt
except: raise RuntimeError("TwitterSheep requires matplotlib. You must install the package: Run `pip install matplotlib` from your terminal.") from None



class TwitterSheep(object):

    def __init__(self, username=None, quiet=False):
        
        if username is None: raise RuntimeError("You must provide a Twitter username.")
        
        # Set up tweepy's API
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        
        # Test cache
        self.cache_path = Path(CACHE_DIR)
        while not self.cache_path.exists() and not self.cache_path.is_dir(): os.mkdir(self.cache_path) # if the cache folder does not exist, create it
        
        self.username, self.quiet = username, quiet
        
        self.friend_ids = self._get_friend_ids()
        self.follower_ids = self._get_follower_ids()
        
        self.friend_bios = self._get_bios(self.friend_ids)
        self.follower_bios = self._get_bios(self.follower_ids)

        # Set up bios with unique bios
        self.bios = []
        self.bios.extend(self.friend_bios)
        self.bios.extend(self.follower_bios)
        self.bios = list(set(self.bios))
        
        
    def _get_friend_ids(self):
        cache_file = self.cache_path.joinpath(f"_friends")
        if not cache_file.exists():
            if not self.quiet: print(f"Downloading friend list for {self.username}...")
            
            friend_ids = self.api.friends_ids(self.username)
            _list = []
            for friend in friend_ids:
                _list.append(str(friend))
            with open(cache_file, "w+") as file:
                file.write("\n".join(_list))
        if not self.quiet: print(f"Reading friend list...")
        with open(cache_file, "r") as file:
            data = file.read()
        return(data.split("\n"))        
        
        
    def _get_follower_ids(self):
        cache_file = self.cache_path.joinpath(f"_followers")
        if not cache_file.exists():
            if not self.quiet: print(f"Downloading follower list for {self.username}...")
            
            ids = []
            with open(cache_file, "w+") as file:
                file.write("")
                
            pages = tweepy.Cursor(self.api.followers_ids, screen_name=self.username).pages()
            for page in pages:
                ids.extend(page)
                _list = []
                for friend in page:
                    _list.append(str(friend))

                with open(cache_file, "a") as file:
                    file.write("\n".join(_list))
                
                if not self.quiet: print(f"Waiting 60 seconds...")
                time.sleep(60)
                
        if not self.quiet: print(f"Reading follower list...")
        with open(cache_file, "r") as file:
            data = file.read()
        return(data.split("\n"))
    
    
    def _get_bios(self, _list): # takes one argument, a list of ids
        if not self.quiet: print("Getting all friend bios from list of IDs...")
        _descriptions = []
        if not self.quiet: bar = progressbar.ProgressBar(maxval=len(_list))
        i = 0
        for id in _list:
            i+=1
            if not self.quiet: bar.update(i)
            cache_file = self.cache_path.joinpath(f"{id}.json")
            if not cache_file.exists():
                with open(cache_file, "w+") as file:
                    json.dump(self.api.get_user(id)._json, file)
            with open(cache_file, "r") as file:
                try: data = json.load(file)
                except: print(f"Error opening cache file `{cache_file}`. Try removing it manually and run the script again.")
            _descriptions.append(data['description'])
        if not self.quiet: bar.finish()
        return(_descriptions)

    
    def save_wordcloud(self, path="./wordcloud.png", only_followers=False, only_friends=False):
        if only_followers and only_friends: raise RuntimeError("You have to choose between followers and friends for the wordcloud. Another option is to remove the `only_followers` and `only_friends` setting altogether, to generate the wordcloud from all the bios.")

        # Set up the actual text we'll use
        if only_followers:
            text = " ".join(self.follower_bios)
        elif only_friends:
            text = " ".join(self.friend_bios)
        else:
            text = " ".join(self.bios)
        
        # Lowercase all the words
        text = text.lower()

        # remove stopwords
        stopwords = set(STOPWORDS)
        
        wordcloud = WordCloud(stopwords=stopwords, max_words=1000, width=1500, height=1000, max_font_size=100).generate(text)
        plt.figure( figsize=(20,10) )
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(path, format="png")
        plt.show()