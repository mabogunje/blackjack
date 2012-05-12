'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Preschool Poker Player Bots
'''

from random import choice;
from deck import Card, Hand;

class Action:
    '''
    Possible Player Moves
    '''

    (STAND, DRAW, DISCARD) = range(0, 3);

class Player:
    '''
    Base class for a player bot
    '''

    def __init__(self, name):
        self.name = name;
        self.cards = [];

    def draw(self, num, deck):
        '''
        Draw a card from the deck
        '''

        self.cards.extend(deck.draw(num));

    def discard(self, card, deck):
        '''
        Discards card from hand and draws a new card from the deck 
        '''
        self.cards.remove(card);
        self.draw(1, deck);

    def stand(self):
        '''
        Do Nothing
        '''

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
    
    def play(self, deck):
        raise NotImplementedError('You must implement this method');


class DumbPlayer(Player):
    '''
    DumbPlayer always chooses a random action
    '''

    def play(self, deck):
        moves = [Action.STAND, Action.DRAW, Action.DISCARD];
        action = choice(moves);

        if action == Action.STAND:
            self.stand();

        if action == Action.DRAW:
            self.draw(1, deck);

        if action == Action.DISCARD:
            self.discard(choice(self.cards), deck);


class OddPlayer(Player):
    '''
    OddPlayer always discards the lowest-valued odd-numbered
    '''

    def play(self, deck):
        odd_cards = filter(lambda card: bool(card & 1), self.cards);

        if odd_cards:
            self.discard(min(odd_cards), deck); 

class SmartPlayer(Player):
    '''
    SmartPlayer will (1) never discard a pair; (2) always discard a 1, or (3) stand.
    '''

    def play(self, deck):
        pairs = [Hand.ONE_PAIR, Hand.TWO_PAIR, Hand.THREE_PAIR];
        hand = self.hand();

        if hand not in pairs:
            if Card.ONE in self.cards:
                self.discard(Card.ONE, deck);
        else:
            self.stand();


class Learner(Player):
    '''
    Learner progressively learns how to play via its matches (Reinforcement Learning)
    '''

    def __init__(self, name="PlayerBot"):
        super(Learner, self).__init__(name);
        self.weights = dict();
        self.mapping = dict();

