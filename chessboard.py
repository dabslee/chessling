class Sides:
    WHITE = 1
    BLACK = -1
    NEUTRAL = 0

    def strname(intvalue):
        if intvalue == Sides.WHITE:
            return "White"
        elif intvalue == Sides.BLACK:
            return "Black"
        elif intvalue == Sides.NEUTRAL:
            return "Neutral"

    def chrname(intvalue):
        return Sides.strname(intvalue).lower()[0]

class Piece:
    KING = 'K'
    QUEEN = 'Q'
    ROOK = 'R'
    BISHOP = 'B'
    KNIGHT = 'N'
    PAWN = 'P'

    chrtofull = {'K' : "King",
                 'Q' : "Queen",
                 'N' : "Knight",
                 'B' : "Bishop",
                 'P' : "Pawn",
                 'R' : "Rook",}

    side = 1
    type = ''
    position = [0,0]

    def __init__(self, side, type, position):
        self.side = side
        self.type = type
        self.position = position

class Board:
    allpieces = None

    # Sets up initial piece positions
    def init_positions(self):
        # King
        self.allpieces.append(Piece(Sides.WHITE,Piece.KING,[7,4]))
        self.allpieces.append(Piece(Sides.BLACK,Piece.KING,[0,4]))
        # Queen
        self.allpieces.append(Piece(Sides.BLACK,Piece.QUEEN,[0,3]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.QUEEN,[7,3]))
        # Pawns
        for i in range(8):
            self.allpieces.append(Piece(Sides.BLACK,Piece.PAWN,[1,i]))
            self.allpieces.append(Piece(Sides.WHITE,Piece.PAWN,[6,i]))
        # Rooks
        self.allpieces.append(Piece(Sides.BLACK,Piece.ROOK,[0,0]))
        self.allpieces.append(Piece(Sides.BLACK,Piece.ROOK,[0,7]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.ROOK,[7,0]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.ROOK,[7,7]))
        # Knight
        self.allpieces.append(Piece(Sides.BLACK,Piece.KNIGHT,[0,1]))
        self.allpieces.append(Piece(Sides.BLACK,Piece.KNIGHT,[0,6]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.KNIGHT,[7,1]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.KNIGHT,[7,6]))
        # Bishop
        self.allpieces.append(Piece(Sides.BLACK,Piece.BISHOP,[0,2]))
        self.allpieces.append(Piece(Sides.BLACK,Piece.BISHOP,[0,5]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.BISHOP,[7,2]))
        self.allpieces.append(Piece(Sides.WHITE,Piece.BISHOP,[7,5]))
    def __init__(self):
        self.allpieces = []
        self.init_positions()

    def deepcopy(self):
        thecopy = Board()
        thecopy.allpieces = []
        for p in self.allpieces:
            thecopy.allpieces.append(Piece(p.side, p.type, p.position))
        return thecopy

    # Checks if any side is in check.
    # Returns the side in check if there is one, otherwise returns neutral side
    def check(self):
        for kingside in [Sides.WHITE, Sides.BLACK]:
            kingpos = self.allpieces[0 if kingside == Sides.WHITE else 1].position
            # for each enemy piece, check if endangering king by checking legit_move
            for enemyp in self.allpieces:
                if (enemyp.side == kingside):
                    continue
                legit, rsn = self.legit_move("%d %d %d %d" % (enemyp.position[0], enemyp.position[1], kingpos[0], kingpos[1]), -kingside, False)
                if legit:
                    return kingside
        return Sides.NEUTRAL

    # Checks if side whose turn it is is in checkmate
    # Returns True or False
    def stalemate(self, turn):
        for p in self.allpieces:
            if (p.side != turn):
                continue
            for i in range(8):
                for j in range(8):
                    legit, rsn = self.legit_move("%d %d %d %d" % (p.position[0], p.position[1], i, j), turn, True)
                    if (legit):
                        return False
        return True

    # Checks if any side is in checkmate.
    # Returns the side in checkmate if there is one, otherwise returns neutral side
    def checkmate(self):
        checkedside = self.check()
        if (self.check() == Sides.NEUTRAL): # If not in check, not in checkmate
            return Sides.NEUTRAL
        # For each of pieces in of side in check, check if there are any legitimate moves
        for p in self.allpieces:
            if (p.side != checkedside):
                continue
            for i in range(8):
                for j in range(8):
                    legit, rsn = self.legit_move("%d %d %d %d" % (p.position[0], p.position[1], i, j), checkedside, True)
                    if (legit):
                        return Sides.NEUTRAL
        return checkedside

    # Checks if any pawns are at the opposite ends
    def pawnpromote(self):
        for p in self.allpieces:
            if (p.type == Piece.PAWN and p.position[0] == (0 if p.side == Sides.WHITE else 7)):
                return p
        return -1

    # Translates chess coordinates ("E4") to coordinates readable by legit_move and do_move ("4 4")
    def chess2strmove(chessxy):
        chessxy = chessxy.upper()
        if (len(chessxy) != 2
            or ord(chessxy[0]) < ord('A') or ord(chessxy[0]) > ord('Z')
            or ord(chessxy[1]) < ord('0') or ord(chessxy[1]) > ord('9')):
            return "Failed"
        i = 8 - (ord(chessxy[1]) - ord('0'))
        j = ord(chessxy[0]) - ord('A')
        return ("%d %d" % (i, j))

    # Checks if a move described by a string is legitimate given the current piece positions
    # The move should be in the format "i1 j1 i2 j2" where (i1,j1) is the starting position is the piece
    #   and (i2,j2) is the target position
    # Returns whether legitimate (boolean) and if illegit, the reason for it
    def legit_move(self, strmove, turn, withcheck):
        # Failure to parse
        startpos = []
        endpos = []
        try:
            intarray = [int(s) for s in strmove.split(" ")]
            startpos = intarray[0:2]
            endpos = intarray[2:4]
        except:
            return False, "Failed to parse."

        # Out of bounds
        if (startpos[0] > 7 or startpos[0] < 0 or endpos[0] > 7 or endpos[0] < 0):
            return False, "One or more positions out of bounds."

        # No piece in startpos
        piece = -1
        for p in self.allpieces:
            if (p.position[0] == startpos[0] and p.position[1] == startpos[1]):
                piece = p
                break
        if (piece == -1):
            return False, "No piece in inputted start position."

        # Piece is not your side
        if (piece.side != turn):
            return False, "Can't move opponent piece."

        # Invalid target position for piece
        queen = ""
        if (endpos[0]==startpos[0] and endpos[1]==startpos[1]):
            return False, "Can't move to original position."
        if (piece.type == Piece.KING):
            if (abs(endpos[0]-startpos[0]) > 1 or endpos[1]-startpos[1] > 1):
                return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
        elif (piece.type == Piece.QUEEN):
            if (not((piece.position[0] == endpos[0] or piece.position[1] == endpos[1]) # cardinal
                or abs(piece.position[0]-endpos[0]) == abs(piece.position[1]-endpos[1]))): # diagonal
                return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
            if (piece.position[0] == endpos[0] or piece.position[1] == endpos[1]):
                queen = "Cardinal"
            else:
                queen = "Diagonal"
        elif (piece.type == Piece.ROOK):
            if (not(piece.position[0] == endpos[0] or piece.position[1] == endpos[1])):
                return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
        elif (piece.type == Piece.BISHOP):
            if (not(abs(piece.position[0]-endpos[0]) == abs(piece.position[1]-endpos[1]))):
                return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
        elif (piece.type == Piece.KNIGHT):
            if (not((abs(piece.position[0]-endpos[0]) == 1 and abs(piece.position[1]-endpos[1]) == 2)
                   or (abs(piece.position[1]-endpos[1]) == 1 and abs(piece.position[0]-endpos[0]) == 2))):
                return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
        elif (piece.type == Piece.PAWN):
            if (endpos[0]-piece.position[0] == -piece.side and endpos[1] == piece.position[1]): # Moving 1 forward
                for p in self.allpieces:
                    if (p.position[0] == endpos[0] and p.position[1] == endpos[1]):
                        return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
            elif (endpos[0]-piece.position[0] == -piece.side and abs(endpos[1]-piece.position[1]) == 1): # Moving 1 diagonal to kill piece
                attacking = False
                for p in self.allpieces:
                    if (p.side != piece.side and p.position[0] == endpos[0] and p.position[1] == endpos[1]):
                        attacking = True
                        break
                if not attacking:
                    return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
            else:
                if (not (endpos[0]-piece.position[0] == -piece.side*2
                        and endpos[1] == piece.position[1]
                        and (piece.position[0] == 1 or piece.position[0] == 6))):
                    return False, "Invalid target position for " + Piece.chrtofull[piece.type] + "."
            
        # Jumping over pieces
        for p in self.allpieces:
            if (piece.type == Piece.ROOK or piece.type == Piece.PAWN or (piece.type == Piece.QUEEN and queen == "Cardinal")):
                if ((p.position[0] > min(endpos[0], startpos[0]) and p.position[0] < max(endpos[0], startpos[0]) and p.position[1] == startpos[1])
                    or (p.position[1] > min(endpos[1], startpos[1]) and p.position[1] < max(endpos[1], startpos[1]) and p.position[0] == startpos[0])):
                    return False, Piece.chrtofull[piece.type] + " cannot jump over pieces."
            elif (piece.type == Piece.BISHOP or (piece.type == Piece.QUEEN and queen == "Diagonal")):
                if ((p.position[0] == startpos[0]) or (p.position[0] == endpos[0])
                    or (p.position[1] == startpos[1]) or (p.position[1] == endpos[1])):
                    continue
                if ((p.position[0] > startpos[0]) == (endpos[0] > startpos[0])
                    and ((p.position[1] > startpos[1]) == (endpos[1] > startpos[1]))
                    and (abs(p.position[0] - startpos[0]) == abs(p.position[1] - startpos[1]))
                    and (abs(endpos[0] - startpos[0]) > abs(p.position[0] - startpos[0]))):
                    return False, Piece.chrtofull[piece.type] + " cannot jump over pieces."

        # Causes check
        if withcheck:
            copyboard = self.deepcopy()
            copyboard.do_move(strmove)
            if copyboard.check() == piece.side:
                return False, "Move causes king to be in check."

        # Overlapping own piece
        for p in self.allpieces:
            if (p.side == piece.side and p.position[0] == endpos[0] and p.position[1] == endpos[1]):
                return False, "Spot occupied already by " + Sides.strname(piece.side) + " piece."

        return True, "Legitimate move."

    # Executes a move described by a string
    def do_move(self, strmove):
        intarray = [int(s) for s in strmove.split(" ")]
        startpos = intarray[0:2]
        endpos = intarray[2:4]
        # Get rid of any pieces with position at endpos
        for piece in self.allpieces:
            if (piece.position[0] == endpos[0] and piece.position[1] == endpos[1]):
                self.allpieces.remove(piece)
        # Change position of position at startpos to endpos
        for piece in self.allpieces:
            if (piece.position[0] == startpos[0] and piece.position[1] == startpos[1]):
                piece.position = endpos
                break

    # Returns the current board as a char matrix
    def board_as_charmat(self):
        matrix = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append("  ")
            matrix.append(row)
        for piece in self.allpieces:
            matrix[piece.position[0]][piece.position[1]] = piece.type + Sides.chrname(piece.side)
        return matrix

    # Returns the current board as a string
    def board_as_string(self):
        matrix = self.board_as_charmat()
        # Represent char matrix as string
        retstr = "   0  1  2  3  4  5  6  7\n"
        for i in range(8):
            retstr += str(i) + " |"
            for j in range(8):
                retstr += matrix[i][j] + "|"
            retstr += "\n"
        return retstr

    # Returns piece at given position
    def piece_at_pos(self, pos):
        for p in self.allpieces:
            if (p.position[0] == pos[0] and p.position[1] == pos[1]):
                return p
        return None