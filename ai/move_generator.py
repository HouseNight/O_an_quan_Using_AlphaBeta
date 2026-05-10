# ============================================================
# ai/move_generator.py
# Sinh nước đi hợp lệ cho người và máy
# ============================================================

from core.state import get_player_cells
from core.rules import is_side_empty, can_refill_side


def get_valid_moves(state, player, include_direction=False):
    """
    Thay cho hàm BuocDi() trong file cũ.

    Nếu include_direction = False:
        Trả về danh sách ô, ví dụ: [1, 2, 3, 4, 5]
        Dùng cho giao diện highlight ô.

    Nếu include_direction = True:
        Trả về cả ô và hướng, ví dụ:
        [(1, -1), (1, 1), (2, -1), (2, 1)]
        Dùng cho Alpha-Beta.
    """

    cells = get_player_cells(player)

    # Nếu bên đó hết quân nhưng đủ điểm rải lại,
    # xem như sau khi rải thì 5 ô đều đi được.
    if is_side_empty(state, player):
        if not can_refill_side(state, player):
            return []

        if include_direction:
            moves = []
            for cell in cells:
                moves.append((cell, -1))
                moves.append((cell, 1))
            return moves

        return cells[:]

    valid_cells = [cell for cell in cells if state[cell] > 0]

    if not include_direction:
        return valid_cells

    moves = []

    for cell in valid_cells:
        moves.append((cell, -1))
        moves.append((cell, 1))

    return moves