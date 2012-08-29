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
LEARNING_RATE = 0.7; # EDIT HERE to modify learning rate

MOVES = { Action.STAND: "Stand", 
          Action.DISCARD_ONE: "Discard a (1)",
          Action.DISCARD_TWO: "Discard a (2)",
          Action.DISCARD_THREE: "Discard a (3)"
         };

def main():
    parser = argparse.ArgumentParser(description='Process PreschoolPoker arguments');
    parser.add_argument('-n', '--trials', metavar='NUMBER_OF_TRIALS', type=int, nargs='?',
                        default=DEFAULT_TRIALS,
                        help='Number of times to play game. Must be a positive integer.'
                       );

    args = parser.parse_args();

    try:
        trials = args.trials;
    except:
        trials = DEFAULT_TRIALS;

    run(trials);


def run(trials):
    
    prompt = "> Which Poker rules do you play by?";

    print prompt;
    for i,game in enumerate(GAMES):
        print "(%d): %s" % (i, game.__class__.__name__);
    game = GAMES[input()];
    
    prompt = "> Who should I learn from? (Enter 3 to play against me)";

    print prompt;
    for i,player in enumerate(ROBOTS):
        print "(%d): %s" % (i, player.name);

    try:
        opponent = ROBOTS[input()] ;
    except:
        opponent = Player(raw_input("Enter your name: "));
    finally:
        player = Learner('PlayerBot', LEARNING_RATE);

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

            # Clear player cards and start a new game of the same type
            game = DrawOnePoker() if isinstance(game, DrawOnePoker) else StudPoker();
            player.cards = [];
            opponent.cards = [];
            players = [players[1], players[0]];

    print player.weights;

def run_interactive(game, player, opponent):
    '''
    Play a game of poker with a human opponent
    '''

    players = [player, opponent];
    bot = player if isinstance(player, Learner) else opponent;
    human = opponent if type(opponent) == type(Player("Instance")) else player;


    for p in players:
        p.draw(2, game.deck);

    print "%s's Hand: %s" % (human.name, human.cards);

            
    if isinstance(game, DrawOnePoker):
        prompt = "> What will you do?";

        print prompt;
        for move,repr in MOVES:
            print "(%d): %s" % (move, repr);
        action = input();

        for p in players:
            if p is human:
                if action == Action.STAND:
                    p.stand();

                if Action.is_discard(action):
                    prompt = "> Discard which card?";
                
                    print prompt;
                    for i,card in enumerate(human.cards):
                        print "(%d): %s" % (i, card);
                    card = human.cards[input()];

                    human.discard(card, game.deck);
            else:
                p.play();

    print "My Hand: %s" % bot.cards;
    winner = game.winner(human, bot);

    if winner:
        print "Winner: %s" % winner.name;
    else:
        print "Draw";

    prompt = "> Play again (y/n)?";
    return (raw_input(prompt).lower() == 'y');


if __name__ == "__main__":
    main();
