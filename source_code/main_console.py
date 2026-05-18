from board import Board, HUMAN, AI
from ai import choose_move

def main():
    board = Board(9)
    depth = 3
    algorithm = 'minimax'
    print('=== CARO AI - CONSOLE ===')
    print('Nguoi choi: X | May: O')
    print('Nhap nuoc di theo dang: hang cot, vi du: 4 4')
    while True:
        board.print_board()
        try:
            r, c = map(int, input('Nhap nuoc di cua ban: ').strip().split())
        except Exception:
            print('Nhap sai. Vi du dung: 4 4')
            continue
        if not board.make_move(r, c, HUMAN):
            print('Nuoc di khong hop le.')
            continue
        if board.check_winner(HUMAN):
            board.print_board(); print('Ban thang!'); break
        if board.is_full():
            board.print_board(); print('Hoa!'); break
        info = choose_move(board, depth=depth, algorithm=algorithm)
        move = info['move']
        if move is None:
            board.print_board(); print('Hoa!'); break
        board.make_move(move[0], move[1], AI)
        print(f"May danh: {move} | score={info['score']} | nodes={info['nodes']} | time={info['time_ms']:.2f} ms")
        if board.check_winner(AI):
            board.print_board(); print('May thang!'); break
        if board.is_full():
            board.print_board(); print('Hoa!'); break

if __name__ == '__main__':
    main()
