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

    (STAND, DISCARD) = range(0, 2);

class Player(object):
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

        return (Action.DISCARD, card);

    def stand(self):
        '''
        Do Nothing
        '''
        return Action.STAND;

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

    def __hash__(self):
        return hash(self.name);

class DumbPlayer(Player):
    '''
    DumbPlayer always chooses a random action
    '''

    def play(self, deck):
        moves = [Action.STAND, Action.DISCARD];
        action = choice(moves);

        if action == Action.STAND:
            return self.stand();

        if action == Action.DISCARD:
            return self.discard(choice(self.cards), deck);


class OddPlayer(Player):
    '''
    OddPlayer always discards the lowest-valued odd-numbered
    '''

    def play(self, deck):
        odd_cards = filter(lambda card: bool(card & 1), self.cards);

        if odd_cards:
            return self.discard(min(odd_cards), deck); 

class SmartPlayer(Player):
    '''
    SmartPlayer will (1) never discard a pair; (2) always discard a 1, or (3) stand.
    '''

    def play(self, deck):
        pairs = [Hand.ONE_PAIR, Hand.TWO_PAIR, Hand.THREE_PAIR];
        hand = self.hand();

        if hand not in pairs:
            if Card.ONE in self.cards:
                return self.discard(Card.ONE, deck);
        else:
            return self.stand();


class Learner(Player):
    '''
    Learner learns how to play PreschoolPoker from its matches (Reinforcement Learning)
    '''

    def __init__(self, name="PlayerBot", rate=0.5):
        super(Learner, self).__init__(name);
        self.learning_rate = rate;
        self.weights = dict();
        self.mapping = dict();

    def play(self, deck):
        pass;

    def learn(self, policy, result):
        if not self.weights.values():
            self.mapping = policy;
            self.weights = dict.fromkeys(policy.items(), 0.5);
        else:
            old = set(policy.items()) & set(self.mapping.items()); # Visited States
            new = set(policy.items()) - old; # Unvisited States

            if old:
                for rule in old:
                    if result > self.weights[rule]:
                        self.weights[rule] = self.weights[rule]  + ((result - self.weights[rule]) * self.learning_rate);

            if new:
                for rule in new:
                    self.mapping[rule[0]] = rule[1];
                    self.weights[rule] = result;


