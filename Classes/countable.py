class Countable:
    '''
    A simple class that has two attributes used for combining the name 
    and the number of occurrences

    Attributes:
    name -- the name of the object
    occurrences -- the number of occurences

    Methods:
    addOccurence -- increase the number of occurences by one
    '''

    def __init__(self, name):
        '''
        Initialization function, sets the name to the speciefied name
        and occurences to 0
        '''
        self.name = name
        self.occurrences = 0
    
    def addOccurrence(self):
        """
        Increase the number of occurences by one
        """
        self.occurrences  += 1