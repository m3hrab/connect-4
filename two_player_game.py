import pygame 
from settings import Button

class TwoPlayerGame():

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.players = [Player("Player 1"), Player("Player 2")]
        self.board = Board(screen, settings)

        self.flag = False

        self.current_player = self.players[0]
        self.piece = 1

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('assets/fonts/Akira.otf', 18)
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, 1000)
        self.timer_paused = False
        self.time_left = 30

        self.turn_msg1 = "Player 1's"
        self.turn_msg2 = "Player 2's"

        self.turn_msg1 = self.font.render(self.turn_msg1, True, (255, 255, 0))
        self.turn_msg2 = self.font.render(self.turn_msg2, True, (255, 0, 0))

        self.winner = None
        # Buttons 
        self.pause_button = Button(self.screen, 'Pause', 640, 400, 120, 35, 16, (0, 255, 0))
        self.back_button = Button(self.screen, 'Back', 640, 450, 120, 35, 16)

    def reset(self):
        self.board.reset()
        self.current_player = self.players[0]
        self.piece = 1
        self.time_left = 30

    def switch_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
            self.piece = 2
        else:
            self.current_player = self.players[0]
            self.piece = 1
        self.time_left = 30 


    def handle_events(self, event):

        if event.type == self.timer_event and not self.timer_paused:
            self.time_left -= 1
            if self.time_left == 0:
                self.switch_player()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 20 and mouse_pos[0] <= (int(6*85+85/2) + 40)) and not self.timer_paused:
                column = (mouse_pos[0] - 20) // self.settings.cell_size
                if self.current_player.make_move(self.board, column, self.piece):
                    if self.board.get_winner():
                        self.winner = self.current_player
                        self.reset()
                        return 'game_over_page'
                
                    if self.board.is_full():
                        self.winner = None
                        self.reset()
                        return 'game_over_page'
                    
                    self.switch_player()
                
                    
            if self.pause_button.rect.collidepoint(event.pos):
                self.timer_paused = not self.timer_paused
                if self.pause_button.text == 'Pause':
                    self.pause_button.text = 'Resume'
                    self.pause_button.color = (255, 0, 0)
                else:
                    self.pause_button.text = 'Pause'
                    self.pause_button.color = (0, 255, 0)

            if self.back_button.rect.collidepoint(event.pos):
                self.reset()
                return 'main_menu_page'

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 20 and mouse_pos[0] <= (int(6*85+85/2) + 40)):
                self.flag = True
            else:
                self.flag = False

            if self.pause_button.rect.collidepoint(event.pos):
                self.pause_button.is_hover = True
            else:
                self.pause_button.is_hover = False
            
            if self.back_button.rect.collidepoint(event.pos):
                self.back_button.is_hover = True
            else:
                self.back_button.is_hover = False


    def draw(self):
        self.screen.fill((0, 0, 0))
        self.board.draw(self.screen)

        if self.flag:
            if self.current_player == self.players[0]:
                pygame.draw.circle(self.screen, (255, 255, 0), (pygame.mouse.get_pos()[0], 50), self.settings.radius)
            else:
                pygame.draw.circle(self.screen, (255, 0, 0), (pygame.mouse.get_pos()[0], 50), self.settings.radius)

        timer_text = self.font.render("TIME LEFT", True, (255, 255, 255))
        self.screen.blit(timer_text, (640, 90))
        timer_text = self.font.render(str(self.time_left), True, (255, 0,  0))
        self.screen.blit(timer_text, (690, 115))


        if self.current_player == self.players[0]:
            self.screen.blit(self.turn_msg1, (640, 200))
            self.screen.blit(self.font.render("Turn", True, (255, 255, 0)), (670, 225))
        else:
            self.screen.blit(self.turn_msg2, (640, 200))
            self.screen.blit(self.font.render("Turn", True, (255, 0, 0)), (670, 225))


        self.pause_button.draw()
        self.back_button.draw()


class Player ():

    def __init__(self, name) -> None:
        self.name = name
    
    def make_move(self, board, column, piece):
        # Check the valid moves and update the player pieces 
        if board.is_valid_move(column):
            row = board.get_next_empty_row(column)
            board.drop_piece(row, column, piece)
            return True
        return False
    
    
class Board():

    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings

        # Defines colors 
        # self.board_color = (222, 226, 230)
        self.board_color = (0, 0, 255)
        self.p1_color = (24, 188, 156)
        self.p2_color = (44, 62, 80)

        # creates a 2D array that represents the game board
        self.grid = [[0 for _ in range(self.settings.columns)] for _ in range(self.settings.rows)]
    
    def is_valid_move(self, column):
	    # checks whether a given move is valid or not 
        return self.grid[5][column] == 0
    
    def drop_piece(self, row, column, piece):
        # places a game piece (e.g., a colored disc) in the lowest 
        self.grid[row][column] = piece
            
    def get_next_empty_row(self, col):
	    # returns the index of the lowest empty row in the selected column
        for r in range(6):
            if self.grid[r][col] == 0:
                return r

    def get_winner(self):
        """
        checks if a given move has resulted in a player
        winning the game by connecting four game pieces of the same color 
        vertically, horizontally, or diagonally.
        """

        # Check horizontally 
        for i in range(self.settings.rows):
            for j in range(self.settings.columns - 3):
                if self.grid[i][j] == self.grid[i][j+1] == self.grid[i][j+2] == self.grid[i][j+3] != 0:
                    # return self.grid[i][j]
                    return True

        # Check  vertically
        for i in range(self.settings.rows - 3):
            for j in range(self.settings.columns):
                if self.grid[i][j] == self.grid[i+1][j] == self.grid[i+2][j] == self.grid[i+3][j] != 0:
                    # return self.grid[i][j]
                    return True

        # Check diagonally
        for i in range(self.settings.rows - 3):
            for j in range(self.settings.columns - 3):
                if self.grid[i][j] == self.grid[i+1][j+1] == self.grid[i+2][j+2] == self.grid[i+3][j+3] != 0:
                    # return self.grid[i][j]
                    return True

        for i in range(3, self.settings.rows):
            for j in range(self.settings.columns - 3):
                if self.grid[i][j] == self.grid[i-1][j+1] == self.grid[i-2][j+2] == self.grid[i-3][j+3] != 0:
                    # return self.grid[i][j]
                    return True

        
    def is_full(self):
        # retrun the board is full or not
        for i in range(6):
            for j in range(7):
                if self.grid[i][j] == 0:
                    return False
        return True

    def reset(self):
        # reset the game board
        self.grid = [[0 for _ in range(self.settings.columns)] for _ in range(self.settings.rows)]

    def get_valid_moves(self):
        valid_moves = []
        for i in range(self.settings.columns):
            if self.is_valid_move(i):
                valid_moves.append(i)
        return valid_moves
    
                
    def draw(self, screen):

        # Draw the main board 
        for c in range(self.settings.columns):
            for r in range(self.settings.rows):
                pygame.draw.rect(screen, self.board_color, (c*self.settings.cell_size + 20, r*self.settings.cell_size + self.settings.cell_size, self.settings.cell_size, self.settings.cell_size))
                pygame.draw.circle(screen, 'black', (int(c*self.settings.cell_size+self.settings.cell_size/2) + 20, int(r*self.settings.cell_size+self.settings.cell_size+self.settings.cell_size/2)), self.settings.radius)
        
        # Draw the game pieces
        for c in range(self.settings.columns):
            for r in range(self.settings.rows):
                if self.grid[r][c] == 1:
                    pygame.draw.circle(screen, 'yellow', (int(c*self.settings.cell_size+self.settings.cell_size/2) + 20 , 594-int(r*self.settings.cell_size+self.settings.cell_size/2)), self.settings.radius)
                elif self.grid[r][c] == 2:
                    pygame.draw.circle(screen, 'red', (int(c*self.settings.cell_size+self.settings.cell_size/2) + 20, 594-int(r*self.settings.cell_size+self.settings.cell_size/2)), self.settings.radius)
    

            

