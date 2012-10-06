'''
author: Damola Mabogunje
contact: damola@mabogunje.net
summary: This program allows the user to pit a Markov learning AI 
         against a dealer in a game of White or Greyjack multiple 
         times to learn an optimal strategy. It employs sampling
         and the resulting transition probability matrix is
         printed at the end.
'''

import argparse, math;
from blackjack import *;
from player import *;


GAMES = [Whitejack(), Greyjack()];
ROBOTS = [Learner('Learner')];
LEARNING_RATE = 0.5;

def main():
    parser = argparse.ArgumentParser(prog="Whitejack", description="%(prog)s is a reinforcement learning program for a simplified version of blackjack.\
            You may play against the AI dealer or have it play itself to learn.", epilog="This program was developed by Damola Mabogunje");

    parser.add_argument('-t', '--type', metavar='GAME_TYPE', type=int, choices=range(len(GAMES)),
                        help='Game Type. Must be an integer from [%(choices)s]'
                       );

    parser.add_argument('-o', '--opponent', metavar='OPPONENT', type=int, choices=range(len(ROBOTS)),
                        help='This is the AI player. Must be an integer from [%(choices)s]'
                       );

    parser.add_argument('-n', '--samplings', metavar='SAMPLINGS', type=int, nargs='?',
                        required=True,
                        help='Number of sample games. Must be a positive integer.'
                       );


    parser.add_argument('-r', '--rate', metavar='LEARNING_RATE', type=float, nargs='?',
                        default=LEARNING_RATE,
                        help='Speed of learning. Must be a float between 0 and 1.'
                       );
    
    args = parser.parse_args();

    run(args.type, args.opponent, args.samplings, args.rate);

def run(game, opponent, samplings, learning_rate):
    
    if not game in range(len(GAMES)):
        prompt = "> Which Blackjack rules do you play by?";
        print prompt;

        for i,game in enumerate(GAMES):
            print "(%d): %s" % (i, game.__class__.__name__);
        game = GAMES[input()];
    else:
        game = GAMES[game];
    
    if not opponent in range(len(ROBOTS)):
        prompt = "> Who should I play against?";
        print prompt;
    
        for i,player in enumerate(ROBOTS):
            print "(%d): %s" % (i, player.name);

        try:
            opponent = ROBOTS[input()] ;
            opponent.learning_rate = learning_rate;
            opponent.samplings = samplings;
        except:
            opponent = Player(raw_input("Enter your name: "));
    else:
        opponent = ROBOTS[opponent];
    
    player = Dealer('Dealer', learning_rate);
    player.policy = Dealer.POLICIES['DRAW_BELOW_FOUR'] if isinstance(game, Whitejack) else Dealer.POLICIES['DRAW_BELOW_THREE'];

    players = [player, opponent];

    print '''
          ============================
                GAMES START
          ============================
          '''
    trials = samplings;

    for state in range(1,5):
        games = [state]*trials;
        
        for hand in games:
            game.play(players[0], players[1], hand);

            '''
            Start a new game of the same type
            Clear player cards
            Reverse play order
            '''

            game = Whitejack();
            for p in players: del p.cards[:];

            #players = [players[1], players[0]];
            
        '''
        Get the probability of players transitioning to the next state
        and update the number of games to run for that state accordingly.
        '''
        for p in players:
            if state > 3:
                '''
                Since START (0) and BUST (5) are not playable states, 
                We force their calculation
                '''
                p.calculate_weights(0);
                p.calculate_weights(5);

            p.calculate_weights(state);
        
        print "\n";
    
    print "\nState probabilities:"

    for hand, weight in sorted(player.weights.items(), key=lambda s: s[0]):
        '''
        Print probability matrix in decimal instead of fraction,
        while ignoring the last 2 entries 
        (probabilities of win & loss for that state)
        '''
        print "%s => %s" % (hand, map(float, weight));


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
