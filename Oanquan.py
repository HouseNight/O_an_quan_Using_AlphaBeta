# ============================================================
# main.py
# File chạy chính của game Ô Ăn Quan AI
# Chạy bằng lệnh:
#     python main.py
# ============================================================

import sys
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


# ============================================================
# 1. CẤU HÌNH ĐƯỜNG DẪN PROJECT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

# Cho phép import các file cùng thư mục main.py
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))


# ============================================================
# 2. KIỂM TRA FILE / THƯ MỤC CẦN CÓ
# ============================================================

def check_project_files():
    """
    Kiểm tra nhanh các file quan trọng trước khi chạy game.
    Không bắt buộc ảnh phải đủ vì game_ui_new.py có fallback vẽ bằng Canvas.
    """

    required_files = [
        BASE_DIR / "game_ui_new.py",
        BASE_DIR / "styles.py",
        BASE_DIR / "core" / "state.py",
        BASE_DIR / "core" / "rules.py",
        BASE_DIR / "ai" / "move_generator.py",
        BASE_DIR / "ai" / "alpha_beta.py",
    ]

    missing = []

    for file_path in required_files:
        if not file_path.exists():
            missing.append(str(file_path.relative_to(BASE_DIR)))

    return missing


def check_assets():
    """
    Kiểm tra ảnh trong thư mục images/.
    Thiếu ảnh vẫn chạy được, nhưng giao diện sẽ dùng hình vẽ Canvas thay thế.
    """

    asset_files = [
        BASE_DIR / "images" / "background.png",
        BASE_DIR / "images" / "board.png",
        BASE_DIR / "images" / "flag.png",
        BASE_DIR / "images" / "robot.png",
        BASE_DIR / "images" / "stone.png",
        BASE_DIR / "images" / "quan_left.png",
        BASE_DIR / "images" / "quan_right.png",
    ]

    missing_assets = []

    for file_path in asset_files:
        if not file_path.exists():
            missing_assets.append(str(file_path.relative_to(BASE_DIR)))

    return missing_assets


# ============================================================
# 3. HÀM MAIN CHẠY GAME
# ============================================================

def main():
    """
    Hàm main:
    - Kiểm tra file cần thiết.
    - Import giao diện Game_UI.
    - Tạo cửa sổ Tkinter.
    - Chạy vòng lặp game.
    """

    missing_files = check_project_files()

    if missing_files:
        root = tk.Tk()
        root.withdraw()

        messagebox.showerror(
            "Thiếu file project",
            "Không thể chạy game vì thiếu các file sau:\n\n"
            + "\n".join(f"- {file}" for file in missing_files)
            + "\n\nHãy kiểm tra lại cấu trúc thư mục core/ và ai/."
        )

        root.destroy()
        return

    missing_assets = check_assets()

    try:
        from game_ui_new import Game_UI

        root = tk.Tk()
        root.title("Ô Ăn Quan AI")

        app = Game_UI(root)

        if missing_assets:
            messagebox.showwarning(
                "Thiếu ảnh giao diện",
                "Một số ảnh chưa có trong thư mục images/:\n\n"
                + "\n".join(f"- {file}" for file in missing_assets)
                + "\n\nGame vẫn chạy, nhưng một số phần sẽ được vẽ bằng Canvas."
            )

        root.mainloop()

    except Exception as e:
        error_text = traceback.format_exc()

        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Lỗi khi chạy game",
                f"Game bị lỗi:\n\n{e}\n\nChi tiết lỗi đã được in ra Terminal."
            )
            root.destroy()
        except:
            pass

        print("========== LỖI KHI CHẠY GAME ==========")
        print(error_text)


# ============================================================
# 4. ĐIỂM BẮT ĐẦU CHƯƠNG TRÌNH
# ============================================================

if __name__ == "__main__":
    main()