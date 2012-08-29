'''
author: Damola Mabogunje
contact: damola@mabogunje.net
summary: This program allows the user to pit a Reinforcement learning AI 
         against one of four opponents in a game of PreschoolPoker 
         multiple times to allow the AI to learn an optimal strategy.
'''

import argparse;
from poker import StudPoker, DrawOnePoker;
from player import *;


GAMES = [StudPoker(), DrawOnePoker()];
ROBOTS = [DumbPlayer('Randy'), OddPlayer('OddBall'), SmartPlayer('Deep Preschooler')];
DEFAULT_TRIALS = 10;
LEARNING_RATE = 0.2; # EDIT HERE to modify default learning rate

def main():
    parser = argparse.ArgumentParser(prog="Preschool Poker", description="%(prog)s is a reinforcement learning program for a simplified version of poker.\
            You may play against the computer or have it play one of its robot AI's to learn.", epilog="This program was developed by Damola Mabogunje")

    parser.add_argument('-t', '--type', metavar='GAME_TYPE', type=int, choices=range(len(GAMES)),
                        help='Game Type. Must be an integer from [%(choices)s]'
                       );

    parser.add_argument('-o', '--opponent', metavar='OPPONENT', type=int, choices=range(len(ROBOTS)),
                        help='Robot Opponent. Must be an integer from [%(choices)s]'
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
        prompt = "> Which Poker rules do you play by?";
        print prompt;

        for i,game in enumerate(GAMES):
            print "(%d): %s" % (i, game.__class__.__name__);
        game = GAMES[input()];
    else:
        game = GAMES[game];
    
    if not opponent in range(len(ROBOTS)):
        prompt = "> Who should I learn from? (Enter 3 to play against me)";
        print prompt;
    
        for i,player in enumerate(ROBOTS):
            print "(%d): %s" % (i, player.name);

        try:
            opponent = ROBOTS[input()] ;
        except:
            opponent = Player(raw_input("Enter your name: "));
    else:
        opponent = ROBOTS[opponent];
    
    player = Learner('Computer', learning_rate);

    players = [player, opponent];

    if type(opponent) == type(Player("Instance")):
        while run_interactive(game, players[0], players[1]):

            # Clear player cards and start a new game of the same type
            game = DrawOnePoker() if isinstance(game, DrawOnePoker) else StudPoker();
            player.cards = [];
            opponent.cards = [];
            players = [players[1], players[0]];

    else:
        for i in range(trials):
            game.play(players[0], players[1]);

            '''
            Clear player cards
            Start a new game of the same type
            Reverse play order
            '''

            game = DrawOnePoker() if isinstance(game, DrawOnePoker) else StudPoker();
            player.cards = [];
            opponent.cards = [];
            players = [players[1], players[0]];

    print "\nState probabilities:"
    
    for hand, weight in sorted(player.weights.items(), key=lambda w: w[1]):
        print "%s => %s" % (hand, weight);

def run_interactive(game, player, opponent):
    '''
    Play a game of poker with a human opponent
    '''

    players = [player, opponent];
    bot = player if isinstance(player, Learner) else opponent;
    human = opponent if type(opponent) == type(Player("Instance")) else player;

    print '''
          ============================
                GAME START
          ============================
          '''


    for p in players:
        p.draw(2, game.deck);

    print "%s's Hand: %s\n" % (human.name, human.cards);

    if isinstance(game, DrawOnePoker):
        prompt = "> What will you do?";
        print prompt;
        moves = dict(enumerate(human.get_moves()));

        for i, move in moves.items():
            print "(%d): %s" % (i, Action.describe(move));
        action = moves[input()];

        for p in players:
            if p is human:
                if action is Action.STAND:
                    p.stand();
                elif action is Action.DISCARD_ONE:
                    human.discard(Card.ONE, game.deck);
                elif action is Action.DISCARD_TWO:
                    human.discard(Card.TWO, game.deck);
                elif action is Action.DISCARD_TWO:
                    human.discard(Card.THREE, game.deck);

                print "You performed '%s'" % Action.describe(action);
            else:
                print "\nI shall '%s'" % Action.describe(p.play(game.deck));

    print "\nMy Hand: %s" % bot.cards;
    print "%s's Hand: %s" % (human.name, human.cards);

    winner = game.winner(human, bot);

    if winner:
        if winner is bot:
            bot.learn(tuple(set(bot.cards)), game.WIN);
        else:
            bot.learn(tuple(set(bot.cards)), game.LOSE);

        print "Winner: %s" % winner.name;
    else:
        print "Draw";

    prompt = "> Play again (y/n)?";
    return (raw_input(prompt).lower() == 'y');


if __name__ == "__main__":
    main();
