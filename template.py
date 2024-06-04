from os import truncate
from eca import *
from eca.generators import start_offline_tweets
import  nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from Classes.player import Player
from Classes.team import Team
from Classes.country import Country
from Classes.word import Word
from utilities import *

import time

#create the variable to store all players
playersList = []

#create the variable to store all the teams
teamsList = []

#create the variable to store all the countries
countriesList = []

#create the variable to store all words
wordsList = []

#create the variable to store the most popular player
mostPopularPlayer = Player("Rosca Maxim")

#create the variable to store the most popular team
mostPopularTeam = Team("Republic of Moldova")

#create the variable to store the most active country
mostPopularCountry = Country("Republic Of Moldova")

sia = 0

# function that reports the amount of words in the current tweet to a chart on the dashboard
def tweet_chart(ctx, e):
    try:
        tweetLen = len(e.get('text').split());
        emit('word_counter', {
            'action': 'add',
            'value': tweetLen
        })
    except:
        pass

# function selects and adds the most retweeted tweets to the top tweet list
def top_tweet(ctx, e):
    try :
        # checks whether the current tweet is a retweet whose id isn't in the retweetId_list
        if e.get('retweeted_status') is not None and not e.get('retweeted_status').get('id') in ctx.retweetId_list: # and time.mktime(time.strptime(e.get('retweeted_status').get('created_at'), '%a %b %d %X %z %Y')) >= 1405267200.0:
            # if the original retweet has the most retweets then it will be added to the dashboard list and its id will be added to the id list in the context
            if e.get('retweeted_status').get('retweet_count') >= ctx.most_retweets:
                ctx.most_retweets = e.get('retweeted_status').get('retweet_count');
                ctx.retweetId_list.append(e.get('retweeted_status').get('id'));
                emit('top_tweets', e.get('retweeted_status'));
        # checks whether this tweet is original and if its id isn't in the retweetId_list
        elif e.get('retweet_count') > 0 and e.get('retweeted_status') is None and not e.get('id') in ctx.retweetId_list:
            # if this tweet has the most retweets then it will be added to the dashboard list and its id will pe added to the id list in the context
            if e.get('retweet_count') >= ctx.most_retweets:
                ctx.most_retweets = e.get('retweet_count');
                ctx.retweetId_list.append(e.get('id'));
                emit('top_tweets', e);
                
        emit('top_count', {'text': str(ctx.most_retweets)});
    except:
        pass

def processCountry(location):
    '''
    Function that checks if the location is most popular from a list

    Keyword arguments:
    location -- the location from which the tweet was sent
    '''

    #declare the global variable that is used
    global mostPopularCountry

    #get the country index from the list
    countryIndex = checkNameOccurance(location['country'], countriesList)

    #if the country doesnt exist append it to the list
    if countryIndex == -1:
        countriesList.append(Country(location["country"]))

    #increase the occurrence of the country
    countriesList[countryIndex].addOccurrence()

    #check if the country is the most popular
    if countriesList[countryIndex].occurrences > mostPopularCountry.occurrences:
        mostPopularCountry = countriesList[countryIndex]

def processWord(word):
    forbiddenCharacters = [',', "|", "(c)", "http"]

    if checkWord(word, forbiddenCharacters):
        wordIndex = checkNameOccurance(word, wordsList)

        if wordIndex == -1:
            wordsList.append(Word(word))
        
        wordsList[wordIndex].addOccurrence()

@event('init')
def setup(ctx, e):
    """
    The initial function, called when the 'init' event is pushed

    Keyword arguments:
    ctx -- the context of the app
    e -- the event information
    """
    global sia
    
    ctx.most_retweets = 0
    ctx.lastSearched_Word = ""
    ctx.lastTweetDelay = 0.3
    ctx.retweetId_list = []

    nltk.download('vader_lexicon')

    sia = SentimentIntensityAnalyzer()

    #declare the tweets_count to 0
    ctx.tweets_count = 0

    #populate the list with all the players
    createList('text_files/players_list.txt', Player, playersList)

    #populate the list with all teams
    createList('text_files/countrys_list.txt', Team, teamsList)
    
    #starts reading the tweets from the file and pushes the event 'tweet'
    start_offline_tweets('text_files/worldcupfinal_2014.txt', time_factor=1000, event_name='tweet')


@event('tweet')
def processTweet(ctx, e):
    '''
    Function that processes the tweet and updates the dashboard 
    based on that processing

    Keyword arguments:
    ctx -- the context of the app
    e -- the event information
    '''

    #declare the global variables used in the function
    global mostPopularPlayer
    global mostPopularTeam
    global mostPopularCountry



    try:
        ctx.lastTweetDelay = ctx.tweetDelay;
        ctx.lastSearched_Word = ctx.searched_word;
    except:
        pass
    
    ctx.tweetDelay, ctx.searched_word = readFiltreFile()
    
    if (ctx.tweetDelay != ctx.lastTweetDelay or ctx.searched_word != ctx.lastSearched_Word):
        ctx.most_retweets = 0;

    emitable = isEmitable(ctx.searched_word, e)

    if emitable:
        #store the tweet text in a separate variable, check for null error
        try:
            tweetText = e.data['text']
        except:
            tweetText = ''

        positivity = sia.polarity_scores(tweetText)
    
        top_tweet(ctx, e);
        tweet_chart(ctx, e);

        emit('polarity_table', {'action': 'set', 'series': 'negative', 'value': [0, positivity['neg']]})
        emit('polarity_table', {'action': 'set', 'series': 'neutral', 'value': [1, positivity['neu']]})
        emit('polarity_table', {'action': 'set', 'series': 'positive', 'value': [2, positivity['pos']]})
        
        try:
            for i in e.data['entities']['media']:    
                emit("image", {"src": i["media_url"]})
            
        except:
            pass
        #check for NoneType error
        try:
            #get the location of the tweet
            tweetLocation = e.data['place']

            #call the process function that determines if the location is the most popular
            processCountry(tweetLocation)
        except:
            pass
        
        #check for Occurrence of all players in the tweet text
        mostPopularPlayer = checkOccurrence(playersList, mostPopularPlayer, tweetText)

        #check the Occurrence of all teams in the tweet text, including their
        mostPopularTeam = checkOccurrence(teamsList, mostPopularTeam, tweetText)

        #make the delay for tweets
        time.sleep(ctx.tweetDelay)
        
        #increase the number of tweets count
        ctx.tweets_count += 1

        #sends data to the tweets_list from the html file
        emit('tweets_list', e.data)

        #sends data to the tweets_count from the html file
        emit('tweets_count', {'text': str(ctx.tweets_count)})

        #sends data to the most_popular_player from the html file
        emit('most_popular_player', {'text': mostPopularPlayer.name})

        #sends data to the most_popular_team from the html file
        emit('most_popular_team', {'text': mostPopularTeam.name.split()[0]})

        #sends the data to the most_popular_country from the html file
        emit('most_popular_country', {'text': mostPopularCountry.name})
        # emit('image', {"src": "https://cdn.discordapp.com/attachments/745233662861377596/905142603912183879/Screenshot_from_2021-11-02_18-13-08.png"})

        forbiddenCharacters = [',', "|", "(c)"]

        for word in tweetText.split():
            if checkWord(word, forbiddenCharacters):
                processWord(word)

        wordsList.sort(key=getOccurrences, reverse=True)

        wordRange = len(wordsList) if len(wordsList) < 15 else 15

        for i in range(wordRange):
            emit('word_cloud', {
                'action': 'add',
                'value': [wordsList[i].name, wordsList[i].name]
            })

    #calls the function again
    fire('tweet', delay=0.05)

