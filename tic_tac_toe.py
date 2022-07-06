from player import *
import copy

class TicTacToe(object):

    def __init__(self):

        # if last move is key, check values for win.
        self.win_corresp = {
            0: [[1,2],[3,6],[4,8]],
            1: [[0,2],[4,7]],
            2: [[0,1], [5,8], [4,6]],
            3: [[0,6],[4,5]],
            4: [[3,5],[1,7],[0,8],[2,6]],
            5: [[2,8], [3,4]],
            6: [[0,3], [7,8], [2,4]],
            7: [[6,8],[1,4]],
            8: [[6,7], [2,5], [0,4]]
        }

    def display_grid(self, position):
        display=[' ' for i in range(9)]
        for i in range(9):
            if position[i] == 1:
                display[i] = 'O'
            elif position[i] == 2:
                display[i] = 'X'

        for i in range(3):
            print(f'{display[i*3]}|{display[i*3+1]}|{display[i*3+2]}')
            if i < 2:
                print('-----')


    def play_game(self, player1, player2, silent=False):
        position = [0 for i in range(9)]
        while(True):
            for player in [player1, player2]:
                move = player.next_move(position)
                position[move] = player.mark
                if not silent:
                    self.display_grid(position)
                    print("")
                end = self.test_end_of_game(position, player.mark, move)
                if end:
                    return end


    def test_end_of_game(self, position, mark, last):
        indexes = [i for i,e in enumerate(position) if e==mark]
        for combi in self.win_corresp[last]:
            if all([c in indexes for c in combi]):
                return mark
        if not [i for i in position if i==0]:
            return 3


# Declarations

tic_tac_toe = TicTacToe()

learner = LearningIAPlayer(True)
leaner2 = LearningIAPlayer(False)

dummy = RandomIAPlayer(False)
dummy2 = RandomIAPlayer(True)


# TRAINING / LEARNING

for i in range(5000):
    end = tic_tac_toe.play_game(learner, dummy, True)
    learner.learn_from_game(end)
    print(i)

for i in range(5000):
    end = tic_tac_toe.play_game(dummy2, leaner2, True)
    learner.learn_from_game(end)
    print(i)

for i in range(10000):
    end = tic_tac_toe.play_game(learner, leaner2, True)
    learner.learn_from_game(end)
    print(i)


# Play against human

player = RealPlayer(False)

while True:
    print(learner.positions)
    end = tic_tac_toe.play_game(learner, player)
    learner.learn_from_game(end)
    import pdb; pdb.set_trace()
