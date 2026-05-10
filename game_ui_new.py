import math
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import math
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

from core.state import initial_state
from core.rules import apply_move, is_game_over
from ai.move_generator import get_valid_moves
from ai.alpha_beta import get_best_move

from styles import *


DEPTH = 3
"""
Độ sâu mặc định:
AI nhìn trước 3 lượt để chọn nước đi tốt nhất.
"""


class Game_UI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎉 Ô Ăn Quan - Nhóm 024")
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.state = initial_state()
        self.current_player = "Nguoi"

        self.images = {}
        self.cell_boxes = {}
        self.selected_cell = None
        self.ai_last_move = None

        self.waiting_direction = False

        self.status_message = "👉 Lượt người chơi"
        self.timer = 35
        self.is_ai_thinking = False

        self.TaoMenu()
        self.load_assets()
        self.create_board()
        self.ThayDoi()
        self.tick_timer()

    # =========================
    # Load ảnh giao diện
    # =========================
    def load_assets(self):
        """
        Tự load ảnh nếu file tồn tại.
        Nếu thiếu ảnh, chương trình vẫn chạy bằng hình vẽ Canvas.
        """
        base_dir = Path(__file__).resolve().parent
        asset_names = {
            "background": ASSET_BACKGROUND,
            "board": ASSET_BOARD,
            "flag": ASSET_FLAG,
            "robot": ASSET_ROBOT,
            "stone": ASSET_STONE,
            "quan_left": ASSET_QUAN_LEFT,
            "quan_right": ASSET_QUAN_RIGHT,
        }

        for key, filename in asset_names.items():
            path = base_dir / filename
            if path.exists():
                try:
                    self.images[key] = tk.PhotoImage(file=str(path))
                except tk.TclError:
                    # Ảnh lỗi thì bỏ qua, dùng Canvas vẽ thay thế
                    pass

    # =========================
    # Tạo menu
    # =========================
    def TaoMenu(self):
        menu_bar = tk.Menu(self.root, font=FONT_MENU)

        game_menu = tk.Menu(menu_bar, tearoff=0, font=FONT_MENU)
        game_menu.add_command(label="Chơi mới", command=self.Newgame)
        game_menu.add_command(label="Hướng dẫn", command=self.HuongDan)
        game_menu.add_command(label="Thông tin", command=self.ThongTin)
        game_menu.add_separator()
        game_menu.add_command(label="Thoát", command=self.root.destroy)

        menu_bar.add_cascade(label="Menu", menu=game_menu)
        self.root.config(menu=menu_bar)

    # =========================
    # Tạo bàn cờ bằng Canvas
    # =========================
    def create_board(self):
        self.canvas = tk.Canvas(
            self.root,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=COLOR_BG,
            highlightthickness=0,
        )
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.build_cell_boxes()

    # =========================
    # Tọa độ các ô trên bàn cờ
    # =========================
    def build_cell_boxes(self):
        self.cell_boxes.clear()

        # Ô quan
        self.cell_boxes[0] = LEFT_QUAN_BOX
        self.cell_boxes[6] = RIGHT_QUAN_BOX

        # Hàng trên: Máy, index 1 -> 5
        for i in range(5):
            x0 = GRID_X_LINES[i]
            x1 = GRID_X_LINES[i + 1]
            self.cell_boxes[i + 1] = (x0, GRID_Y_TOP, x1, GRID_Y_MID)

        # Hàng dưới: Người chơi, hiển thị trái sang phải là 11, 10, 9, 8, 7
        bottom_indices = [11, 10, 9, 8, 7]

        for col, idx in enumerate(bottom_indices):
            x0 = GRID_X_LINES[col]
            x1 = GRID_X_LINES[col + 1]
            self.cell_boxes[idx] = (x0, GRID_Y_MID, x1, GRID_Y_BOTTOM)

    # =========================
    # Chơi mới
    # =========================
    def Newgame(self):
        self.state = initial_state()
        self.current_player = "Nguoi"
        self.selected_cell = None
        self.ai_last_move = None
        self.waiting_direction = False
        self.status_message = "👉 Lượt người chơi"
        self.timer = 35
        self.is_ai_thinking = False
        self.ThayDoi()

    # =========================
    # Cập nhật giao diện
    # =========================
    def ThayDoi(self):
        self.draw_scene()

    # =========================
    # Vẽ toàn bộ giao diện
    # =========================
    def draw_scene(self):
        c = self.canvas
        c.delete("all")

        self.draw_background()
        self.draw_header()
        self.draw_score_panel()
        self.draw_board()
        self.draw_status_bar()

        if self.waiting_direction and self.selected_cell is not None:
            self.draw_direction_panel()

    # =========================
    # Vẽ hướng chọn trái phải cho người chơi
    # =========================

    def draw_direction_panel(self):
        c = self.canvas

        # Tiêu đề chọn hướng
        c.create_rounded_rect(
            330, 560, 770, 605,
            18,
            fill=COLOR_PANEL_GREEN,
            outline=COLOR_PANEL_OUTLINE,
            width=3
        )

        c.create_text(
            550, 582,
            text=f"Chọn hướng đi cho ô {self.selected_cell}",
            font=FONT_CELL_SMALL,
            fill=COLOR_TEXT
        )

        # Nút trái
        c.create_rounded_rect(
            360, 615, 515, 660,
            18,
            fill=COLOR_BROWN_DARK,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )
        c.create_text(
            437, 638,
            text="← Trái",
            font=FONT_BUTTON,
            fill="white"
        )

        # Nút phải
        c.create_rounded_rect(
            585, 615, 740, 660,
            18,
            fill=COLOR_BROWN_DARK,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )
        c.create_text(
            662, 638,
            text="Phải →",
            font=FONT_BUTTON,
            fill="white"
        )

    # =========================
    # Vẽ nền
    # =========================
    def draw_background(self):
        c = self.canvas
        c.create_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fill=COLOR_BG, outline="")

        if "background" in self.images:
            c.create_image(WINDOW_WIDTH // 2, HEADER_BG_Y, image=self.images["background"])
        else:
            for x in range(0, WINDOW_WIDTH, 30):
                for y in range(0, WINDOW_HEIGHT, 30):
                    c.create_oval(x, y, x + 2, y + 2, fill=COLOR_BG_DOT, outline="")

            for x in [20, WINDOW_WIDTH - 40]:
                for y in range(0, WINDOW_HEIGHT, 70):
                    c.create_rectangle(
                        x, y, x + 18, y + 65,
                        fill=COLOR_GREEN,
                        outline=COLOR_GREEN_DARK,
                        width=2,
                    )

    # =========================
    # Vẽ tiêu đề + timer
    # =========================
    def draw_header(self):
        c = self.canvas

        c.create_text(
            WINDOW_WIDTH // 2, 48,
            text="Ô ĂN QUAN",
            font=FONT_TITLE,
            fill=COLOR_BROWN_DARK,
        )

        c.create_text(
            WINDOW_WIDTH // 2, 86,
            text=f"AI Alpha-Beta   |   Depth = {DEPTH}",
            font=FONT_SUBTITLE,
            fill=COLOR_MUTED,
        )

        # Timer
        c.create_rounded_rect(
            38, 35, 325, 98, 18,
            fill=COLOR_PANEL_GREEN,
            outline=COLOR_PANEL_OUTLINE,
            width=3
        )
        c.create_text(118, 66, text="Thời gian:", font=FONT_SUBTITLE, fill=COLOR_TEXT)
        c.create_text(248, 66, text=f"0 : {self.timer:02d}", font=FONT_SUBTITLE, fill="black")

        # Nút chơi mới
        c.create_rounded_rect(
            925, 35, 1060, 102, 22,
            fill=COLOR_BROWN_DARK,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )
        c.create_text(992, 68, text="Chơi mới", font=FONT_BUTTON, fill="white")

    # =========================
    # Vẽ bảng điểm
    # =========================
    def draw_score_panel(self):
        c = self.canvas
        score_nguoi = self.get_state_value(12, 0)
        score_may = self.get_state_value(13, 0)

        # Người
        c.create_rounded_rect(
            400, 130, 510, 205, 20,
            fill=COLOR_PANEL,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )
        c.create_text(455, 155, text="Người", font=FONT_CELL_SMALL, fill=COLOR_MUTED)
        c.create_text(455, 182, text=str(score_nguoi), font=FONT_SCORE, fill=COLOR_BROWN_DARK)

        # Máy
        c.create_rounded_rect(
            590, 130, 700, 205, 20,
            fill=COLOR_PANEL,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )
        c.create_text(645, 155, text="Máy", font=FONT_CELL_SMALL, fill=COLOR_MUTED)
        c.create_text(645, 182, text=str(score_may), font=FONT_SCORE, fill=COLOR_BROWN_DARK)

        # Cờ giữa
        c.create_line(550, 195, 550, 132, fill=COLOR_BROWN_DARK, width=3)
        c.create_polygon(550, 135, 610, 155, 550, 175, fill=COLOR_RED, outline="darkred")

    # =========================
    # Vẽ bàn cờ
    # =========================
    def draw_board(self):
        c = self.canvas

        # Bóng đổ nền bàn cờ
        c.create_rounded_rect(
            BOARD_X0 - 8, BOARD_Y0 + 12, BOARD_X1 + 10, BOARD_Y1 + 18,
            28,
            fill=COLOR_SHADOW,
            outline=""
        )

        # Nền trắng mờ phía sau
        c.create_rectangle(
            BOARD_X0 - 20, BOARD_Y0 - 8, BOARD_X1 + 20, BOARD_Y1 + 8,
            fill="#f8f4e8",
            outline=""
        )

        if "board" in self.images:
            c.create_image(BOARD_CENTER_X, BOARD_CENTER_Y, image=self.images["board"])
        else:
            self.draw_board_fallback()

        self.draw_board_lines_overlay()

        for idx in [0, 1, 2, 3, 4, 5, 6, 11, 10, 9, 8, 7]:
            box = self.cell_boxes[idx]
            count = self.get_state_value(idx, 0)
            is_quan = idx in (0, 6)
            self.draw_cell_content(idx, box, count, is_quan=is_quan)

    def draw_board_fallback(self):
        c = self.canvas
        c.create_rectangle(DAN_X0, DAN_Y0, DAN_X1, DAN_Y1, outline=COLOR_BROWN, width=4)
        c.create_oval(*LEFT_QUAN_BOX, outline=COLOR_BROWN, width=4)
        c.create_oval(*RIGHT_QUAN_BOX, outline=COLOR_BROWN, width=4)
        c.create_line(DAN_X0, DAN_Y0 + DAN_ROW_H, DAN_X1, DAN_Y0 + DAN_ROW_H, fill=COLOR_BROWN, width=3)
        for i in range(1, 5):
            x = DAN_X0 + i * DAN_COL_W
            c.create_line(x, DAN_Y0, x, DAN_Y1, fill=COLOR_BROWN, width=3)

    def draw_board_lines_overlay(self):
        c = self.canvas
        valid_moves = set(get_valid_moves(self.state, "Nguoi")) if self.current_player == "Nguoi" else set()

        for idx, box in self.cell_boxes.items():
            x0, y0, x1, y1 = box

            # Ô hợp lệ: viền cam mảnh
            if SHOW_VALID_MOVE_HINT and idx in valid_moves and idx != self.selected_cell:
                c.create_rounded_rect(
                    x0 + 6, y0 + 6, x1 - 6, y1 - 6,
                    14,
                    fill="",
                    outline=COLOR_HIGHLIGHT_OUTLINE,
                    width=2,
                )

            # Ô đang chọn / ô máy vừa đi
            if idx == self.selected_cell or idx == self.ai_last_move:
                c.create_rounded_rect(
                    x0 + 8, y0 + 8, x1 - 8, y1 - 8,
                    14,
                    fill="",
                    outline=COLOR_RED,
                    width=4,
                )

            # Ẩn số debug nếu không cần
            if SHOW_CELL_INDEX:
                c.create_text(
                    x0 + 18, y0 + 16,
                    text=str(idx),
                    font=FONT_CELL_SMALL,
                    fill=COLOR_MUTED,
                )

    # =========================
    # Vẽ quân trong ô
    # =========================
    def draw_cell_content(self, idx, box, count, is_quan=False):
        c = self.canvas
        x0, y0, x1, y1 = box
        cx = (x0 + x1) / 2
        cy = (y0 + y1) / 2

        if is_quan:
            color = COLOR_QUAN_LEFT if idx == 0 else COLOR_QUAN_RIGHT
            outline = "#6d747e" if idx == 0 else "#6b4735"
            c.create_oval(cx - 32, cy - 42, cx + 32, cy + 42, fill=color, outline=outline, width=3)
            c.create_text(cx, cy, text=str(count), font=FONT_CELL, fill=COLOR_TEXT)
            return

        # Vẽ tối đa 12 viên để không rối, số thật vẫn hiện ở giữa
        draw_count = min(int(count), 12)
        if draw_count > 0:
            radius_x = 30
            radius_y = 22
            for i in range(draw_count):
                angle = i * (2 * math.pi / max(draw_count, 1))
                sx = cx + radius_x * math.cos(angle)
                sy = cy + radius_y * math.sin(angle)
                c.create_oval(
                    sx - 9, sy - 6, sx + 9, sy + 6,
                    fill=COLOR_STONE,
                    outline=COLOR_STONE_OUTLINE,
                    width=1,
                )

        # Số quân trong ô
        c.create_oval(cx - 18, cy - 18, cx + 18, cy + 18, fill=COLOR_WHITE, outline=COLOR_BROWN_LIGHT, width=2)
        c.create_text(cx, cy, text=str(count), font=FONT_CELL, fill=COLOR_BROWN_DARK)

    # =========================
    # Thanh trạng thái
    # =========================
    def draw_status_bar(self):
        c = self.canvas

        c.create_rounded_rect(
            250, 665, 850, 715,
            20,
            fill=COLOR_PANEL,
            outline=COLOR_BROWN_LIGHT,
            width=3
        )

        if self.current_player == "Nguoi":
            text = self.status_message or "👉 Lượt người chơi"
        else:
            text = self.status_message or "🤖 Máy đang suy nghĩ..."

        c.create_text(
            550, 690,
            text=text,
            font=FONT_STATUS,
            fill=COLOR_BROWN_DARK
        )

    # =========================
    # Click chuột trên Canvas
    # =========================
    # =========================
# Click chuột trên Canvas
# =========================
    def on_canvas_click(self, event):
    # Nút chơi mới
        if 925 <= event.x <= 1060 and 35 <= event.y <= 102:
            self.Newgame()
            return

        if self.current_player != "Nguoi" or self.is_ai_thinking:
            return

        # Nếu đang chờ chọn hướng
        if self.waiting_direction and self.selected_cell is not None:
            # Nút trái
            if 360 <= event.x <= 515 and 615 <= event.y <= 660:
                self.player_move_with_direction(self.selected_cell, 1)
                return

            # Nút phải
            if 585 <= event.x <= 740 and 615 <= event.y <= 660:
                self.player_move_with_direction(self.selected_cell, -1)
                return

        index = self.get_cell_at(event.x, event.y)
        if index is None:
            return

        self.player_select_cell(index)

    def get_cell_at(self, x, y):
        """
        Lấy ô được click trên bàn cờ.
        Trả về index ô 0-11.
        Nếu click ngoài bàn cờ thì trả về None.
        """

        for idx, box in self.cell_boxes.items():
            x0, y0, x1, y1 = box

            if x0 <= x <= x1 and y0 <= y <= y1:
                return idx

        return None

    # =========================
    # Người chơi đi
    # =========================
    def player_select_cell(self, index):
        if self.current_player != "Nguoi":
            return

        valid_moves = get_valid_moves(self.state, "Nguoi")

        if index not in valid_moves:
            self.status_message = "⚠️ Ô này không đi được"
            self.ThayDoi()
            return

        self.selected_cell = index
        self.ai_last_move = None
        self.waiting_direction = True
        self.status_message = f"👉 Đã chọn ô {index}. Chọn hướng trái hoặc phải"
        self.ThayDoi()


    def player_move_with_direction(self, index, direction):
        if self.current_player != "Nguoi":
            return

        valid_moves = get_valid_moves(self.state, "Nguoi")

        if index not in valid_moves:
            self.status_message = "⚠️ Ô này không đi được"
            self.ThayDoi()
            return

        self.waiting_direction = False

        # direction = -1 là trái, direction = 1 là phải
        self.state = apply_move(self.state, (index, direction), "Nguoi")

        self.current_player = "May"
        self.status_message = "🤖 Máy đang suy nghĩ..."
        self.is_ai_thinking = True
        self.ThayDoi()

        if is_game_over(self.state):
            self.end_game()
        else:
            self.root.after(650, self.MayChoi)

    # =========================
    # Máy chơi bằng Alpha-Beta
    # =========================
    def MayChoi(self):
        if self.current_player != "May":
            return

        best_move = get_best_move(self.state, DEPTH)

        if best_move is not None:
            self.state = apply_move(self.state, best_move, "May")

            # best_move dạng (ô, hướng)
            move_index = best_move[0]
            move_direction = best_move[1]

            self.ai_last_move = move_index

            huong_text = "trái" if move_direction == -1 else "phải"
            self.status_message = f"👉 Lượt người chơi | Máy vừa đi ô {move_index}, hướng {huong_text}"

        else:
            self.status_message = "👉 Lượt người chơi"

        self.selected_cell = None
        self.current_player = "Nguoi"
        self.is_ai_thinking = False
        self.timer = 35
        self.ThayDoi()

        if is_game_over(self.state):
            self.end_game()

    # =========================
    # Kết thúc game
    # =========================
    def end_game(self):
        self.is_ai_thinking = False
        score_nguoi = self.get_state_value(12, 0)
        score_may = self.get_state_value(13, 0)

        if score_may > score_nguoi:
            result = "Máy thắng!"
        elif score_nguoi > score_may:
            result = "Người chơi thắng!"
        else:
            result = "Hòa!"

        messagebox.showinfo(
            "Kết thúc",
            f"Game Over!\n\nNgười chơi: {score_nguoi}\nMáy: {score_may}\n\n{result}",
        )

    # =========================
    # Timer trang trí
    # =========================
    def tick_timer(self):
        if self.current_player == "Nguoi" and not self.is_ai_thinking:
            self.timer -= 1
            if self.timer < 0:
                self.timer = 35
        self.ThayDoi()
        self.root.after(1000, self.tick_timer)

    # =========================
    # Helpers
    # =========================
    def get_state_value(self, index, default=0):
        try:
            return self.state[index]
        except (IndexError, TypeError):
            return default

    # =========================
    # Hướng dẫn
    # =========================
    def HuongDan(self):
        messagebox.showinfo(
            "Hướng dẫn",
            "Luật chơi Ô Ăn Quan:\n\n"
            "- Người chơi chọn một ô dân hợp lệ bên mình.\n"
            "- Chương trình sẽ gọi apply_move() để rải quân và ăn quân.\n"
            "- Sau lượt người chơi, máy dùng Alpha-Beta để nhìn trước nhiều lượt.\n"
            "- Ô viền vàng là ô có thể chọn.\n"
            "- Ô viền đỏ là ô vừa được chọn.\n"
        )

    # =========================
    # Thông tin
    # =========================
    def ThongTin(self):
        messagebox.showinfo(
            "Thông tin",
            "Đề tài: Ô Ăn Quan AI\n"
            "Thuật toán: Minimax + Alpha-Beta Pruning\n"
            f"Depth = {DEPTH}\n"
            "Giao diện: Tkinter Canvas + styles.py\n"
            "Nhóm 024"
        )


# =========================
# Bổ sung create_rounded_rect cho Canvas
# =========================
def _create_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return self.create_polygon(points, smooth=True, **kwargs)


# Gắn hàm vào tk.Canvas để gọi c.create_rounded_rect(...)
tk.Canvas.create_rounded_rect = _create_rounded_rect


# =========================
# Chạy chương trình
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    game = Game_UI(root)
    root.mainloop()
