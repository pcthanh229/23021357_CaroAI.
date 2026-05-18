import tkinter as tk
from tkinter import messagebox
from board import Board, HUMAN, AI
from ai import choose_move

BOARD_SIZE = 9
CELL = 48
MARGIN = 38
BOARD_PX = CELL * BOARD_SIZE
CANVAS_W = BOARD_PX + MARGIN * 2
CANVAS_H = BOARD_PX + MARGIN * 2

BG = '#0f1220'
PANEL = '#171a2b'
BOARD_BG = '#111426'
GRID = '#2f344d'
GRID_BOLD = '#414866'
TEXT = '#f1f5f9'
MUTED = '#aab3c5'
X_COLOR = '#2dd4bf'
O_COLOR = '#fb3d72'
ACCENT = '#7c3aed'
LAST = '#facc15'
HOVER = '#27304a'

class CaroApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Caro AI - Minimax & Alpha-Beta')
        self.root.geometry('760x720')
        self.root.minsize(720, 680)
        self.root.configure(bg=BG)

        self.board = Board(BOARD_SIZE)
        self.algorithm = tk.StringVar(value='alphabeta')
        self.depth = tk.IntVar(value=3)
        self.game_over = False
        self.last_move = None
        self.hover_cell = None

        self.build_ui()
        self.draw_board()

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill='x', padx=18, pady=(14, 8))

        title_box = tk.Frame(header, bg=BG)
        title_box.pack(side='left')
        tk.Label(title_box, text='CARO AI', font=('Segoe UI', 24, 'bold'), fg=TEXT, bg=BG).pack(anchor='w')
        tk.Label(title_box, text='Người chơi X  •  Máy O  •  Thắng khi có 4 quân liên tiếp',
                 font=('Segoe UI', 10), fg=MUTED, bg=BG).pack(anchor='w')

        control = tk.Frame(header, bg=PANEL, bd=0, highlightthickness=1, highlightbackground='#252a42')
        control.pack(side='right', padx=4, pady=2)

        tk.Label(control, text='AI', fg=MUTED, bg=PANEL, font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, padx=(14, 4), pady=(10, 2), sticky='w')
        alg = tk.OptionMenu(control, self.algorithm, 'minimax', 'alphabeta')
        self.style_option(alg)
        alg.grid(row=1, column=0, padx=(12, 6), pady=(0, 12))

        tk.Label(control, text='DEPTH', fg=MUTED, bg=PANEL, font=('Segoe UI', 9, 'bold')).grid(row=0, column=1, padx=4, pady=(10, 2), sticky='w')
        dep = tk.OptionMenu(control, self.depth, 1, 2, 3, 4)
        self.style_option(dep)
        dep.grid(row=1, column=1, padx=6, pady=(0, 12))

        reset_btn = tk.Button(control, text='Ván mới', command=self.reset, bg=ACCENT, fg='white',
                              activebackground='#6d28d9', activeforeground='white', bd=0,
                              font=('Segoe UI', 10, 'bold'), padx=16, pady=7, cursor='hand2')
        reset_btn.grid(row=1, column=2, padx=(6, 14), pady=(0, 12))

        self.status = tk.Label(self.root, text='Lượt của bạn: bấm vào ô để đánh X.',
                               font=('Segoe UI', 12, 'bold'), fg=TEXT, bg=BG)
        self.status.pack(fill='x', padx=18, pady=(0, 8))

        board_frame = tk.Frame(self.root, bg=PANEL, highlightthickness=1, highlightbackground='#252a42')
        board_frame.pack(padx=18, pady=2)
        self.canvas = tk.Canvas(board_frame, width=CANVAS_W, height=CANVAS_H,
                                bg=BOARD_BG, highlightthickness=0, cursor='hand2')
        self.canvas.pack(padx=12, pady=12)
        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<Motion>', self.on_motion)
        self.canvas.bind('<Leave>', self.on_leave)

        self.info = tk.Label(self.root, text='Nước máy: -    |    Score: 0    |    Nodes: 0    |    Time: 0 ms',
                             font=('Consolas', 10), fg=MUTED, bg=BG)
        self.info.pack(fill='x', padx=18, pady=(8, 2))

        self.tip = tk.Label(self.root, text='Gợi ý: dùng Alpha-Beta với depth 3 hoặc 4 để AI chơi nhanh hơn.',
                            font=('Segoe UI', 9), fg='#7dd3fc', bg=BG)
        self.tip.pack(fill='x', padx=18, pady=(0, 10))

    def style_option(self, widget):
        widget.configure(bg='#232840', fg=TEXT, activebackground='#303653', activeforeground=TEXT,
                         bd=0, highlightthickness=0, font=('Segoe UI', 10), padx=8, pady=5)
        widget['menu'].configure(bg='#232840', fg=TEXT, activebackground=ACCENT, activeforeground='white')

    def reset(self):
        self.board = Board(BOARD_SIZE)
        self.game_over = False
        self.last_move = None
        self.hover_cell = None
        self.status.config(text='Lượt của bạn: bấm vào ô để đánh X.', fg=TEXT)
        self.info.config(text='Nước máy: -    |    Score: 0    |    Nodes: 0    |    Time: 0 ms')
        self.draw_board()

    def cell_from_event(self, event):
        c = (event.x - MARGIN) // CELL
        r = (event.y - MARGIN) // CELL
        if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
            return int(r), int(c)
        return None

    def on_motion(self, event):
        cell = self.cell_from_event(event)
        if cell != self.hover_cell:
            self.hover_cell = cell
            self.draw_board()

    def on_leave(self, event):
        self.hover_cell = None
        self.draw_board()

    def draw_board(self):
        self.canvas.delete('all')

        # Nền bàn cờ bo góc giả lập bằng hình chữ nhật lớn
        self.canvas.create_rectangle(MARGIN, MARGIN, MARGIN + BOARD_PX, MARGIN + BOARD_PX,
                                     fill=BOARD_BG, outline='#24293f', width=2)

        # Hover cell
        if self.hover_cell and not self.game_over:
            r, c = self.hover_cell
            if self.board.grid[r][c] == 0:
                x1 = MARGIN + c * CELL
                y1 = MARGIN + r * CELL
                self.canvas.create_rectangle(x1+2, y1+2, x1+CELL-2, y1+CELL-2,
                                             fill=HOVER, outline='')

        # Last move highlight
        if self.last_move:
            r, c = self.last_move
            x1 = MARGIN + c * CELL
            y1 = MARGIN + r * CELL
            self.canvas.create_rectangle(x1+4, y1+4, x1+CELL-4, y1+CELL-4,
                                         outline=LAST, width=2)

        # Grid + tọa độ
        for i in range(BOARD_SIZE + 1):
            x = MARGIN + i * CELL
            y = MARGIN + i * CELL
            color = GRID_BOLD if i in (0, BOARD_SIZE) else GRID
            width = 2 if i in (0, BOARD_SIZE) else 1
            self.canvas.create_line(MARGIN, y, MARGIN + BOARD_PX, y, fill=color, width=width)
            self.canvas.create_line(x, MARGIN, x, MARGIN + BOARD_PX, fill=color, width=width)

        for i in range(BOARD_SIZE):
            cx = MARGIN + i * CELL + CELL / 2
            cy = MARGIN + i * CELL + CELL / 2
            self.canvas.create_text(cx, 20, text=str(i + 1), fill=MUTED, font=('Segoe UI', 9, 'bold'))
            self.canvas.create_text(20, cy, text=str(i + 1), fill=MUTED, font=('Segoe UI', 9, 'bold'))

        # Quân cờ
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x1 = MARGIN + c * CELL
                y1 = MARGIN + r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL
                piece = self.board.grid[r][c]
                if piece == HUMAN:
                    self.draw_x(x1, y1, x2, y2)
                elif piece == AI:
                    self.draw_o(x1, y1, x2, y2)

    def draw_x(self, x1, y1, x2, y2):
        pad = 15
        self.canvas.create_line(x1+pad, y1+pad, x2-pad, y2-pad, fill=X_COLOR, width=4, capstyle='round')
        self.canvas.create_line(x1+pad, y2-pad, x2-pad, y1+pad, fill=X_COLOR, width=4, capstyle='round')

    def draw_o(self, x1, y1, x2, y2):
        pad = 13
        self.canvas.create_oval(x1+pad, y1+pad, x2-pad, y2-pad, outline=O_COLOR, width=4)
        self.canvas.create_oval(x1+pad+6, y1+pad+6, x2-pad-6, y2-pad-6, outline='#ff86a5', width=1)

    def on_click(self, event):
        if self.game_over:
            return
        cell = self.cell_from_event(event)
        if not cell:
            return
        r, c = cell
        if not self.board.make_move(r, c, HUMAN):
            return
        self.last_move = (r, c)
        self.draw_board()

        if self.board.check_winner(HUMAN):
            self.finish_game('Bạn thắng!', X_COLOR)
            return
        if self.board.is_full():
            self.finish_game('Hòa!', LAST)
            return

        self.status.config(text='Máy đang suy nghĩ...', fg='#7dd3fc')
        self.root.update_idletasks()

        info = choose_move(self.board, depth=self.depth.get(), algorithm=self.algorithm.get())
        move = info['move']
        if move:
            self.board.make_move(move[0], move[1], AI)
            self.last_move = move

        self.draw_board()
        display_move = (move[0] + 1, move[1] + 1) if move else None
        self.info.config(text=f"Nước máy: {display_move}    |    Score: {info['score']}    |    Nodes: {info['nodes']}    |    Time: {info['time_ms']:.2f} ms")

        if self.board.check_winner(AI):
            self.finish_game('Máy thắng!', O_COLOR)
        elif self.board.is_full():
            self.finish_game('Hòa!', LAST)
        else:
            self.status.config(text=f"Lượt của bạn. AI = {self.algorithm.get()} | depth = {self.depth.get()}", fg=TEXT)

    def finish_game(self, text, color):
        self.game_over = True
        self.status.config(text=text, fg=color)
        messagebox.showinfo('Kết quả', text)

if __name__ == '__main__':
    root = tk.Tk()
    app = CaroApp(root)
    root.mainloop()
