# Ô ăn quan sử dụng thuật toán AlphaBeta

Sử dụng python để Mô phỏng game Ô ăn quan với giao diện UI

Sử dụng DEPTH = 3  <=> chế độ chơi Trung bình 

Code by Phúc Hiệp, Nam, Long Ngô


## Cách sử dụng:

Run Oanquan.py to play game

## Chi tiết các Folder:

ui/   → giao diện người dùng bằng Tkinter
core/ → luật chơi và trạng thái bàn cờ
ai/   → thuật toán AI Alpha-Beta

## 1. Thư mục ui/

Thư mục ui/ chứa toàn bộ phần giao diện của game. Đây là nơi người dùng nhìn thấy bàn cờ, quân, điểm số, nút chơi mới, thanh trạng thái và thao tác click chuột.

main.py

Đây là file chạy chính của chương trình.

Nhiệm vụ:

- Khởi động chương trình.
- Kiểm tra các file cần thiết.
- Import class Game_UI từ game_ui_new.py.
- Tạo cửa sổ Tkinter.
- Chạy vòng lặp giao diện root.mainloop().

## 2. Thư mục core/

Thư mục core/ chứa phần luật chơi chính và trạng thái bàn cờ.

### core/state.py

File này quản lý trạng thái bàn cờ.

Nhiệm vụ:

- Khai báo các ô trên bàn cờ.
- Khai báo ô nào là của người chơi.
- Khai báo ô nào là của máy.
- Khai báo vị trí lưu điểm người và điểm máy.
- Tạo trạng thái ban đầu của ván game.

Quy ước hiện tại nếu bạn đã sửa người chơi nằm dưới:

0     = Ô quan trái
1-5   = Ô dân của máy, nằm hàng trên
6     = Ô quan phải
7-11  = Ô dân của người chơi, nằm hàng dưới
12    = Điểm người chơi
13    = Điểm máy

| Hàm                    | Nhiệm vụ                                    |
| ---------------------- | ------------------------------------------- |
| `initial_state()`      | Tạo bàn cờ ban đầu                          |
| `clone_state()`        | Sao chép state để không làm hỏng bàn cờ gốc |
| `normalize_position()` | Đưa vị trí về vòng 0 đến 11                 |
| `get_score()`          | Lấy điểm người hoặc máy                     |
| `get_player_cells()`   | Lấy danh sách ô dân của người hoặc máy      |


### core/rules.py

Đây là file xử lý luật chơi quan trọng nhất.

Nhiệm vụ:

- Kiểm tra bên nào hết quân.
- Xử lý mượn quân khi thiếu quân.
- Xử lý rải quân.
- Xử lý ăn quân.
- Xử lý kết thúc game.
- Cộng quân còn lại khi game kết thúc.

Các hàm chính:

Hàm	Nhiệm vụ
is_side_empty()	Kiểm tra 5 ô dân của một bên có hết quân không
refill_side_if_needed()	Nếu hết quân thì rải lại mỗi ô 1 quân và trừ 5 điểm
finalize_game()	Cộng quân còn lại vào điểm khi kết thúc
is_game_over()	Kiểm tra game kết thúc chưa
_move_with_direction()	Hàm lõi xử lý rải quân và ăn quân
choose_best_direction()	Tự chọn hướng tốt nếu không truyền hướng
apply_move()	Hàm chính để thực hiện một nước đi

## 3. Thư mục ai/

Thư mục ai/ chứa toàn bộ phần trí tuệ nhân tạo của máy.

### ai/move_generator.py

File này sinh ra các nước đi hợp lệ cho người hoặc máy.

Nhiệm vụ:

- Kiểm tra bên đang chơi có những ô nào có thể đi.
- Nếu include_direction=False thì chỉ trả về danh sách ô.
- Nếu include_direction=True thì trả về cả ô và hướng.

### ai/evaluation.py

File này chứa hàm đánh giá bàn cờ.

Nhiệm vụ:

- Tính xem trạng thái hiện tại đang có lợi cho máy hay người.
- Trả về một con số điểm.
- Điểm càng lớn thì càng có lợi cho máy.
- Điểm càng nhỏ thì càng có lợi cho người chơi.

Hàm chính:

evaluate(state)

Cách đánh giá thường dùng:

Điểm đánh giá = điểm máy - điểm người

### ai/alpha_beta.py

Đây là file xử lý thuật toán AI chính.

Nhiệm vụ:

- Duyệt cây trạng thái game.
- Giả lập nhiều nước đi trong tương lai.
- Dùng Minimax để chọn nước tốt.
- Dùng Alpha-Beta để cắt tỉa nhánh không cần xét.

Các hàm chính:

Hàm	Nhiệm vụ
alphabeta()	Hàm đệ quy Alpha-Beta
get_best_move()	Tìm nước đi tốt nhất cho máy
