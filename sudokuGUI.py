import pygame
import sys
import random
import copy
from solver import is_valid, find_empty_cell, solve_sudoku, generate_sudoku
import optionsWindow

# Moved pygame initialization to start_game() so pygame doesn't open automatically
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTGRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (34,139,34)
LIGHTRED = (255, 182, 193)
LIGHTBLUE = (173, 216, 230)

# Screen dimensions
SCREEN_WIDTH = 594  # Changed from 600: (594 // (600 // 9) = 9), avoids drawing lines where it shouldn't be drawn
SCREEN_HEIGHT = 650
GRID_HEIGHT = 594  # Changed from 600: (594 // (600 // 9) = 9), avoids drawing lines where it shouldn't be drawn

def draw_grid(screen, puzzle, playable_field, solved_puzzle):
    # Draw minor lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 9):  # Vertical lines
        pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, GRID_HEIGHT))
    for y in range(0, GRID_HEIGHT, GRID_HEIGHT // 9):  # Horizontal lines
        pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREEN_WIDTH, y))

    # Draw major lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 3):  # Vertical lines
        pygame.draw.line(screen, BLACK, (x-1, 0), (x-1, GRID_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_HEIGHT // 3):  # Horizontal lines
        pygame.draw.line(screen, BLACK, (0, y-1), (SCREEN_WIDTH, y-1))

    # Highlight the selected cell with a light blue background
    if selected_cell:
        x, y = selected_cell[1] * (SCREEN_WIDTH // 9), selected_cell[0] * (GRID_HEIGHT // 9)
        pygame.draw.rect(screen, LIGHTBLUE, (x+1, y, SCREEN_WIDTH // 9, GRID_HEIGHT // 9))

    # Draw the numbers from the sudoku_puzzle
    font = pygame.font.Font(None, 36)
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] > 0:
                if playable_field[i][j]:  # Differentiating between user input and computer-generated puzzle
                    if puzzle[i][j] == solved_puzzle[i][j]:
                        text = font.render(str(puzzle[i][j]), True, GREEN)
                    else:
                        text = font.render(str(puzzle[i][j]), True, RED)
                else:
                    text = font.render(str(puzzle[i][j]), True, BLACK)
                screen.blit(text, (j * (SCREEN_WIDTH // 9) + 15, i * (GRID_HEIGHT // 9) + 15))


def draw_grid_lines_only(screen):  # function only to draw gridlines so that a selected box doesn't overlap the grid lines
    # Draw minor lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 9):  # Vertical lines
        pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, GRID_HEIGHT))
    for y in range(0, GRID_HEIGHT, GRID_HEIGHT // 9):  # Horizontal lines
        pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREEN_WIDTH, y))

    # Draw major lines
    for x in range(0, SCREEN_WIDTH, SCREEN_WIDTH // 3):  # Vertical lines
        pygame.draw.line(screen, BLACK, (x - 1, 0), (x - 1, GRID_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_HEIGHT // 3):  # Horizontal lines
        pygame.draw.line(screen, BLACK, (0, y - 1), (SCREEN_WIDTH, y - 1))


def get_clicked_pos(pos, playable_field):
    x, y = pos
    if y < GRID_HEIGHT:
        row = y // (GRID_HEIGHT // 9)
        col = x // (SCREEN_WIDTH // 9)
        print(f"Calculated cell: (row={row}, col={col})")   #debugging print statement
        if playable_field[row][col]:
            return row, col
        else:
            print("You cannot select this cell.")  #debugging print statement
            return None


selected_cell = None

def get_playable_field(board):
    playable_field = [[True if board[i][j] == 0 else False for j in range(9)] for i in range(9)]
    return playable_field


def provide_hint(screen, sudoku_puzzle, playable_field, solved_puzzle):
    cells = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(cells)
    
    for row, col in cells:
        if playable_field[row][col] and sudoku_puzzle[row][col] == 0:
            for num in range(1, 10):
                if num == solved_puzzle[row][col]:
                    x, y = col * (SCREEN_WIDTH // 9), row * (GRID_HEIGHT // 9)
                    pygame.draw.rect(screen, LIGHTBLUE, (x+1, y, SCREEN_WIDTH // 9, GRID_HEIGHT // 9))
                    pygame.display.flip()
                    pygame.time.delay(500)  # Show hint for 0.5 seconds
                    return row, col, num  # Return the hint number

    return None, None, None  # No valid hint found


def game_over_popup(screen):
    DEFAULT_BUTTON_COLOR = (150,150,147)
    HOVER_BUTTON_COLOR = (217,217,214)
    pygame.display.flip()  # Update screen
    pygame.time.delay(1000)
    large_font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 30)
    screen.fill(LIGHTRED)
    basic_lose_text = large_font.render("Game Over!", True, BLACK)
    lose_description = small_font.render("You entered too many mistakes.", True, BLACK)
    screen.blit(basic_lose_text, (175, 295))
    pygame.display.flip()  # Update screen
    pygame.time.delay(2000)
    screen.blit(lose_description, (135, 355))
    pygame.display.flip()  # Update screen
    pygame.time.delay(1000)
    menu_button = pygame.Rect(222, 590, 150, 50)
    while True:
        color = DEFAULT_BUTTON_COLOR
        if menu_button.collidepoint(pygame.mouse.get_pos()):
            color = HOVER_BUTTON_COLOR
        pygame.draw.rect(screen, color, menu_button)
        menu_text = small_font.render("Main Menu", True, BLACK)
        text_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click anywhere to return to the main menu (placeholder for now)
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    optionsWindow.OptionsWindow()
        pygame.display.flip()

def win_popup(screen):
    DEFAULT_BUTTON_COLOR = (150, 150, 147)
    HOVER_BUTTON_COLOR = (217, 217, 214)
    pygame.display.flip()  # Update screen
    pygame.time.delay(1000)
    large_font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 30)
    screen.fill(WHITE)
    basic_win_text = large_font.render("You win!", True, BLACK)
    screen.blit(basic_win_text, (210, 295))
    pygame.display.flip()  # Update screen
    pygame.time.delay(1000)
    menu_button = pygame.Rect(222, 590, 150, 50)
    while True:
        color = DEFAULT_BUTTON_COLOR
        if menu_button.collidepoint(pygame.mouse.get_pos()):
            color = HOVER_BUTTON_COLOR
        pygame.draw.rect(screen, color, menu_button)
        menu_text = small_font.render("Main Menu", True, BLACK)
        text_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, text_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click anywhere to return to the main menu (placeholder for now)
                if menu_button.collidepoint(pygame.mouse.get_pos()):
                    optionsWindow.OptionsWindow()
        pygame.display.flip()


def start_game(difficulty):
    # Initialize pygame
    ico = pygame.image.load("sudokuIcon.ico")
    pygame.display.set_icon(ico)
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sudoku')

    # Generate a random Sudoku puzzle for the player
    sudoku_puzzle = generate_sudoku(difficulty)
    playable_field = get_playable_field(sudoku_puzzle)
    solved_puzzle = copy.deepcopy(sudoku_puzzle)
    solve_sudoku(solved_puzzle)

    global selected_cell
    print("Starting game loop...")

    if difficulty == "Easy":
        mistakes_remaining = 6
    elif difficulty == "Medium":
        mistakes_remaining = 4
    elif difficulty == "Hard":
        mistakes_remaining = 2
    else:
        mistakes_remaining = 1

    hint_button = pygame.Rect(225, 600, 150, 40)
    hints = 5  # Number of available hints

    last_input_was_mistake = False  # Variable for checking if the last input was a mistake
    while True:
        screen.fill(WHITE)  # Fill the screen with a white background to start off
        draw_grid(screen, sudoku_puzzle, playable_field, solved_puzzle)  #  Drawing the sudoku grid on top of the white background
        # pygame.draw.rect(screen, RED, (50, 50, 100, 100)) # what is this red box for? - howard

        # Draw Hint button
        pygame.draw.rect(screen, LIGHTGRAY, hint_button)
        font = pygame.font.Font(None, 28)
        hint_text = font.render(f"Hints: {hints}", True, BLACK)
        screen.blit(hint_text, (240, 610))
        if last_input_was_mistake:
            last_mistake_text = font.render("Incorrect input!", True, RED)
            screen.blit(last_mistake_text, (440, 610))
        if mistakes_remaining <= 1:
            mistakes_text = font.render(f"Allowed Mistakes: {mistakes_remaining}", True, RED)
        else:
            mistakes_text = font.render(f"Allowed Mistakes: {mistakes_remaining}", True, BLACK)
        screen.blit(mistakes_text, (10, 610))

        if sudoku_puzzle == solved_puzzle:
            pygame.display.flip()  # Update the screen
            win_popup(screen)

        if mistakes_remaining <= 0:
            pygame.display.flip()  # Update the screen so the user can see that they have no mistakes left
            game_over_popup(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Click
                pos = pygame.mouse.get_pos()
                print(f"Mouse clicked at position: {pos}")  #debugging print statement
                selected_cell = get_clicked_pos(pos, playable_field)    #debugging print statement
                print(f"Selected cell: {selected_cell}")
                # Check if hint button is clicked
                if hint_button.collidepoint(event.pos):
                    if hints > 0:
                        # Perform hint logic here
                        hint_row, hint_col, hint_num = provide_hint(screen, sudoku_puzzle, playable_field, solved_puzzle)
                        if hint_row is not None and hint_col is not None and hint_num is not None:
                            if hint_num != 0:
                                # Draw the hint number (blinking with lower opacity)
                                font = pygame.font.Font(None, 36)
                                hint_text = font.render(str(hint_num), True, (0, 0, 0))
                                for i in range(6):  # Blink hint for 3 seconds (6 frames at 500ms delay)
                                    if i % 2 == 0:
                                        screen.blit(hint_text, (hint_col * (SCREEN_WIDTH // 9) + 15, hint_row * (GRID_HEIGHT // 9) + 15))
                                    else:
                                        screen.fill(WHITE, (hint_col * (SCREEN_WIDTH // 9) + 1, hint_row * (GRID_HEIGHT // 9) + 1, SCREEN_WIDTH // 9, GRID_HEIGHT // 9))
                                    draw_grid_lines_only(screen)  # Make sure the flashing doesn't overlap with the grid
                                    pygame.display.flip()
                                    pygame.time.delay(500)
                                hints -= 1
                                print("Hint provided!")

            if event.type == pygame.KEYDOWN:  # Number key or backspace is pressed
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7,
                                 pygame.K_8, pygame.K_9, pygame.K_BACKSPACE]:
                    if selected_cell:
                        row, col = selected_cell
                        if event.key != pygame.K_BACKSPACE:
                            num = event.key - pygame.K_0
                            if num == sudoku_puzzle[row][col]:  # Ignore if user enters the same number in the same tile
                                pass
                            elif num == solved_puzzle[row][col]:  # Assuming sudoku_puzzle is your board
                                sudoku_puzzle[row][col] = num
                                last_input_was_mistake = False
                            else:
                                mistakes_remaining -= 1
                                sudoku_puzzle[row][col] = num
                                last_input_was_mistake = True
                                pass
                        else:  # Backspace
                            sudoku_puzzle[row][col] = 0
                            last_input_was_mistake = False
                            pass
        draw_grid_lines_only(screen)
        pygame.display.flip()  # Displays board after taking all events into consideration
