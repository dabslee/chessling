import pygame
import time
import os

import chessboard

pygame.init()
screen = pygame.display.set_mode((720,960), pygame.RESIZABLE)
running = True
clock = pygame.time.Clock()

pygame.display.set_caption("Chess Lite")
scale = 1
windowsize = (720,960)

board = chessboard.Board()
turn = chessboard.Sides.WHITE # setting the first turn to be white

selectedposition = None
showntext = ""
gameover = False

# Basic color library
class COLOR:
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255,0,0)
    ORANGE = (255,165,0)
    YELLOW = (255,255,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    INDIGO = (75,0,130)
    VIOLET = (238,130,238)
    MAGENTA = (0,255,255)

    def GREY(proportion, color=WHITE):
        return list((proportion*i for i in color))

# Importing images
_image_library = {}
def get_image(path):
    path = "resources/images/" + path
    global _image_library
    image = _image_library.get(path)
    if image == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        image = pygame.image.load(canonicalized_path)
        _image_library[path] = image
    return image.convert_alpha()

# Draw the board
def draw_board():
    screen.fill(COLOR.WHITE)
    sqlength = int(70*scale)
    startx = int(windowsize[0]/2 - sqlength*4)
    starty = int(windowsize[1]/2.6 - sqlength*4)
    # the squares and pieces
    charmat = board.board_as_charmat()
    for i in range(8):
        for j in range(8):
            # square
            pygame.draw.rect(screen,(COLOR.GREY(0.7) if (i+j)%2==0 else COLOR.GREY(0.3)),
                             (startx+i*sqlength, starty+j*sqlength, sqlength, sqlength))
            # highlight square if selected
            if (selectedposition != None and selectedposition[0] == j and selectedposition[1] == i):
                pygame.draw.rect(screen,COLOR.GREY(0.5,COLOR.GREEN),(startx+i*sqlength, starty+j*sqlength, sqlength, sqlength))
            # highlight square if possible move for selected position
            if (selectedposition != None):
                strmove = "%s %s %s %s" % (selectedposition[0],selectedposition[1],j,i)
                legitmove,rsn = board.legit_move(strmove,turn,True)
                if (legitmove):
                    pygame.draw.rect(screen,COLOR.YELLOW,(startx+i*sqlength, starty+j*sqlength, sqlength, sqlength))
            # piece
            if (charmat[j][i] != "  "):
                screen.blit(pygame.transform.scale(get_image(charmat[j][i] + ".png"),
                                                   (sqlength,sqlength)),
                            (startx+i*sqlength, starty+j*sqlength))
    # the coordinates
    font = pygame.font.Font("resources/fonts/Consolas.ttf", int(30*scale))
    for i in range(8):
        text = font.render(str(8-i),True,COLOR.BLACK)
        screen.blit(text,(startx-sqlength//2,starty+sqlength//2+sqlength*i))
    for i in range(8):
        text = font.render(chr(i+ord('A')),True,COLOR.BLACK)
        screen.blit(text, (startx+sqlength//2+sqlength*i,starty-sqlength//2))

# Show text under board
def show_text(text):
    font = pygame.font.Font("resources/fonts/Consolas.ttf", int(20*scale))
    textsurf = font.render(text,True,COLOR.BLACK)
    screen.blit(textsurf,(windowsize[0]//2-textsurf.get_width()//2,int(windowsize[1]//1.4)))

# Main loop
while running:

    # Get the scale
    windowsize = pygame.display.get_surface().get_size()
    if (windowsize[0] < windowsize[1]):
        scale = windowsize[0]/720
    else:
        scale = windowsize[1]/960

    # Draw everything
    screen.fill(COLOR.BLUE)
    draw_board()
    show_text(showntext)
    pygame.display.flip()

    # Event handling
    for event in pygame.event.get():
        if (event.type == pygame.VIDEORESIZE):
            pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            if not gameover:
                mousepos = pygame.mouse.get_pos()
                sqlength = int(70*scale)
                startx = int(windowsize[0]/2 - sqlength*4)
                starty = int(windowsize[1]/2.6 - sqlength*4)
                if (mousepos[0] > startx and mousepos[0] < startx+sqlength*8
                    and mousepos[1] > starty and mousepos[1] < starty+sqlength*8):
                    if (selectedposition == None):
                        selectedposition = [(mousepos[1]-starty)//sqlength,
                                            (mousepos[0]-startx)//sqlength]
                        if (board.piece_at_pos(selectedposition) == None
                            or board.piece_at_pos(selectedposition).side != turn):
                            selectedposition = None
                    else:
                        strmove = ("%s %s %s %s") % (selectedposition[0],
                                                     selectedposition[1],
                                                     (mousepos[1]-starty)//sqlength,
                                                     (mousepos[0]-startx)//sqlength)
                        legit, invalid_reason = board.legit_move(strmove, turn, True)
                        if legit:
                            board.do_move(strmove)
                            selectedposition = None
                            showntext = ""
                            
                            # Checking for pawn promotions
                            p = board.pawnpromote()
                            if p != -1:
                                showntext = "To what would you like to promote the pawn?"                                
                                promotetarget = ""
                                while (promotetarget == ""):
                                    draw_board()
                                    show_text(showntext)
                                    screen.blit(pygame.transform.scale(get_image("Qb.png"),
                                                                       (sqlength,sqlength)),
                                                (int(windowsize[0]/2-sqlength*1.5),int(windowsize[1]//1.3)))
                                    screen.blit(pygame.transform.scale(get_image("Rb.png"),
                                                                       (sqlength,sqlength)),
                                                (int(windowsize[0]/2-sqlength*0.5),int(windowsize[1]//1.3)))
                                    screen.blit(pygame.transform.scale(get_image("Nb.png"),
                                                                       (sqlength,sqlength)),
                                                (int(windowsize[0]/2+sqlength*0.5),int(windowsize[1]//1.3)))
                                    screen.blit(pygame.transform.scale(get_image("Bb.png"),
                                                                       (sqlength,sqlength)),
                                                (int(windowsize[0]/2+sqlength*1.5),int(windowsize[1]//1.3)))
                                    pygame.display.flip()
                                    for event in pygame.event.get():
                                        if (event.type == pygame.VIDEORESIZE):
                                            pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                                        if (event.type == pygame.MOUSEBUTTONDOWN):
                                            mousepos = pygame.mouse.get_pos()
                                            if (mousepos[1] > int(windowsize[1]//1.3) and mousepos[1] < int(windowsize[1]//1.3) + sqlength):
                                                if (mousepos[0] > int(windowsize[0]/2-sqlength*1.5) and mousepos[0] < int(windowsize[0]/2-sqlength*0.5)):
                                                    promotetarget = 'Q'
                                                elif (mousepos[0] > int(windowsize[0]/2-sqlength*0.5) and mousepos[0] < int(windowsize[0]/2+sqlength*0.5)):
                                                    promotetarget = 'R'
                                                elif (mousepos[0] > int(windowsize[0]/2+sqlength*0.5) and mousepos[0] < int(windowsize[0]/2+sqlength*1.5)):
                                                    promotetarget = 'N'
                                                elif (mousepos[0] > int(windowsize[0]/2+sqlength*1.5) and mousepos[0] < int(windowsize[0]/2+sqlength*2.5)):
                                                    promotetarget = 'B'
                                        elif (event.type == pygame.QUIT):
                                            running = False
                                            break
                                    clock.tick(60)
                                p.type = promotetarget
                            # Checking for checkmate
                            side_checkmate = board.checkmate()
                            if (side_checkmate != chessboard.Sides.NEUTRAL):
                                showntext = chessboard.Sides.strname(side_checkmate)+" is in checkmate!"
                                gameover = True # Checkmate ends the game
                                break

                            # Checks for stalemate
                            if (board.stalemate(turn)):
                                showntext = chessboard.Sides.strname(turn) + " cannot move. It's a stalemate!"
                                gameover = False # Stalemate ends the game
                                break

                            # Checking for check
                            side_check = board.check()
                            if (side_check != chessboard.Sides.NEUTRAL):
                                showntext = chessboard.Sides.strname(side_check)+" is in check!"

                            turn *= -1 # switches turn from white to black or vice versa
                        else:
                            selectedposition = None
                else:
                    selectedposition = None
        elif (event.type == pygame.QUIT):
            running = False
            break

    clock.tick(60)