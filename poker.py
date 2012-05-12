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

    def __init__(self):
        self.deck = Deck();

    def play(self, plyrA, plyrB):
        raise NotImplementedError("You must implement this method");


class StudPoker(PreschoolPoker):
    '''
    In Stud Poker, the winner of the game is determined immediately after the cards are dealt.
    '''

    def play(self, plyrA, plyrB):

        plyrA.draw(2, self.deck);
        plyrB.draw(2, self.deck);

        if plyrA.hand() > plyrB.hand():
            print plyrA.cards, plyrB.cards, "Player 1 wins!";
        else:
            print plyrA.cards, plyrB.cards, "Player 2 wins!";

game = StudPoker();
game.play(Player(), Player());
