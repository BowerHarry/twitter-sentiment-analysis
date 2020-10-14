###This file is a working progress of trying to make the analysis more accurate

##Importing external modules

from tweepy import OAuthHandler, Stream, StreamListener
import csv
import nltk

####### Setting up the sentiment analyser #######

##Open the spreadsheet for reading

tweets_trump = open("tweets_trump.csv", "rb")

##Initialising all the lists and dictionaries that will be used

pos_tweets = {}
neg_tweets = {}
big_list = []
all_tweets = []

##Big_list contains every tweet that is in the spreadsheet

for line in tweets_trump:
    big_list.append(line) 

##Cleansing the tweet of bad characters

for tweet in big_list:

    tweet = tweet.replace(",", " ")
    tweet = tweet.replace("\r\n", "")
    tweet = tweet.replace("  ", "")
    words = tweet
    
    try:

##If tweet has "negative" at the end add it to the dictionary of negative tweets and remove the "negative"
##In the format [("tweet"), negative]

        if words.rsplit(None, 1)[-1] == "negative":
            tweet = tweet.replace("negative", "")
            neg_tweets[tweet] = "negative"
        
##If tweet has "positive" at the end add it to the dictionary of positive tweets and remove the "positive"
##In the format [("tweet"), positive]

        elif words.rsplit(None, 1)[-1] == "positive":
            tweet = tweet.replace("positive", "")
            pos_tweets[tweet] = "positive"
            

        else:
            pass

##Was always producing an IndexError after the last tweet

    except IndexError:
        pass

##Merging the two dictionaries into a single list 
##In the format (["I", "hate", "you"], "negative")

for (string, sentiment) in pos_tweets.items() + neg_tweets.items():
    one_tweet=[]
    for word in string.split():
        one_tweet.append(word)
    #no_short_words = [e.lower() for e in words.split() if len(e) >= 3]
    all_tweets.append((one_tweet, sentiment))

##This function produces list of all the words in the tweets (including duplicates)

def get_all_words(all_tweets):
    all_words = []
    for (string, _ ) in all_tweets:
        all_words.extend(string)
    return all_words


def get_word_features(word_list):
    word_list = nltk.FreqDist(word_list)
    word_features = word_list.keys()
    return word_features

word_features = get_word_features(get_all_words(all_tweets))

##Set() gets rid of duplicate elements
##Not 100% sure what this actually does

def extract_features(document):
    setOfDocument = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in setOfDocument)
    return features

training_set = nltk.classify.apply_features(extract_features, all_tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)

####### Setting up the twitter stream #######

##Keys used to connect to Twitter

c_key = "3cxMzzO3SWCzB1hucia32cYih"
c_secret = "Gk385f2mh7bWWdQPS6NLy3m4sK3hw9U6HrQhOLRnOWOfcQXFjF"
a_token = "1008713854887579648-0WabjK5ZztKpXusyh4pXVwlmDLESjF"
a_secret = "KcvivXHmKIyS7rIbOXAAE2kAgh4PARnUsTFwqpHUQNw38"

##Starting the stream

class listener(StreamListener):

    def on_status(self, status):
        try:
            tweet = str(status.text)

##Splits the tweet into a list of words

            tweet = tweet.split(" ")

##Cleansing the tweet of bad characters

            n = 0
            for word in tweet:
                if word.startswith("@") or word.startswith("https") or word.startswith("#"):
			        tweet.pop(n)
            else:
                n+=1

            print(tweet)

##Analyse the tweet
            tweet = str(tweet)
            print (classifier.classify(extract_features(tweet.split())))
            print("~~~~")

##Continues the stream

            return True

        except UnicodeEncodeError:
			pass

    def on_error(self, status):
        print(status)

##Sets up the Twitter stream

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener(), tweet_mode='extended')
twitterStream.filter(track=["trump"])