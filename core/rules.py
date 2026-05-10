# ============================================================
# core/rules.py
# Luật chơi chính: rải quân, ăn quân, thiếu quân, kết thúc game
# ============================================================

from core.state import (
    O_QUAN,
    HUMAN_CELLS,
    AI_CELLS,
    HUMAN_SCORE_INDEX,
    AI_SCORE_INDEX,
    normalize_position,
    clone_state,
    get_player_cells,
)


def is_side_empty(state, player):
    """
    Kiểm tra 5 ô dân của một bên có hết quân không.
    """

    cells = get_player_cells(player)
    return all(state[i] == 0 for i in cells)


def can_refill_side(state, player):
    """
    Kiểm tra người chơi có đủ 5 điểm để rải lại quân khi thiếu quân không.
    """

    if player == "Nguoi":
        return state[HUMAN_SCORE_INDEX] >= 5

    if player == "May":
        return state[AI_SCORE_INDEX] >= 5

    return False


def refill_side_if_needed(state, player):
    """
    Thay cho logic ThieuQuan().

    Nếu 5 ô dân của bên đang chơi đều bằng 0:
    - Nếu đủ điểm: trừ 5 điểm, rải mỗi ô 1 quân.
    - Nếu không đủ điểm: giữ nguyên, game sẽ kết thúc.
    """

    new_state = clone_state(state)
    cells = get_player_cells(player)

    if not all(new_state[i] == 0 for i in cells):
        return new_state

    if player == "Nguoi":
        if new_state[HUMAN_SCORE_INDEX] >= 5:
            new_state[HUMAN_SCORE_INDEX] -= 5
            for i in cells:
                new_state[i] = 1

    elif player == "May":
        if new_state[AI_SCORE_INDEX] >= 5:
            new_state[AI_SCORE_INDEX] -= 5
            for i in cells:
                new_state[i] = 1

    return new_state


def finalize_game(state):
    """
    Cộng toàn bộ quân dân còn lại vào điểm khi kết thúc game.

    Người chơi lấy các ô 1-5.
    Máy lấy các ô 7-11.
    Hai ô quan 0 và 6 không cộng thêm vì đã được ăn trong quá trình chơi.
    """

    new_state = clone_state(state)

    human_remaining = sum(new_state[i] for i in HUMAN_CELLS)
    ai_remaining = sum(new_state[i] for i in AI_CELLS)

    new_state[HUMAN_SCORE_INDEX] += human_remaining
    new_state[AI_SCORE_INDEX] += ai_remaining

    for i in HUMAN_CELLS + AI_CELLS:
        new_state[i] = 0

    return new_state


def is_game_over(state):
    """
    Kiểm tra game kết thúc.

    Game kết thúc khi:
    - Hai ô quan đều hết quân.
    - Hoặc một bên hết quân dân và không đủ điểm để rải lại.
    """

    if state[0] == 0 and state[6] == 0:
        return True

    if is_side_empty(state, "Nguoi") and not can_refill_side(state, "Nguoi"):
        return True

    if is_side_empty(state, "May") and not can_refill_side(state, "May"):
        return True

    return False


def _move_with_direction(state, index, direction, player):
    """
    Hàm lõi xử lý rải quân và ăn quân.

    Đây là phần được tách từ hàm Move() trong loi_o_an_quan.py.
    direction:
        -1: đi ngược chiều
         1: đi thuận chiều
    """

    board = clone_state(state)

    if index in O_QUAN:
        return board

    if board[index] <= 0:
        return board

    current_pos = index
    stones = board[current_pos]
    board[current_pos] = 0

    eaten_score = 0
    end_turn = False

    while not end_turn:

        # Rải quân
        while stones > 0:
            current_pos = normalize_position(current_pos + direction)
            board[current_pos] += 1
            stones -= 1

        next_pos = normalize_position(current_pos + direction)
        next_next_pos = normalize_position(next_pos + direction)

        # Nếu ô kế tiếp là ô trống
        if board[next_pos] == 0:

            # Nếu ô sau ô trống cũng trống thì mất lượt
            if board[next_next_pos] == 0:
                end_turn = True

            # Nếu ô sau ô trống có quân thì ăn
            else:
                eaten_score += board[next_next_pos]
                board[next_next_pos] = 0

                current_pos = next_next_pos

                # Sau khi ăn, nếu ô kế tiếp có quân thì dừng lượt
                check_pos = normalize_position(current_pos + direction)
                if board[check_pos] > 0:
                    end_turn = True

        # Nếu ô kế tiếp có quân
        else:
            # Nếu ô kế tiếp là ô quan thì không được bốc tiếp
            if next_pos in O_QUAN:
                end_turn = True

            # Nếu là ô dân thì bốc lên rải tiếp
            else:
                stones = board[next_pos]
                board[next_pos] = 0
                current_pos = next_pos

    # Cộng điểm ăn được
    if player == "Nguoi":
        board[HUMAN_SCORE_INDEX] += eaten_score
    elif player == "May":
        board[AI_SCORE_INDEX] += eaten_score

    return board


def choose_best_direction(state, index, player):
    """
    Vì game_ui_new.py hiện tại chỉ click vào ô, chưa có nút chọn hướng trái/phải,
    nên hàm này tự chọn hướng tốt hơn cho nước đi đó.

    Nếu muốn đúng luật hơn, sau này có thể sửa UI để người chơi chọn -1 hoặc 1.
    """

    candidates = []

    for direction in [-1, 1]:
        next_state = _move_with_direction(state, index, direction, player)

        if player == "Nguoi":
            score = next_state[HUMAN_SCORE_INDEX] - next_state[AI_SCORE_INDEX]
        else:
            score = next_state[AI_SCORE_INDEX] - next_state[HUMAN_SCORE_INDEX]

        candidates.append((score, direction))

    candidates.sort(reverse=True)
    return candidates[0][1]


def apply_move(state, move, player):
    """
    Hàm được game_ui_new.py gọi.

    Có thể nhận:
    - move = index, ví dụ: 3
    - move = (index, direction), ví dụ: (3, -1)

    Nếu move chỉ là index thì chương trình tự chọn hướng tốt hơn.
    """

    working_state = refill_side_if_needed(state, player)

    if is_game_over(working_state):
        return finalize_game(working_state)

    if isinstance(move, (list, tuple)):
        index = move[0]
        direction = move[1]
    else:
        index = move
        direction = choose_best_direction(working_state, index, player)

    new_state = _move_with_direction(working_state, index, direction, player)

    if is_game_over(new_state):
        new_state = finalize_game(new_state)

    return new_state