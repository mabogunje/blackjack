'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Whitejack Player Bots
'''

import numpy;
from random import choice;
from math import floor, ceil;
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

    (STAND, HIT) = range(0, 2);

    @staticmethod
    def describe(move):
        descriptions = { None: "hold",
                         Action.STAND: "hold",
                         Action.HIT: "hit"
                       };

        return descriptions[move];

class WhitejackPlayer(object):
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
        
        return Action.HIT;

    def get_moves(self):
        return [Action.STAND, Action.HIT];

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




class DumbPlayer(WhitejackPlayer):
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
                'DRAW_BELOW_FOUR': POLICY(lambda dealer, deck: dealer.draw(1, deck) if dealer.hand() < 4 else dealer.stand()),
                'DRAW_BELOW_SEVENTEEN': POLICY(lambda dealer, deck: dealer.draw(1, deck) if dealer.hand() < 17 else dealer.stand())
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

    def upcard(self):
        '''
        First card dealt to dealer is his upcard and thus public
        '''
        return self.cards[0];


class BlackjackPlayer(WhitejackPlayer):
    '''
    This player knows the stationary probabilities of reaching terminal states 
    for certain dealer policies. With this knowledge it can determine what action 
    to take in any state against a dealer using a known policy.
    '''

    # Terminal Stationary Probabilities for dealer policies 
    P_DEALER = dict();
    P_DEALER[Dealer.POLICIES['DRAW_BELOW_SEVENTEEN']] = numpy.matrix([[0.13, 0.01, 0.12, 0.01, 0.12, 0.01, 0.10, 0.01, 0.12, 0.40],
                                                                      [0.12, 0.01, 0.12, 0.01, 0.11, 0.01, 0.11, 0.01, 0.12, 0.42],
                                                                      [0.10, 0.08, 0.11, 0.00, 0.11, 0.01, 0.10, 0.01, 0.10, 0.43],
                                                                      [0.37, 0.00, 0.07, 0.08, 0.08, 0.00, 0.08, 0.01, 0.08, 0.27],
                                                                      [0.14, 0.00, 0.36, 0.00, 0.06, 0.08, 0.07, 0.00, 0.07, 0.25],
                                                                      [0.13, 0.00, 0.13, 0.00, 0.35, 0.00, 0.05, 0.08, 0.07, 0.24],
                                                                      [0.12, 0.00, 0.12, 0.00, 0.12, 0.00, 0.34, 0.00, 0.12, 0.22],
                                                                      [0.12, 0.00, 0.12, 0.00, 0.12, 0.00, 0.12, 0.00, 0.34, 0.22],
                                                                      [0.11, 0.00, 0.11, 0.00, 0.10, 0.00, 0.10, 0.00, 0.10, 0.48],
                                                                      [0.05, 0.11, 0.05, 0.10, 0.05, 0.10, 0.05, 0.11, 0.16, 0.24],
                                                                      [0.10, 0.00, 0.10, 0.00, 0.10, 0.00, 0.10, 0.00, 0.10, 0.52],
                                                                      [0.05, 0.10, 0.05, 0.10, 0.05, 0.10, 0.05, 0.10, 0.15, 0.27],
                                                                      [0.09, 0.00, 0.09, 0.00, 0.09, 0.00, 0.09, 0.00, 0.09, 0.55],
                                                                      [0.05, 0.09, 0.05, 0.09, 0.05, 0.09, 0.05, 0.09, 0.15, 0.30],
                                                                      [0.09, 0.00, 0.09, 0.00, 0.09, 0.00, 0.09, 0.00, 0.09, 0.58],
                                                                      [0.06, 0.09, 0.06, 0.09, 0.06, 0.09, 0.06, 0.09, 0.14, 0.33],
                                                                      [0.08, 0.00, 0.08, 0.00, 0.08, 0.00, 0.08, 0.00, 0.08, 0.61],
                                                                      [0.06, 0.08, 0.06, 0.08, 0.06, 0.08, 0.06, 0.08, 0.14, 0.35],
                                                                      [1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00, 0.00],
                                                                      [0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 1.00]
                                                                     ]);

    def __init__(self, name="Computer", rate=0.5):
        super(BlackjackPlayer, self).__init__(name);

    def hand(self):
        return sum(self.cards); 

    def min_hand(self, policy):
        '''
        Returns the minimum hand on which a dealer will stand 
        using policy.

        ::KLUDGE:: Should be a property of the policy
        '''
        if policy is Dealer.POLICIES['DRAW_BELOW_SEVENTEEN']:
            return 17;

        return None;

    def play(self, deck, policy, upcard):

        # Always hit before the dealers lowest possible stand
        if self.hand() < self.min_hand(policy):
            return self.draw(1, deck);

        '''
        We add the least possible additional card to upcard to get the least possible
        belief state. Then we deduct 4 from this value to get our starting row into the 
        P_DEALER matrix because state 0,1,2,3 are omitted in our matrix.

        For our starting column, we simply deduct the value of the lowest state the
        dealer will stand on.

        ::KLUDGE::
        ciel() is being used to account for soft states. I valued my ACE at 11.5 instead
        of 11 so it could access soft states when present in a hand by rounding up.
        So hand comparison must be done using floor()
        '''
        row = ceil(upcard + min(deck.CARDS)) - 4;
        col = ceil(self.hand() - self.min_hand(policy));

        move = self.think(policy, row, col);

        if move is Action.HIT:
            return self.draw(1, deck);
        else:
            return self.stand();
        

    def think(self, policy, row, col):
        '''
        Given a dealer policy, and row and column into the transition matrix, 
        the player determines the best action and returns it.
        '''

        # Get relevant sub-matrix
        pDealer = BlackjackPlayer.P_DEALER[policy][row:, 0:];

        #print row, col;
        #print pDealer;

        # Calculate possible outcomes
        outcomes = numpy.array([[p[0, col:8].sum(), # p(LOSE)
                                 p[0, col] if (row <= 8 and col < 9)  else p[0, col:col+2].sum(), # p(DRAW)
                                (p[0, 9] + p[0, 0:col].sum())] # {p(BUST) +  p(WORSE_HAND)} = p(WIN)
                                for p in pDealer
                               ]
                              );
        numpy.resize(outcomes, (numpy.size(pDealer, 0), 3)); # For readability on print
        #print outcomes;

        expected_outcomes = [max(p) for p in outcomes];
        rewards = [];

        for i, p in enumerate(expected_outcomes):
            '''
            If we are likely not to lose this hand, reward. Otherwise, penalise
            '''
            if expected_outcomes[i] > outcomes[i, 0]:
                rewards.append(expected_outcomes[i] * 1);
            else:
                rewards.append(expected_outcomes[i] * -1);
                
        rating = sum(rewards);
        #print rating;

        # Decide action based on rating       
        if rating >= 0: 
            return Action.STAND;
        else:
            return Action.HIT;


