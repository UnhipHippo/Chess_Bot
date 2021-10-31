import sys, pygame
import math
import chess
import chess.engine

pygame.init()

num_rows = 8
size = 678

letters = ["a","b","c","d","e","f","g","h"]
board= chess.Board()


white = 255, 178, 102
black = 255, 128, 0
highlight = 192, 192, 192
title = "Chess"

width = int(size/num_rows)  # width of the square
original_color = ''

screen = pygame.display.set_mode((size,size))
pygame.display.set_caption(title)

rect_list = list()  # this is the list of brown rectangle

# used this loop to create a list of brown rectangles
for i in range(0, 8):  # control the row
    for j in range(0, 8):  # control the column
        if i % 2 == 0:  # which means it is an even row
            if j % 2 != 0:  # which means it is an odd column
                rect_list.append(pygame.Rect(j * width, i * width, width, width))
        else:
            if j % 2 == 0:  # which means it is an even column
                rect_list.append(pygame.Rect(j * width, i * width, width, width))

# create main surface and fill the base color with light brown color
chess_board_surface = pygame.Surface((size,size))
chess_board_surface.fill(white)

# next draws the dark brown rectangles on the chess board surface
for chess_rect in rect_list:
    pygame.draw.rect(chess_board_surface, black, chess_rect)


move = ""

while True:
    if board.turn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                x = math.floor(pos[0] / width)
                y = math.floor(pos[1] / width)
                if move == (letters[x]+str(num_rows-y)):
                    move = ""
                move = move +letters[x]+str(num_rows-y)
                if(len(move)>=4):
                    if chess.Move.from_uci(move) in board.legal_moves:
                        board.push_san(move)
                        move = ""
                    else:
                        move = move[-2:]
                original_color = chess_board_surface.get_at((x * width, y * width))
                pygame.draw.rect(chess_board_surface, highlight, pygame.Rect((x) * width, (y) * width, width, width))
            if event.type == pygame.MOUSEBUTTONUP:
                x = math.floor(pos[0] / width)
                y = math.floor(pos[1] / width)
                pygame.draw.rect(chess_board_surface, original_color, pygame.Rect((x) * width, (y) * width, width, width))
    else:
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")

        limit = chess.engine.Limit(time=2.0)
        board.push_san(str(engine.play(board, limit).move))
        engine.quit()

    # displayed the chess surface
    screen.blit(chess_board_surface, (0, 0))
    x=0
    y=0

    FEN = board.fen()
    for square in FEN:
        if square is " ":
            break
        elif square is "/":
            y += width
            x = 0
        elif square in map(str, range(1,9)):
            x += width * int(square)
        else:
            image = pygame.image.load("pieces/%s.png" % square)
            image = pygame.transform.scale(image, (width, width))
            screen.blit(image, (x, y))
            x += width


    if board.outcome() is not None:
        font = pygame.font.Font(None, 100)
        if board.turn:
            text = font.render("Black wins!", True, [0,0,0])
        else:
            text = font.render("White wins!", True, [255, 255, 255])
        text_rect = text.get_rect(center=(size / 2, size/ 2))
        screen.blit(text, text_rect)



    pygame.display.update()