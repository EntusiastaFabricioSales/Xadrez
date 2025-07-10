import os

class Piece:
    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.first_move = True  # usado para roque e en passant
        self.image = None  # opcional

    def get_valid_moves(self, board):
        return []

    def get_potential_moves(self, board):
        return self.get_valid_moves(board)
