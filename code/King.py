from code.Piece import Piece

class King(Piece):

    def get_valid_moves(self, board):
        moves = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                r = self.row + dr
                c = self.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.get_piece(r, c)
                    if target is None or target and target.color != self.color:
                        if not board.is_square_attacked(self.color, r, c):
                            moves.append((r, c))

        #Roque
        if self.first_move and not board.is_square_attacked(self.color, self.row, self.col):
            row = self.row
            
            #Roque pequeno
            rook = board.get_piece(row, 7)
            if isinstance(rook, Piece):
                if rook and rook.first_move:
                    if all(board.get_piece(row, col) is None for col in [5, 6]):
                        if not board.is_square_attacked(self.color, row, 5) and not board.is_square_attacked(self.color, row, 6):
                            moves.append((row, 6))

            #Roque grande
            rook = board.get_piece(row, 0)
            if isinstance(rook, Piece):
                if rook and rook.first_move:
                    if all(board.get_piece(row, col) is None for col in [1, 2, 3]):
                        if not board.is_square_attacked(self.color, row, 2) and not board.is_square_attacked(self.color, row, 6):
                            moves.append((row, 2)) 

        return moves
    
    def get_potential_moves(self, board):
        moves = []

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r = self.row + dr
                c = self.col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    target = board.get_piece(r, c)
                    if target is None or target.color != self.color:
                        moves.append((r, c))
        return moves
