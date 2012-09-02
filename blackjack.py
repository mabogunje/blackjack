'''
@author: Damola Mabogunje
@contact: damola@mabogunje.net
@summary: The game of Whitejack
'''

from deck import *;
from player import *;

class Whitejack(object):
    '''
    Whitejack is a variant of Blackjack where the deck contains an unlimited supply of cards with face values 1-4 in equal quantities. 
    The player and dealer are each dealt one card, face up. Each is allowed to request additional cards (hits).
    The player wins by scoring higher than the dealer without busting, which occurs when the sum of card values 
    reaches 5 or more.
    '''

    MATCH = "%s versus %s";
    WINNER = "%s wins!\n";
    (LOSE, WIN) = range(0, 2); 

    def __init__(self):
        self.deck = Deck();

    def play(self, plyrA, plyrB):

        players = [plyrA, plyrB];
        moves = [];

        # Deal cards if they have not been dealt, then show hand and decide on next move.
        for p in players:
            if p.cards:
                pass;
            else:
                p.draw(1, self.deck);
            
            print "%s's Hand: %s" % (p.name, p.cards);
            moves.append(p.play(self.deck));

        # Show hands and moves
        for i, p in enumerate(players):
            print "%s performed '%s'" % (p.name, Action.describe(moves[i]));

        # Game ends if a player stands or busts
        if (Action.STAND in moves) or (5 in [plyrA.hand(), plyrB.hand()]):
            winner = self.winner(plyrA, plyrB);

            if winner is plyrA:
                if isinstance(plyrA, Learner):
                    plyrA.learn(plyrA.hand(), self.WIN);
                else:
                    plyrB.learn(plyrB.hand(), self.LOSE);
                    
                print Whitejack.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % winner.name;
                return self.WIN;

            elif winner is plyrB:
                if isinstance(plyrB, Learner):
                    plyrB.learn(plyrB.hand(), self.WIN);
                else:
                    plyrA.learn(plyrA.hand(), self.LOSE);
                    
                print Whitejack.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % winner.name;
                return self.LOSE;

            else:
                print Whitejack.MATCH % (plyrA.cards, plyrB.cards), "DRAW";
                self.LOSE;
        else:
            return self.play(plyrA, plyrB);


    def winner(self, plyrA, plyrB):

        if plyrA.hand() == plyrB.hand():
            return None;
        elif plyrA.hand() >= 5:
            return plyrB;
        elif plyrB.hand() >= 5:
            return plyrA;
        else:
            return plyrA if plyrA.hand() > plyrB.hand() else plyrB;

