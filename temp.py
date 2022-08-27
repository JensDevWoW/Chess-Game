import pygame

import time

import sys

class Board:
    def __init__(self, simulated, white, black, grid, WIN, WIDTH):
        self.move_log = []
        self.simulated = simulated
        self.last_moved_piece = []
        self.matrix = [[' ' for i in range(8)] for i in range(8)]
        self.last_position = []
        self.this_position = []
        self.last_piece_taken = ' '
        self.white = white
        self.black = black
        self.WIDTH = WIDTH
        self.grid = grid
        self.WIN = WIN
        self.moves = 0
        self.current_turn = None
        self.starting_order = {(0, 0): Piece(self.black, 'r', 'b_rook.png', [], False, 'q'), (0, 1): Piece(self.black, 'kn', 'b_knight.png', [], False),
                          (0, 2): Piece(self.black, 'b', 'b_bishop.png', [], False), (0, 4): Piece(self.black, 'k', 'b_king.png', [], False),
                          (0, 3): Piece(self.black, 'q', 'b_queen.png', [], False), (0, 5): Piece(self.black, 'b', 'b_bishop.png', [], False),
                          (0, 6): Piece(self.black, 'kn', 'b_knight.png', [], False), (0, 7): Piece(self.black, 'r', 'b_rook.png', [], False, 'k'),
                          (1, 0): Piece(self.black, 'p', 'b_pawn.png', [], False), (1, 1): Piece(self.black, 'p', 'b_pawn.png', [], False),
                          (1, 2): Piece(self.black, 'p', 'b_pawn.png', [], False), (1, 3): Piece(self.black, 'p', 'b_pawn.png', [], False),
                          (1, 4): Piece(self.black, 'p', 'b_pawn.png', [], False), (1, 5): Piece(self.black, 'p', 'b_pawn.png', [], False),
                          (1, 6): Piece(self.black, 'p', 'b_pawn.png', [], False), (1, 7): Piece(self.black, 'p', 'b_pawn.png', [], False),

                          (2, 0): ' ', (2, 1): ' ', (2, 2): ' ', (2, 3): ' ',
                          (2, 4): ' ', (2, 5): ' ', (2, 6): ' ', (2, 7): ' ',
                          (3, 0): ' ', (3, 1): ' ', (3, 2): ' ', (3, 3): ' ',
                          (3, 4): ' ', (3, 5): ' ', (3, 6): ' ', (3, 7): ' ',
                          (4, 0): ' ', (4, 1): ' ', (4, 2): ' ', (4, 3): ' ',
                          (4, 4): ' ', (4, 5): ' ', (4, 6): ' ', (4, 7): ' ',
                          (5, 0): ' ', (5, 1): ' ', (5, 2): ' ', (5, 3): ' ',
                          (5, 4): ' ', (5, 5): ' ', (5, 6): ' ', (5, 7): ' ',

                          (6, 0): Piece(self.white, 'p', 'w_pawn.png', [], False), (6, 1): Piece(self.white, 'p', 'w_pawn.png', [], False),
                          (6, 2): Piece(self.white, 'p', 'w_pawn.png', [], False), (6, 3): Piece(self.white, 'p', 'w_pawn.png', [], False),
                          (6, 4): Piece(self.white, 'p', 'w_pawn.png', [], False), (6, 5): Piece(self.white, 'p', 'w_pawn.png', [], False),
                          (6, 6): Piece(self.white, 'p', 'w_pawn.png', [], False), (6, 7): Piece(self.white, 'p', 'w_pawn.png', [], False),
                          (7, 0): Piece(self.white, 'r', 'w_rook.png', [], False, 'q'), (7, 1): Piece(self.white, 'kn', 'w_knight.png', [], False),
                          (7, 2): Piece(self.white, 'b', 'w_bishop.png', [], False), (7, 3): Piece(self.white, 'q', 'w_queen.png', [], False),
                          (7, 4): Piece(self.white, 'k', 'w_king.png', [], False), (7, 5): Piece(self.white, 'b', 'w_bishop.png', [], False),
                          (7, 6): Piece(self.white, 'kn', 'w_knight.png', [], False), (7, 7): Piece(self.white, 'r', 'w_rook.png', [], False, 'k'),}
        for i in range(8):
            for j in range(8):
                self.matrix[i][j] = self.starting_order[i,j]
                if self.matrix[i][j] != ' ':
                    self.matrix[i][j].position = [i,j]
        
        if simulated != True: 
            for i in range(8):
                for g in range(8):
                    if self.matrix[i][g] != ' ':
                        if self.matrix[i][g].team == self.white:
                            self.white.piece_list.append(self.matrix[i][g])
                        else:
                            self.black.piece_list.append(self.matrix[i][g])
    def on_board(self, position):
        if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[1] < 8:
            return True
    
    def deselect(self):
        for row in range(len(self.matrix)):
            for column in range(len(self.matrix[0])):
                if self.matrix[row][column] == 'x ':
                    self.matrix[row][column] = ' '
                else:
                    try:
                        self.matrix[row][column].Killable = False
                    except:
                        pass
    def Do_Move(self, piece, x, y, row, col, WIN, grid, simulated):
        piece.position = [x,y]
        last_piece = ' '
        if self.matrix[x][y] != ' ':      # Taking a piece
            for taken_piece in self.matrix[x][y].team.piece_list:
                if taken_piece == self.matrix[x][y]:
                    self.matrix[x][y].team.piece_list.remove(taken_piece)
                    last_piece = taken_piece
                    break
        self.last_position = [row, col]
        self.this_position = [last_piece, x, y]
        self.last_moved_piece = piece
        self.matrix[x][y] = self.matrix[row][col]
        self.matrix[row][col] = ' '
        square = square_names[x,y]
        if simulated == False:
            if piece.type != 'p':
                self.move_log.append(piece.type + square)
            else:
                self.move_log.append(square)
    def check_team(self, moves, index):
        row, col = index
        if moves%2 == 0:
            if self.matrix[row][col].team == self.white:
                return True, self.white
        else:
            if self.matrix[row][col].team == self.black:
                return True, self.black
    def Reverse_Move(self, piece, sim):
        last_piece,x,y = self.this_position
        row,col = self.last_position
        self.matrix[row][col] = piece
        self.matrix[x][y] = last_piece
        piece.position = [row,col]
        self.moves = self.moves - 1
        if sim != True:
            if self.current_turn == self.white:
                self.current_turn = self.black
            else:
                self.current_turn = self.white
        
    def update_moveSet(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] != ' ':
                    self.empty_pieceMoveList(self.matrix[i][j])
                    self.matrix[i][j].getMoves(self)
    def clear_moveSet(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] != ' ':
                    self.empty_pieceMoveList(self.matrix[i][j])
                        
    def empty_teamMoveList(self):
        self.white.possible_moves.clear()
        self.black.possible_moves.clear()

    def empty_pieceMoveList(self, piece):
        piece.available_moves.clear()
        
class Team:
    def __init__(self, colour, piece_list, possible_moves, in_check, King):
        self.colour = colour
        self.piece_list = piece_list
        self.in_check = in_check
        self.possible_moves = possible_moves
        self.King = King
        self.can_castle_queenside = True
        self.can_castle_kingside = True
    
    def update_piece_list(self, original_piece, new_piece):
        current_piece = self.piece_list.index(original_piece)
        self.piece_list[current_piece] = new_piece
        
    def empty_possible_moves(self):
        self.possible_moves.clear()
        
    def check_king(self, other_team, grid):                   # Check if certain team's king is under attack
        for piece in self.piece_list:
            for move in piece.available_moves:
                if move == other_team.King.position:
                    return True
        return False    
    def get_team(self):
        return self
    
    def update_moveSet(self, board):
        for i in range(len(board.matrix)):
            for j in range(len(board.matrix[0])):
                if board.matrix[i][j] != ' ':
                    if board.matrix[i][j].team == self:
                        board.empty_pieceMoveList(board.matrix[i][j])
                        board.matrix[i][j].getMoves(board)
        
    def get_legalMoves(self, piece, board, team1, team2, sim_team1, sim_team2, grid, WIN):
        # This happens when we are in check
        # Check to see which moves we can make to get out of check, if there are none, game is over
        # Very inefficient way to do this, I will add the right way later
        moves_to_remove = []
        for move in reversed(piece.available_moves):
            board.Do_Move(piece, move[0], move[1], piece.position[0], piece.position[1], None, grid, False)
            team2.update_moveSet(board)
            if team2.check_king(team1, grid) == True:
                board.Reverse_Move(piece, True)
                moves_to_remove.append(move)
            else:
                board.Reverse_Move(piece, True)
            
        for move in reversed(piece.available_moves):
            if move in moves_to_remove:
                piece.available_moves.remove(move)
class Piece:
    def __init__(self, team, type, image, available_moves, add = True, side = 'n'):
        self.team = team
        self.type = type
        self.has_moved = False
        self.Killable = False
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (100,100))
        self.available_moves = available_moves
        self.side = side
        self.position = []
        if self.type == 'k':
            self.team.King = self
            if self.team.colour == 'w':
                self.position = [7,4]
            else:
                self.position = [0,4]
        if add:
            team.piece_list.append(self)
    
    def getMoves(self, board):
        index = self.position
        if self.type == 'p':
            if self.team.colour == 'b':
                pawnRow = index[0]
                pawnColumn = index[1]
                if pawnRow == 1:
                    if board.matrix[pawnRow + 2][pawnColumn] == ' ' and board.matrix[pawnRow + 1][pawnColumn] == ' ': 
                        self.available_moves.append([pawnRow + 2, pawnColumn])
                        self.available_moves.append([pawnRow + 1, pawnColumn])
                        
                bottom3 = [[pawnRow + 1, pawnColumn + i] for i in range(-1, 2)] 
                
                ## Example position [1, -1]
                for position in bottom3:
                    if board.on_board(position): ##Check if [1,-1] is within [0,8][0,8]
                        if bottom3.index(position) % 2 == 0:  ## If true, piece is there?
                            try:
                                if board.matrix[position[0]][position[1]].team.colour != 'b':
                                    board.matrix[position[0]][position[1]].Killable = True
                                    self.available_moves.append([position[0], position[1]])
                            except:
                                pass
                        else:
                            if board.matrix[position[0]][position[1]] == ' ':
                                self.available_moves.append([position[0], position[1]])
            else:
                pawn_row = index[0]
                pawn_column = index[1]
                if pawn_row == 6:
                    if board.matrix[pawn_row - 2][pawn_column] == ' ' and board.matrix[pawn_row - 1][pawn_column] == ' ':
                            self.available_moves.append([pawn_row - 2, pawn_column])
                            self.available_moves.append([pawn_row - 1, pawn_column])
                top3 = [[pawn_row - 1, pawn_column + i] for i in range(-1, 2)]
                
                for position in top3:
                    if board.on_board(position):
                        if top3.index(position) % 2 == 0:
                            try:
                                if board.matrix[position[0]][position[1]].team.colour != 'w':
                                    board.matrix[position[0]][position[1]].Killable = True
                                    self.available_moves.append([position[0], position[1]])
                            except:
                                pass
                        else:
                            if board.matrix[position[0]][position[1]] == ' ':
                                self.available_moves.append([position[0], position[1]])
        elif self.type == 'r':
            cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
                     [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
                     [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
                     [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]
            for direction in cross:
                for position in direction:
                    if board.on_board(position):
                        if board.matrix[position[0]][position[1]] == ' ':
                            self.available_moves.append([position[0], position[1]])
                        else:
                            if board.matrix[position[0]][position[1]].team.colour != self.team.colour:
                                board.matrix[position[0]][position[1]].Killable = True
                                self.available_moves.append([position[0], position[1]])
                            break
        elif self.type == 'b':
            diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                         [[index[0] + i, index[1] - i] for i in range(1, 8)],
                         [[index[0] - i, index[1] + i] for i in range(1, 8)],
                         [[index[0] - i, index[1] - i] for i in range(1, 8)]]
            
            for direction in diagonals:
                for position in direction:
                    if board.on_board(position):
                        if board.matrix[position[0]][position[1]] == ' ':
                            self.available_moves.append([position[0], position[1]])
                        else:
                            if board.matrix[position[0]][position[1]].team.colour != self.team.colour:
                                board.matrix[position[0]][position[1]].Killable = True
                                self.available_moves.append([position[0], position[1]])
                            break
        elif self.type == 'kn':
            for i in range(-2, 3):
                for j in range(-2, 3):
                    if i ** 2 + j ** 2 == 5:
                        if board.on_board((index[0] + i, index[1] + j)):
                            if board.matrix[index[0] + i][index[1] + j] == ' ':
                                self.available_moves.append([index[0] + i, index[1] + j])
                            else:
                                if board.matrix[index[0] + i][index[1] + j].team.colour != self.team.colour:
                                    board.matrix[index[0] + i][index[1] + j].Killable = True
                                    self.available_moves.append([index[0] + i, index[1] + j])
        elif self.type == 'k':
            king_row = index[0] ## Starting king row: 0
            king_column = index[1] ## Starting king column: 4
            for y in range(3): ## Example: 1
                for x in range(3): ## Example: 0
                    if board.on_board((king_row - 1 + y, king_column - 1 + x)): ## Example: 0,3
                        if board.matrix[king_row - 1 + y][king_column - 1 + x] == ' ':
                            self.available_moves.append([king_row - 1 + y, king_column - 1 + x])
                        else:
                            if board.matrix[king_row - 1 + y][king_column - 1 + x].team != self.team: ## Check if piece is on my team
                                board.matrix[king_row - 1 + y][king_column - 1 + x].Killable = True ## If not, allow the king to take it
                                self.available_moves.append([king_row - 1 + y, king_column - 1 + x])
            ## Castling
            if self.team.can_castle_kingside:
                if board.matrix[king_row][king_column + 1] == ' ' and board.matrix[king_row][king_column + 2] == ' ':
                    self.available_moves.append([king_row, king_column + 2])
            if self.team.can_castle_queenside:
                if board.matrix[king_row][king_column - 1] == ' ' and board.matrix[king_row][king_column - 2] == ' ':
                    self.available_moves.append([king_row, king_column - 2])
            
            
        elif self.type == 'q':
            cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
                     [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
                     [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
                     [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]
            diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                         [[index[0] + i, index[1] - i] for i in range(1, 8)],
                         [[index[0] - i, index[1] + i] for i in range(1, 8)],
                         [[index[0] - i, index[1] - i] for i in range(1, 8)]]
            for direction in cross:
                for position in direction:
                    if board.on_board(position):
                        if board.matrix[position[0]][position[1]] == ' ':
                            self.available_moves.append([position[0], position[1]])
                        else:
                            if board.matrix[position[0]][position[1]].team.colour != self.team.colour:
                                board.matrix[position[0]][position[1]].Killable = True
                                self.available_moves.append([position[0], position[1]])
                            break
            for direction in diagonals:
                for position in direction:
                    if board.on_board(position):
                        if board.matrix[position[0]][position[1]] == ' ':
                            self.available_moves.append([position[0], position[1]])
                        else:
                            if board.matrix[position[0]][position[1]].team.colour != self.team.colour:
                                board.matrix[position[0]][position[1]].Killable = True
                                self.available_moves.append([position[0], position[1]])
                            break
        return self.available_moves
        
        

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

def select_moves(piece):    
    return piece.available_moves
    
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
        self.pass_num = 0
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

def update_display(board, WIN, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(WIN)
            spot.setup(board, WIN)
    draw_grid(WIN, rows, width)
    pygame.display.update()

def Find_Node(pos, WIDTH):
    interval = WIDTH / 8
    x, y = pos
    rows = y // interval
    columns = x // interval
    return int(rows), int(columns)

def display_potential_moves(positions, grid):
    for i in positions:
        x, y = i
        grid[x][y].colour = BLUE
    
def remove_highlight(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i+j)%2 == 0:
                grid[i][j].colour = WHITE
            else:
                grid[i][j].colour = GREY
    return grid


def main(WIN, WIDTH):
    pygame.init()
    selected = False
    piece_to_move=[]
    selected_piece = ' '
    grid = make_grid(8, WIDTH)
    
    white_team = Team('w', [], [], False, ' ')
    black_team = Team('b', [], [], False, ' ')
    game_board = Board(False, white_team, black_team, grid, WIN, WIDTH)
    game_board.current_turn = game_board.white
    game_board.update_moveSet()
    other_team = game_board.black
    
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
                    selected_piece = game_board.matrix[x][y]
                    if selected_piece == ' ':
                        pass
                    else:
                        if selected_piece.team == game_board.current_turn:
                            if game_board.current_turn.in_check == True:
                                game_board.current_turn.get_legalMoves(selected_piece, game_board, game_board.current_turn, other_team, game_board.current_turn, other_team, grid, WIN)
                            possible = selected_piece.available_moves  
                            for position in possible:
                                row, col = position
                                grid[row][col].colour = BLUE
                            piece_to_move = x,y
                            selected = True
                        else:
                            selected_piece = []
                            piece_to_move = []
                            print('Can\'t select')
                else:
                    if [x,y] in selected_piece.available_moves:
                        row, col = piece_to_move
                        game_board.deselect()
                        remove_highlight(grid)
                        game_board.Do_Move(selected_piece, x, y, row, col, WIN, grid, False)
                        game_board.moves += 1
                        game_board.update_moveSet()
                        
                        ## Add in Castling check
                        ## Step 1: Check if moved piece was a rook and that the team that moved can castle in any particular direction
                        if (game_board.current_turn.can_castle_kingside == True or game_board.current_turn.can_castle_queenside == True):
                            if selected_piece.type == 'r':   
                                ## Step 2: Check if kingside or kingside rook with variable
                                if selected_piece.side == 'k': ## Kingside Rook
                                    game_board.current_turn.can_castle_kingside = False  ## Step 3: Set castling availability to false in all cases
                                else:
                                    game_board.current_turn.can_castle_queenside = False
                            elif selected_piece.type == 'k':
                                ## In this case, any king moves immediately disallows castling on either side
                                game_board.current_turn.can_castle_kingside = False
                                game_board.current_turn.can_castle_queenside = False        
                        
                        ## Add in castling functionality
                        ## Step 1: Check if the piece moved was a king and if it moved two spaces to the right or two spaces to the left
                        if selected_piece.type == 'k':
                            if y == (col + 2): ## Kingside castle
                                ## Step 2: Move the rook over 1 step to the left of the king
                                kingside_rook = game_board.matrix[x][y + 1] ## One side step over from the king's new position is the rook
                                game_board.Do_Move(kingside_rook, x, y - 1, x, y + 1, WIN, grid, False)
                                game_board.update_moveSet()
                            elif y == (col - 2): ## Queenside castle
                                queenside_rook = game_board.matrix[x][y - 2] ## Two side steps over from the king's new position is the rook
                                game_board.Do_Move(queenside_rook, x, y + 1, x, y - 2, WIN, grid, False)
                                game_board.update_moveSet()
                                
                        print(game_board.current_turn.can_castle_kingside)
                        print(game_board.current_turn.can_castle_queenside)
                        
                        in_check = game_board.current_turn.check_king(other_team, grid)
                        if game_board.current_turn == game_board.white:
                            game_board.current_turn = game_board.black
                            other_team = game_board.white
                        else:
                            game_board.current_turn = game_board.white
                            other_team = game_board.black
                        game_board.current_turn.in_check = in_check
                    else:
                        game_board.deselect()
                        remove_highlight(grid)
                        selected = False
                        selected_piece = []
                        piece_to_move = []
                        print("Invalid move")
                    selected = False
            elif event.type == pygame.KEYDOWN:
                game_board.Reverse_Move(game_board.last_moved_piece, False)
            update_display(game_board.matrix, WIN, grid, 8, WIDTH)
            
    
main(WIN, WIDTH)   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
