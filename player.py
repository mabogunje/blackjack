'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: Preschool Poker Player Bots
'''

from random import choice;
from deck import Card, Hand;

class Action(object):
    '''
    Possible Player Moves
    '''

    (STAND, DISCARD_ONE, DISCARD_TWO, DISCARD_THREE) = range(0, 4);

    @staticmethod
    def is_discard(move):
        return (move in [Action.DISCARD_ONE, Action.DISCARD_TWO, Action.DISCARD_THREE]);

    @staticmethod
    def describe(move):
        descriptions = { None: "Stand",
                         Action.STAND: "Stand",
                         Action.DISCARD_ONE: "Discard a (1)",
                         Action.DISCARD_TWO: "Discard a (2)",
                         Action.DISCARD_THREE: "Discard a (3)"
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

    def get_moves(self):
        moves = [Action.STAND];

        if Card.ONE in self.cards:
            moves.append(Action.DISCARD_ONE);

        if Card.TWO in self.cards:
            moves.append(Action.DISCARD_TWO);

        if Card.THREE in self.cards:
            moves.append(Action.DISCARD_THREE);

        return moves;

    def discard(self, card, deck):
        '''
        Discards card from hand and draws a new card from the deck 
        '''
        discards = { Card.ONE: Action.DISCARD_ONE, 
                     Card.TWO: Action.DISCARD_TWO,
                     Card.THREE: Action.DISCARD_THREE
                   };

        self.cards.remove(card);
        self.draw(1, deck);

        return discards[card];

    def stand(self):
        '''
        Do Nothing
        '''
        return Action.STAND;

    def hand(self):
        if len(self.cards) == len(set(self.cards)):
            return sum(self.cards);
        else:
            pairs = [self.cards[k] for k,v in enumerate(self.cards) if self.cards.count(v) > 1];

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
        moves = [Action.STAND, Action.DISCARD_ONE, Action.DISCARD_TWO, Action.DISCARD_THREE];
        action = choice(moves);

        if action == Action.STAND:
            return self.stand();

        if Action.is_discard(action):
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


class Learner(SmartPlayer):
    '''
    Learner learns how to play PreschoolPoker from its matches (Reinforcement Learning)
    '''

    def __init__(self, name="PlayerBot", rate=0.5):
        super(Learner, self).__init__(name);
        self.learning_rate = rate;

        self.states = [ set([Card.THREE, Card.THREE]),  # [3,3]
                        set([Card.TWO, Card.TWO]),      #[2,2]
                        set([Card.ONE, Card.ONE]),       #[1,1]
                        set([Card.ONE, Card.TWO]),      #[1,2], [2,1]
                        set([Card.ONE, Card.THREE]),    #[1,3], [3,1]
                        set([Card.TWO, Card.THREE])     #[2,3], [3,2]
                      ];

        # All states are initially assigned an equal weight
        self.weights = dict.fromkeys([tuple(x) for x in self.states], 0.5);

    def play(self, deck):
        '''
        Find accessible states and sort by probability of winning
        - An accessible state will have at least one card 
          in common with the current state
        '''
        is_accessible = lambda state: (set(state) & set(self.cards));
        new_states = filter(is_accessible, self.states);
        probabilities = [p for p in self.weights.items() if p[0] in new_states]; 
        probabilities = sorted(probabilities, key=lambda p: p[1]);

        '''
        If there are any better accessible states, try to reach 
        the state with the best chance of winning.
        '''
        if probabilities:
            desired_state = probabilities[-1];

            if desired_state[1] > self.weights[set(self.cards)]:
                bad_cards = set(self.cards) - desired_state[0];
                worst_card = min(list(bad_cards));

                return self.discard(worst_card, deck);
            else:
                return self.stand();
        else:
            return super(Learner, self).play(deck);

    def learn(self, state, result):
        '''
        Given a state and its win/loss result, update its weight reinforcing towards the result
        '''
        self.weights[state] = self.weights[state] + (self.learning_rate * (result - self.weights[state]));

