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


class Learner(Player):
    '''
    Learner learns how to play PreschoolPoker from its matches (Reinforcement Learning)
    '''

    def __init__(self, name="PlayerBot", rate=0.5):
        super(Learner, self).__init__(name);
        self.learning_rate = rate;

        '''
        self.mapping is a a list of all possible state/action pairs

        ::KLUDGE:: States are duplicated because state/action pairs must be distinct. 
        There should be a better way to do this
        '''
        self.mapping = [ ((Card.THREE, Card.THREE), Action.STAND),            # [3,3]
                         ((Card.THREE, Card.THREE), Action.DISCARD_THREE),
                         ((Card.TWO, Card.TWO), Action.STAND),                #[2,2]
                         ((Card.TWO, Card.TWO), Action.DISCARD_TWO),
                         ((Card.ONE, Card.ONE), Action.STAND),                #[1,1]
                         ((Card.ONE, Card.ONE), Action.DISCARD_ONE),
                         ((Card.ONE, Card.TWO), Action.STAND),                #[1,2]
                         ((Card.ONE, Card.TWO), Action.DISCARD_ONE),
                         ((Card.ONE, Card.TWO), Action.DISCARD_TWO),
                         ((Card.TWO, Card.ONE), Action.STAND),                #[2,1] 
                         ((Card.TWO, Card.ONE), Action.DISCARD_ONE),
                         ((Card.TWO, Card.ONE), Action.DISCARD_TWO),
                         ((Card.ONE, Card.THREE), Action.STAND),              #[1,3]
                         ((Card.ONE, Card.THREE), Action.DISCARD_ONE),
                         ((Card.ONE, Card.THREE), Action.DISCARD_THREE),
                         ((Card.THREE, Card.ONE), Action.STAND),              #[3,1]
                         ((Card.THREE, Card.ONE), Action.DISCARD_ONE),
                         ((Card.THREE, Card.ONE), Action.DISCARD_THREE),
                         ((Card.TWO, Card.THREE), Action.STAND),              #[2,3]
                         ((Card.TWO, Card.THREE), Action.DISCARD_TWO),
                         ((Card.TWO, Card.THREE), Action.DISCARD_THREE),
                         ((Card.THREE, Card.TWO), Action.STAND),              #[3,2]
                         ((Card.THREE, Card.TWO), Action.DISCARD_TWO),
                         ((Card.THREE, Card.TWO), Action.DISCARD_THREE)
                       ];

        # All mappings i.e (state/action pairs) are initially assigned an equal weight
        self.weights = dict.fromkeys(self.mapping, 0.5);

    def play(self, deck):
        '''
        Select only the mappings that apply to the current hand
        and order them by weight
        '''
        explored = filter(lambda visited: set(self.cards) == set(visited[0]), self.weights.keys());
        exploits = sorted(explored, key=lambda x: x[1]);

        discards = { Action.DISCARD_ONE: Card.ONE,
                     Action.DISCARD_TWO: Card.TWO,
                     Action.DISCARD_THREE: Card.THREE
                   };

        action = Action.STAND; # Initialize action variable

        '''
        If there are applicable rules, exploit them and select the 
        action with the most weight.
        '''
        if exploits:
            action == exploits[-1][1];

            if Action.is_discard(action):
                return self.discard(discards[action], deck);
            elif action == Action.STAND:
                return self.stand();
        else:
            return self.stand();

    def learn(self, policy, result):
        '''
        Given a previous policy (state/action pair) and the corresponding win/lose result, 
        If the policy result is better than the current weight, reinforce the rule
        '''
        old = set(policy.items()) & set(self.mapping); # Visited States

        for rule in old:

            if result > self.weights[rule]:
                self.weights[rule] = self.weights[rule] + ((result - self.weights[rule]) * self.learning_rate);

