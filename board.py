import sys, pygame
import math
import chess

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

"""
for square in FEN:
    if square is "p":
        image = pygame.image.load("/home/sam/Documents/My_project/pieces/bP.jpg")
        screen.blit(image, (x, y))
    if square is "/":
        y+=width
    else:
        x+=width"""
move = ""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            x = math.floor(pos[0] / width)
            y = math.floor(pos[1] / width)
            if move == (letters[x]+str(num_rows-y)):
                move = ""
            else:
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

    # displayed the chess surface
    screen.blit(chess_board_surface, (0, 0))
    x=0
    y=0
    """
    p = pygame.image.load("/home/sam/Documents/My_project/pieces/bP.png")
    b = pygame.image.load("/home/sam/Documents/My_project/pieces/bB.png")
    k = pygame.image.load("/home/sam/Documents/My_project/pieces/bK.png")
    n = pygame.image.load("/home/sam/Documents/My_project/pieces/bN.png")
    q = pygame.image.load("/home/sam/Documents/My_project/pieces/bQ.png")
    r = pygame.image.load("/home/sam/Documents/My_project/pieces/bR.png")
    P = pygame.image.load("/home/sam/Documents/My_project/pieces/wP.png")
    B = pygame.image.load("/home/sam/Documents/My_project/pieces/wB.png")
    K = pygame.image.load("/home/sam/Documents/My_project/pieces/wK.png")
    N = pygame.image.load("/home/sam/Documents/My_project/pieces/wN.png")
    Q = pygame.image.load("/home/sam/Documents/My_project/pieces/wQ.png")
    R = pygame.image.load("/home/sam/Documents/My_project/pieces/wR.png")
    """
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



    pygame.display.update()