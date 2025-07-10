from code.Pawn import Pawn
from code.Piece import Piece
from code.Rook import Rook
from code.Knight import Knight
from code.Bishop import Bishop
from code.Queen import Queen
from code.King import King

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.en_passant_target = None
        self.setup_board()

    def setup_board(self):
        #Pretas
        self.grid[0] = [
            Rook("black", 0, 0), Knight("black", 0, 1), Bishop("black", 0, 2), Queen("black", 0, 3),
            King("black", 0, 4), Bishop("black", 0, 5), Knight("black", 0, 6), Rook("black", 0, 7)
            ]
        self.grid[1] = [Pawn("black", 1, col) for col in range(8)]

        #Brancas
        self.grid[7] = [
            Rook("white", 7, 0), Knight("white", 7, 1), Bishop("white", 7, 2), Queen("white", 7, 3),
            King("white", 7, 4), Bishop("white", 7, 5), Knight("white", 7, 6), Rook("white", 7, 7)
            ]
        self.grid[6] = [Pawn("white", 6, col) for col in range(8)]

    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.grid[row][col]
        
        return None
    
    def move_piece(self, piece, new_row, new_col):
        target = self.get_piece(new_row, new_col)

        #En passant captura
        if isinstance(piece, Pawn) and self.en_passant_target == (new_row, new_col):
            captured_row = piece.row
            self.grid[captured_row][new_col] = None

        #Roque
        if isinstance(piece, Rook) and abs(new_col - piece.col) == 2:
            #Roque grande
            if new_col == 6:
                rook = self.get_piece(piece.row, 7)
                self.grid[piece.row][5] = rook
                self.grid[piece.row][7] = None
                rook.col = 5
                rook.first_move = False
            #Roque pequeno
            elif new_col == 2:
                rook = self.get_piece(piece.row, 0)
                self.grid[piece.row][3] = rook
                self.grid[piece.row][0] = None
                rook.col = 3
                rook.first_move = False

        #Atualiza a posição
        self.grid[piece.row][piece.col] = None
        piece.row = new_row
        piece.col = new_col
        piece.first_move = False
        self.grid[new_row][new_col] = piece

        #En passant marcação
        self.en_passant_target = None
        if isinstance(piece, Pawn):
            if abs(new_row - piece.row) == 2:
                self.en_passant_target = ((new_row + piece.row) // 2, new_col)
            
            #promoção
            if new_row == 0 or new_row == 7:
                return "promote"
            
        return target
    
    def is_in_check(self, color):
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece.color == color and piece.__class__.__name__ == "King":
                    king_pos = (row, col)
                    break

        if not king_pos:
            return True
        
        return self.is_square_attacked(color, king_pos[0], king_pos[1])
    
    def is_square_attacked(self, color, row, col):
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color != color:
                    if (row, col) in piece.get_potential_moves(self):
                        return True
                    
        return False
    
    def get_legal_moves(self, piece):
        legal_moves = []
        orig_row, orig_col = piece.row, piece.col

        for move in piece.get_valid_moves(self):
            target_piece = self.get_piece(*move)

            #simula movimento
            self.grid[orig_row][orig_col] = None
            piece.row, piece.col = move
            self.grid[move[0]][move[1]] = piece

            if not self.is_in_check(piece.color):
                legal_moves.append(move)

            #desfaz simulação
            self.grid[orig_row][orig_col] = piece
            self.grid[move[0]][move[1]] = target_piece
            piece.row, piece.col = orig_row, orig_col

        return legal_moves