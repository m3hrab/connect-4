import pygame 
from settings import Button
import numpy as np

class TwoPlayerGame():

    def __init__(self, screen, settings):
        
        # Initialize the game page attributes
        self.screen = screen
        self.settings = settings

        # Players attributes
        self.players = [Player("Player 1"), Player("Player 2")]
        self.winner = None
        self.current_player = self.players[0]
        self.piece = 1

        # Board attributes
        self.board = Board(screen, settings)
        self.flag = False

        # Timer attributes
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, 1000) # Custom event for the timer
        self.timer_paused = False
        self.time_left = 30


        # Font attributes
        self.font = pygame.font.Font('assets/fonts/Akira.otf', 18)

        # Player turn messages
        self.turn_msg1 = "Player 1's"
        self.turn_msg2 = "Player 2's"
        self.turn_msg1 = self.font.render(self.turn_msg1, True, (255, 255, 0))
        self.turn_msg2 = self.font.render(self.turn_msg2, True, (255, 0, 0))

        # Buttons 
        self.pause_button = Button(self.screen, 'Pause', 640, 400, 120, 35, 16, (0, 255, 0))
        self.back_button = Button(self.screen, 'Back', 640, 450, 120, 35, 16)

    def reset(self):
        # Reset the game board and  set the current player, time left
        self.board.reset()
        self.current_player = self.players[0]
        self.piece = 1
        self.time_left = 30

    def switch_player(self):
        # Switch the current player and set the piece
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
            self.piece = 2
        else:
            self.current_player = self.players[0]
            self.piece = 1
        self.time_left = 30 


    def handle_events(self, event):

        # Handle the events for the game page
        if event.type == self.timer_event and not self.timer_paused:
            self.time_left -= 1
            if self.time_left == 0:
                self.switch_player()


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if (mouse_pos[0] >= 20 and mouse_pos[0] <= (int(6*85+85/2) + 40)) and not self.timer_paused: # Check if the mouse is within the game board
                self.settings.piece_drop_sound.play()
                column = (mouse_pos[0] - 20) // self.settings.cell_size # Get the column index
                if self.current_player.make_move(self.board, column, self.piece): # Make a move(drop piece on the board) if the move is valid
                    if self.board.get_winner(): # check if there is connect-4
                        self.settings.game_over_sound.play()
                        self.winner = self.current_player.name
                        self.draw()
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        self.reset()
                        return 'game_over_page'
                
                    if self.board.is_full():
                        self.settings.game_over_sound.play()
                        self.winner = None
                        self.draw()
                        pygame.display.flip()
                        pygame.time.wait(2000)
                        self.reset()
                        return 'game_over_page'
                    
                    self.switch_player() # Switch the current player Turn
                
            
            # Buttons
            if self.pause_button.rect.collidepoint(event.pos):
                self.settings.button_click_sound.play()
                self.timer_paused = not self.timer_paused
                if self.pause_button.text == 'Pause':
                    self.pause_button.text = 'Resume'
                    self.pause_button.color = (255, 0, 0)
                else:
                    self.pause_button.text = 'Pause'
                    self.pause_button.color = (0, 255, 0)

            if self.back_button.rect.collidepoint(event.pos):
                self.settings.button_click_sound.play()
                self.reset()
                return 'main_menu_page'


        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse is within the game board to set the flag to draw placeholder piece at top of the board 
            if (mouse_pos[0] >= 20 and mouse_pos[0] <= (int(6*85+85/2) + 40)):
                self.flag = True
            else:
                self.flag = False

            # Buttons collsion detection
            if self.pause_button.rect.collidepoint(event.pos):
                self.pause_button.is_hover = True
            else:
                self.pause_button.is_hover = False
            
            if self.back_button.rect.collidepoint(event.pos):
                self.back_button.is_hover = True
            else:
                self.back_button.is_hover = False


    def draw(self):

        self.screen.fill((0, 0, 0)) # Game bg
        self.board.draw(self.screen) # Draw the game board

        # Draw the current player placeholder piece at the top of the board
        if self.flag:
            if self.current_player == self.players[0]:
                pygame.draw.circle(self.screen, (255, 255, 0), (pygame.mouse.get_pos()[0], 50), self.settings.radius)
            else:
                pygame.draw.circle(self.screen, (255, 0, 0), (pygame.mouse.get_pos()[0], 50), self.settings.radius)

        # Timer text
        timer_text = self.font.render("TIME LEFT", True, (255, 255, 255))
        self.screen.blit(timer_text, (640, 90))
        timer_text = self.font.render(str(self.time_left), True, (255, 0,  0))
        self.screen.blit(timer_text, (690, 115))


        # Player turn message
        if self.current_player == self.players[0]:
            self.screen.blit(self.turn_msg1, (640, 200))
            self.screen.blit(self.font.render("Turn", True, (255, 255, 0)), (670, 225))
        else:
            self.screen.blit(self.turn_msg2, (640, 200))
            self.screen.blit(self.font.render("Turn", True, (255, 0, 0)), (670, 225))

        # Draw the buttons
        self.pause_button.draw()
        self.back_button.draw()


class Player ():

    def __init__(self, name):
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
        self.grid = np.zeros((6,7), dtype=int) # Create a 6x7 grid(2d list) with 0 to represent the game board
        self.board_color = (0, 0, 255)
    
    def is_valid_move(self, column):
        # Check if the column is not full
        return self.grid[5][column] == 0
    
    def drop_piece(self, row, column, piece):
        # Update the grid with the player piece
        self.grid[row][column] = piece
            
    def get_next_empty_row(self, col):
        # Get the next empty row in the column
        for r in range(6):
            if self.grid[r][col] == 0:
                return r

    def get_winner(self):
        # check for connect-4 in horizontal, vertical and diagonal, reverse diagonal

        # Horizontal
        for i in range(6):
            for j in range(4):
                if self.grid[i][j] == self.grid[i][j+1] == self.grid[i][j+2] == self.grid[i][j+3] != 0:
                    return True
        
        # Vertical
        for i in range(3):
            for j in range(7):
                if self.grid[i][j] == self.grid[i+1][j] == self.grid[i+2][j] == self.grid[i+3][j] != 0:
                    return True
        # Diagonal
        for i in range(3):
            for j in range(4):
                if self.grid[i][j] == self.grid[i+1][j+1] == self.grid[i+2][j+2] == self.grid[i+3][j+3] != 0:
                    return True
        # Reverse Diagonal
        for i in range(3, 6):
            for j in range(4):
                if self.grid[i][j] == self.grid[i-1][j+1] == self.grid[i-2][j+2] == self.grid[i-3][j+3] != 0:
                    return True
        
    def is_full(self):
        # Check if the board is full
        return not any(0 in row for row in self.grid)

    def reset(self):
        # Reset the game board
        self.grid = np.zeros((6,7), dtype=int)

    def get_valid_moves(self):
        # Get the valid moves
        return [col for col in range(7) if self.is_valid_move(col)]
    
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
    
