'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: The game of Preschool Poker
'''

from deck import *;
from player import *;

class PreschoolPoker(object):
    '''
    The game of Preschool Poker involves 2 players who are each dealt 2 cards from a shuffled deck. 
    The deck contains 9 cards: 3 each bearing the values {1, 2, 3}. 
    The highest ranking hand is a pair of 3's, followed successively by a pair of 2's and a pair of 1's. 
    If a player's hand does not contain a pair, the hand is ranked according to the sum total of its cards.
    '''

    MATCH = "%s versus %s";
    WINNER = "%s wins!";
    (LOSE, WIN) = range(0, 2); 

    def __init__(self):
        self.deck = Deck();

    def play(self, plyrA, plyrB):

        # Deal cards
        plyrA.draw(2, self.deck);
        plyrB.draw(2, self.deck);

        print "= Starting Hands =\n%s: %s\n%s: %s\n" % (plyrA.name, str(plyrA.cards), plyrB.name, str(plyrB.cards));

    def winner(self, plyrA, plyrB):

        if plyrA.hand() > plyrB.hand():
            return plyrA;
        elif plyrB.hand() > plyrA.hand():
            return plyrB;
        else:
            return None;


class StudPoker(PreschoolPoker):
    '''
    In Stud Poker, the winner of the game is determined immediately after the cards are dealt.
    '''

    def play(self, plyrA, plyrB):
        super(StudPoker, self).play(plyrA, plyrB);

        # Convert to list of cards to sets for easy comparison
        cardsA = set(plyrA.cards);
        cardsB = set(plyrB.cards);

        # Check for winner
        if self.winner(plyrA, plyrB) is plyrA:
            if isinstance(plyrA, Learner):
                plyrA.learn(tuple(cardsA), self.WIN);
            else:
                plyrB.learn(tuple(cardsB), self.LOSE);

            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), PreschoolPoker.WINNER % plyrA.name;
        elif self.winner(plyrA, plyrB) is plyrB:
            if isinstance(plyrB, Learner):
                plyrB.learn(tuple(cardsB), self.WIN);
            else:
                plyrA.learn(tuple(cardsA), self.LOSE);

            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), PreschoolPoker.WINNER % plyrB.name;
        else:
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), "DRAW";


class DrawOnePoker(PreschoolPoker):
    '''
    In DrawOnePoker, each player is permitted to discard one card, and replace it with another from the deck.
    '''

    def play(self, plyrA, plyrB):
        super(DrawOnePoker, self).play(plyrA, plyrB);

        # Take an action (draw, discard, or stand)
        moveA = plyrA.play(self.deck);
        moveB = plyrB.play(self.deck);

        print "= Player Moves =\n%s: %s\n%s: %s\n" % (plyrA.name, Action.describe(moveA), plyrB.name, Action.describe(moveB));

        # Convert to sets for easy comparison
        cardsA = set(plyrA.cards);
        cardsB = set(plyrB.cards);

        print "= Closing Hands =\n%s: %s\n%s: %s\n" % (plyrA.name, str(plyrA.cards), plyrB.name, str(plyrB.cards));

        if self.winner(plyrA, plyrB) is plyrA:
            if isinstance(plyrA, Learner):
                plyrA.learn(tuple(cardsA), self.WIN);
            else:
                plyrB.learn(tuple(cardsB), self.LOSE);

            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % plyrA.name;
            return self.WIN;

        elif self.winner(plyrA, plyrB) is plyrB:
            if isinstance(plyrB, Learner):
                plyrB.learn(tuple(cardsB), self.WIN);
            else:
                plyrA.learn(tuple(cardsA), self.LOSE);
            
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % plyrB.name;
            return self.LOSE;

        else:
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), "DRAW";
            return self.LOSE;

