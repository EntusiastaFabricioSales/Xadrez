from code.Piece import Piece

class Rook(Piece):
    
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = self.row, self.col
            while True:
                r += dr
                c += dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.get_piece(r, c)
                    if target is None:
                        moves.append((r, c))
                    elif target.color != self.color:
                        moves.append((r, c))
                        break
                    else:
                        break
                else:
                    break
        return moves
    
    def get_potential_moves(self, board):
        return self.get_valid_moves(board)