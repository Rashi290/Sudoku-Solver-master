#!/usr/bin/python
# -*- coding: utf-8 -*-
from sudokutools import valid, solve, find_empty, generate_board
from copy import deepcopy
from sys import exit
import pygame
import time
import random

pygame.init()

# Modern vibrant color scheme
COLORS = {
    'bg': (240, 242, 247),
    'board_bg': (255, 255, 255),
    'board_shadow': (220, 220, 230),
    'grid_line': (230, 232, 240),
    'grid_bold': (80, 90, 120),
    'selected': (100, 180, 255),
    'selected_light': (200, 230, 255),
    'correct': (76, 175, 80),
    'correct_light': (200, 230, 200),
    'incorrect': (244, 67, 54),
    'incorrect_light': (255, 200, 200),
    'original_text': (25, 25, 35),
    'user_text': (50, 60, 80),
    'button': (99, 102, 241),
    'button_hover': (79, 70, 229),
    'button_shadow': (60, 50, 200),
    'button_text': (255, 255, 255),
    'timer_bg': (99, 102, 241),
    'timer_shadow': (60, 50, 200),
    'timer_text': (255, 255, 255),
    'title': (30, 30, 50),
    'subtitle': (100, 100, 120),
}


class Button:
    def __init__(self, x, y, width, height, text, color=COLORS['button'], hover_color=COLORS['button_hover']):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.clicked = False
        
    def draw(self, window):
        # Check if mouse is hovering
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        
        # Draw shadow
        shadow_rect = pygame.Rect(self.rect.x + 3, self.rect.y + 3, self.rect.width, self.rect.height)
        pygame.draw.rect(window, COLORS['button_shadow'], shadow_rect, border_radius=8)
        
        # Draw button with gradient effect
        pygame.draw.rect(window, self.current_color, self.rect, border_radius=8)
        
        # Draw inner highlight
        highlight_rect = pygame.Rect(self.rect.x + 1, self.rect.y + 1, self.rect.width - 2, 15)
        highlight_surface = pygame.Surface((self.rect.width - 2, 15))
        highlight_surface.set_alpha(100)
        highlight_surface.fill((255, 255, 255))
        window.blit(highlight_surface, (self.rect.x + 1, self.rect.y + 1))
        
        # Draw text with shadow
        font = pygame.font.SysFont("Arial", 20, bold=True)
        text_surface = font.render(self.text, True, COLORS['button_text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Text shadow
        shadow_text = font.render(self.text, True, (0, 0, 0))
        shadow_rect_text = shadow_text.get_rect(center=(self.rect.centerx + 1, self.rect.centery + 1))
        window.blit(shadow_text, shadow_rect_text)
        window.blit(text_surface, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Board:
    def __init__(self, window):
        """
        Initializes a Board object.
        """
        # Generate a new Sudoku board and create a solved version of it.
        self.board = generate_board()
        # Store original board to prevent editing pre-filled cells
        self.originalBoard = [row[:] for row in self.board]
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        # Create a 2D list of Tile objects to represent the Sudoku board.
        # Tile(x, y) where x is column (j) and y is row (i)
        self.tiles = [
            [Tile(self.board[i][j], window, j * 60, i * 60) for j in range(9)]
            for i in range(9)
        ]
        self.window = window

    def generate_new(self):
        """Generate a new puzzle"""
        self.board = generate_board()
        self.originalBoard = [row[:] for row in self.board]
        self.solvedBoard = deepcopy(self.board)
        solve(self.solvedBoard)
        # Tile(x, y) where x is column (j) and y is row (i)
        self.tiles = [
            [Tile(self.board[i][j], self.window, j * 60, i * 60) for j in range(9)]
            for i in range(9)
        ]
        # Reset tile states
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].selected = False
                self.tiles[i][j].correct = False
                self.tiles[i][j].incorrect = False

    def draw_board(self):
        """
        Draws the Sudoku board on the Pygame window.
        """
        # Draw shadow for board
        shadow_rect = pygame.Rect(5, 5, 540, 540)
        pygame.draw.rect(self.window, COLORS['board_shadow'], shadow_rect, border_radius=5)
        
        # Draw background for board
        board_rect = pygame.Rect(0, 0, 540, 540)
        pygame.draw.rect(self.window, COLORS['board_bg'], board_rect, border_radius=5)
        
        for i in range(9):
            for j in range(9):
                # Draw vertical lines every three columns.
                if j % 3 == 0 and j != 0:
                    pygame.draw.line(
                        self.window,
                        COLORS['grid_bold'],
                        (j * 60, 0),
                        (j * 60, 540),
                        3,
                    )
                # Draw horizontal lines every three rows.
                if i % 3 == 0 and i != 0:
                    pygame.draw.line(
                        self.window,
                        COLORS['grid_bold'],
                        (0, i * 60),
                        (540, i * 60),
                        3,
                    )
                # Draw the Tile object on the board.
                self.tiles[i][j].draw(COLORS['grid_line'], 1)

                # Display the Tile value if it is not 0 (empty).
                if self.tiles[i][j].value != 0:
                    # Use different styling for original (pre-filled) numbers vs user-entered
                    if hasattr(self, 'originalBoard') and self.originalBoard[i][j] != 0:
                        # Original number - use bold and darker color
                        self.tiles[i][j].display(
                            self.tiles[i][j].value, (0, 0), COLORS['original_text'], bold=True
                        )
                    else:
                        # User-entered number - use regular color
                        self.tiles[i][j].display(
                            self.tiles[i][j].value, (0, 0), COLORS['user_text'], bold=False
                        )
        # Draw border around board with shadow effect
        pygame.draw.rect(self.window, COLORS['grid_bold'], board_rect, width=4, border_radius=5)

    def deselect(self, tile):
        """
        Deselects all tiles except the given tile.
        """
        for i in range(9):
            for j in range(9):
                if self.tiles[i][j] != tile:
                    self.tiles[i][j].selected = False

    def redraw(self, keys, wrong, time_str, buttons, wrong_moves=0, game_over=False):
        """
        Redraws the Sudoku board with modern UI.
        """
        # Fill background
        self.window.fill(COLORS['bg'])
        
        # Draw board
        self.draw_board()
        
        # Draw tiles with highlights and values
        for i in range(9):
            for j in range(9):
                # Draw background highlight first
                if self.tiles[i][j].selected:
                    # highlight selected tiles with light background
                    highlight_rect = pygame.Rect(j * 60 + 1, i * 60 + 1, 58, 58)
                    pygame.draw.rect(self.window, COLORS['selected_light'], highlight_rect, border_radius=3)
                    self.tiles[i][j].draw(COLORS['selected'], 3)
                elif self.tiles[i][j].correct:
                    # highlight correct tiles
                    highlight_rect = pygame.Rect(j * 60 + 1, i * 60 + 1, 58, 58)
                    pygame.draw.rect(self.window, COLORS['correct_light'], highlight_rect, border_radius=3)
                    self.tiles[i][j].draw(COLORS['correct'], 3)
                elif self.tiles[i][j].incorrect:
                    # highlight incorrect tiles
                    highlight_rect = pygame.Rect(j * 60 + 1, i * 60 + 1, 58, 58)
                    pygame.draw.rect(self.window, COLORS['incorrect_light'], highlight_rect, border_radius=3)
                    self.tiles[i][j].draw(COLORS['incorrect'], 3)
                
                # Always display the value if it exists (after highlights so it's on top)
                if self.tiles[i][j].value != 0:
                    if hasattr(self, 'originalBoard') and self.originalBoard[i][j] != 0:
                        # Original number - bold
                        self.tiles[i][j].display(
                            self.tiles[i][j].value, (0, 0), COLORS['original_text'], bold=True
                        )
                    else:
                        # User-entered number - regular
                        self.tiles[i][j].display(
                            self.tiles[i][j].value, (0, 0), COLORS['user_text'], bold=False
                        )

        # Display preview values (from keyDict) - only if cell is empty
        if len(keys) != 0:
            for value in keys:
                row, col = value
                # Only show preview if cell is actually empty
                if self.tiles[row][col].value == 0:
                    self.tiles[row][col].display(
                        keys[value],
                        (0, 0),
                        (150, 150, 150),
                        bold=False
                    )

        # Draw title
        title_font = pygame.font.SysFont("Arial", 32, bold=True)
        title_text = title_font.render("SUDOKU", True, COLORS['title'])
        title_rect = title_text.get_rect(center=(660, 30))
        # Title shadow
        title_shadow = title_font.render("SUDOKU", True, (200, 200, 220))
        title_shadow_rect = title_shadow.get_rect(center=(661, 31))
        self.window.blit(title_shadow, title_shadow_rect)
        self.window.blit(title_text, title_rect)
        
        # Draw timer with modern design and shadow
        timer_rect = pygame.Rect(560, 60, 200, 70)
        # Shadow
        timer_shadow_rect = pygame.Rect(563, 63, 200, 70)
        pygame.draw.rect(self.window, COLORS['timer_shadow'], timer_shadow_rect, border_radius=12)
        # Main timer box
        pygame.draw.rect(self.window, COLORS['timer_bg'], timer_rect, border_radius=12)
        
        font = pygame.font.SysFont("Arial", 12, bold=True)
        label = font.render("⏱ TIME", True, COLORS['timer_text'])
        label_rect = label.get_rect(center=(660, 80))
        self.window.blit(label, label_rect)
        
        font = pygame.font.SysFont("Arial", 28, bold=True)
        time_text = font.render(time_str, True, COLORS['timer_text'])
        time_rect = time_text.get_rect(center=(660, 105))
        # Text shadow
        time_shadow = font.render(time_str, True, (60, 50, 200))
        time_shadow_rect = time_shadow.get_rect(center=(661, 106))
        self.window.blit(time_shadow, time_shadow_rect)
        self.window.blit(time_text, time_rect)

        # Draw wrong moves counter (X/3) - always show if wrong_moves > 0
        if wrong_moves > 0:
            wrong_moves_rect = pygame.Rect(560, 145, 200, 60)
            # Shadow
            wrong_moves_shadow_rect = pygame.Rect(563, 148, 200, 60)
            # Color gets more intense as wrong moves increase
            if wrong_moves >= 3:
                bg_color = COLORS['incorrect']
                shadow_color = (200, 50, 50)
            elif wrong_moves == 2:
                bg_color = (255, 152, 0)
                shadow_color = (200, 100, 0)
            else:
                bg_color = (255, 193, 7)
                shadow_color = (200, 150, 0)
            
            pygame.draw.rect(self.window, shadow_color, wrong_moves_shadow_rect, border_radius=10)
            # Main wrong moves box
            pygame.draw.rect(self.window, bg_color, wrong_moves_rect, border_radius=10)
            
            font = pygame.font.SysFont("Arial", 13, bold=True)
            label = font.render("⚠ WRONG MOVES", True, COLORS['button_text'])
            label_rect = label.get_rect(center=(660, 165))
            self.window.blit(label, label_rect)
            
            font = pygame.font.SysFont("Arial", 24, bold=True)
            wrong_moves_text = font.render(f"{wrong_moves}/3", True, COLORS['button_text'])
            wrong_moves_rect_text = wrong_moves_text.get_rect(center=(660, 185))
            # Text shadow
            wrong_moves_shadow = font.render(f"{wrong_moves}/3", True, (150, 0, 0))
            wrong_moves_shadow_rect_text = wrong_moves_shadow.get_rect(center=(661, 186))
            self.window.blit(wrong_moves_shadow, wrong_moves_shadow_rect_text)
            self.window.blit(wrong_moves_text, wrong_moves_rect_text)
        
        # Draw mistakes counter with shadow (always show if wrong > 0)
        if wrong > 0:
            mistake_rect = pygame.Rect(560, 215, 200, 60)
            # Shadow
            mistake_shadow_rect = pygame.Rect(563, 218, 200, 60)
            pygame.draw.rect(self.window, (200, 50, 50), mistake_shadow_rect, border_radius=10)
            # Main mistake box
            pygame.draw.rect(self.window, COLORS['incorrect'], mistake_rect, border_radius=10)
            
            font = pygame.font.SysFont("Arial", 13, bold=True)
            label = font.render("❌ MISTAKES", True, COLORS['button_text'])
            label_rect = label.get_rect(center=(660, 235))
            self.window.blit(label, label_rect)
            
            font = pygame.font.SysFont("Arial", 24, bold=True)
            mistake_text = font.render(str(wrong), True, COLORS['button_text'])
            mistake_rect_text = mistake_text.get_rect(center=(660, 255))
            # Text shadow
            mistake_shadow = font.render(str(wrong), True, (150, 0, 0))
            mistake_shadow_rect = mistake_shadow.get_rect(center=(661, 256))
            self.window.blit(mistake_shadow, mistake_shadow_rect)
            self.window.blit(mistake_text, mistake_rect_text)

        # Draw buttons
        for button in buttons:
            button.draw(self.window)
        
        # Draw game over overlay on top of everything if game is over
        if game_over:
            # Draw semi-transparent overlay over board
            overlay = pygame.Surface((540, 540))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, 0))
            
            # Game over text box - centered on board
            game_over_box = pygame.Rect(120, 220, 300, 100)
            game_over_shadow = pygame.Rect(123, 223, 300, 100)
            pygame.draw.rect(self.window, (50, 50, 70), game_over_shadow, border_radius=15)
            pygame.draw.rect(self.window, (255, 255, 255), game_over_box, border_radius=15)
            pygame.draw.rect(self.window, COLORS['incorrect'], game_over_box, width=4, border_radius=15)
            
            # GAME OVER text - bigger and more prominent
            font = pygame.font.SysFont("Arial", 56, bold=True)
            title = font.render("GAME OVER", True, COLORS['incorrect'])
            title_rect = title.get_rect(center=(270, 250))
            # Shadow
            title_shadow = font.render("GAME OVER", True, (200, 50, 50))
            title_shadow_rect = title_shadow.get_rect(center=(271, 251))
            self.window.blit(title_shadow, title_shadow_rect)
            self.window.blit(title, title_rect)
            
            # Message
            font = pygame.font.SysFont("Arial", 18, bold=True)
            message = font.render("Click 'New Puzzle' to restart", True, COLORS['subtitle'])
            msg_rect = message.get_rect(center=(270, 285))
            self.window.blit(message, msg_rect)
            
        pygame.display.flip()

    def visualSolve(self, wrong, time_str, buttons, wrong_moves=0, game_over=False):
        """
        Recursively solves the Sudoku board visually.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        empty = find_empty(self.board)
        if not empty:
            return True

        for nums in range(9):
            if valid(self.board, (empty[0], empty[1]), nums + 1):
                self.board[empty[0]][empty[1]] = nums + 1
                self.tiles[empty[0]][empty[1]].value = nums + 1
                self.tiles[empty[0]][empty[1]].correct = True
                pygame.time.delay(50)
                self.redraw({}, wrong, time_str, buttons, wrong_moves, game_over)

                if self.visualSolve(wrong, time_str, buttons, wrong_moves, game_over):
                    return True

                self.board[empty[0]][empty[1]] = 0
                self.tiles[empty[0]][empty[1]].value = 0
                self.tiles[empty[0]][empty[1]].incorrect = True
                self.tiles[empty[0]][empty[1]].correct = False
                pygame.time.delay(50)
                self.redraw({}, wrong, time_str, buttons, wrong_moves, game_over)

    def fill_all_answers(self):
        """Fill all empty cells with correct answers"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.board[i][j] = self.solvedBoard[i][j]
                    self.tiles[i][j].value = self.solvedBoard[i][j]
                    self.tiles[i][j].correct = True
                    self.tiles[i][j].incorrect = False

    def check_solution(self):
        """Check if current solution is correct"""
        return self.board == self.solvedBoard

    def hint(self, keys):
        """
        Provides a hint by filling in a random empty tile with the correct number.
        """
        if self.board == self.solvedBoard:
            return False
        
        empty_cells = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    empty_cells.append((i, j))
        
        if not empty_cells:
            return False
        
        row, col = random.choice(empty_cells)
        
        if (row, col) in keys:
            del keys[(row, col)]
        
        self.board[row][col] = self.solvedBoard[row][col]
        self.tiles[row][col].value = self.solvedBoard[row][col]
        self.tiles[row][col].correct = True
        self.tiles[row][col].incorrect = False
        
        return True


class Tile:
    def __init__(self, value, window, x1, y1):
        self.value = value
        self.window = window
        self.rect = pygame.Rect(x1, y1, 60, 60)
        self.selected = False
        self.correct = False
        self.incorrect = False

    def draw(self, color, thickness):
        pygame.draw.rect(self.window, color, self.rect, thickness)

    def display(self, value, position, color, bold=False):
        if bold:
            font = pygame.font.SysFont("Arial", 45, bold=True)
        else:
            font = pygame.font.SysFont("Arial", 45)
        text = font.render(str(value), True, color)
        # Center the text in the cell
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.window.blit(text, text_rect)

    def clicked(self, mousePos):
        if self.rect.collidepoint(mousePos):
            self.selected = True
        return self.selected


def show_game_over_screen(screen, time_str, buttons):
    """Display game over screen when player makes 3 wrong moves"""
    # Draw semi-transparent overlay (only over board area)
    overlay = pygame.Surface((540, 540))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Game over box with shadow
    game_over_box = pygame.Rect(200, 150, 400, 300)
    game_over_shadow = pygame.Rect(203, 153, 400, 300)
    pygame.draw.rect(screen, (50, 50, 70), game_over_shadow, border_radius=20)
    pygame.draw.rect(screen, (255, 255, 255), game_over_box, border_radius=20)
    pygame.draw.rect(screen, COLORS['incorrect'], game_over_box, width=4, border_radius=20)
    
    # Title
    font = pygame.font.SysFont("Arial", 48, bold=True)
    title = font.render("GAME OVER", True, COLORS['incorrect'])
    title_rect = title.get_rect(center=(400, 190))
    # Shadow
    title_shadow = font.render("GAME OVER", True, (200, 50, 50))
    title_shadow_rect = title_shadow.get_rect(center=(401, 191))
    screen.blit(title_shadow, title_shadow_rect)
    screen.blit(title, title_rect)
    
    # Message
    font = pygame.font.SysFont("Arial", 24, bold=True)
    message = font.render("You made 3 wrong moves!", True, COLORS['subtitle'])
    msg_rect = message.get_rect(center=(400, 240))
    screen.blit(message, msg_rect)
    
    # Time
    font = pygame.font.SysFont("Arial", 20, bold=True)
    time_text = font.render(f"⏱ Time: {time_str}", True, COLORS['user_text'])
    time_rect = time_text.get_rect(center=(400, 280))
    screen.blit(time_text, time_rect)
    
    # Instruction
    font = pygame.font.SysFont("Arial", 18)
    instruction = font.render("Click anywhere to start a new game", True, COLORS['subtitle'])
    inst_rect = instruction.get_rect(center=(400, 320))
    screen.blit(instruction, inst_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    pygame.display.flip()
    
    # Wait for click to close and restart game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                # Any click will restart the game
                waiting = False
                return "restart"  # Signal to restart game
        pygame.time.delay(50)


def show_score_screen(screen, score, correct, wrong, empty, time_str, buttons):
    """Display score screen with statistics"""
    # Draw semi-transparent overlay (only over board area)
    overlay = pygame.Surface((540, 540))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    # Score box with shadow
    score_box = pygame.Rect(200, 150, 400, 350)
    score_shadow = pygame.Rect(203, 153, 400, 350)
    pygame.draw.rect(screen, (50, 50, 70), score_shadow, border_radius=20)
    pygame.draw.rect(screen, (255, 255, 255), score_box, border_radius=20)
    pygame.draw.rect(screen, COLORS['button'], score_box, width=4, border_radius=20)
    
    # Title
    font = pygame.font.SysFont("Arial", 42, bold=True)
    title = font.render("📊 YOUR SCORE", True, COLORS['button'])
    title_rect = title.get_rect(center=(400, 190))
    screen.blit(title, title_rect)
    
    # Score display (big and prominent)
    font = pygame.font.SysFont("Arial", 72, bold=True)
    if score >= 80:
        score_color = COLORS['correct']
    elif score >= 50:
        score_color = (255, 165, 0)
    else:
        score_color = COLORS['incorrect']
    
    score_text = font.render(f"{score}", True, score_color)
    score_rect = score_text.get_rect(center=(400, 250))
    # Shadow
    score_shadow_text = font.render(f"{score}", True, (200, 200, 220))
    score_shadow_rect = score_shadow_text.get_rect(center=(401, 251))
    screen.blit(score_shadow_text, score_shadow_rect)
    screen.blit(score_text, score_rect)
    
    # Out of 100
    font = pygame.font.SysFont("Arial", 24, bold=True)
    out_of = font.render("/ 100", True, COLORS['subtitle'])
    out_of_rect = out_of.get_rect(center=(400, 290))
    screen.blit(out_of, out_of_rect)
    
    # Statistics
    font = pygame.font.SysFont("Arial", 20, bold=True)
    stats_y = 320
    
    # Correct cells
    correct_text = font.render(f"✓ Correct: {correct}", True, COLORS['correct'])
    correct_rect = correct_text.get_rect(center=(400, stats_y))
    screen.blit(correct_text, correct_rect)
    
    # Wrong cells
    wrong_text = font.render(f"❌ Wrong: {wrong}", True, COLORS['incorrect'])
    wrong_rect = wrong_text.get_rect(center=(400, stats_y + 30))
    screen.blit(wrong_text, wrong_rect)
    
    # Empty cells
    empty_text = font.render(f"○ Empty: {empty}", True, COLORS['subtitle'])
    empty_rect = empty_text.get_rect(center=(400, stats_y + 60))
    screen.blit(empty_text, empty_rect)
    
    # Time
    time_text = font.render(f"⏱ Time: {time_str}", True, COLORS['user_text'])
    time_rect = time_text.get_rect(center=(400, stats_y + 90))
    screen.blit(time_text, time_rect)
    
    # Message based on score
    font = pygame.font.SysFont("Arial", 18)
    if score == 100:
        message = "Perfect! 🎉"
        msg_color = COLORS['correct']
    elif score >= 80:
        message = "Great job! Keep going! 💪"
        msg_color = COLORS['correct']
    elif score >= 50:
        message = "Good progress! 👍"
        msg_color = (255, 165, 0)
    else:
        message = "Keep practicing! 💪"
        msg_color = COLORS['incorrect']
    
    msg_text = font.render(message, True, msg_color)
    msg_rect = msg_text.get_rect(center=(400, stats_y + 120))
    screen.blit(msg_text, msg_rect)
    
    # Draw buttons
    for button in buttons:
        button.draw(screen)
    
    pygame.display.flip()
    
    # Wait for click to close and restart game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                # Any click will restart the game
                waiting = False
                return "restart"  # Signal to restart game
        pygame.time.delay(50)


def game_loop(screen, board=None):
    """Main game loop - can be called multiple times for new games"""
    # Initialize or reset variables
    if board is None:
        # Display "Generating Random Grid" text
        screen.fill(COLORS['bg'])
        font = pygame.font.SysFont("Arial", 40, bold=True)
        text = font.render("Generating", True, COLORS['user_text'])
        screen.blit(text, (300, 250))
        
        font = pygame.font.SysFont("Arial", 40, bold=True)
        text = font.render("Random Grid...", True, COLORS['user_text'])
        screen.blit(text, (260, 300))
        pygame.display.flip()
        
        board = Board(screen)
    
    wrong = 0
    wrong_moves = 0  # Track wrong moves for game over (max 3)
    selected = (-1, -1)
    keyDict = {}
    solved = False
    game_over = False
    startTime = time.time()
    finalTime = None  # Store final time when solved
    
    # Create buttons with better spacing (adjusted to avoid overlap with counters)
    change_btn = Button(560, 285, 200, 55, "🔄 New Puzzle", COLORS['button'])
    submit_btn = Button(560, 355, 200, 55, "✓ Submit", (76, 175, 80), (56, 142, 60))
    answer_btn = Button(560, 425, 200, 55, "💡 Show Answer", (255, 152, 0), (245, 124, 0))
    buttons = [change_btn, submit_btn, answer_btn]

    # Main game loop - continue even when game_over to show message
    while not solved:
        # Get elapsed time (only if not solved yet)
        if finalTime is None:
            elapsed = time.time() - startTime
            passedTime = time.strftime("%M:%S", time.gmtime(elapsed))
        else:
            # Use final time when solved (timer paused)
            passedTime = finalTime

        # Check if solved
        if board.check_solution():
            solved = True
            # Store final time (pause timer)
            if finalTime is None:
                elapsed = time.time() - startTime
                finalTime = time.strftime("%M:%S", time.gmtime(elapsed))
                passedTime = finalTime
        
        # Check if game over - just continue showing the board with game over message

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                
                # Check button clicks
                if change_btn.is_clicked(mousePos):
                    # Generate new puzzle - restart everything
                    board.generate_new()
                    wrong = 0
                    wrong_moves = 0
                    game_over = False
                    startTime = time.time()
                    finalTime = None
                    selected = (-1, -1)
                    keyDict = {}
                    solved = False
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    continue
                
                # If game is over, don't allow other interactions except New Puzzle button
                if game_over:
                    continue
                    
                elif submit_btn.is_clicked(mousePos):
                    # Calculate score and show score screen
                    correct_count = 0
                    wrong_count = 0
                    empty_count = 0
                    total_cells = 81
                    
                    for i in range(9):
                        for j in range(9):
                            if board.originalBoard[i][j] != 0:
                                continue  # Skip original cells
                            if board.board[i][j] == 0:
                                empty_count += 1
                            elif board.board[i][j] == board.solvedBoard[i][j]:
                                correct_count += 1
                                board.tiles[i][j].correct = True
                                board.tiles[i][j].incorrect = False
                            else:
                                wrong_count += 1
                                board.tiles[i][j].incorrect = True
                                board.tiles[i][j].correct = False
                    
                    wrong = wrong_count
                    
                    # Calculate score (out of 100)
                    filled_cells = total_cells - empty_count - sum(1 for i in range(9) for j in range(9) if board.originalBoard[i][j] != 0)
                    if filled_cells > 0:
                        score = int((correct_count / filled_cells) * 100)
                    else:
                        score = 0
                    
                    # Redraw board first to show highlights
                    board.redraw(keyDict, wrong, passedTime, buttons, wrong_moves, game_over)
                    # Show score screen
                    result = show_score_screen(screen, score, correct_count, wrong_count, empty_count, passedTime, buttons)
                    
                    # If score screen returns "restart", start new game
                    if result == "restart":
                        board.generate_new()
                        wrong = 0
                        wrong_moves = 0
                        game_over = False
                        startTime = time.time()
                        finalTime = None
                        selected = (-1, -1)
                        keyDict = {}
                        solved = False
                        for i in range(9):
                            for j in range(9):
                                board.tiles[i][j].selected = False
                                board.tiles[i][j].correct = False
                                board.tiles[i][j].incorrect = False
                        continue
                    
                    # Check if completely solved
                    if board.check_solution():
                        solved = True
                    
                elif answer_btn.is_clicked(mousePos):
                    # Fill all answers immediately
                    board.fill_all_answers()
                    # Redraw to show filled board
                    board.redraw(keyDict, wrong, passedTime, buttons, wrong_moves, game_over)
                    solved = True
                    
                else:
                    # Check if a Tile is clicked
                    for i in range(9):
                        for j in range(9):
                            if board.tiles[i][j].clicked(mousePos):
                                selected = (i, j)
                                board.deselect(board.tiles[i][j])
                                
            elif event.type == pygame.KEYDOWN:
                # Don't allow input if game is over
                if game_over:
                    continue
                    
                # Handle key presses
                if selected != (-1, -1):
                    row, col = selected
                    # Only allow editing if the cell was originally empty
                    if board.originalBoard[row][col] == 0:
                        entered_value = None
                        if event.key == pygame.K_1:
                            entered_value = 1
                        elif event.key == pygame.K_2:
                            entered_value = 2
                        elif event.key == pygame.K_3:
                            entered_value = 3
                        elif event.key == pygame.K_4:
                            entered_value = 4
                        elif event.key == pygame.K_5:
                            entered_value = 5
                        elif event.key == pygame.K_6:
                            entered_value = 6
                        elif event.key == pygame.K_7:
                            entered_value = 7
                        elif event.key == pygame.K_8:
                            entered_value = 8
                        elif event.key == pygame.K_9:
                            entered_value = 9
                        
                        # Immediately fill the cell when number is pressed
                        if entered_value is not None:
                            # Check if the entered value is correct
                            is_correct = (entered_value == board.solvedBoard[row][col])
                            
                            # Fill the cell
                            board.tiles[row][col].value = entered_value
                            board.board[row][col] = entered_value
                            
                            # Set correct/incorrect flags
                            if is_correct:
                                board.tiles[row][col].correct = True
                                board.tiles[row][col].incorrect = False
                            else:
                                board.tiles[row][col].correct = False
                                board.tiles[row][col].incorrect = True
                                # Increment wrong moves counter
                                wrong_moves += 1
                                
                                # Check if game over (3 wrong moves)
                                if wrong_moves >= 3:
                                    game_over = True
                                    # Store final time
                                    if finalTime is None:
                                        elapsed = time.time() - startTime
                                        finalTime = time.strftime("%M:%S", time.gmtime(elapsed))
                            
                            # Remove from keyDict if present
                            if selected in keyDict:
                                del keyDict[selected]
                                
                        elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            # Clear the cell
                            board.tiles[row][col].value = 0
                            board.board[row][col] = 0
                            board.tiles[row][col].correct = False
                            board.tiles[row][col].incorrect = False
                            if selected in keyDict:
                                del keyDict[selected]

                # Handle hint key
                if event.key == pygame.K_h:
                    board.hint(keyDict)

        board.redraw(keyDict, wrong, passedTime, buttons, wrong_moves, game_over)
        
    # Keep window open after solving or game over - just pause, no victory screen
    while True:
        # Just redraw the board normally with paused timer
        board.redraw(keyDict, wrong, passedTime, buttons, wrong_moves, game_over)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()
                if change_btn.is_clicked(mousePos):
                    # Generate new puzzle and restart
                    board.generate_new()
                    wrong = 0
                    wrong_moves = 0
                    game_over = False
                    startTime = time.time()
                    finalTime = None
                    selected = (-1, -1)
                    keyDict = {}
                    solved = False
                    for i in range(9):
                        for j in range(9):
                            board.tiles[i][j].selected = False
                            board.tiles[i][j].correct = False
                            board.tiles[i][j].incorrect = False
                    return True  # Signal to restart
        pygame.time.delay(100)


def main():
    # Set up the pygame window - bigger to accommodate buttons
    screen = pygame.display.set_mode((800, 600))
    screen.fill(COLORS['bg'])
    pygame.display.set_caption("Modern Sudoku Solver")
    try:
        icon = pygame.image.load("assets/thumbnail.png")
        pygame.display.set_icon(icon)
    except:
        pass
    
    # Main loop - restart game when needed
    board = None
    while True:
        restart = game_loop(screen, board)
        if not restart:
            break
        # Keep the same board instance for new puzzle
        if board is None:
            board = Board(screen)
        else:
            board.generate_new()


main()
pygame.quit()
