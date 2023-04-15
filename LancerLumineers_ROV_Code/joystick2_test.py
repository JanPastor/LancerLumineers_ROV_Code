# DaFluffly Potato Controller Pygame Code Tutorial

import sys
import pygame

from pygame.locals import * 
pygame.init()
pygame.display.set_caption('game base')
screen = pygame.display.set_mode((500,500),0,32)
clock = pygame.time.Clock()

pygame.joystick.init() # Initializes joystick module to use joystick/controller
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
# Line 13 initializes the joysticks and gets a list comprehension of available joysticks connected to the computer
for joystick in joysticks:
    print(joystick.get_name()) # Prints the name of the button or joystick being used


my_square = pygame.Rect(50,50,50,50)
my_square.clamp_ip(screen.get_rect())
my_square_color = 0
colors = [(255, 0, 255), (0,128,128), (255,20,147)]
motion = [0,0]

while True:
    screen.fill((0,0,0))
    pygame.draw.rect(screen, colors[my_square_color], my_square)
    if abs(motion[0]) < 0.1:  # Defining a deadzone for the horizontal axis
        motion[0] = 0
    if abs(motion[1]) < 0.1:  # Defining a deadzone for the vertical axis
        motion[1] = 0
    my_square.x += motion[0] * 10
    my_square.y += motion[1] * 10 

    for event in pygame.event.get():
        if event.type == JOYBUTTONDOWN:
            print(event)
            if event.button == 0:
                my_square_color = (my_square_color + 1) % len(colors)
        if event.type == JOYBUTTONUP:
            print(event)
        if event.type == JOYAXISMOTION:
            print(event)
            if event.axis < 2:
                motion[event.axis] = event.value
        if event.type == JOYHATMOTION:
            print(event)
        # Line 48-51 checks for any additional joysticks plugged in after Pygame has been initialized. Reinitializes joysticks to add new controller.
        if event.type == JOYDEVICEADDED:
            joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            for joystick in joysticks:
                print(joystick.get_name())
        if event.type == JOYDEVICEREMOVED:
            joysticks == [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    pygame.display.update()
    clock.tick(60)


