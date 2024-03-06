LOWERBOUND, EXACT, UPPERBOUND = -1, 0, 1
inf = float("infinity")


def expectimax(game, depth, origDepth, scoring, alpha=+inf, beta=-inf, tt=None):
    alphaOrig = alpha

    lookup = None if (tt is None) else tt.lookup(game)

    if lookup is not None:
        if lookup["depth"] >= depth:
            flag, value = lookup["flag"], lookup["value"]
            if flag == EXACT:
                if depth == origDepth:
                    game.ai_move = lookup["move"]
                return value
            elif flag == LOWERBOUND:
                alpha = max(alpha, value)
            elif flag == UPPERBOUND:
                beta = min(beta, value)

            if alpha >= beta:
                if depth == origDepth:
                    game.ai_move = lookup["move"]
                return value

    if (depth == 0) or game.is_over():
        return scoring(game) * (1 + 0.001 * depth)

    if lookup is not None:
        possible_moves = game.possible_moves()
        possible_moves.remove(lookup["move"])
        possible_moves = [lookup["move"]] + possible_moves

    else:
        possible_moves = game.possible_moves()

    state = game
    best_move = possible_moves[0]
    if depth == origDepth:
        state.ai_move = possible_moves[0]

    bestValue = -inf

    for move in possible_moves:
        move_nimbed = f"{move.split(',')[0]},{max(int(move.split(',')[1]), 1) - 1}"
        game.make_move(move, calculation=True)
        game.switch_player()

        move_alpha = -expectimax(game, depth - 1, origDepth, scoring, -beta, -alpha, tt)

        game.switch_player()
        game.unmake_move(move)

        game.make_move(move_nimbed, calculation=True)
        game.switch_player()

        move_alpha_nimbed = -expectimax(game, depth - 1, origDepth, scoring, -beta, -alpha, tt)

        game.switch_player()
        game.unmake_move(move_nimbed)

        if abs(move_alpha - move_alpha_nimbed) > 0.1:
            pass
        move_alpha = 0.1 * move_alpha_nimbed + 0.9 * move_alpha

        # bestValue = max( bestValue,  move_alpha )
        if bestValue < move_alpha:
            bestValue = move_alpha
            best_move = move

        if alpha < move_alpha:
            alpha = move_alpha
            # best_move = move
            if depth == origDepth:
                state.ai_move = move
            if alpha >= beta:
                break

    if tt is not None:

        assert best_move in possible_moves
        tt.store(
            game=state,
            depth=depth,
            value=bestValue,
            move=best_move,
            flag=UPPERBOUND
            if (bestValue <= alphaOrig)
            else (LOWERBOUND if (bestValue >= beta) else EXACT),
        )

    return bestValue


class Expectimax:
    def __init__(self, depth, scoring=None, win_score=+inf, tt=None):
        self.scoring = scoring
        self.depth = depth
        self.tt = tt
        self.win_score = win_score

    def __call__(self, game):
        scoring = (
            self.scoring if self.scoring else (lambda g: g.scoring())
        )  # horrible hack

        self.alpha = expectimax(
            game,
            self.depth,
            self.depth,
            scoring,
            -self.win_score,
            +self.win_score,
            self.tt,
        )
        return game.ai_move
