import chess

# Probably make this a class
#Very slow, should add Alpha beta pruning

board = chess.Board()
values = {
    "K": 1000,
    "Q": 90,
    "R": 50,
    "B": 30,
    "N": 30,
    "P": 10
}

"""
Ways to improve evaluation function:
Make mobility better in relation to each individual piece, 
also change current mobility function so that evaluation(black) = -evaluation(white)
Consider the piece control of board, with more so to center pieces, 
Give more to advanced pawns, 
as well as potential subtraction for doubled or isolated pawns
Change evaluation for castling, so that castling is encouraged,
or alternatively encourage king safety
"""
def evaluate(board):
    fen = board.fen()
    evaluation = 0
    if board.is_stalemate():
        return evaluation
    for i in fen:
        if i is " ":
            break
        if i.upper() in ["Q", "K", "B", "P", "R", "N"]:  # edit pieces to be better
            if i.isupper():
                evaluation += values[i]
            else:
                #print(i)
                evaluation -= values[i.upper()]
    """
    if board.is_attacked_by(chess.WHITE, chess.D4):
        print(len(board.attackers(chess.WHITE, chess.D4)))
        evaluation+=len(board.attackers(chess.WHITE, chess.D4))  #
    if board.is_attacked_by(chess.BLACK, chess.D4):
        #print(len(board.attackers(chess.BLACK, chess.D4)))
        evaluation+=len(board.attackers(chess.BLACK, chess.D4))*4
    """
    if board.has_kingside_castling_rights(chess.BLACK):
        evaluation -= 1
    if board.has_queenside_castling_rights(chess.BLACK):
        evaluation -=1

    if not board.turn:
        evaluation += board.legal_moves.count() #potentially change to psuedo legal moves
        if board.is_checkmate():
            evaluation += 1000
        if board.is_check():
            evaluation += 1
    else:   #This code won't be reached, so I don't think it'll be wary of checks, have to add this
        evaluation -= board.legal_moves.count()
        if board.is_checkmate():
            evaluation -= 1000
        if board.is_check():
            evaluation -= 1
    return evaluation


def bestMove(moves, board):
    legals = board.legal_moves  # list of legal moves
    best_move = None  # stores best move
    best_eval = 10000  # stores best evaluation with move
    if moves == 0:
        return legals[0]  # maybe change this
    for i in legals:
        board.push_san(str(i))
        eval = bestEval(moves - 1, board)
        board.pop()
        #print(str(i) +" "+ str(eval))
        if eval < best_eval:
            best_eval = eval
            best_move = i
    return str(best_move)


def bestEval(moves, board):
    best_eval = -10000
    if moves == 0:
        return evaluate(board)
    legals = board.legal_moves
    for i in legals:
        board.push_san(str(i))
        min = 100
        for j in board.legal_moves:
            board.push_san(str(j))
            eval = bestEval(moves - 1, board)
            board.pop()
            if eval < min:  #here we're getting player twos best move
                min = eval
        board.pop()
        if min > best_eval:
            best_eval = min
    return best_eval

    # board.legal_moves
    # chess.Move.from_uci("a8a1") in board.legal_moves


#bestMove(2, board)
