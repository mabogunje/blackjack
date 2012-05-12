'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Defines the classes necessary for a deck of preschool poker cards
'''

from random import shuffle;


class Card:
    '''
    A Preschool Poker Card
    '''

    (ONE, TWO, THREE) = range(1,4);


class Hand:
    '''
    Preschool Poker Hand Rankings
    '''

    (ONE_PAIR, TWO_PAIR, THREE_PAIR) = range(6,9);


class Deck:
    '''
    A Preschool Poker Deck of Cards
    '''

    SIZE = 9;
    CARDS = [Card.ONE, Card.TWO, Card.THREE];

    def __init__(self):
        self.cards = [];

        for card in Deck.CARDS:
            self.cards.extend([card] * 3);

        shuffle(self.cards);

    def shuffle(self):
        shuffle(self.cards);

    def draw(self, num=1):
        return [self.cards.pop() for i in range(num)]; 

    def __repr__(self):
        return self.cards;

    def __str__(self):
        return str(self.cards);

