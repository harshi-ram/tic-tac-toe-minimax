import pygame
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 450  # Increased for better layout
LINE_WIDTH = 6
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (40, 40, 60)
LINE_COLOR = (200, 200, 200)
CIRCLE_COLOR = (100, 200, 255)
CROSS_COLOR = (255, 100, 100)
TEXT_COLOR = (255, 255, 255)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
font = pygame.font.SysFont("arial", 24, bold=True)

# Board
board = np.zeros((BOARD_ROWS, BOARD_COLS))
player_wins = 0
ai_wins = 0

def draw_lines():
    screen.fill(BG_COLOR)
    # Horizontal
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, SQUARE_SIZE * 3), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            elif board[row][col] == -1:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def draw_scoreboard():
    pygame.draw.rect(screen, (30, 30, 45), (0, HEIGHT - 60, WIDTH, 60))
    score_text = f"Player Wins: {player_wins}    AI Wins: {ai_wins}"
    info_text = "Press R to Restart"
    score_surface = font.render(score_text, True, TEXT_COLOR)
    info_surface = font.render(info_text, True, TEXT_COLOR)
    screen.blit(score_surface, (20, HEIGHT - 55))
    screen.blit(info_surface, (20, HEIGHT - 30))

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return not (board == 0).any()

def check_winner(player):
    for i in range(BOARD_ROWS):
        if np.all(board[i, :] == player): return True
        if np.all(board[:, i] == player): return True
    if np.all(np.diag(board) == player): return True
    if np.all(np.diag(np.fliplr(board)) == player): return True
    return False

def minimax(board, depth, is_maximizing):
    if check_winner(-1): return 1
    if check_winner(1): return -1
    if is_board_full(): return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = -1
                    score = minimax(board, depth + 1, False)
                    board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == 0:
                    board[row][col] = 1
                    score = minimax(board, depth + 1, True)
                    board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -float('inf')
    move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                board[row][col] = -1
                score = minimax(board, 0, False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move:
        mark_square(move[0], move[1], -1)

def restart():
    global board
    board = np.zeros((BOARD_ROWS, BOARD_COLS))
    screen.fill(BG_COLOR)
    draw_lines()

# Start the game
draw_lines()
game_over = False
player = 1  # human is 1, AI is -1

while True:
    draw_figures()
    draw_scoreboard()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            if mouseY < SQUARE_SIZE * 3:
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE

                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    if check_winner(player):
                        player_wins += 1
                        game_over = True
                    elif is_board_full():
                        game_over = True
                    else:
                        best_move()
                        if check_winner(-1):
                            ai_wins += 1
                            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False
