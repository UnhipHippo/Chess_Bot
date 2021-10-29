#This file works on the backend of the board

import chess
board= chess.Board()
board.legal_moves
board.push_san("Nc3")
board.push_san("Nc6")

def getFEN():
    return board.fen()
print(board.can_claim_threefold_repetition())
print(board.can_claim_draw())
print(board)