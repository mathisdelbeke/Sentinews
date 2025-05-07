import _pickle as cPickle
import twitter_scanner as twitter_scanner

class Updater:
    def __init__(self):
        #self.tweets = self.read_tweets()
        self.tweets = [""]

        self.sentiments = self.predict_sentiments()
        self.write_sentiments()

    def read_tweets(self):
        tweet_reader = twitter_scanner.TweetReader()
        tweets = tweet_reader.get_tweets()
        return tweets

    def predict_sentiments(self):
        model = self.deserialize_model()
        sentiments = model.predict(self.tweets)
        return sentiments

    def deserialize_model(self):
        with (open("Resources/tfidf_model.pk", "rb")) as openfile:
            model = cPickle.load(openfile)
            return model

    def write_sentiments(self):
        file = None
        tweets_and_sentiments = list(zip(self.tweets, self.sentiments))
        for tweet in tweets_and_sentiments:
            if tweet[1] == 'positive':
                file = open('Resources/positive_tweets.txt', 'a')
            elif tweet[1] == 'neutral':
                file = open('Resources/neutral_tweets.txt', 'a')
            else:
                file = open('Resources/negative_tweets.txt', 'a')
            file.write(tweet[0]+"\n")
            file.close()

test = Updater()
