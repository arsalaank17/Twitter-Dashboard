from Classes import *

def createList(file, c, list):
    """
    Function that populates a list of a countable class from the specified file

    Keyword arguments:
    file -- the file that is used for extracting data
    c -- the countable class of which the data is
    list -- the list where all the data should be stored
    """

    #open the players_list.txt file for read
    f = open(file, "r", encoding="utf8")

    #read the lines and store them in fileContents
    fileContents = f.readlines()

    #go through all the names in the file, create a new Player class instance and
    #store it in the playersList
    for name in fileContents:
        list.append(c(name))

    #return noting, maybe reduntant return
    return 0

def checkOccurrence(li, mostp, tweetText):
    '''
    Function that goes through a list and checks if their countable.name is in the
    tweet text

    Keword arguments:
    li -- the list whcih is iterated
    mostp -- most popular or highest value that should be replaced
    tweetText- the text that is checked for containing the name
    '''
    
    #declares a list of forbidden words that can be contained in players
    #names or country names and can give wrong statistics
    forbiddenWords = ['de', 'si', 'di', 'ha', 'ki', 'per', 'and']

    #go through all players from list
    for p in li:
        #go through all the names of a player
        namesList = p.name.split()
 
        for i in namesList:
            #check if it's in the tweettext
            if str(i).lower() in tweetText.lower() and str(i).lower() not in forbiddenWords:
                #increase the number of Occurrences of the player
                p.addOccurrence()

                #checks if the current player has more Occurrences than the current most popular player
                if p.occurrences > mostp.occurrences:
                    mostp = p

                #break, not checking more than one name,
                break

    #return the most occurred elment
    return mostp


def checkNameOccurance(name, list):
    '''
    Function that checks if the countable element exists
    in the list and returns it's index, -1 otherwise

    Keyword arguments:
    name -- the name of the word that should be searched
    list -- the list in which the word is searched
    '''

    #goes through the whole list 
    for i in range(len(list)):
        #checks if the elemnt from the list is equal to the name
        if list[i].name == name:
            #if the list elemnts's name is equal to the name, return the index
            return i

    #if no element found return -1
    return -1


def readFiltreFile():
    '''
    Function that read the file filtru.txt in which the current url is stored
    and returns the needed information for the search form
    '''
    
    f = open("text_files/filtru.txt", "r")

    try:
        text = (f.read().split("&"))
        searched_word = text[0].split("=",1)[1]
        timee = text[1].split("=",1)[1]

    except:
        timee = 0.3
        searched_word = ""
        pass

    try:
        float(timee)
    except:
        timee = 0.3

    return float(timee), searched_word

def isEmitable(searched_word, e):
    '''
    Function that checks if a tweet should appear in the list or not, based on
    the search requirements the user provided
    '''

    if searched_word == '':
        return True
    try:
        if searched_word == "" and e.data["lang"] == "en":
            return True

        if (searched_word != "" and e.data["lang"] == "en"):
            try:
                if searched_word.lower() in e.data["text"].lower():
                    return True
            except:
                pass
    except:
        pass

    return False


def getOccurrences(countable):
    '''
    Return the number of occurrences of countable class
    '''
    return countable.occurrences

def checkWord(word, l):
    '''
    Function that checks if there is a character in l that occurs
    in word, returns false if so

    Keyword arguments:
    word -- the word in which the charcters are searched
    l -- the list of characters which should be searched
    '''

    for character in l:
        if character in word or len(word) < 6:
            return False
    return True