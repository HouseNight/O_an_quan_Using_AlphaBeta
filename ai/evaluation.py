# ============================================================
# ai/evaluation.py
# Hàm đánh giá trạng thái bàn cờ cho AI
# ============================================================

from core.state import (
    HUMAN_CELLS,
    AI_CELLS,
    HUMAN_SCORE_INDEX,
    AI_SCORE_INDEX,
)


def evaluate(state):
    """
    Thay cho hàm DanhGia() trong file cũ.

    Điểm càng lớn thì càng có lợi cho máy.
    Điểm càng nhỏ thì càng có lợi cho người chơi.
    """

    score_human = state[HUMAN_SCORE_INDEX]
    score_ai = state[AI_SCORE_INDEX]

    human_stones = sum(state[i] for i in HUMAN_CELLS)
    ai_stones = sum(state[i] for i in AI_CELLS)

    # Trọng số:
    # - Điểm ăn được quan trọng nhất.
    # - Quân còn trên bàn chỉ là phụ.
    score_diff = score_ai - score_human
    stone_diff = ai_stones - human_stones

    return score_diff * 10 + stone_diff