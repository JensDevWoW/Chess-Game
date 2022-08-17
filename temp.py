import pygame

import time

import sys

board = [[' ' for i in range(8)] for i in range(8)]
board_sim = [[' ' for i in range(8)] for i in range(8)]

class Team:
    def __init__(self, colour, piece_list = [], possible_moves = [], in_check = False):
        self.colour = colour
        self.piece_list = piece_list
        self.in_check = in_check
        self.possible_moves = possible_moves
    
    def update_piece_list(self, original_piece, new_piece):
        current_piece = self.piece_list.index(original_piece)
        self.piece_list[current_piece] = new_piece
        
    def empty_possible_moves(self):
        self.possible_moves.clear()

white_team = Team('w')
black_team = Team('b')

class Piece:
    def __init__(self, team, type, image, add = True, Killable=False, has_moved=False):
        self.team = team
        self.type = type
        self.Killable = Killable
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100,100))
        if add:
            if team == white_team:
                white_team.piece_list.append(self)
            else:
                black_team.piece_list.append(self)
        
        
bp = Piece(black_team, 'p', 'b_pawn.png', False)
wp = Piece(white_team, 'p', 'w_pawn.png', False)
bk = Piece(black_team, 'k', 'b_king.png', False)
wk = Piece(white_team, 'k', 'w_king.png', False)
br = Piece(black_team, 'r', 'b_rook.png', False)
wr = Piece(white_team, 'r', 'w_rook.png', False)
bb = Piece(black_team, 'b', 'b_bishop.png', False)
wb = Piece(white_team, 'b', 'w_bishop.png', False)
bq = Piece(black_team, 'q', 'b_queen.png', False)
wq = Piece(white_team, 'q', 'w_queen.png', False)
bkn = Piece(black_team, 'kn', 'b_knight.png', False)
wkn = Piece(white_team, 'kn', 'w_knight.png', False)

square_names = {
    (7, 7): 'h1',
    (7, 6): 'g1',
    (7, 5): 'f1',
    (7, 4): 'e1',
    (7, 3): 'd1',
    (7, 2): 'c1',
    (7, 1): 'b1',
    (7, 0): 'a1',
    (6, 7): 'h2',
    (6, 6): 'g2',
    (6, 5): 'f2',
    (6, 4): 'e2',
    (6, 3): 'd2',
    (6, 2): 'c2',
    (6, 1): 'b2',
    (6, 0): 'a2',
    (5, 7): 'h3',
    (5, 6): 'g3',
    (5, 5): 'f3',
    (5, 4): 'e3',
    (5, 3): 'd3',
    (5, 2): 'c3',
    (5, 1): 'b3',
    (5, 0): 'a3',
    (4, 7): 'h4',
    (4, 6): 'g4',
    (4, 5): 'f4',
    (4, 4): 'e4',
    (4, 3): 'd4',
    (4, 2): 'c4',
    (4, 1): 'b4',
    (4, 0): 'a4',
    (3, 7): 'h5',
    (3, 6): 'g5',
    (3, 5): 'f5',
    (3, 4): 'e5',
    (3, 3): 'd5',
    (3, 2): 'c5',
    (3, 1): 'b5',
    (3, 0): 'a5',
    (2, 7): 'h6',
    (2, 6): 'g6',
    (2, 5): 'f6',
    (2, 4): 'e6',
    (2, 3): 'd6',
    (2, 2): 'c6',
    (2, 1): 'b6',
    (2, 0): 'a6',
    (1, 7): 'h7',
    (1, 6): 'g7',
    (1, 5): 'f7',
    (1, 4): 'e7',
    (1, 3): 'd7',
    (1, 2): 'c7',
    (1, 1): 'b7',
    (1, 0): 'a7',
    (0, 7): 'h8',
    (0, 6): 'g8',
    (0, 5): 'f8',
    (0, 4): 'e8',
    (0, 3): 'd8',
    (0, 2): 'c8',
    (0, 1): 'b8',
    (0, 0): 'a8',
    }

starting_order = {(0, 0): br, (0, 1): bkn,
                  (0, 2): bb, (0, 4): bk,
                  (0, 3): bq, (0, 5): bb,
                  (0, 6): bkn, (0, 7): br,
                  (1, 0): bp, (1, 1): bp,
                  (1, 2): bp, (1, 3): bp,
                  (1, 4): bp, (1, 5): bp,
                  (1, 6): bp, (1, 7): bp,

                  (2, 0): ' ', (2, 1): ' ', (2, 2): ' ', (2, 3): ' ',
                  (2, 4): ' ', (2, 5): ' ', (2, 6): ' ', (2, 7): ' ',
                  (3, 0): ' ', (3, 1): ' ', (3, 2): ' ', (3, 3): ' ',
                  (3, 4): ' ', (3, 5): ' ', (3, 6): ' ', (3, 7): ' ',
                  (4, 0): ' ', (4, 1): ' ', (4, 2): ' ', (4, 3): ' ',
                  (4, 4): ' ', (4, 5): ' ', (4, 6): ' ', (4, 7): ' ',
                  (5, 0): ' ', (5, 1): ' ', (5, 2): ' ', (5, 3): ' ',
                  (5, 4): ' ', (5, 5): ' ', (5, 6): ' ', (5, 7): ' ',

                  (6, 0): wp, (6, 1): wp,
                  (6, 2): wp, (6, 3): wp,
                  (6, 4): wp, (6, 5): wp,
                  (6, 6): wp, (6, 7): wp,
                  (7, 0): wr, (7, 1): wkn,
                  (7, 2): wb, (7, 3): wq,
                  (7, 4): wk, (7, 5): wb,
                  (7, 6): wkn, (7, 7): wr,}

def create_board(board, simulated):
    
    for i in range(8):
        for j in range(8):
            board[i][j] = starting_order[i,j]
    
    if simulated != True: 
        for i in range(8):
            for g in range(8):
                if board[i][g] != ' ':
                    if board[i][g].team == white_team:
                        white_team.piece_list.append(board[i][g])
                    else:
                        black_team.piece_list.append(board[i][g])
                
    return board           

def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
        return True
    
def convert_to_readable(board):
    output = ''
    
    for i in board:
        for j in i:
            try:
                output += j.team + j.type + ', '
            except:
                output += j + ', '
        output += '\n'
    return output

def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = ' '
            else:
                try:
                    board[row][column].Killable = False
                except:
                    pass
    
   # return convert_to_readable(board)

#def highlight(team):
   # highlighted = []
   # for i in range(len(team.possible_moves)):
    #    for j in range(len(board[0])):
    #        if board[i][j] == 'x ':
   #             highlighted.append((i, j))
   #         else:
   #             try:
    #                if board[i][j].Killable:
    #                    highlighted.append((i, j))
    #            except:
    #                pass
    #return team.possible_moves

def check_team(moves, index):
    row, col = index
    if moves%2 == 0:
        if board[row][col].team == white_team:
            return True, white_team
    else:
        if board[row][col].team == black_team:
            return True, black_team

def select_moves(piece, index, moves, team):
    print(piece.type)
    if piece.type == 'p':
        if piece.team == black_team:
            pawn_moves_b(index)
        else:
            print("tried doing pawn")
            pawn_moves_w(index)
        
    if piece.type == 'k':
        king_moves(index, team)
    
    if piece.type == 'r':
        rook_moves(index, team)
    
    if piece.type == 'b':
        bishop_moves(index, team)
    
    if piece.type == 'q':
        queen_moves(index, team)
    
    if piece.type == 'kn':
        knight_moves(index, team)
        
    return team.possible_moves

def team_lost(team, board, grid):     # Check if this particular team has any moves left that don't put him into check again, if so: lost
    for i in range(len(board)):
        for j in range(len(board[0])):
            piece = board[i][j]
            piece_pos = [i,j]
            if piece.type == 'p' and piece.team == white_team:
                pawn_moves_w(piece_pos, team)
            if piece.type == 'p' and piece.team == black_team:
                pawn_moves_b(piece_pos, team)
            
            if piece.type == 'r':
                rook_moves(piece_pos, team)
            if piece.type == 'b':
                bishop_moves(piece_pos, team)
            if piece.type == 'kn':
                knight_moves(piece_pos, team)
            if piece.type == 'q':
                queen_moves(piece_pos, team)
    
    ## We need to calculate if any of our available moves gets us out of check
    ## Best way to do that is: 
    #for move in team.possible_moves:
        

def check_king(team, board, grid):                   # Check if certain team's king is under attack
    ## First: Figure out king piece
    for i in range(len(board)):
        for j in range(len(board[0])):
            current_piece = board[i][j]
            current_pos = [i,j]
            if current_piece != ' ':
                if current_piece.type == 'k' and current_piece.team != team:
                    king_pos = [i,j]
                if current_piece.team == team:
                    if current_piece.type == 'p' and current_piece.team == white_team:
                        pawn_moves_w(current_pos)
                    if current_piece.type == 'p' and current_piece.team == black_team:
                        pawn_moves_b(current_pos)
                    
                    if current_piece.type == 'r':
                        rook_moves(current_pos, team)
                    
                    if current_piece.type == 'b':
                        queen_moves(current_pos, team)
                    
                    if current_piece.type == 'kn':
                        knight_moves(current_pos, team)
                    
                    if current_piece.type == 'q':
                        queen_moves(current_pos, team)
                
    for move in team.possible_moves:
        if move == king_pos:
            remove_highlight(grid)
            empty_moveList()
            return True
    
    remove_highlight(grid)
    empty_moveList()
    
    return False
    

def pawn_moves_b(index):
    pawnRow = index[0]
    pawnColumn = index[1]
    if pawnRow == 1:
        if board[pawnRow + 2][pawnColumn] == ' ' and board[pawnRow + 1][pawnColumn] == ' ': 
            black_team.possible_moves.append([pawnRow + 2, pawnColumn])
            black_team.possible_moves.append([pawnRow + 1, pawnColumn])
    bottom3 = [[pawnRow + 1, pawnColumn + i] for i in range(-1, 2)] 
    
    ## Example position [1, -1]
    for position in bottom3:
        if on_board(position): ##Check if [1,-1] is within [0,8][0,8]
            if bottom3.index(position) % 2 == 0:  ## If true, piece is there?
                try:
                    if board[position[0]][position[1]].team != black_team:
                        board[position[0]][position[1]].Killable = True
                        black_team.possible_moves.append([position[0], position[1]])
                except:
                    pass
            else:
                if board[position[0]][position[1]] == ' ':
                    black_team.possible_moves.append([position[0], position[1]])
    return black_team.possible_moves

def pawn_moves_w(index):
    pawn_row = index[0]
    pawn_column = index[1]
    if pawn_row == 6:
        if board[pawn_row - 2][pawn_column] == ' ' and board[pawn_row - 1][pawn_column] == ' ':
                white_team.possible_moves.append([pawn_row - 2,pawn_column])
                white_team.possible_moves.append([pawn_row - 1,pawn_column])
    top3 = [[pawn_row - 1, pawn_column + i] for i in range(-1, 2)]
    
    for position in top3:
        if on_board(position):
            if top3.index(position) % 2 == 0:
                try:
                    if board[position[0]][position[1]].team != white_team:
                        board[position[0]][position[1]].Killable = True
                        white_team.possible_moves.append([position[0],position[1]])
                except:
                    pass
            else:
                if board[position[0]][position[1]] == ' ':
                    white_team.possible_moves.append([position[0],position[1]])
    return white_team.possible_moves
    

def king_moves(index, team):
    king_row = index[0] ## Starting king row: 0
    king_column = index[1] ## Starting king column: 4
    for y in range(3): ## Example: 1
        for x in range(3): ## Example: 0
            if on_board((king_row - 1 + y, king_column - 1 + x)): ## Example: 0,3
                if board[king_row - 1 + y][king_column - 1 + x] == ' ':
                    team.possible_moves.append([king_row - 1 + y, king_column - 1 + x])
                else:
                    if board[king_row - 1 + y][king_column - 1 + x].team != board[king_row][king_column].team: ## Check if piece is on my team
                        board[king_row - 1 + y][king_column - 1 + x].Killable = True ## If not, allow the king to take it
                        team.possible_moves.append([king_row - 1 + y, king_column - 1 + x])
    return team.possible_moves
        
def rook_moves(index, team):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]
    for direction in cross:
        for position in direction:
            if on_board(position):
                if board[position[0]][position[1]] == ' ':
                    team.possible_moves.append([position[0], position[1]])
                else:
                    if board[position[0]][position[1]].team.colour != team.colour:
                        board[position[0]][position[1]].Killable = True
                        team.possible_moves.append([position[0], position[1]])
                    break
    return team.possible_moves

def bishop_moves(index, team):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]
    
    for direction in diagonals:
        for position in direction:
            if on_board(position):
                if board[position[0]][position[1]] == ' ':
                    team.possible_moves.append([position[0], position[1]])
                else:
                    if board[position[0]][position[1]].team.colour != board[index[0]][index[1]].team.colour:
                        board[position[0]][position[1]].Killable = True
                        team.possible_moves.append([position[0], position[1]])
                    break
    return team.possible_moves

def queen_moves(index, team):
    rook_moves(index, team)
    bishop_moves(index, team)
    return team.possible_moves

def knight_moves(index, team):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == ' ':
                        team.possible_moves.append([index[0] + i, index[1] + j])
                    else:
                        if board[index[0] + i][index[1] + j].team.colour != team.colour:
                            board[index[0] + i][index[1] + j].Killable = True
                            team.possible_moves.append([index[0] + i, index[1] + j])
    return team.possible_moves

def empty_moveList():
    white_team.possible_moves.clear()
    black_team.possible_moves.clear()

WIDTH = 800

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Chess")
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.occupied = None
    
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / 8, WIDTH / 8))
        
    def setup(self, board, WIN):
        if board[self.row][self.col]:
            if board[self.col][self.row] == ' ':
                pass
            else:
                WIN.blit(board[self.col][self.row].image, (self.x, self.y))
                
                
def make_grid(rows, width):
    grid = []
    gap = WIDTH // rows
    print(gap)
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j, i, gap)
            grid[i].append(node)
            if (i+j)%2 == 1:
                grid[i][j].colour = GREY
    return grid

def draw_grid(win, rows, width):
    gap = width // 8
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def update_display(board, win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
            spot.setup(board, win)
    draw_grid(win, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    x, y = pos
    rows = y // interval
    columns = x // interval
    print(int(rows), int(columns))
    return int(rows), int(columns)

def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE
        
def Do_Move(board, x, y, row, col, OriginalPos, FinalPosition, WIN):
    #starting_order[FinalPosition] = starting_order[OriginalPos]
    #starting_order[OriginalPos] = None
    board[x][y] = board[row][col]
    board[row][col] = ' '
    
def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid

create_board(board, False)
create_board(board_sim, True)
def main(WIN, WIDTH):
    pygame.init()
    moves = 0
    selected = False
    piece_to_move=[]
    grid = make_grid(8, WIDTH)
    turn = white_team
    while True:
        pygame.time.delay(50) ## Stops CPU dying
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = Find_Node(pos, WIDTH)
                if selected == False:
                    if board[x][y] == ' ':
                        pass
                    else:
                        if board[x][y].team == turn:
                            possible = select_moves((board[x][y]), (x, y), moves, turn)
                            for position in possible:
                                row, col = position
                                grid[row][col].colour = BLUE
                            piece_to_move = x,y
                            selected = True
                        else:
                            piece_to_move = []
                            print('Can\'t select')
                        #print(piece_to_move)
                else:
                    if [x,y] in turn.possible_moves:
                        row, col = piece_to_move
                        deselect()
                        remove_highlight(grid)
                        empty_moveList()
                        Do_Move(board, x, y, row, col, (col, row), (y, x), WIN)
                        moves += 1
                        in_check = check_king(turn, board, grid)
                        if turn == white_team:
                            turn = black_team
                        else:
                            turn = white_team
                        turn.in_check = in_check
                        print(in_check)
                       # print(convert_to_readable(board))
                    else:
                        deselect()
                        remove_highlight(grid)
                        selected = False
                        print("Invalid move")
                    selected = False
                    
            update_display(board, WIN, grid, 8, WIDTH)
            
    
main(WIN, WIDTH)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
