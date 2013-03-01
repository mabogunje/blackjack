'''
author: Damola Mabogunje
contact: damola@mabogunje.net
summary: This program pits a POMDP AI against a Blackjack dealer. 
         The dealer has a fixed policy of hitting until its hand is >= 17.
         The AI is aware of this policy and can observes the dealer's
         upfacing card. Based on this it decides what move to make
         in all possible states.

         The result is an optimal policy outputted to the console
         of the form [player_state],[observed_card]: [move]
'''

import argparse, math;
from blackjack import *;
from player import *;
from deck import *;

GAME = Blackjack();

DEALER = Dealer('Dealer', 0.5);
DEALER.policy = Dealer.POLICIES['DRAW_BELOW_SEVENTEEN'];

PLAYER = BlackjackPlayer('Two Bit Hand');
STATES = range(4, 22) + [12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5]; # Hard States + Soft States
STATES.sort();

'''
DEALER.cards = [Card.KING];
PLAYER.cards = [17];
move = PLAYER.play(GAME.deck, DEALER.policy, DEALER.upcard());
'''

for state in STATES:
    PLAYER.cards = [state] # ::HACK:: Since player's state is a sum of his cards, we can jump to any state by inserting the desired sum in card list

    for card in set(GAME.deck.cards):
        DEALER.cards = [card];
        move = PLAYER.play(GAME.deck, DEALER.policy, DEALER.upcard());
        
        if ceil(state) == state:
            print "%d,%d: %s" % (state, DEALER.upcard(), Action.describe(move));
        else:
            print "S%d,%d: %s" % (state, DEALER.upcard(), Action.describe(move));
        
        if move is Action.HIT:
            PLAYER.cards.pop();

