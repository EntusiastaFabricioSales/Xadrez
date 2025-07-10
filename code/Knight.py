from code.Piece import Piece

class Knight(Piece):

    def get_valid_moves(self, board):
        moves = []
        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1),
                      (-1, -2), (-1, 2), (1, -2), (1, 2)]
        
        for dr, dc in directions:
            r = dr + self.row
            c = dc + self.col

            if 0 <= r < 8 and 0 <= c < 8:
                target = board.get_piece(r, c)
                if target is None or target and target.color != self.color:
                    moves.append((r, c))

        return moves
    
    def get_potential_moves(self, board):
        return self.get_valid_moves(board)
