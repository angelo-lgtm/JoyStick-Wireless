import pygame
from os.path import join
from random import randint

pygame.init()

#display of the windows informations specifically the width and height
# info = pygame.display.Info()
# print(info.current_w, info.current_h) 

win_width, win_height = 1350, 700
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("WINGS OF WAR")

playing = True

#surface
surf = pygame.Surface((100, 200))
surf.fill('lightblue')
x = 100
y = 200

#importing an image
img = pygame.image.load(join('Images', 'de3471dd-c3b1-4467-8320-67e8a96d0737-removebg-preview.png')).convert_alpha()
img_rect = img.get_frect(center = (0,0))
img = pygame.transform.scale(img,(150,200)) #this is to change the size
img2 = pygame.image.load(join('Images', 'star.png')).convert_alpha()
img2 = pygame.transform.scale(img2,(80,135))
star_position = [(randint(0, win_width), randint(0, win_height)) for i in range(20)]

while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

    win.fill('darkgray')
    #this make the motion of the rectangle sruface that we have created
    win.blit(img, (x, y))
    for i in star_position:
        win.blit(img2, i)
    pygame.display.update()

pygame.quit()