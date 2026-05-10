# ============================================================
# ai/alpha_beta.py
# Thuật toán Minimax + Alpha-Beta Pruning
# ============================================================

from core.rules import apply_move, is_game_over, finalize_game
from ai.move_generator import get_valid_moves
from ai.evaluation import evaluate


def alphabeta(state, depth, alpha, beta, maximizing_player):
    """
    Thay cho hàm DeQuy() trong file cũ.

    maximizing_player = True:
        Máy đi, cần chọn điểm lớn nhất.

    maximizing_player = False:
        Người đi, cần chọn điểm nhỏ nhất.
    """

    if depth == 0 or is_game_over(state):
        if is_game_over(state):
            state = finalize_game(state)
        return evaluate(state)

    if maximizing_player:
        player = "May"
        moves = get_valid_moves(state, player, include_direction=True)

        if not moves:
            return evaluate(finalize_game(state))

        best_value = -float("inf")

        for move in moves:
            new_state = apply_move(state, move, player)
            value = alphabeta(
                new_state,
                depth - 1,
                alpha,
                beta,
                False
            )

            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if alpha >= beta:
                break

        return best_value

    else:
        player = "Nguoi"
        moves = get_valid_moves(state, player, include_direction=True)

        if not moves:
            return evaluate(finalize_game(state))

        best_value = float("inf")

        for move in moves:
            new_state = apply_move(state, move, player)
            value = alphabeta(
                new_state,
                depth - 1,
                alpha,
                beta,
                True
            )

            best_value = min(best_value, value)
            beta = min(beta, best_value)

            if alpha >= beta:
                break

        return best_value


def get_best_move(state, depth=3):
    """
    Thay cho hàm MinimaxSearch() trong file cũ.

    Trả về nước đi tốt nhất cho máy.
    Kết quả dạng:
        (index, direction)

    Ví dụ:
        (9, -1)
    """

    best_value = -float("inf")
    best_move = None

    moves = get_valid_moves(state, "May", include_direction=True)

    for move in moves:
        new_state = apply_move(state, move, "May")

        value = alphabeta(
            new_state,
            depth - 1,
            -float("inf"),
            float("inf"),
            False
        )

        if value > best_value:
            best_value = value
            best_move = move

    return best_move