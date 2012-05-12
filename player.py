'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Preschool Poker Player Bots
'''

from deck import Card, Hand;


class Player:
    '''
    Base class for a player bot
    '''

    def __init__(self):
        self.cards = [];

    def draw(self, num, deck):
        self.cards.extend(deck.draw(num));

    def discard(self, card):
        self.cards.remove(card);

    def hand(self):
        if len(self.cards) == len(set(self.cards)):
            return sum(self.cards);
        else:
            pairs = [self.cards[i] for i,v in enumerate(self.cards) if self.cards.count(v) > 1];

            if Card.THREE in pairs:
                return Hand.THREE_PAIR;

            if Card.TWO in pairs:
                return Hand.TWO_PAIR;

            if Card.ONE in pairs:
                return Hand.ONE_PAIR;


