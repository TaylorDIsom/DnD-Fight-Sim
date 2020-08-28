import pandas as pd
import random

tttDF = pd.read_csv("tic-tac-toe-endgame.csv")

# print(tic_tac_toe_data.head())
class TicTacToe:

    def __init__(self):
        self.board = self.newBoard()
        self.piece = 'x'


    # Array of nine elements, b = blank,
    def newBoard(self):
        board = ['b', 'b', 'b',
                 'b', 'b', 'b',
                 'b', 'b', 'b']
        return board

    def placePiece(self, piece, place):
        if place >= 0 and place <= 8 and self.board[place] == 'b':
            self.board[place] = piece
            return place
        else:
            return -1

    def choosePlace(self):
        place = random.randint(0, 9)
        return place

    def takeTurn(self, piece):
        piecePlaced = False
        while not piecePlaced:
            place = self.choosePlace()
            piecePlaced = self.placePiece(piece, place) != -1

    def checkForWin(self, index1, index2, index3):
        if self.board[index1] == self.board[index2] == self.board[index3] != 'b':
            return self.board[index1]
        else:
            return False

    # from top(1) to bottom(3) and from left(1) to right(3)
    def checkGameState(self):
        isWinRow1 = self.checkForWin(0, 1, 2)
        if isWinRow1:
            return isWinRow1
        isWinRow2 = self.checkForWin(3, 4, 5)
        if isWinRow2:
            return isWinRow2
        isWinRow3 = self.checkForWin(6, 7, 8)
        if isWinRow3:
            return isWinRow3
        isWinCol1 = self.checkForWin(0, 3, 6)
        if isWinCol1:
            return isWinCol1
        isWinCol2 = self.checkForWin(1, 4, 7)
        if isWinCol2:
            return isWinCol2
        isWinCol3 = self.checkForWin(2, 5, 8)
        if isWinCol3:
            return isWinCol3
        isWinDiagonal1 = self.checkForWin(0, 4, 8)
        if isWinDiagonal1:
            return isWinDiagonal1
        isWinDiagonal2 = self.checkForWin(2, 4, 6)
        if isWinDiagonal2:
            return isWinDiagonal2
        if not 'b' in self.board:
            return 'c'
        else:
            return False

    def changePiece(self, piece):
        if piece == 'x':
            return 'o'
        if piece == 'o':
            return 'x'
        else:
            print("error")

    def playGame(self):
        piece = 'x'
        isGameOver = False
        self.board = self.newBoard()
        while not isGameOver:
            self.takeTurn(piece)
            isGameOver = self.checkGameState()
            piece = self.changePiece(piece)
            print(isGameOver)
            # print(self.board)
        print(self.board)


# def listPieceIndicies(board):
#     xIndicies = []
#     oIndicies = []
#     for index in range(len(board)):
#         if board[index] == 'x':
#             xIndicies.append(index)
#         elif board[index] == 'o':
#             oIndicies.append(index)
#         else: # probably b
#             pass
#     return xIndicies, oIndicies

def createConditions(df, board):
    conditions = 1
    for index in range(len(board)):
        if board[index] != 'b':
            column = df.columns[index]
            tempCondition = df[column] == board[index]
            conditions &= tempCondition
    return conditions

def findSimilarBoards(board):
    conditions = createConditions(tttDF, board)
    similarBoardList = tttDF[conditions]

    return similarBoardList

# TODO fix the additional index, add the header
def setResults(win, lose, draw):
    tempGame = TicTacToe()
    tempDF = pd.read_csv("tic-tac-toe-endgame.csv")
    tempArray = tempDF.to_numpy()
    print(tempArray[0])
    for game in tempArray:
        tempGame.board = game[0:9]
        state = tempGame.checkGameState()
        value = 0
        if state == 'x':
            value = 1
        elif state == 'o':
            value = -1
        game[9] = value

    tempDF = pd.DataFrame(tempArray)
    csvString = tempDF.to_csv("tttCSV.csv")
    # tttFile = open("tttCSV.csv", "w")
    # tttFile.write(csvString)
    # tttFile.close()

    print(tempDF.head())

    games = tttDF.iloc[1, 0:2]
    # tempGame.board = games[1]
    print(tttDF.shape,"games\n", games, "\n")




setResults(1,-1,0)

print("tic tac toe")
ttt = TicTacToe()
ttt.playGame()
 # = findSimilarBoards(ttt.board)
# print(x, o)
s = tttDF.shape
print(s, "\n")

cols = tttDF.columns
# print(cols)

#
# df = tttDF
# temp = df.columns[0]
# cond1 = (df[temp] == 'x')
# cond2 = (df.V2 == 'x' )
# cond8 = (df.V8 == 'o' )
# cond = cond1 & cond2 & cond8
# print("conditions", cond )
#
# x1 = df[ cond ]
# print(df.columns[0], x1.head())

sims = findSimilarBoards(ttt.board)
print(sims)

'''
# tic_tac_toe_data.index.to_series()
v1x = tic_tac_toe_data.where(
    (tic_tac_toe_data.V1 == 'x') &
    (tic_tac_toe_data.V2 == 'o') &
    (tic_tac_toe_data.V3 == 'x') &
    (tic_tac_toe_data.V4 == 'o') &
    (tic_tac_toe_data.V5 == 'x') &
    (tic_tac_toe_data.V6 == 'o') &
    (tic_tac_toe_data.V7 == ?) &
    (tic_tac_toe_data.V8 == ?) &
    (tic_tac_toe_data.V9 == ?)
    )
h = v1x.head()
print(v1x.shape, "poop", h)
'''

print("done")
