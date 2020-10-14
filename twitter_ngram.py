###This program takes word pairings, evaluates the sentiment of each pairing and takes and average over the ###tweet

##Importing external modules
from tweepy import OAuthHandler, Stream, StreamListener
import json
import re
from textblob import TextBlob


##List with all streamed tweets in

tweet_data = []

##Keys used to connect to Twitter

c_key = "3cxMzzO3SWCzB1hucia32cYih"
c_secret = "Gk385f2mh7bWWdQPS6NLy3m4sK3hw9U6HrQhOLRnOWOfcQXFjF"
a_token = "1008713854887579648-0WabjK5ZztKpXusyh4pXVwlmDLESjF"
a_secret = "KcvivXHmKIyS7rIbOXAAE2kAgh4PARnUsTFwqpHUQNw38"

##Defining what will be global variable

n_tweets = 0
n_neg_tweets = 0
n_pos_tweets = 0
n_calc_tweets = 0
tweet_sentiment = 0


class listener(StreamListener):

	def on_data(self, data):
		try:

			##Encode and then decode to get rid of characters python can't process

			encoded_data = json.loads(data)["text"].encode("windows-1250")
			decoded_data = encoded_data.decode("windows-1250")

			##Removes all non alphabetic characters (except spaces)

			decoded_data = re.sub(r"[^\s\w]|_+", "", decoded_data)

			##Removes all words with less than 3 characters (not important)

			decoded_data = " ".join([w for w in decoded_data.split() if len(w) > 3])
			tweet_data.append(decoded_data)

			print("\nTWEET: " + str(decoded_data))

			##Accessing global variables

			global n_tweets
			global n_neg_tweets
			global n_pos_tweets
			global n_calc_tweets
			global tweet_sentiment

			##Sentiment analysis of the tweet

			ngram_str = " "
			blob = TextBlob(decoded_data)
			tweet_total_polarity = 0
			tweet_average_polarity = 0
			n_ngram = 0

			for ngram in blob.ngrams(2):
				ngram_str = TextBlob(str(ngram))
				n_ngram += 1
				tweet_total_polarity = tweet_total_polarity + ngram_str.sentiment.polarity

			if n_ngram != 0:
				tweet_average_polarity = tweet_total_polarity / n_ngram
				tweet_sentiment = (round(tweet_average_polarity, 2))
				n_tweets += 1

				##Evaluating tweet sentiment

				if tweet_sentiment > 0:
					n_pos_tweets += 1
					n_calc_tweets += 1
				elif tweet_sentiment < 0:
					n_neg_tweets += 1
					n_calc_tweets += 1
				else:
					pass

			else:
				n_tweets += 1
				pass

			##Outputting results

			print("Total number of tweets = " + str(n_tweets))
			print("Total number of calculated tweets = " + str(n_calc_tweets))
			print("Total number of positive tweets = " + str(n_pos_tweets))
			print("Total number of negative tweets = " + str(n_neg_tweets))
			print(tweet_sentiment)

			##Continues the stream

			return True

##If the tweet can't be encoded it is skipped over			

		except (UnicodeError, KeyError) as e:
			pass

	def on_error(self, status):
		print(status)


##Setting up Twitter stream

auth = OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token, a_secret)
twitterStream = Stream(auth, listener(), tweet_mode='extended')
twitterStream.filter(track=["trump"])