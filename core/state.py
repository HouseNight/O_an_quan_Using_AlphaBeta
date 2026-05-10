# ============================================================
# core/state.py
# Quản lý trạng thái ban đầu của bàn cờ Ô Ăn Quan
# ============================================================

# Index bàn cờ:
# 0  = Ô quan trái
# 1-5 = Ô dân máy, nằm hàng trên
# 6  = Ô quan phải
# 7-11 = Ô dân người chơi, nằm hàng dưới
# 12 = Điểm người chơi
# 13 = Điểm máy

LEFT_QUAN = 0
RIGHT_QUAN = 6

# ĐỔI 2 DÒNG NÀY
AI_CELLS = [1, 2, 3, 4, 5]
HUMAN_CELLS = [7, 8, 9, 10, 11]

HUMAN_SCORE_INDEX = 12
AI_SCORE_INDEX = 13

O_QUAN = [LEFT_QUAN, RIGHT_QUAN]


def initial_state():
    """
    Tạo trạng thái ban đầu.

    Mỗi ô dân có 5 quân.
    Mỗi ô quan có 10 điểm.
    Điểm người và điểm máy ban đầu bằng 0.
    """

    board = [
        10,     # 0: quan trái
        5, 5, 5, 5, 5,     # 1-5: người
        10,     # 6: quan phải
        5, 5, 5, 5, 5,     # 7-11: máy
        0,      # 12: điểm người
        0       # 13: điểm máy
    ]

    return board


def clone_state(state):
    """
    Sao chép state để tránh làm thay đổi bàn cờ gốc khi AI giả lập.
    """
    return state[:]


def normalize_position(pos):
    """
    Thay cho hàm SuaViTri() trong file cũ.
    Đưa vị trí về vòng 0 -> 11.
    """

    if pos < 0:
        return 11

    if pos > 11:
        return 0

    return pos


def get_score(state, player):
    """
    Lấy điểm theo người chơi.
    """

    if player == "Nguoi":
        return state[HUMAN_SCORE_INDEX]

    if player == "May":
        return state[AI_SCORE_INDEX]

    raise ValueError("player phải là 'Nguoi' hoặc 'May'")


def get_player_cells(player):
    """
    Trả về danh sách ô dân của người hoặc máy.
    """

    if player == "Nguoi":
        return HUMAN_CELLS

    if player == "May":
        return AI_CELLS

    raise ValueError("player phải là 'Nguoi' hoặc 'May'")