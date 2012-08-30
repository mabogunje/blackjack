'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Whitejack Player Bots
'''

from random import choice;
from deck import Card;

class Action(object):
    '''
    Possible Player Moves
    '''

    (STAND, DRAW) = range(0, 2);

    @staticmethod
    def describe(move):
        descriptions = { None: "Stand",
                         Action.STAND: "Stand",
                         Action.DRAW: "Request a Hit"
                       };

        return descriptions[move];

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
        
        return Action.DRAW;

    def get_moves(self):
        return [Action.STAND, Action.DRAW];

    def stand(self):
        '''
        Do Nothing
        '''
        return Action.STAND;

    def hand(self):
        value = sum(self.cards); 
        
        if value >= 5: 
            value = 5;

        return value;

    def play(self, deck):
        raise NotImplementedError('You must implement this method');

    def __hash__(self):
        return hash(self.name);


class Dealer(Player):
    '''
    The Dealer is required to hit if the value of his hand is less than 4
    Otherwise, he must stand
    '''

    def __init__(self, name="Dealer"):
        super(Dealer, self).__init__(name);

    def play(self, deck):

        if self.hand() < 4:
            return self.draw(1, deck);

        return self.stand();


class DumbPlayer(Player):
    '''
    DumbPlayer always chooses a random action
    '''

    def play(self, deck):
        moves = [Action.STAND, Action.DISCARD_ONE, Action.DISCARD_TWO, Action.DISCARD_THREE];
        action = choice(moves);

        if action == Action.STAND:
            return self.stand();

        if Action.is_discard(action):
            return self.discard(choice(self.cards), deck);


class Learner(Dealer):
    '''
    Learner plays just like Dealer, but learns from its matches (Reinforcement Learning)
    '''

    def __init__(self, name="Computer", rate=0.5):
        super(Learner, self).__init__(name);
        self.learning_rate = rate;

        self.states = [ float('-inf'),  # START
                        1,              # STATE 1
                        2,              # STATE 2
                        3,              # STATE 3
                        4,              # STATE 4
                        5,              # BUST
                      ];

        # All states are initially assigned an equal weight
        self.weights = dict.fromkeys(tuple(self.states), 0.5);

    def play(self, deck):
        '''
        Find accessible states and sort by probability of winning
        - An accessible state will have a value greater or equal
          to the current state, and less than BUST 
        '''
        is_accessible = lambda state: (state > self.hand()) & (state < 5);
        new_states = filter(is_accessible, self.states);
        probabilities = [p for p in self.weights.items() if p[0] in new_states]; 
        probabilities = sorted(probabilities, key=lambda p: p[1]);

        '''
        If there are any better accessible states, try to reach 
        the state with the best chance of winning.
        '''
        if probabilities:
            desired_state = probabilities[-1];

            if desired_state[1] > self.weights[self.hand()]:
                return self.draw(1, deck);
            else:
                return self.stand();
        else:
            return super(Learner, self).play(deck);

    def learn(self, state, result):
        '''
        Given a state and its win/loss result, update its weight reinforcing towards the result
        '''
        self.weights[state] = self.weights[state] + (self.learning_rate * (result - self.weights[state]));

