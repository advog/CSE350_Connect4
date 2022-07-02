def check_valid(board, column):
    for i in range(6):
        if(board[column][i] == 0):
            return True
    return False

def add_piece(board, column, turn):
    for i in range(5,-1, -1):
        if(board[column][i] == 0):
            board[column][i] = turn%2+1
            return

def check_win(board, turn):
    for x in range(7):
        for y in range(6):
            #vertical
            if(y > 2):
                if(board[x][y] == board[x][y-1] == board[x][y-2] == board[x][y-3] != 0):
                    return board[x][y]
            #up diagnal
            if (y > 2 and x < 4):
                if (board[x][y] == board[x+1][y - 1] == board[x+2][y - 2] == board[x+3][y - 3] != 0):
                    return board[x][y]
            #horizontal
            if (x < 4):
                if (board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] != 0):
                    return board[x][y]
            #down diagnal
            if (x < 4 and y < 3):
                if (board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] != 0):
                    return board[x][y]

    if (turn == 42):
        return 0

    return -1