'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Defines the classes necessary for a deck of cards
'''

from random import choice;


class Card:
    '''
    A face card
    Note: The value of 11.5 assigned to ACE should be kept unless you know what you are doing
    math.floor and math.ceil are used elsewhere on it for other purposes
    '''

    (ONE, TWO, THREE, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, KING, QUEEN, JACK, ACE) = [1,2,3,4,5,6,7,8,9,10,10,10,11.5];


class Deck(object):
    '''
    A Whitejack deck of cards
    '''

    SIZE = float("inf");
    CARDS = [Card.ONE, Card.TWO, Card.THREE, Card.FOUR];

    def __init__(self):
        self.cards = Deck.CARDS;
        self.size = Deck.SIZE;

    def draw(self, num=1):
        return [choice(self.cards) for i in range(num)]; 

    def __repr__(self):
        return self.size;

    def __str__(self):
        return str(self.size);


class FullDeck(Deck):
    '''
    A full deck of cards
    '''

    CARDS = [Card.TWO, Card.THREE, Card.FOUR, Card.FIVE, Card.SIX, Card.SEVEN, Card.EIGHT, Card.NINE, Card.KING, Card.QUEEN, Card.JACK, Card.ACE];

    def __init__(self):
        self.cards = dict.fromkeys(FullDeck.CARDS, 4);
        self.size = sum(self.cards.values());

    def draw(self, num=1):
        cards_left = [c for c in self.cards.keys() if self.cards[c] > 0];
        chosen = [choice(cards_left) for i in range(num)]; 
        
        ''' Uncommenting this, gives a finite 52 card deck
        for card in chosen:
            self.cards[c] = self.cards[card] - 1;
        '''

        return chosen; 

    def __repr__(self):
        return self.cards;

    def __str__(self):
        return str(self.cards);

