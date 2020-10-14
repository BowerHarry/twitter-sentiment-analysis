###This file is a working progress of trying to make the analysis more accurate

##Importing external modules

from tweepy import OAuthHandler, Stream, StreamListener
import csv, nltk, string, re

file = "tweets_trump.csv"
min_word_size = 3
training_count = 10

####### Setting up the sentiment analyser #######

##Open the spreadsheet for reading

tweets_trump = open(file, "rb")

##Initialising all the lists and dictionaries that will be used

pos_tweets = {}
neg_tweets = {}
neutral_tweets = {}
big_list = []
all_tweets = []

# when reading the data and when receiving tweets
def clean_word(word):
    word = word.lower()
    if word.startswith("@") or word.startswith("http") or word.startswith("#"):
        return ""
    return re.sub(r'[^\w\s]','',word)

def clean_tweet(tweet):
    tweet = tweet.replace(",", " ")
    tweet = tweet.replace("\r\n", "")
    tweet = tweet.strip() 
    cleaned = []
    for word in tweet.split():
        cleanword = clean_word(word)
        if len(cleanword)>min_word_size:
            cleaned.append(cleanword)
    return ' '.join(cleaned)

##Big_list contains every tweet that is in the spreadsheet

for line in tweets_trump:
    big_list.append(line) 

##Cleansing the tweet of bad characters

for tweet in big_list:
    words = clean_tweet(tweet)
    
#Only process non-blank lines - get's rid of index error

    if len(words) > 0:

##If tweet has "negative" at the end add it to the dictionary of negative tweets and remove the "negative"
##In the format [("tweet"), negative]

        if words.rsplit(None, 1)[-1] == "negative":
            words = words.replace("negative", "")
            neg_tweets[words] = "negative"
        
##If tweet has "positive" at the end add it to the dictionary of positive tweets and remove the "positive"
##In the format [("tweet"), positive]

        elif words.rsplit(None, 1)[-1] == "positive":
            words = words.replace("positive", "")
            pos_tweets[words] = "positive"

##If tweet has "neutral" at the end add it to the dictionary of positive tweets and remove the "neutral"
##In the format [("tweet"), neutral]

        elif words.rsplit(None, 1)[-1] == "neutral":
            words = words.replace("neutral", "")
            neutral_tweets[words] = "neutral"     

        else:
            pass

####### Outputting useful info #######
pos= float(len(pos_tweets))
neg= float(len(neg_tweets))
neu=float(len(neutral_tweets))
perc_pos=int((pos/(pos+neg+neu))*100)
perc_neg=int((neg/(pos+neg+neu))*100)
perc_neu=int((neu/(pos+neg+neu))*100)
print ("~~~~~Training set info~~~~~")
print ("\nPositive tweets count=" + str(pos))
print ("Percentage of tweets that are positive:" + str(perc_pos))
print ("\nNegative tweets count=" + str(len(neg_tweets)))
print ("Percentage of tweets that are negative:" + str(perc_neg))
print ("\nNeutral tweets count=" + str(len(neutral_tweets)))
print ("Percentage of tweets that are neutral:" + str(perc_neu))

##Merging the two dictionaries into a single list 
##In the format (["I", "hate", "you"], "negative")

for (string, sentiment) in pos_tweets.items() + neg_tweets.items() + neutral_tweets.items():
    one_tweet=[]
    for word in string.split():
        one_tweet.append(word)
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
    for word in setOfDocument:
        features['contains(%s)' % word] = True
    return features

training_set = nltk.classify.apply_features(extract_features, all_tweets)
classifier = nltk.NaiveBayesClassifier.train(training_set)
for i in range(training_count):
    classifier.train(training_set)

####### Test training set ######
#print(nltk.classify.accuracy(classifier, training_set))

####### Test tweets #######

#tweet = "i love trump".lower().split()
#tweet_features = extract_features(tweet)
#print (classifier.classify(tweet_features))

#tweet = "i hate trump".lower().split()
#tweet_features = extract_features(tweet)
#print (classifier.classify(tweet_features))

#classifier.show_most_informative_features()

####### Setting up the twitter stream #######


##Keys used to connect to Twitter

c_key = "3cxMzzO3SWCzB1hucia32cYih"
c_secret = "Gk385f2mh7bWWdQPS6NLy3m4sK3hw9U6HrQhOLRnOWOfcQXFjF"
a_token = "1008713854887579648-0WabjK5ZztKpXusyh4pXVwlmDLESjF"
a_secret = "KcvivXHmKIyS7rIbOXAAE2kAgh4PARnUsTFwqpHUQNw38"

n_positive=float(0)
n_negative=float(0)
n_neutral=float(0)

##Starting the stream

class listener(StreamListener):

    def on_status(self, status):
        try:
            ##Convert tweet from unicode
            tweet = status.text.encode('ascii', 'ignore')
            print(tweet)

            ##Cleansing the tweet of bad characters
            tweet = clean_tweet(tweet)
            print(tweet)

            ##Splits the tweet into a list of words
            tweet = tweet.split(" ")

            ##Analyse the tweet
            print (classifier.classify(extract_features(tweet)))
            sentiment = str(classifier.classify(extract_features(tweet)))

            global n_positive
            global n_neutral
            global n_negative

            if sentiment == "positive":
                n_positive+=1
            elif sentiment == "neutral":
                n_neutral+=1
            elif sentiment == "negative":
                n_negative+=1
            else:
                pass

            n_total=n_positive+n_negative+n_neutral
            perc_pos=int((n_positive/(n_total))*100)
            perc_neg=int((n_negative/(n_total))*100)
            perc_neu=int((n_neutral/(n_total))*100)
            print ("Percentage of tweets that are positive:" + str(perc_pos))
            print ("Percentage of tweets that are negative:" + str(perc_neg))
            print ("Percentage of tweets that are neutral:" + str(perc_neu))
            print ("Total tweets:" + str(n_total))

            print("----")

        except IOError:
            pass

        ##Continues the stream

        return True

    def on_error(self, status):
        print(status)

##Sets up the Twitter stream

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["trump"])