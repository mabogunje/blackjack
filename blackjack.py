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
    WINNER = "%s wins!";
    GOAL = 4; 
    (LOSE, WIN) = range(0, 2); 

    def __init__(self):
        self.deck = Deck();

    def play(self, plyrA, plyrB, starting_hand=None):

        players = [plyrA, plyrB];
        moves = [];


        # Deal cards if they have not been dealt, then show hand and decide on next move.
        for p in players:
            if p.cards:
                pass;
            else:
                # Rig dealer `starting_hand` if provided
                if starting_hand and isinstance(p, Dealer):
                    p.cards.append(starting_hand);
                    p.learn(0, starting_hand, None);
                else:
                    p.draw(1, self.deck);

            
            print "%s's Hand: %s" % (p.name, p.cards);
            moves.append(p.play(self.deck));

        # Show hands and moves
        for i, p in enumerate(players):
            print "%s performed '%s'" % (p.name, Action.describe(moves[i]));

        # Game ends if a player stands or busts
        if (Action.STAND in moves) or ((Whitejack.GOAL+1) in [plyrA.hand(), plyrB.hand()]):
            winner = self.winner(plyrA, plyrB);

            if winner is None:
                print self.MATCH % (plyrA.cards, plyrB.cards), "DRAW";
            else:
                winner.learn((Whitejack.GOAL+1),0, None); # ::HACK:: Force learning that BUST takes you START
                winner.learn(winner.hand() - winner.cards[-1], winner.hand(), self.WIN);
                print Whitejack.MATCH % (plyrA.cards, plyrB.cards), self.WINNER % winner.name;

            return;
        else:
            return self.play(plyrA, plyrB);


    def winner(self, plyrA, plyrB):

        if plyrA.hand() == plyrB.hand():
            return None;
        elif plyrA.hand() >= self.GOAL:
            return plyrB;
        elif plyrB.hand() >= self.GOAL:
            return plyrA;
        else:
            return plyrA if plyrA.hand() > plyrB.hand() else plyrB;


class Greyjack(Whitejack):
    '''
    This class is merely an alias readability. Greyjack is the same as Whitejack but for Dealer policy. 
    Dealer policies are defined in the Dealer class.
    
    See player.py.
    '''

class Blackjack(Whitejack):
    '''
    An implementation of the game of Blackjack. Similar to Whitejack but with a full deck and goal of 21.
    '''

    GOAL = 21;

    def __init__(self):
        self.deck = FullDeck();

    def play(self, plyrA, plyrB, starting_hand=None):

        players = [plyrA, plyrB];
        moves = [];


        # Deal cards if they have not been dealt, then show hand and decide on next move.
        for p in players:
            if p.cards:
                pass;
            else:
                # Rig dealer `starting_hand` if provided
                if starting_hand and isinstance(p, Dealer):
                    p.cards.append(starting_hand);
                    p.learn(0, starting_hand, None);
                else:
                    p.draw(2, self.deck);

            
            print "%s's Hand: %s" % (p.name, p.cards);

            if isinstance(p, BlackjackAgent):
                dealer = next(obj for obj in players if isinstance(obj, Dealer));
                moves.append(p.play(self.deck, dealer.upcard())); 
            else:
                moves.append(p.play(self.deck));

        # Show hands and moves
        for i, p in enumerate(players):
            print "%s performed '%s'" % (p.name, Action.describe(moves[i]));

        # Game ends if a player stands or busts
        if (Action.STAND in moves) or ((Blackjack.GOAL+1) in [plyrA.hand(), plyrB.hand()]):
            winner = self.winner(plyrA, plyrB);

            if winner is None:
                print Blackjack.MATCH % (plyrA.cards, plyrB.cards), "DRAW";
            else:
                winner.learn((Blackjack.GOAL+1),0, None); # ::HACK:: Force learning that BUST takes you START
                winner.learn(winner.hand() - winner.cards[-1], winner.hand(), Blackjack.WIN);
                print Blackjack.MATCH % (plyrA.cards, plyrB.cards), Blackjack.WINNER % winner.name;

            return;
        else:
            return self.play(plyrA, plyrB);
