import pygame
import serial

pygame.init()

win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Gravity Sensor Game")

clock = pygame.time.Clock
FPS = 60

character_size = 50
character_color = (0, 255, 0)
character_x = win_width // 2
character_y = win_height //2

arduino_port = 'COM3'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def map_range(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode('utf-8').strip()
        if line:
            data = line.split(',')
            if len(data) == 3:
                acc_x, acc_y, acc_z = map(float, data)
                
                new_x = map_range(acc_x, -1, 1, character_size//2, win_width - character_size//2)
                new_y = map_range(acc_y, -1, 1, character_size//2, win_height - character_size//2)

                if abs(acc_x)>0.05:
                    character_x = new_x
                if abs(acc_y)>0.05:
                    character_y = new_y

    except:
        pass

    win.fill((0, 0, 0))
    pygame.draw.circle(win, character_color, (character_x, character_y), character_size//2)
    pygame.display.flip()

pygame.quit()
ser.close()