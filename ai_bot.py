import pygame
import numpy as np
from settings import Button
import random
from two_player_game import Player, Board 

class AIBotGame:

    def __init__(self, screen, settings):

        # Initialzie the AI Bot game page attributes
        self.screen = screen
        self.settings = settings

        # Players attributes
        self.players = [Player("You"), Player("AI Bot")]
        self.current_player = self.players[0]
        self.winner = None

        # Board attributes
        self.board = Board(screen, settings)
        self.empty = 0
        self.piece = 1

        # Timer attributes
        self.clock = pygame.time.Clock()
        self.timer_event = pygame.USEREVENT+1
        pygame.time.set_timer(self.timer_event, 1000) # Custom event for the timer
        self.timer_paused = False
        self.time_left = 30
        self.flag = False
        self.wait_time_flag = False
        self.turn_wait_time = random.randint(26, 29)

        # Font attributes
        self.font = pygame.font.Font('assets/fonts/Akira.otf', 18)

        # Player turn messages
        self.turn_msg1 = self.font.render("Your's", True, (255, 255, 0))
        self.turn_msg2 = self.font.render("AI Bot's", True, (255, 0, 0))

        # Buttons
        self.pause_button = Button(screen, 'Pause', 640, 400, 120, 35, 16, (0, 255, 0))
        self.back_button = Button(screen, 'Back', 640, 450, 120, 35, 16)


    def reset(self):
        # Reset the game board and  set the current player, time left 
        self.board.reset()
        self.current_player = self.players[0]
        self.piece = 1
        self.time_left = 30

    def switch_player(self):
        # Switch the current player and set the piece
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        self.piece = 2 if self.current_player == self.players[1] else 1
        self.time_left = 30

    def handle_events(self, event):

        # Timer event
        if event.type == self.timer_event and not self.timer_paused:
            self.time_left -= 1
            if self.time_left == 0:
                self.switch_player()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if the mouse is clicked on the game board x pos
            if (20 <= mouse_pos[0] <= int(6*self.settings.cell_size+85/2) + 40) and not self.timer_paused:
                column = (mouse_pos[0] - 20) // self.settings.cell_size # Get the column index

                self.settings.piece_drop_sound.play()
                if self.current_player.make_move(self.board, column, self.piece): 
                    if self.board.get_winner():
                        self.winner = self.current_player.name
                        self.draw()
                        pygame.display.flip()
                        pygame.time.wait(2000) # wait 2second befor ethe game over page
                        self.reset()
                        return 'game_over_page'
                    
                    if self.board.is_full():
                        self.winner = None
                        self.draw()
                        pygame.display.flip()
                        pygame.time.wait(2000) # wait 2 seconds
                        self.reset()
                        return 'game_over_page'
                    
                    self.switch_player()

            # Buttons
            if self.pause_button.rect.collidepoint(event.pos):
                self.settings.button_click_sound.play()
                self.timer_paused = not self.timer_paused
                self.pause_button.text = 'Resume' if self.pause_button.text == 'Pause' else 'Pause'
                self.pause_button.color = (255, 0, 0) if self.pause_button.text == 'Resume' else (0, 255, 0)

            if self.back_button.rect.collidepoint(event.pos):
                self.settings.button_click_sound.play()
                self.reset()
                return 'main_menu_page'

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            # Buttons hover
            self.flag = 20 <= mouse_pos[0] <= int(6*self.settings.cell_size+85/2) + 40
            self.pause_button.is_hover = self.pause_button.rect.collidepoint(event.pos)
            self.back_button.is_hover = self.back_button.rect.collidepoint(event.pos)

        # AI player move
        if self.current_player == self.players[1]:
            if not self.wait_time_flag:
                self.turn_wait_time = random.randint(26, 29)
                self.wait_time_flag = True

            if self.time_left < self.turn_wait_time:
                column = self.pick_best_move()
                self.settings.piece_drop_sound.play()
                if self.current_player.make_move(self.board, column, self.piece):
                    if self.board.get_winner():
                        self.settings.game_over_sound.play()
                        self.winner = self.current_player.name
                        self.draw()
                        pygame.display.flip()
                        self.reset()
                        pygame.time.wait(2000) # wait 2 seconds
                        return 'game_over_page'
                    
                    if self.board.is_full():
                        self.settings.game_over_sound.play()
                        self.winner = None
                        self.draw()
                        pygame.display.flip()
                        self.reset()

                        pygame.time.wait(2000)
                        return 'game_over_page'
                    
                    self.switch_player()
                    self.wait_time_flag = False

    def evaluate_window(self, window):
        # Evaluate the window and check number of consecutive pieces to set the score
        score = 0
        if window.count(2) == 4: # check for 4 consecutive pieces
            score += 100
        elif window.count(2) == 3 and window.count(self.empty) == 1: # check for 3 consecutive pieces(2) and 1 empty(0) space
            score += 10
        elif window.count(2) == 2 and window.count(self.empty) == 2:
            score += 5
        if window.count(1) == 3 and window.count(self.empty) == 1:
            score -= 80
        return score

    def score_position(self, board):
        # Score the position of the board
        score = 0
        center_array = [int(i) for i in list(board[:,3])]
        center_count = center_array.count(self.piece)
        score += center_count * 6
        # Horizontal
        for r in range(6):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(4):
                window = row_array[c:c+4]
                score += self.evaluate_window(window)
        # Vertical
        for c in range(7):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(6-3):
                window = col_array[r:r+4]
                score += self.evaluate_window(window)

        # Diagonal 
        for r in range(3):
            for c in range(4):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window)
        # Reverse Diagonal
        for r in range(3):
            for c in range(4):
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window)
        return score

    def pick_best_move(self):

        valid_moves = self.board.get_valid_moves() # Get the valid moves 
        best_score = -10000
        best_col = np.random.choice(valid_moves) 

        # Check for the best move
        for col in valid_moves:
            row = self.board.get_next_empty_row(col) # Get the next empty row
            temp_board = self.board.grid.copy()
            temp_board[row][col] = self.piece
            score = self.score_position(temp_board)
            if score > best_score:
                best_score = score
                best_col = col
        return best_col

    def draw(self):

        # Draw the game page elements
        self.screen.fill((0, 0, 0)) # background

        # Draw the game board
        self.board.draw(self.screen)

        # Placeholder piece(circle) for the player 
        if self.flag and self.current_player == self.players[0] and not self.timer_paused:
            color = (255, 255, 0) if self.current_player == self.players[0] else (255, 0, 0)
            pygame.draw.circle(self.screen, color, (pygame.mouse.get_pos()[0], 50), self.settings.radius)

        # Timer
        timer_text = self.font.render("TIME LEFT", True, (255, 255, 255))
        self.screen.blit(timer_text, (640, 90))

        timer_text = self.font.render(str(self.time_left), True, (255, 0, 0))
        self.screen.blit(timer_text, (690, 115))

        # Player turn messages
        player_color = (255, 255, 0) if self.current_player == self.players[0] else (255, 0, 0)
        self.screen.blit(self.turn_msg1 if player_color == (255, 255, 0) else self.turn_msg2, (660, 200))
        self.screen.blit(self.font.render("Turn", True, player_color), (670, 225))
        self.pause_button.draw()
        self.back_button.draw()


  