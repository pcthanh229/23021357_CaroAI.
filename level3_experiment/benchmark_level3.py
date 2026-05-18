import csv
from board import Board, HUMAN, AI
from ai import choose_move

def make_board(moves):
    b = Board(9)
    for r, c, p in moves:
        b.make_move(r, c, p)
    return b

def test_states():
    return {
        '1_dau_van': [],
        '2_may_co_the_thang_ngay': [(4,3,AI), (4,4,AI), (4,5,AI), (3,3,HUMAN), (3,4,HUMAN)],
        '3_nguoi_sap_thang_can_chan': [(2,2,HUMAN), (2,3,HUMAN), (2,4,HUMAN), (4,4,AI), (5,5,AI)],
        '4_giua_van_can_bang': [(4,4,HUMAN), (4,5,AI), (5,4,HUMAN), (3,4,AI), (5,5,HUMAN), (3,5,AI)],
        '5_phuc_tap_nhieu_nhanh': [(4,4,HUMAN), (4,5,AI), (5,4,HUMAN), (3,4,AI), (5,5,HUMAN), (3,5,AI), (2,6,HUMAN), (6,2,AI), (6,6,HUMAN), (2,2,AI), (4,3,HUMAN), (4,6,AI)],
    }

def main():
    rows = []
    for name, moves in test_states().items():
        for depth in [1, 2, 3]:
            for algorithm in ['minimax', 'alphabeta']:
                board = make_board(moves)
                info = choose_move(board, depth=depth, algorithm=algorithm)
                row = {'state': name, 'depth': depth, 'algorithm': algorithm, 'move': info['move'], 'score': info['score'], 'nodes': info['nodes'], 'time_ms': round(info['time_ms'], 3)}
                rows.append(row)
                print(row)
    with open('benchmark_results.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['state', 'depth', 'algorithm', 'move', 'score', 'nodes', 'time_ms'])
        writer.writeheader(); writer.writerows(rows)
    print('
Da tao file benchmark_results.csv')

if __name__ == '__main__':
    main()
