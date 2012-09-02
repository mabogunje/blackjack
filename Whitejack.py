'''
author: Damola Mabogunje
contact: damola@mabogunje.net
summary: This program allows the user to pit a Reinforcement learning AI 
         against an AI opponent in a game of Whitejack multiple times to 
         allow the AI to learn an optimal strategy.
'''

import argparse;
from blackjack import Whitejack;
from player import *;


GAMES = [Whitejack()];
ROBOTS = [Learner('Learner')];
DEFAULT_TRIALS = 10;
LEARNING_RATE = 0.5; # EDIT HERE to modify default learning rate

def main():
    parser = argparse.ArgumentParser(prog="Whitejack", description="%(prog)s is a reinforcement learning program for a simplified version of blackjack.\
            You may play against the AI dealer or have it play itself to learn.", epilog="This program was developed by Damola Mabogunje");

    parser.add_argument('-t', '--type', metavar='GAME_TYPE', type=int, choices=range(len(GAMES)),
                        help='Game Type. Must be an integer from [%(choices)s]'
                       );

    parser.add_argument('-o', '--opponent', metavar='OPPONENT', type=int, choices=range(len(ROBOTS)),
                        help='This is the AI dealer. Must be an integer from [%(choices)s]'
                       );

    parser.add_argument('-n', '--trials', metavar='NUMBER_OF_TRIALS', type=int, nargs='?',
                        default=DEFAULT_TRIALS,
                        help='Number of times to play game. Must be a positive integer.'
                       );

    parser.add_argument('-r', '--rate', metavar='LEARNING_RATE', type=float, nargs='?',
                        default=LEARNING_RATE,
                        help='Speed of learning. Must be a float between 0 and 1.'
                       );
    
    args = parser.parse_args();

    run(args.type, args.opponent, args.trials, args.rate);


def run(game, opponent, trials, learning_rate):
    
    if not game in range(len(GAMES)):
        prompt = "> Which Blackjack rules do you play by?";
        print prompt;

        for i,game in enumerate(GAMES):
            print "(%d): %s" % (i, game.__class__.__name__);
        game = GAMES[input()];
    else:
        game = GAMES[game];
    
    if not opponent in range(len(ROBOTS)):
        prompt = "> Who should I play against? (Enter 1 to be my opponent)";
        print prompt;
    
        for i,player in enumerate(ROBOTS):
            print "(%d): %s" % (i, player.name);

        try:
            opponent = ROBOTS[input()] ;
            opponent.learning_rate = learning_rate;
        except:
            opponent = Player(raw_input("Enter your name: "));
    else:
        opponent = ROBOTS[opponent];
    
    player = Dealer('Dealer', learning_rate);

    players = [player, opponent];

    print '''
          ============================
                GAME START
          ============================
          '''

    for p in players:
        p.draw(1, game.deck);

    if type(opponent) == type(Player("Instance")):
        while run_interactive(game, players[0], players[1]):
            pass; # Keep Prompting

        winner = game.winner(player, opponent);

        if winner:
            losers = [p for p in players if p is not winner];

            if isinstance(winner, Learner):
                winner.learn(winner.hand(), game.WIN);
            elif isinstance(losers[0], Learner):
                losers[0].learn(losers[0].hand(), game.LOSE);
            
            print "Winner: %s" % winner.name;
            
        else:
             print "Draw";

        for p in players:
            del p.cards[:];
    else:
        for i in range(trials):
            game.play(players[0], players[1]);

            '''
            Clear player cards
            Start a new game of the same type
            Reverse play order
            '''

            game = Whitejack();

            for p in players:
                del p.cards[:];

            players = [players[1], players[0]];

    print "\nState probabilities:"
    
    for hand, weight in sorted(player.weights.items(), key=lambda w: w[1]):
        print "%s => %s" % (hand, weight);

def run_interactive(game, player, opponent):
    '''
    Play a game of blackjack with a human opponent
    '''

    players = [player, opponent];
    bot = player if isinstance(player, Learner) else opponent;
    human = opponent if type(opponent) == type(Player("Instance")) else player;
    action = bot_move = Action.DRAW;

    for p in players:
        print "%s's Hand: %s\n" % (p.name, p.cards);

    if isinstance(game, Whitejack):
            prompt = "> What will you do?";
            print prompt;
            moves = dict(enumerate(human.get_moves()));

            for i, move in moves.items():
                print "(%d): %s" % (i, Action.describe(move));
            action = moves[input()];

            for p in players:
                if p is human:
                    print "You performed '%s'" % Action.describe(action);
                    
                    if action is Action.STAND:
                        p.stand();
                    elif action is Action.DRAW:
                        p.draw(1, game.deck);
                else:
                    bot_move = p.play(game.deck);
                    print "\nI shall '%s'" % Action.describe(bot_move);

                print "%s's Hand: %s\n" % (p.name, p.cards);
                
            for p in players:
                if p.hand() >= 5:
                    return;

            return ((action is Action.DRAW) and (bot_move is Action.DRAW));

    '''
    prompt = "> Play again (y/n)?";
    return (raw_input(prompt).lower() == 'y');
'''

if __name__ == "__main__":
    main();
