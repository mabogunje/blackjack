'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Defines the classes necessary for a deck of whitejack cards
'''

from random import choice;


class Card:
    '''
    A Whitejack Card
    '''

    (ONE, TWO, THREE,FOUR) = range(1,5);


class Deck:
    '''
    A Whitejack  Deck of Cards
    '''

    SIZE = float("inf");
    CARDS = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR];

    def __init__(self):
        '''
        Do nothing
        '''
        pass;

    def draw(self, num=1):
        return [choice(Deck.CARDS) for i in range(num)]; 

    def __repr__(self):
        return self.SIZE;

    def __str__(self):
        return str(self.SIZE);

