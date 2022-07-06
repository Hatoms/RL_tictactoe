import random
import numpy as np
from prompt_toolkit import prompt
from utils import reorder
from symmetries import symmetries
from numpy.random import choice

class Player(object):
    """type of tic_tac_toe player"""

    def __init__(self, circle=True):
        if circle:
            self.mark = 1
        else:
            self.mark = 2

class LearningIAPlayer(Player):

    def __init__(self, circle=True):
        self.positions = {}
        self.total_seeds = 24 # param for learning
        super(LearningIAPlayer, self).__init__(circle)
        self.pos_memory = {}

    def create_seed_pos(self, pos):
        str_pos = ''.join([str(x) for x in pos])
        nb_zero = len([i for i in pos if i==0])
        seed_pos = [self.total_seeds//nb_zero if pos[i] == 0 else 0 for i in range(9)]
        self.positions[str_pos] = seed_pos

    def check_for_symmetries(self, pos):
        for sym_name, sym in symmetries.items():
            str_pos = ''.join([str(x) for x in reorder(pos, sym)])
            if str_pos in self.positions:
                if sym_name == 'rg':
                    sym_opp = symmetries['rd']
                elif sym_name == 'rd':
                    sym_opp = symmetries['rg']
                else:
                    sym_opp = sym

                probas = reorder(self.positions[str_pos], sym_opp)
                try:
                    next_move = choice(9,p=[i/sum(probas) for i in probas])
                except ValueError:
                    import pdb; pdb.set_trace()
                self.pos_memory[str_pos] = sym[next_move]

                return next_move


    def next_move(self, position):
        next_move = self.check_for_symmetries(position)
        if next_move is not None:
            return next_move

        str_pos = ''.join([str(x) for x in position])
        if str_pos not in self.positions:
            self.create_seed_pos(position)

        probas = self.positions[str_pos]
        next_move = choice(9,p=[i/sum(probas) for i in probas])
        self.pos_memory[str_pos] = next_move

        return next_move



    def learn_from_game(self, result):
        for pos, pick in self.pos_memory.items():
            if result == self.mark:
                self.positions[pos][pick] += 3
            elif result == 3:
                self.positions[pos][pick] += 1
            else:
                self.positions[pos][pick] -= 1

        self.pos_memory = {}


    def probas_for_position(self, str_pos):
        pos = [int(i) for i in str_pos]
        import pdb; pdb.set_trace()
        if str_pos in self.positions:
            print(self.positions[str_pos])
            return
        for sym_name, sym in symmetries.items():
            str_pos = ''.join([str(x) for x in reorder(pos, sym)])
            if str_pos in self.positions:
                if sym_name == 'rg':
                    sym_opp = symmetries['rd']
                elif sym_name == 'rd':
                    sym_opp = symmetries['rg']
                else:
                    sym_opp = sym
                print(reorder(self.positions[str_pos], sym_opp))



class RandomIAPlayer(Player):

    def next_move(self, position):
        possible_moves = [i for i, e in enumerate(position) if e==0]
        next_move = random.choice(possible_moves)
        return next_move

class RealPlayer(Player):

    def next_move(self, position):
        corresp = {'1': 6, '2': 7, '3': 8, '4': 3, '5': 4, '6': 5, '7': 0, '8': 1, '9': 2}
        possible_moves = [i for i, e in enumerate(position) if e==0]
        next_move = prompt('next_move: ')
        next_move = corresp[next_move]
        while next_move not in possible_moves:
            next_move = prompt('try again: ')
            next_move = corresp[next_move]
        return next_move
