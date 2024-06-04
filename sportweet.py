from eca import *
from eca.generators import start_offline_tweets
root_content_path = 'sportweet_static'
import datetime
import textwrap

#counter = [soccer,basketball,football,rugby] for graphs
Counter = [0,0,0,0]

@event('init')
def setup(ctx, e):
    # start the offline tweet stream
    start_offline_tweets('sports.txt', 'classify', time_factor=2)

@event('classify')
def classify(ctx,e):
    # we receive a tweet
    tweet = e.data

    # parse date
    time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

    # nicify text
    text = textwrap.fill(tweet['text'],initial_indent='    ', subsequent_indent='    ')
    text = text.lower()
    # classify the tweet as one sport or other
    # 4 most relevant sports as seperate tweet streams
    if "soccer" in text:
        Counter[0] = Counter[0] + 1
        emit('soccer',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('soccer',1)
        })
        fire('soccer',e.data)    
    elif "basketball" in text:
        Counter[1] = Counter[1] + 1
        emit('basketball',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('basketball',1)
        })
        fire
    elif "football" in text:
        Counter[2] = Counter[2] + 1
        emit('football',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('football',1)
        })
        fire('football',e.data)
    elif "rugby" in text:
        Counter[3] = Counter[3] + 1
        emit('rugby',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('rugby',1)
        })
        fire('rugby',e.data)
    # other sports printed to other and wordcloud
    elif "volleyball" in text:
        emit('other',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('volleyball',1)
        })
    elif "baseball" in text:
        emit('other',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('baseball',1)
        })
    elif "tennis" in text:
        emit('other',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('tennis',1)
        })
    elif "cricket" in text:
        emit('other',e.data)
        emit('wordcloud', {
            'action': 'add',
            'value': ('cricket',1)
        })
    # tweets that can't be classified get printed to other
    else:
        emit('other',e.data)
    # create event that prints to all sports graphs
    fire('trending',e.data)

@event('trending')
def trending(ctx,e):
    output0 = Counter[0]
    output1 = Counter[1]
    output2 = Counter[2]
    output3 = Counter[3]
    
    emit('trending_soccer',{
        'action': 'add',
        'value': output0
        })
    emit('trending_basketball',{
        'action': 'add',
        'value': output1
        })
    emit('trending_football',{
        'action': 'add',
        'value': output2
        })
    emit('trending_rugby',{
        'action': 'add',
        'value': output3
        })
    
