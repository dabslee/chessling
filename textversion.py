import chessboard

print("Welcome to Chess Lite!")
print("Example notation for inputting moves: E2 E4")
board = chessboard.Board()

turn = chessboard.Sides.WHITE # setting the first turn to be white
while board.checkmate() == chessboard.Sides.NEUTRAL:
    print()
    print(board.board_as_string())
    print()
    
    # Move is inputted and executed
    legit = False
    while not legit:
        userinput = input(chessboard.Sides.strname(turn)+" move: ")
        try:
            positions = [chessboard.Board.chess2strmove(s) for s in userinput.split(" ")]
            strmove = ("%s %s") % (positions[0], positions[1])
        except:
            strmove = userinput
        legit, invalid_reason = board.legit_move(strmove, turn, True)
        if legit:
            board.do_move(strmove)
        else:
            print("Invalid move! " + invalid_reason)
            print()

    # Checking for pawn promotions
    p = board.pawnpromote()
    if p != -1:
        while (promotetarget not in ['Q','R','N','B','P']):
            promotetarget = input("What would you like to promote your pawn to (Q, R, N, B, P)? ")
            if (promotetarget not in ['Q','R','N','B','P']):
                print("Invalid input. Please try again.")
            else:
                p.type = promotetarget
                print("Pawn promoted.")

    # Checking for checkmate
    side_checkmate = board.checkmate()
    if (side_checkmate != chessboard.Sides.NEUTRAL):
        print(chessboard.Sides.strname(side_checkmate)+" is in checkmate!")
        break # Checkmate ends the loop

    # Checks for stalemate
    if (board.stalemate(turn)):
        print(chessboard.Sides.strname(turn) + " cannot move. It's a stalemate!")
        break # Stalemate ends the loop

    # Checking for check
    side_check = board.check()
    if (side_check != chessboard.Sides.NEUTRAL):
        print(chessboard.Sides.strname(side_check)+" is in check!")

    turn *= -1 # switches turn from white to black or vice versa

print("Game over")
print()