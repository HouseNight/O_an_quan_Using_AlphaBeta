"""
styles.py
Cấu hình giao diện Ô Ăn Quan
"""

# =========================
# KÍCH THƯỚC CỬA SỔ
# =========================
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 720
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"

# =========================
# MÀU SẮC
# =========================
COLOR_BG = "#e8c56d"
COLOR_BG_DOT = "#d6b35a"

COLOR_BROWN = "#8a5114"
COLOR_BROWN_DARK = "#4a2a08"
COLOR_BROWN_LIGHT = "#b87927"

COLOR_PANEL = "#fff1c9"
COLOR_PANEL_GREEN = "#dce7b1"
COLOR_PANEL_OUTLINE = "#6f8e35"

COLOR_TEXT = "#332004"
COLOR_MUTED = "#6b4a18"

COLOR_RED = "#c83024"
COLOR_GREEN = "#5c9b39"
COLOR_GREEN_DARK = "#356b20"

COLOR_WHITE = "#fff8df"
COLOR_SHADOW = "#a3772f"

COLOR_HIGHLIGHT = "#fff176"
COLOR_HIGHLIGHT_OUTLINE = "#ef8a17"

COLOR_DISABLED = "#a68b50"
COLOR_STONE = "#d8d1c5"
COLOR_STONE_OUTLINE = "#8a8177"

COLOR_QUAN_LEFT = "#b9c0c9"
COLOR_QUAN_RIGHT = "#9a6b52"

# =========================
# FONT CHỮ
# =========================
FONT_TITLE = ("Segoe Print", 24, "bold")
FONT_SUBTITLE = ("Segoe Print", 13, "bold")
FONT_STATUS = ("Segoe Print", 16, "bold")
FONT_MENU = ("Segoe UI", 10)
FONT_CELL = ("Segoe Print", 15, "bold")
FONT_CELL_SMALL = ("Segoe UI", 10, "bold")
FONT_SCORE = ("Segoe Print", 18, "bold")
FONT_BUTTON = ("Segoe Print", 13, "bold")
FONT_NORMAL = ("Segoe UI", 11)

# =========================
# TÙY CHỌN HIỂN THỊ
# =========================
SHOW_CELL_INDEX = False      # ẩn số 0..11 cho gọn
SHOW_VALID_MOVE_HINT = True  # hiện viền ô hợp lệ

# =========================
# VỊ TRÍ TỔNG THỂ
# =========================
HEADER_BG_Y = 160

# =========================
# VỊ TRÍ BÀN CỜ
# =========================
BOARD_CENTER_X = 550
BOARD_CENTER_Y = 390

BOARD_X0 = 180
BOARD_Y0 = 240
BOARD_X1 = 920
BOARD_Y1 = 540


# Tọa độ lưới khớp với board.png
GRID_X_LINES = [286, 389, 488, 587, 688, 802]
GRID_Y_TOP = 276
GRID_Y_MID = 383
GRID_Y_BOTTOM = 498

LEFT_QUAN_BOX = (180, GRID_Y_TOP, 286, GRID_Y_BOTTOM)
RIGHT_QUAN_BOX = (802, GRID_Y_TOP, 920, GRID_Y_BOTTOM)

DAN_X0 = GRID_X_LINES[0]
DAN_X1 = GRID_X_LINES[-1]
DAN_Y0 = GRID_Y_TOP
DAN_Y1 = GRID_Y_BOTTOM

# =========================
# VỊ TRÍ BÀN CỜ
# =========================
BOARD_CENTER_X = 550
BOARD_CENTER_Y = 390

BOARD_X0 = 180
BOARD_Y0 = 240
BOARD_X1 = 920
BOARD_Y1 = 540

GRID_X_LINES = [286, 389, 488, 587, 688, 802]
GRID_Y_TOP = 276
GRID_Y_MID = 383
GRID_Y_BOTTOM = 498

LEFT_QUAN_BOX = (180, GRID_Y_TOP, 286, GRID_Y_BOTTOM)
RIGHT_QUAN_BOX = (802, GRID_Y_TOP, 920, GRID_Y_BOTTOM)

DAN_X0 = GRID_X_LINES[0]
DAN_X1 = GRID_X_LINES[-1]
DAN_Y0 = GRID_Y_TOP
DAN_Y1 = GRID_Y_BOTTOM

DAN_COL_W = (DAN_X1 - DAN_X0) / 5
DAN_ROW_H = GRID_Y_MID - GRID_Y_TOP

# =========================
# TÊN FILE ẢNH
# =========================
ASSET_BACKGROUND = "images/background.png"
ASSET_BOARD = "images/board.png"
ASSET_FLAG = "images/flag.png"
ASSET_ROBOT = "images/robot.png"
ASSET_STONE = "images/stone.png"
ASSET_QUAN_LEFT = "images/quan_left.png"
ASSET_QUAN_RIGHT = "images/quan_right.png"