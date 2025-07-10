from code.Piece import Piece

class Pawn(Piece):

    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == "white" else 1
        start_row = 6 if self.color == "white" else 1

        #avanço normal
        front_row = self.row + direction
        if 0 <= front_row < 8 and board.get_piece(front_row, self.col) is None:
            moves.append((front_row, self.col))
            if self.row == start_row:
                next_row = front_row + direction
                if board.get_piece(next_row, self.col) is None:
                    moves.append((next_row, self.col))

        #captura diagonal
        for dc in [-1, 1]:
            col = self.col + dc
            if 0 <= col < 8 and 0 <= front_row < 8:
                target = board.get_piece(front_row, col)
                if target and target.color != self.color:
                    moves.append((front_row, col))

        #En passant
        if board.en_passant_target:
            ep_row, ep_col = board.en_passant_target
            if 0 <= ep_row < 8 and 0 <= ep_col < 8:
                if ep_row == self.row + direction and abs(ep_col - self.col) == 1:
                    moves.append((ep_row, ep_col))

        return moves
    
    def get_potential_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        front_row = self.row + direction

        for dc in [-1, 1]:
            col = self.col + dc
            if 0 <= col < 8 and 0 <= front_row < 8:
                moves.append((front_row, col))
        return moves

        