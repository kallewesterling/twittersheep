# TwitterSheep Python Port

Remember TwitterSheep.com and how it used to work? 

Well, I wrote a simple Python port that works the same way (ish). Feel free to suggest changes via pull requests or issues.

The result is a wordcloud like this one (based on [my twitter account](http://www.twitter.com/kallewesterling)):

![Image showing an example of my wordcloud generated using the script.](images/my_wordcloud.png)

## Requirements

You have to install a couple of Python packages for this script to run:
- tweepy
- wordcloud
- progressbar
- matplotlib

You can use `pip install` to install all of the packages above (i.e. `pip install tweepy` etc.).

## How-to

### Step 1

Fill in [your Twitter credentials](https://developer.twitter.com/en/apply-for-access.html) in `config.py`:

```python
    '''
    Set up your Twitter authentication here.
    '''
    CONSUMER_KEY = "**************************"
    CONSUMER_SECRET = "**********************************************"
    ACCESS_TOKEN = "********-**********************************************"
    ACCESS_TOKEN_SECRET = "**********************************************"
```

### Step 2

Import the TwitterSheep class from the file:

```python
from twittersheep import TwitterSheep
```

### Step 3

Run the TwitterSheep class using the username you want to use:

```python
herd = TwitterSheep(username="kallewesterling")
```

It will take some time when you run the script the first time as it has to download all the data from Twitter, and the `tweepy` package will manage the rate limit for you.

If you don't want to see progress bars while the script runs, you can run it with the `quiet` option set to `True`:

```python
herd = TwitterSheep(username="kallewesterling", quiet=True)
```

### Step 4

Save the wordcloud made from all of your followers

```python
herd.save_wordcloud()
```

Used with no settings, the script will save a 1500x1000 pixel PNG file based on the top 1000 words in the bios from your followers and your friends (the people you follow) to `wordcloud.png` in the directory where you places `twittersheep.py`.

If you want to show words from bios of only your followers (the original intent of TwitterSheep.com), then use the setting `only_followers` set to `True`:

```python
herd.save_wordcloud(only_followers=True)
```

## Customizations

### Saving to a Specific File

Sometimes you may want to save your wordcloud to a specific place. You can do so by adding the option `path` and provide a valid path to the `save_wordcloud()` method:

```python
herd.save_wordcloud(path="../Desktop/my_real_unique_wordcloud.png")
```

Make sure that the path that you're adding the file to exists and that the file ending is `.png` as you will be saving a PNG file.


### Adding Stopwords

If you want to add stopwords to remove certain words from your wordcloud—say, for instance, if you already knew that some keywords would occur but you wanted to make clearer which ones were unexpected.

In the following example, I have chosen to remove a few keywords that I already knew would occur frequently in my follower's bios: theatre, digital, digital humanities, cuny, phd, candidate, phd student, student, and new york. I do so by adding the option `extend_stopwords` to the function and providing it with a list of the words:

```python
herd.save_wordcloud(only_followers=True, extend_stopwords=['theatre', 'digital', 'digital humanities', 'cuny', 'phd', 'candidate', 'phd student', 'student', 'new york'])
```

The result can be seen in the following two wordclouds:

No added stopwords             |  After adding stopwords
:-------------------------:|:-------------------------:
![](images/my_wordcloud.png)  |  ![](images/my_wordcloud_after_filtering.png)


### Getting All The Bios

If you want to see a list of all the bios in your herd, you can do so by accessing the list variables: `herd.friend_bios` and `herd.follower_bios`.

If you want to see all of the bios, you can access them through the list variable `herd.bios`.
