import pygame
import serial

pygame.init()

win_width, win_height = 1000,800
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("FOOTBALL GAME")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
GREEN = (0, 153, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

player_size = 40
player_speed = 15

player1_x, player1_y = 100, win_height //2
player2_x, player2_y = win_width - 160, win_height //2

ball_size = 20
ball_x, ball_y = win_width // 2, win_height //2
ball_speed_x, ball_speed_y = 4, 4

arduino_port = "COM4"
try: 
    ser = serial.Serial(arduino_port, 9600, timeout=1)
except serial.SerialException as e:
    print(f"Could not open {arduino_port}: {e}")
    exit()

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline(). decode(errors='ignore').strip()
        if line:
            data = line.split(',')
            if len(data) == 3:
                try: 
                    joy_x, joy_y, button_state = map(int, data)
                except ValueError: 
                    continue

                player1_x +=(joy_x - 512) // 100 * player_speed
                player1_y +=(joy_y - 512) // 100 * player_speed

                player1_x = max(0, min(win_width//2 - player_size, player1_x))
                player1_y = max(0, min(win_width//2 - player_size, player1_y))

    except serial.SerialException:
        pass 

        # --- Player 2 controls (arrow keys) ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player2_y > 0:
        player2_y -= player_speed
    if keys[pygame.K_DOWN] and player2_y < win_height - player_size:
        player2_y += player_speed
    if keys[pygame.K_LEFT] and player2_x > win_width//2:
        player2_x -= player_speed
    if keys[pygame.K_RIGHT] and player2_x < win_width - player_size:
        player2_x += player_speed

    # --- Ball movement ---
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Bounce ball on top/bottom
    if ball_y <= 0 or ball_y >= win_height - ball_size:
        ball_speed_y *= -1

    # Bounce ball on players
    if (player1_x < ball_x < player1_x + player_size and
        player1_y < ball_y < player1_y + player_size):
        ball_speed_x *= -1
    if (player2_x < ball_x < player2_x + player_size and
        player2_y < ball_y < player2_y + player_size):
        ball_speed_x *= -1

    # Bounce ball on left/right (simple goal detection)
    if ball_x <= 0 or ball_x >= win_width - ball_size:
        ball_x, ball_y = win_width//2, win_height//2  # Reset ball

    # --- Drawing ---
    win.fill(GREEN)  # Field background
    pygame.draw.rect(win, BLUE, (player1_x, player1_y, player_size, player_size))
    pygame.draw.rect(win, RED, (player2_x, player2_y, player_size, player_size))
    pygame.draw.circle(win, WHITE, (ball_x + ball_size//2, ball_y + ball_size//2), ball_size//2)

    pygame.display.flip()

ser.close()
pygame.quit()