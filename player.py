'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Whitejack Player Bots
'''

from random import choice;
from fractions import Fraction;
from collections import namedtuple;

from deck import Card;

'''
A policy is a mapping of states to actions. 
As a namedtuple it works as a wrapper for any function. 
Allowing us to enforce type-checking for a function 
as a policy.

Every policy should be uniquely named and used as follows:

    DOUBLE_DOWN = POLICY(function(*args));
'''
POLICY = namedtuple('POLICY', 'eval');


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




class DumbPlayer(Player):
    '''
    DumbPlayer always requests a hit
    '''

    def play(self, deck):
        return self.draw(1, deck);


class Learner(DumbPlayer):
    '''
    Learner learns from its matches (Sampling)
    '''

    def __init__(self, name="Computer", rate=0.5):
        super(Learner, self).__init__(name);
        self.learning_rate = rate;

        self.states = [ 0,  # START
                        1,  # STATE 1
                        2,  # STATE 2
                        3,  # STATE 3
                        4,  # STATE 4
                        5,  # BUST
                      ];
        
        self.samples = dict.fromkeys(self.states, 0);

        '''
        Creates an m X m probability matrix of state transitions 
        with an additional 2 slots for the probability of loosing
        and winning in each state.

        The probability of winning is the very last value in each row.
        '''

        self.weights = dict((s, list([0]*(len(self.states)+1))) for s in self.states);

    def draw(self, num, deck):
        old = self.hand();
        action = super(Learner, self).draw(num, deck);
        
        self.learn(old, self.hand(), None);
        return action;
        

    def play(self, deck):
        '''
        Find accessible states and sort by probability of winning
        - An accessible state will have a value greater or equal
          to the current state, and less than BUST 
        '''
        is_accessible = lambda state: (state >= self.hand()) and (state < 5);
        new_states = filter(is_accessible, self.states);
        probabilities = [p for p in self.weights.items() if p[0] in new_states];

        probabilities = sorted(probabilities, key=lambda p: p[1][-1]); # Sort by probability of winning

        '''
        If there are any better accessible states, try to reach 
        the state with the best chance of winning.
        '''
        if probabilities:
            desired_state = probabilities[-1];

            if desired_state[1][-1] > self.weights[self.hand()][-1] and desired_state[0] > self.hand():
                action = self.draw(1, deck);
                self.learn(self.hand() - self.cards[-1], self.hand(), None);

                return action;
            else:
                return self.stand();
        else:
            return super(Learner, self).play(deck);

    def learn(self, old, curr, result):
        '''
        Given a previous state, state and its win/loss result, 
        increase the probability that the old state will result in the current state
        and that the current state may result in a win.
        '''

        # 1 is Whitejack.WIN
        if result == 1:
            self.samples[curr] += 1;
            self.weights[curr][-1] += 1;
        else:
            self.samples[old] += 1;
            self.weights[old][curr] += 1;

    def calculate_weights(self, state=None):
        '''
        Calculates the probability weights of transitions.
        By default, this updates the whole matrix but can
        be limited to a specific state
        '''
        
        if state is not None and self.samples[state] > 0:
            self.weights[state] = map(lambda w: Fraction(w, self.samples[state]), self.weights[state]);
        else:
            for key in self.states:
                if self.samples[key] > 0:
                    self.weights[key] = map(lambda w: Fraction(w, self.samples[key]), self.weights[key]);
        


class Dealer(Learner):
    '''
    Although the Dealer learns from his moves, 
    He may be required to use a fixed policy
    '''

    # Default Dealer Policies.
    POLICIES = { 
                'DRAW_BELOW_THREE': POLICY(lambda dealer, deck: dealer.draw(1, deck) if dealer.hand() < 3 else dealer.stand()),
                'DRAW_BELOW_FOUR': POLICY(lambda dealer, deck: dealer.draw(1, deck) if dealer.hand() < 4 else dealer.stand())
               };


    def __init__(self, name="Dealer", rate=0.5, policy=POLICY(None)):
        super(Dealer, self).__init__(name, rate);
        self.policy = policy;

    def play(self, deck):
        '''
        If we don't have a known policy, play based on learnt rules
        Otherwise use policy
        '''

        if id(self.policy) not in map(id, Dealer.POLICIES.values()):
            return super(Dealer, self).play(deck);
        else:
            return self.policy.eval(self, deck);

