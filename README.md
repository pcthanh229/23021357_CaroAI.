# CaroAI 3 Levels - Bản đã sửa lỗi

Bản này dùng **tkinter** cho giao diện, nên **không cần cài pygame**.

## Yêu cầu

- Python 3.x
- Không cần thư viện ngoài

## Chạy nhanh bản giao diện

Có thể bấm đúp file:

```text
RUN_GUI.bat
```

Hoặc mở CMD tại thư mục project và chạy:

```bash
cd source_code
python main.py
```

## Chạy theo đúng 3 Level

### Level 1 - Minimax console

```bash
cd level1_minimax
python main_level1.py
```

### Level 2 - Alpha-Beta + giao diện tkinter

```bash
cd level2_alphabeta_gui
python main_level2_gui.py
```

### Level 3 - Thực nghiệm benchmark

```bash
cd level3_experiment
python benchmark_level3.py
```

Sau khi chạy Level 3, chương trình tạo file `benchmark_results.csv`.

## Nội dung đáp ứng đề bài

- Bàn cờ 9x9.
- Người chơi là X, máy là O.
- Thắng khi có 4 quân liên tiếp theo hàng ngang, dọc hoặc chéo.
- Không xét luật chặn hai đầu.
- Có Minimax giới hạn độ sâu.
- Có Alpha-Beta pruning.
- Có hàm đánh giá trạng thái.
- Có đo số trạng thái đã xét và thời gian chạy.
- Có benchmark 5 trạng thái kiểm thử.


## Sửa lỗi v2
File `source_code/main.py` đã được sửa để tự mở cửa sổ Tkinter khi chạy `python main.py`. Nếu bấm `RUN_GUI.bat`, chương trình tự chuyển vào `source_code` và chạy game.

## Ghi chú về file .bat
- `RUN_GUI.bat` chỉ là file chạy nhanh, có thể xóa mà không ảnh hưởng source code.
- Nếu xóa file này, chạy game bằng lệnh: `cd source_code` rồi `python main.py`.
- `RUN_BENCHMARK.bat` cũng chỉ là file tiện ích để chạy benchmark nhanh.
