import sys
import pygame
import time
import random

class MINIMAX_ALGORITHM:
    def __init__(self, depth):
        """Initialize the MINIMAX_ALGORITHM object with a specified depth"""
        self.depth = depth

    def is_terminal(self, state):
        """Check if the current state of the game is terminal.

        Args:
            True (bool): If the current state is terminal.
            False (bool): If the current state is not terminal.
        """
        if self.is_winner(state, 'O') or self.is_winner(state, 'X'):
            return True
        return all(cell != '.' for row in state for cell in row)

    def is_winner(self, state, player):
        """Check if the specified player has won in the given game state.

        Args:
            state (list): The current state of the game.
            player (str): The player to check for a winning sequence ('X' or 'O').

        Returns:
            True (bool): If the player has won.
            False (bool): If the player has not won.
        """
        # Verify if is the winner on the rows
        for row in state:
            for col in range(len(row) - 3):
                if all(cell == player for cell in row[col:col + 4]):
                    return True
        # Verify if is the winner on the columns
        for col in range(len(state[0])):
            for row in range(len(state) - 3):
                if all(state[row + i][col] == player for i in range(4)):
                    return True
        # Verify if is the winner on the first diagonals
        for row in range(len(state) - 3):
            for col in range(len(state[0]) - 3):
                if all(state[row + i][col + i] == player for i in range(4)):
                    return True
        # Verify if is the winner on the second diagonals
        for row in range(len(state) - 3):
            for col in range(3, len(state[0])):
                if all(state[row + i][col - i] == player for i in range(4)):
                    return True
        return False

    def get_possible_moves(self, state):
        """Get a list of possible moves in the current game state.

        Args:
            state (list): The current state of the game.

        Returns:
            possible_moves (list): A list of column indices representing the possible moves.
        """
        possible_moves = []
        for col in range(0,len(state[0])):
            if state[0][col] == '.':
                possible_moves.append(col)
        return possible_moves

    def make_move(self, state, move, player):
        """Make a move in the current game state.

        Args:
            state (list): The current state of the game.
            move (int): The column index where the move will be made.
            player (str): The player making the move ('X' or 'O').

        Returns:
            new_state (list): The new state of the game after making the move.
        """
        col = move
        new_state = [row[:] for row in state]
        for r in range(len(new_state) - 1, -1, -1):
            if new_state[r][col] == '.':
                new_state[r][col] = player
                break
        return new_state

    def evaluate(self, state):
        """Evaluate the score of the given game state.

        Args:
            state (list): The current state of the game.

        Returns:
            score (int): The score of the game state.
        """
        score = 0
        # Compute the score on the rows
        for row in state:
            for col in range(len(row) - 3):
                window = row[col:col + 4]
                score += self.evaluate_window(window)
        # Compute the score on the columns
        for col in range(len(state[0])):
            for row in range(len(state) - 3):
                window = [state[row + i][col] for i in range(4)]
                score += self.evaluate_window(window)
        # Compute the score on the first diagonals
        for row in range(len(state) - 3):
            for col in range(len(state[0]) - 3):
                window = [state[row + i][col + i] for i in range(4)]
                score += self.evaluate_window(window)
        # Compute the score on the second diagonals
        for row in range(len(state) - 3):
            for col in range(3, len(state[0])):
                window = [state[row + i][col - i] for i in range(4)]
                score += self.evaluate_window(window)
        return score

    def evaluate_window(self, window):
        """Evaluate the score of a window (subsequence) in the game state.

        Args:
            window (list): A window of the game state.

        Returns:
            int: The score of the window.
        """
        if window.count('O') == 4:
            return 100
        elif window.count('X') == 4:
            return -100
        elif window.count('O') == 3 and window.count('.') == 1:
            return 5
        elif window.count('O') == 2 and window.count('.') == 2:
            return 2
        elif window.count('X') == 3 and window.count('.') == 1:
            return -5
        elif window.count('X') == 2 and window.count('.') == 2:
            return -2
        else:
            return 0

    def minimax(self, state, depth, maximizing_player):
        """Minimax algorithm for evaluating the game state.

        Args:
            state (list): The current game state.
            depth (int): The depth of the minimax search.
            maximizing_player (bool): True if the current player is maximizing, False otherwise.

        Returns:
            max_eval (int): The max evaluation score for the current state.
            min_eval (int): The min evaluation score for the current state.
        """
        if depth == 0 or self.is_terminal(state):
            return self.evaluate(state)
        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_possible_moves(state):
                child_state = self.make_move(state, move, 'O')
                eval = self.minimax(child_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_possible_moves(state):
                child_state = self.make_move(state, move, 'X')
                eval = self.minimax(child_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def find_best_move(self, state):
        """Finds the best move for the AI using the minimax algorithm.

        Args:
            state (list): The current game state.

        Returns:
            best_move (int): The best move for the AI.
        """
        best_score = float('-inf')
        best_move = None
        for move in self.get_possible_moves(state):
            child_state = self.make_move(state, move, 'O')
            score = self.minimax(child_state, self.depth, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move
    
class MOVABLE_PIECE():
    def __init__(self, cell_size, columns_number, first_player):
        """Initialize the object with specified parameters.

        Args:
            cell_size (int): The size of each cell in the game grid.
            columns_number (int): The number of columns in the game grid.
            first_player (str): The starting player ("player1", "player2", "human", or "computer").
        """
        if first_player == "player1":
            self.computer_game = False
            self.current_player = 1
            self.color = (255, 0, 0)
        elif first_player == "player2":
            self.computer_game = False
            self.current_player = 2
            self.color = (230, 230, 0)
        elif first_player == "human":
            self.computer_game = True
            self.current_player = 1
            self.color = (255, 0, 0)
        elif first_player == "computer":
            self.computer_game = True
            self.current_player = 2
            self.color = (230, 230, 0)
        if columns_number % 2 != 0:
            self.center_x = (columns_number * cell_size) // 2
        else:
            self.center_x = (columns_number * cell_size) // 2 - cell_size // 2
        self.center_y = cell_size // 2
        self.radius = 60

    def compute_position(self, mouse_x, cell_size):
        """Compute the new position of the piece grid based on the mouse input.

        Args:
            mouse_x (int): The x-coordinate of the mouse position.
            cell_size (int): The size of each cell in the game grid.
        """
        location_on_column = mouse_x // cell_size
        self.center_x = location_on_column * cell_size + cell_size // 2

    def draw(self, screen, cell_size):
        """Draw the piece in the game

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
            cell_size (int): The size of each cell in the game grid.
        """
        if self.computer_game == False or (self.computer_game == True and self.current_player == 1):
            pygame.draw.circle(screen, self.color, (self.center_x, self.center_y), cell_size - 60)
            pygame.draw.circle(screen, (0, 0, 0), (self.center_x, self.center_y), cell_size - 60, 2)
    
    def change_player(self):
        """Switch the current player and update the player's color."""
        if self.current_player == 2:
            self.current_player = 1
            self.color = (255, 0, 0)
        else:
            self.current_player = 2
            self.color = (230, 230, 0)

    def update_color(self, player):
        """Update the current player and associated color based on the specified player type.

        Args:
            player (str): The player type ("player1", "player2", "computer", or "human").
        """
        if player == "player1":
            self.current_player = 1
            self.color = (255, 0, 0)
        elif player == "player2":
            self.current_player = 2
            self.color = (230, 230, 0)
        elif player == "computer":
            self.current_player = 2
            self.color = (230, 230, 0)
        elif player == "human":
            self.current_player = 1
            self.color = (255, 0, 0)

class MENU_PAGE():
    def __init__(self):
        """Initialize the menu configuration."""
        self.width = 800
        self.height = 800
        self.button_width = 350
        self.button_height = 100
        self.button_color = (150, 0, 0)
        self.button_text_color = (230, 230, 0)
        self.caption = "Menu"
        self.button_spacing = 30
        self.font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)
        self.logo_font = pygame.font.Font('Font/FaseBulan-BW633.otf', 70)
    
    def compute_button_rect(self, button_texts):
        """Compute the rectangles for menu buttons based on the specified button texts.

        Args:
            button_texts (list): A list of strings representing the text for each menu button.

        Returns:
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                  and its corresponding text.
        """
        buttons = []
        for i, text in enumerate(button_texts):
            button_rect = pygame.Rect(
                                (self.width - self.button_width) // 2,
                                (self.height - (self.button_height + self.button_spacing) * len(button_texts)) // 2 
                                            + i * (self.button_height + self.button_spacing),
                                self.button_width, 
                                self.button_height)
            buttons.append((button_rect, text))
        return buttons
    
    def draw_buttons(self, screen, buttons):
        """Draw menu buttons on the specified Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                            and its corresponding text.
        """
        for button_rect, text in buttons:
            pygame.draw.rect(screen, self.button_color, button_rect, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=15, width=3)
            button_text = self.font.render(text, True, self.button_text_color)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                            button_rect.centery - button_text.get_height() // 2))
    
    def show_menu(self, opponent_type):
        """Display the menu screen with buttons based on the specified opponent type.

        Args:
            opponent_type (str): The type of opponent ("human" or "computer").

        Returns:
            test (str): The selected option ("Play", "Easy", "Medium", "Hard", "Exit") or exits the program.
        """
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.caption)
        if opponent_type == "human":
            button_texts = ["Play", "Exit"]
        elif opponent_type == "computer":
            button_texts = ["Easy", "Medium", "Hard", "Exit"]    
        buttons = self.compute_button_rect(button_texts)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(event.pos):
                            if text == "Exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                pygame.quit()
                                return text
            screen.fill((0, 0, 100)) 
            title_text = self.logo_font.render("4 in a ROW", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.width // 2, 70))
            screen.blit(title_text, title_rect)   
            self.draw_buttons(screen, buttons)
            pygame.display.flip()

class WINNER_PAGE_AI:
    """Initialize the configuration of the winner's page for the computer opponent selection."""
    def __init__(self):
        self.width = 800
        self.height = 800
        self.button_width = 350
        self.button_height = 100
        self.button_color = (150, 0, 0)
        self.button_text_color = (230, 230, 0)
        self.buttons_texts = ["Easy", "Medium", "Hard", "Exit"]
        self.button_spacing = 30

    def show_winner_page(self, winner):
        """Display the winner and option buttons.

        Args:
            winner (str): The winner of the game ("X", "O", or ".").

        Returns:
            test (str): The selected option ("Easy", "Medium", "Hard", "Exit") or exits the program.
        """
        pygame.init()
        message_font = pygame.font.Font('Font/FaseBulan-BW633.otf', 80)
        buttons_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("4 in a ROW")
        if winner == "X":
            winner_text = message_font.render(f"YOU  WON!", True, (255, 0, 0))
        elif winner == "O":
            winner_text = message_font.render(f"Computer won!", True, (230, 230, 0))
        else:
            winner_text = message_font.render(f"Draw!", True, (255, 255, 255))
        buttons = self.compute_button_rect(self.buttons_texts)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(event.pos):
                            if text == "Exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                pygame.quit()
                                return text
            screen.fill((0, 0, 100))
            if winner == "X":
                screen.blit(winner_text, (250, 50))
            elif winner == "O":
                screen.blit(winner_text, (200, 50))
            else :
                screen.blit(winner_text, (300, 50))
            self.draw_buttons(screen, buttons, buttons_font)
            pygame.display.flip()

    def compute_button_rect(self, buttons_texts):
        """Compute the rectangles for winner's page buttons based on the specified button texts.

        Args:
            buttons_texts (list): A list of strings representing the text for each button.

        Returns:
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                  and its corresponding text.
        """
        buttons = []
        for i, text in enumerate(buttons_texts):
            button_rect = pygame.Rect((self.width - self.button_width) // 2,
                                      (self.height - (self.button_height + self.button_spacing) * len(buttons_texts)) // 2 
                                                + i * (self.button_height + self.button_spacing),
                                      self.button_width, 
                                      self.button_height)
            buttons.append((button_rect, text))
        return buttons

    def draw_buttons(self, screen, buttons, buttons_font):
        """Draw winner's page buttons on the specified Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                            and its corresponding text.
            buttons_font (pygame.font.Font): The font used for the text on the buttons.
        """
        for button_rect, text in buttons:
            pygame.draw.rect(screen, self.button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=10, width=3)
            button_text = buttons_font.render(text, True, self.button_text_color)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                      button_rect.centery - button_text.get_height() // 2))

class WINNER_PAGE_1v1:
    """Initialize the configuration of the winner's page for the human opponent selection."""
    def __init__(self):
        self.width = 800
        self.height = 800
        self.button_width = 350
        self.button_height = 100
        self.button_color = (150, 0, 0)
        self.button_text_color = (230, 230, 0)
        self.buttons_texts = ['Play again', 'Exit']
        self.button_spacing = 30

    def show_winner_page(self, winner):
        """Display the winner and option buttons.

        Args:
            winner (str): The winner of the game ("X", "O", or "." for a draw).

        Returns:
            test (str): The selected option ("Play again", "Exit") or exits the program.
        """
        pygame.init()
        message_font = pygame.font.Font('Font/FaseBulan-BW633.otf', 80)
        buttons_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 40)
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("4 in a ROW")
        if winner == "X":
            winner_text = message_font.render(f"Winner:     PLAYER  1!", True, (255, 0, 0))
        elif winner == "O":
            winner_text = message_font.render(f"Winner:     PLAYER  2!", True, (230, 230, 0))
        else:
            winner_text = message_font.render(f"Draw!", True, (255, 255, 255))
        buttons = self.compute_button_rect(self.buttons_texts)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button_rect, text in buttons:
                        if button_rect.collidepoint(event.pos):
                            if text == "Exit":
                                pygame.quit()
                                sys.exit()
                            else:
                                pygame.quit()
                                return text
            screen.fill((0, 0, 100))
            if winner == ".":
                screen.blit(winner_text, (300,100))
            else:
                screen.blit(winner_text, (150, 100))
            self.draw_buttons(screen, buttons, buttons_font)
            pygame.display.flip()

    def compute_button_rect(self, buttons_texts):
        """Compute the rectangles for menu buttons based on the specified button texts.

        Args:
            buttons_texts (list): A list of strings representing the text for each menu button.

        Returns:
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                  and its corresponding text.
        """
        buttons = []
        for i, text in enumerate(buttons_texts):
            button_rect = pygame.Rect((self.width - self.button_width) // 2,
                                      (self.height - (self.button_height + self.button_spacing) * len(buttons_texts)) // 2 
                                                    + i * (self.button_height + self.button_spacing),
                                      self.button_width,
                                      self.button_height)
            buttons.append((button_rect, text))
        return buttons

    def draw_buttons(self, screen, buttons, buttons_font):
        """Draw menu buttons on the specified Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
            buttons (list): A list of tuples, where each tuple contains a button rectangle (pygame.Rect) 
                            and its corresponding text.
            buttons_font (pygame.font.Font): The font used for the text on menu buttons.
        """
        for button_rect, text in buttons:
            pygame.draw.rect(screen, self.button_color, button_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), button_rect, border_radius=10, width=3)
            button_text = buttons_font.render(text, True, self.button_text_color)
            screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                      button_rect.centery - button_text.get_height() // 2))

class GAME_1V1():
    def __init__(self, row_size, column_size, first_player):
        """Initialize the game with the specified parameters.

        Args:
            row_size (int): The number of rows in the game board.
            column_size (int): The number of columns in the game board.
            first_player (str): The player who move first ("player1" or "player2").
        """
        self.caption = "4 in a ROW"
        self.winning_pieces = None
        self.rows_number = row_size
        self.columns_number = column_size
        self.first_player = first_player
        self.cell_size = 100
        self.state = [['.' for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        self.movable_piece = MOVABLE_PIECE(self.cell_size, self.columns_number, first_player)
        self.winner_page = WINNER_PAGE_1v1()

    def play(self):
        """Main game loop to handle player input, execute moves, and display the game state."""
        screen = pygame.display.set_mode((self.cell_size * self.columns_number, self.cell_size * (self.rows_number + 1)))
        pygame.display.set_caption(self.caption)
        while True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.movable_piece.compute_position(mouse_x, self.cell_size)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1: 
                            if self.is_valid_move():
                                self.execute_move()
                                self.movable_piece.change_player()
            response_winner = self.is_a_winner()
            response_draw = self.is_draw()
            if response_draw == True:
                self.winning_pieces = ['.']
                for i in range(self.rows_number):
                    for j in range(self.columns_number):
                        self.winning_pieces.append((i, j))
            if response_winner is not None:
                self.winning_pieces = []
                self.winning_pieces = response_winner
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 100), (0, self.cell_size, self.cell_size * self.columns_number, self.cell_size * self.rows_number))
            self.generate_pieces(screen)
            self.movable_piece.draw(screen, self.cell_size)
            if self.winning_pieces != None:
                self.color_winning_pieces(screen, self.winning_pieces[1:])
                pygame.display.flip()
                time.sleep(2)
                pygame.quit()
                result = self.winner_page.show_winner_page(self.winning_pieces[0])
                if result == "Play again":
                    self.movable_piece.update_color(self.first_player)
                    self.reset_state()
                    self.play()
            else:
                pygame.display.flip()

    def generate_pieces(self, screen):
        """Draw game pieces on the Pygame screen based on the current game state.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
        """
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                center_x = (j + 1) * self.cell_size - self.cell_size // 2
                center_y = (i + 2) * self.cell_size - self.cell_size // 2 
                if (self.state[i][j] == '.'):
                    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)
                elif self.state[i][j] == 'O':
                    pygame.draw.circle(screen, (230, 230, 0), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)

    def is_valid_move(self):
        """Check if the current position of the movable piece represents a valid move.

        Returns:
            True (bool): if the move is valid.
            False (bool): if the move is not valid.
        """
        column = self.movable_piece.center_x // self.cell_size
        for i in range(self.rows_number):
            if self.state[i][column] == '.':
                return True
        return False
    
    def execute_move(self):
        """Execute the current player's move and update the game state."""
        column = self.movable_piece.center_x // self.cell_size
        line = self.get_available_position(column)
        if self.movable_piece.current_player == 1:
            self.state[line][column] = 'X'
        else:
            self.state[line][column] = 'O'

    def get_available_position(self, column):
        """Get the available position (row) in the specified column.

        Args:
            column (int): The column index.

        Returns:
            line (int): The row of the available cell
        """
        line = 0
        for i in range(self.rows_number):
            if self.state[i][column] == '.':
                line = i
        return line
    
    def is_draw(self):
        """Check if the current game state represents a draw.

        Returns:
            True (bool): if the game is a draw.
            False (bool): if the game is not a draw.
        """
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                if self.state[i][j] == '.':
                    return False
        return True
    
    def is_a_winner(self):
        """Check if there is a winner in the current game state.

        Returns:
            (list): List containing the winning player, and positions of the winning pieces, if a winner is found.
            None: if no winner is found.
        """
        rows = len(self.state)
        cols = len(self.state[0])
        matrix = self.state
        # Verify if is a winner on the rows
        for row in range(rows):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row][col + 1] == matrix[row][col + 2] == matrix[row][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row, col + 1), (row, col + 2), (row, col + 3)]
        # Verify if is a winner on the columns
        for row in range(rows - 3):
            for col in range(cols):
                if matrix[row][col] == matrix[row + 1][col] == matrix[row + 2][col] == matrix[row + 3][col] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col),  (row+1,col),(row+2,col), (row+3,col)]
        # Verify if is a winner on the first diagonal
        for row in range(rows - 3):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row + 1][col + 1] == matrix[row + 2][col + 2] == matrix[row + 3][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row+1,col+1), (row+2,col+2), (row+3,col+3)]
        # Verify if is a winner on the second diagonal
        for row in range(3, rows):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row - 1][col + 1] == matrix[row - 2][col + 2] == matrix[row - 3][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row - 1,col + 1), (row - 2, col + 2), (row - 3,col + 3)]
        return None
    
    def reset_state(self):
        """Reset the game state to its initial configuration."""
        self.state = [['.' for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        self.winning_pieces = None
    
    def color_winning_pieces(self, screen, pieces):
        """Highlight the winning pieces on the Pygame screen.

        Args:
            screen (pygame.Surface): The Pygame screen surface to draw on.
            pieces (list): List of positions representing the winning pieces.
        """
        for piece in pieces:
            center_x = (piece[1] + 1) * self.cell_size - self.cell_size // 2
            center_y = (piece[0] + 2) * self.cell_size - self.cell_size // 2 
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.cell_size - 60, 3)

class GAME_AI():
    def __init__(self,row_size, column_size, first_player, game_mode):
        """Initialize the AI version of the 4 in a Row game.

        Args:
            row_size (int): Number of rows in the game grid.
            column_size (int): Number of columns in the game grid.
            first_player (str): Identifier for the first player ('human' or 'computer').
            game_mode (str): Game mode identifier ('Easy', 'Medium', 'Hard').
        """
        self.caption = "4 in a Row"
        self.last_move = "Random"
        self.rows_number = row_size
        self.columns_number = column_size
        self.first_player = first_player
        self.current_player = first_player
        self.game_mode = game_mode
        self.winning_pieces = None
        self.cell_size = 100
        self.state = [['.' for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        self.movable_piece = MOVABLE_PIECE(self.cell_size, self.columns_number, first_player)
        self.winner_page = WINNER_PAGE_AI()
        self.minimax_hard = MINIMAX_ALGORITHM(3)
        self.minimax_medium = MINIMAX_ALGORITHM(2)
        self.minimax_easy = MINIMAX_ALGORITHM(0)
    
    def play(self):
        """Main game loop for playing the AI version of 4 in a Row."""
        screen = pygame.display.set_mode((self.cell_size * self.columns_number, self.cell_size * (self.rows_number + 1)))
        pygame.display.set_caption(self.caption)
        while True:
            if self.current_player == "human":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEMOTION:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        self.movable_piece.compute_position(mouse_x, self.cell_size)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.is_valid_move():
                                self.execute_move()
                                self.movable_piece.change_player()
                                self.current_player = "computer"
            elif self.current_player == "computer":
                if self.game_mode == "Easy":
                    if self.last_move == "Random":
                        ai_move = self.minimax_easy.find_best_move(self.state)
                        self.execute_ai_move(ai_move)
                        self.current_player = "human"
                        self.movable_piece.change_player()
                        self.start_move = "Smart"
                    else:
                        ai_move = random.randint(0, self.columns_number - 1)
                        while self.state[0][ai_move] != '.':
                            ai_move = random.randint(0, self.columns_number - 1)
                        self.execute_ai_move(ai_move)
                        self.current_player = "human"
                        self.movable_piece.change_player()
                        self.start_move = "Random"
                elif self.game_mode == "Medium":
                    ai_move = self.minimax_medium.find_best_move(self.state)
                    self.execute_ai_move(ai_move)
                    self.current_player = "human"
                    self.movable_piece.change_player()
                elif self.game_mode == "Hard":
                    ai_move = self.minimax_hard.find_best_move(self.state)
                    self.execute_ai_move(ai_move)
                    self.current_player = "human"
                    self.movable_piece.change_player()
            response_winner = self.is_a_winner()
            response_draw = self.is_draw()
            if response_draw == True:
                self.winning_pieces = ['.']
                for i in range(self.rows_number):
                    for j in range(self.columns_number):
                        self.winning_pieces.append((i, j))
            if response_winner is not None:
                self.winning_pieces = []
                self.winning_pieces = response_winner
            screen.fill((255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 100), (0, self.cell_size, self.cell_size * self.columns_number, self.cell_size * self.rows_number))
            self.generate_pieces(screen)
            self.movable_piece.draw(screen, self.cell_size)
            if self.winning_pieces != None:
                self.color_winning_pieces(screen, self.winning_pieces[1:])
                pygame.display.flip()
                time.sleep(2)
                pygame.quit()
                result = self.winner_page.show_winner_page(self.winning_pieces[0])
                if result == "Easy":
                    self.current_player = self.first_player
                    self.movable_piece.update_color(self.first_player)
                    self.reset_state()
                    self.game_mode = "Easy"
                    self.play()
                elif result == "Medium":
                    self.movable_piece.update_color(self.first_player)
                    self.current_player = self.first_player
                    self.reset_state()
                    self.game_mode = "Medium"
                    self.play()
                    return 0
                elif result == "Hard":
                    self.movable_piece.update_color(self.first_player)
                    self.current_player = self.first_player
                    self.reset_state()
                    self.game_mode = "Hard"
                    self.play()
            else:
                pygame.display.flip()
    
    def execute_ai_move(self,ai_move):
        """Execute the AI move and update the game state.

        Args:
            ai_move (int): The column where the AI (computer) decides to make a move.
        """
        line = self.get_available_position(ai_move)
        self.state[line][ai_move] = 'O'

    def generate_pieces(self, screen):
        """Generate and draw the game pieces on the screen based on the current game state.

        Args:
            screen (pygame.Surface): The surface representing the game window.
        """
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                center_x = (j + 1) * self.cell_size - self.cell_size // 2
                center_y = (i + 2) * self.cell_size - self.cell_size // 2 
                if (self.state[i][j] == '.'):
                    pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)
                elif self.state[i][j] == 'O':
                    pygame.draw.circle(screen, (230, 230, 0), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)
                else:
                    pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), self.cell_size - 60)
                    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), self.cell_size - 60, 3)

    def is_a_winner(self):
        """Check if there is a winner on the game board.

        Returns:
            (list): If there is a winner, returns a list of tuples with winner's pieces
            None: If there is not a winner.
        """
        rows = len(self.state)
        cols = len(self.state[0])
        matrix = self.state
        # Verify if is a winner on the rows
        for row in range(rows):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row][col + 1] == matrix[row][col + 2] == matrix[row][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row, col + 1), (row, col + 2), (row, col + 3)]
        # Verify if is a winner on the columns
        for row in range(rows - 3):
            for col in range(cols):
                if matrix[row][col] == matrix[row + 1][col] == matrix[row + 2][col] == matrix[row + 3][col] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col),  (row+1,col),(row+2,col), (row+3,col)]
        # Verify if is a winner on the first diagonals
        for row in range(rows - 3):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row + 1][col + 1] == matrix[row + 2][col + 2] == matrix[row + 3][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row+1,col+1), (row+2,col+2), (row+3,col+3)]
        # Verify if is a winner on the second diagonals
        for row in range(3, rows):
            for col in range(cols - 3):
                if matrix[row][col] == matrix[row - 1][col + 1] == matrix[row - 2][col + 2] == matrix[row - 3][col + 3] and matrix[row][col] != '.':
                    return [matrix[row][col], (row,col), (row - 1,col + 1), (row - 2, col + 2), (row - 3,col + 3)]
        return None
    
    def is_valid_move(self):
        """Check if the current move is valid.

        Returns:
            True (bool): If the move is valid.
            False (bool): If the move is not valid.
        """
        column = self.movable_piece.center_x // self.cell_size
        for i in range(self.rows_number):
            if self.state[i][column] == '.':
                return True
        return False

    def execute_move(self):
        """Execute the current move."""
        column = self.movable_piece.center_x // self.cell_size
        line = self.get_available_position(column)
        self.state[line][column] = 'X'

    def get_available_position(self, column):
        """Get the available position (line) in the selected column.

        Args:
            column (int): The column index for which to find the available position.
        """
        line = 0
        for i in range(self.rows_number):
            if self.state[i][column] == '.':
                line = i
        return line
    
    def color_winning_pieces(self, screen, pieces):
        """Highlight the winning pieces on the game screen.

        Args:
            screen (pygame.Surface): The surface to draw on.
            pieces (list): List of winning piece positions, where each piece is represented as a tuple (row, column).
        """
        for piece in pieces:
            center_x = (piece[1] + 1) * self.cell_size - self.cell_size // 2
            center_y = (piece[0] + 2) * self.cell_size - self.cell_size // 2 
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), self.cell_size - 60, 3)

    def is_draw(self):
        """Check if the game is a draw.

        Returns:
            True (bool): If the game is a draw.
            False (bool): If the game is not a draw.
        """
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                if self.state[i][j] == '.':
                    return False
        return True
    
    def reset_state(self):
        """Reset the game state and winning pieces."""
        self.state = [['.' for _ in range(self.columns_number)] for _ in range(self.rows_number)]
        self.winning_pieces = None
    
def FourInROW_game(opponent_type, row_size, column_size, first_player):
    """Main function to start the Four in a Row game.

    Args:
        opponent_type (str): Type of opponent ("human" or "computer").
        row_size (int): Number of rows in the game grid.
        column_size (int): Number of columns in the game grid.
        first_player (str): Starting player ("player1", "player2", "human", or "computer").
    """
    pygame.init()
    menu = MENU_PAGE()
    while(True):
        game_mode = menu.show_menu(opponent_type)
        if game_mode == "Play":
            game_1v1 = GAME_1V1(row_size, column_size, first_player)
            game_1v1.play()
        if game_mode == "Easy" or game_mode == "Medium" or game_mode == "Hard":
            game_ai = GAME_AI(row_size, column_size, first_player, game_mode)
            game_ai.play()

def validate(opponent_type, row_size, column_size, first_player):
    """Validate input parameters for starting the Four in a Row game.

    Args:
        opponent_type (str): Type of opponent ("human" or "computer").
        row_size (str): Number of rows in the game grid.
        column_size (str): Number of columns in the game grid.
        first_player (str): Starting player ("player1", "player2", "human", or "computer").
    """
    try:
        if opponent_type != "human" and opponent_type != "computer":
            raise Exception(f"ERROR: Opponent type must be 'human' or 'computer'!")
        if int(row_size) < 4 or int(row_size) > 8:
            raise Exception(f"ERROR: The number of rows must be between 4 and 8!")
        if int(column_size) < 4 or int(column_size) > 16:
            raise Exception(f"ERROR: The number of columns must be between 4 and 16!")
        if opponent_type == "human":
            if first_player != "player1" and first_player != "player2":
                raise Exception(f"ERROR: In 1v1 games, the first move should be made by 'player1' or 'player2'!")
        elif opponent_type == "computer": 
            if first_player != "computer" and first_player != "human":
                raise Exception(f"ERROR: In the games against computer, the first move should be made by 'Computer' or 'Human'!")

    except ValueError as e:
        print(e)
    except Exception  as e:
        print(e)
    else:
        FourInROW_game(opponent_type, int(row_size), int(column_size), first_player)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Start game: python 4inaROW.py <opponent_type> <row_size> <column_size> <first_player>")
    else:
        validate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])