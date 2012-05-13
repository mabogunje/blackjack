'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: The game of Preschool Poker
'''

from deck import *;
from player import *;

class PreschoolPoker:
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


class StudPoker(PreschoolPoker):
    '''
    In Stud Poker, the winner of the game is determined immediately after the cards are dealt.
    '''

    def play(self, plyrA, plyrB):
        super(StudPoker, self).play(plyrA, plyrB);

        # Check for winner
        if plyrA.hand() > plyrB.hand():
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), PreschoolPoker.WINNER % plyrA.name;
        elif plyrB.hand() > plyrA.hand():
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), PreschoolPoker.WINNER % plyrB.name;
        else:
            print "DRAW";


class DrawOnePoker(PreschoolPoker):
    '''
    In DrawOnePoker, each player is permitted to discard one card, and replace it with another from the deck.
    '''

    def play(self, plyrA, plyrB):
        super(DrawOnePoker, self).play(plyrA, plyrB);

        # Save initial states
        cardsA = plyrA.cards;
        cardsB = plyrB.cards;

        # Take an action (draw, discard, or stand)
        moveA = plyrA.play(self.deck);
        moveB = plyrB.play(self.deck);

        # Check for winner ::KLUDGE:: Assumes plyrA as Learner when returning win value
        if plyrA.hand() > plyrB.hand():
            if isinstance(plyrA, Learner):
                plyrA.learn({cardsA: moveA}, self.WIN);
            else:
                plyrA.learn({cardsA: moveA}, self.LOSE);

            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % plyrA.name;
            return self.WIN;

        elif plyrB.hand() > plyrA.hand():
            if isinstance(plyrB, Learner):
                plyrB.learn({cardsB: moveB}, self.WIN);
            else:
                plyrB.learn({cardsB: moveB}, self.LOSE);
            
            print PreschoolPoker.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % plyrB.name;
            return self.LOSE;

        else:
            print "DRAW";
            return self.LOSE;

