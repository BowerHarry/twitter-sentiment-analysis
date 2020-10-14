# twitter-sentiment-analysis
I created a program that streams live tweets using Twitter's API and uses several methods of sentiment analysis to make an educated prediction of a global sentiment towards a topic.
I attempted several different algorithms with varying degree of success.
- Original: 
  - Uses TextBlob on the tweet as a whole
- Ngram:
  - Takes word pairings and analyses the sentiment of each pairing, then takes an average over the tweet
- Word: 
  - Creates a training set from a list of already gathered tweets (and confirmed sentiments)
  - Uses a Naive Bayes algorithm 
  - Uses NLTK sentiment analysis on each word
- Naive Bayes:
  - Slightly better version of 'Word', including running the training set 100's of times
  Currently the programs are set to analyse tweets on Donald Trump and in tweets_csv tweets are recorded, waiting for me to classify them (this becomes the training set).
  
  
Update: NOW OUT OF DATE - these programs are NO LONGER WORKING, I think the new Twitter API is incompatible with the previous one.
