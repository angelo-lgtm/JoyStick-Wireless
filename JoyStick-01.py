import pygame
import serial
import serial.tools.list_ports

pygame.init()

win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick Game")

character_size = 50
character_color = (0, 255, 0)
character_x, character_y = win_width // 2, win_height // 2

arduino_port = 'COM10'
try:
    ser = serial.Serial(arduino_port, 9600, timeout=1)
except serial.SerialException as e:
    print(f"Could not open {arduino_port}: {e}")
    exit()

dead_zone = 30 

def map_range(val, in_min, in_max, out_min, out_max):
    return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode(errors='ignore').strip()
        if line:
            data = line.split(',')
            if len(data) == 3:
                try:
                    joy_x, joy_y, button_state = map(int, data)
                except ValueError:
                    print(f"Skipping invalid line: {line}")
                    continue

                print(f"X: {joy_x}, Y: {joy_y}, Button: {button_state}")

                if abs(joy_x - 512) < dead_zone:
                    joy_x = 512
                if abs(joy_y - 512) < dead_zone:
                    joy_y = 512

                new_x = map_range(joy_x, 0, 1023, character_size // 2, win_width - character_size // 2)
                new_y = map_range(joy_y, 0, 1023, character_size // 2, win_height - character_size // 2)

                character_x, character_y = new_x, new_y

                character_color = (0, 0, 255) if button_state == 1 else (255, 0, 0)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break

    win.fill((255, 255, 255))
    pygame.draw.circle(win, character_color, (character_x, character_y), character_size // 2)
    pygame.display.flip()

ser.close()
pygame.quit()
