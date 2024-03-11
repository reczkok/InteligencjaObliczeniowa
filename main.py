from easyAI import TwoPlayerGame
import random
import time
from copy import deepcopy

from Expectiminimax import Expectimax
from NegamaxNoABP import NegamaxNoABP
from Negamax import Negamax


class NimNonD(TwoPlayerGame):
    def __init__(self, players=None, max_removals_per_turn=None, piles=(5, 5, 5, 5), start_player=1):
        """ Default for `piles` is 5 piles of 5 pieces. """
        self.players = players
        self.piles = list(piles)
        self.max_removals_per_turn = max_removals_per_turn
        self.current_player = start_player
        self.player_1_times = []
        self.player_2_times = []
        self.nimbed = False

    def possible_moves(self):
        return [
            "%d,%d" % (i + 1, j)
            for i in range(len(self.piles))
            for j in range(
                1,
                self.piles[i] + 1
                if self.max_removals_per_turn is None
                else min(self.piles[i] + 1, self.max_removals_per_turn),
            )
        ]

    def make_move(self, move, calculation=False):
        move = list(map(int, move.split(",")))
        if calculation:
            self.piles[move[0] - 1] -= move[1]
            return
        if random.random() < 0.1:
            self.nimbed = True
            self.piles[move[0] - 1] -= move[1] - 1
        else:
            self.nimbed = False
            self.piles[move[0] - 1] -= move[1]

    def unmake_move(self, move):
        move = list(map(int, move.split(",")))
        self.piles[move[0] - 1] += move[1]

    def show(self):
        print(" ".join(map(str, self.piles)))

    def win(self):
        return max(self.piles) == 0

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0

    def ttentry(self):
        return tuple(self.piles)  # optional, speeds up AI

    def play(self, nmoves=1000, verbose=True):
        history = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):

            if self.is_over():
                break

            start = time.time()
            move = self.player.ask_move(self)
            end = time.time()
            if self.current_player == 1:
                self.player_1_times.append(end - start)
            else:
                self.player_2_times.append(end - start)
            history.append((deepcopy(self), move))
            self.make_move(move)

            if verbose:
                print(
                    "\nMove #%d: player %d plays %s :"
                    % (self.nmove, self.current_player, str(move))
                )
                if self.nimbed:
                    print("Nimbed!")
                self.show()

            self.switch_player()

        history.append(deepcopy(self))

        return history

    def get_avg_time(self, player):
        if player == 1:
            return sum(self.player_1_times) / len(self.player_1_times)
        else:
            return sum(self.player_2_times) / len(self.player_2_times)


class Nim(TwoPlayerGame):
    def __init__(self, players=None, max_removals_per_turn=None, piles=(5, 5, 5, 5), start_player=1):
        """ Default for `piles` is 5 piles of 5 pieces. """
        self.players = players
        self.piles = list(piles)
        self.max_removals_per_turn = max_removals_per_turn
        self.current_player = start_player
        self.player_1_times = []
        self.player_2_times = []

    def possible_moves(self):
        return [
            "%d,%d" % (i + 1, j)
            for i in range(len(self.piles))
            for j in range(
                1,
                self.piles[i] + 1
                if self.max_removals_per_turn is None
                else min(self.piles[i] + 1, self.max_removals_per_turn),
            )
        ]

    def make_move(self, move, calculation=False):
        move = list(map(int, move.split(",")))
        self.piles[move[0] - 1] -= move[1]

    def unmake_move(self, move):  # optional, speeds up the AI
        move = list(map(int, move.split(",")))
        self.piles[move[0] - 1] += move[1]

    def show(self):
        print(" ".join(map(str, self.piles)))

    def win(self):
        return max(self.piles) == 0

    def is_over(self):
        return self.win()

    def scoring(self):
        return 100 if self.win() else 0

    def ttentry(self):
        return tuple(self.piles)  # optional, speeds up AI

    def play(self, nmoves=1000, verbose=True):
        history = []

        if verbose:
            self.show()

        for self.nmove in range(1, nmoves + 1):

            if self.is_over():
                break

            start = time.time()
            move = self.player.ask_move(self)
            end = time.time()
            if self.current_player == 1:
                self.player_1_times.append(end - start)
            else:
                self.player_2_times.append(end - start)
            history.append((deepcopy(self), move))
            self.make_move(move)

            if verbose:
                print(
                    "\nMove #%d: player %d plays %s :"
                    % (self.nmove, self.current_player, str(move))
                )
                self.show()

            self.switch_player()

        history.append(deepcopy(self))

        return history

    def get_avg_time(self, player):
        if player == 1:
            return sum(self.player_1_times) / len(self.player_1_times)
        else:
            return sum(self.player_2_times) / len(self.player_2_times)

def run_game(n,f, depth=2):
    ai1 = Expectimax(depth)
    ai2 = Negamax(depth)

    ai1_score = 0
    ai2_score = 0
    ai1_times = []
    ai2_times = []

    for i in range(n):
        game = NimNonD([AI_Player(ai1), AI_Player(ai2)], start_player=i % 2 + 1)
        print(f"Game {i + 1}")
        if i % 50 == 0:
            game.play(verbose=True)
            print('Player 1 avg time:', game.get_avg_time(1))
            print('Player 2 avg time:', game.get_avg_time(2))
        else:
            game.play(verbose=False)
        ai1_times.append(game.get_avg_time(1))
        ai2_times.append(game.get_avg_time(2))
        player = game.current_player
        if player == 1:
            ai1_score += game.win()
        else:
            ai2_score += game.win()

    print(f"AI 1 score: {ai1_score}")
    print(f"AI 2 score: {ai2_score}")
    print(f"AI 1 avg time: {sum(ai1_times) / len(ai1_times)}")
    print(f"AI 2 avg time: {sum(ai2_times) / len(ai2_times)}")

    f.write(f"{ai1_score},{ai2_score},{sum(ai1_times) / len(ai1_times)},{sum(ai2_times) / len(ai2_times)}\n")



if __name__ == "__main__":

    from easyAI import AI_Player


    for DEPTH in [3, 5]:
        N = 100
        open(f'data_depth{DEPTH}_expecti.csv', 'w').close()
        f = open(f"data_depth{DEPTH}.csv", "a")
        f.write("ai1_score,ai2_score,ai1_avg_time,ai2_avg_time\n")
        for i in range(N):
            print(f"--------------Game {i + 1}, Depth {DEPTH} --------------")
            run_game(100, f, DEPTH)