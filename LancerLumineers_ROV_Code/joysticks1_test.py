import sys
import pygame # From NeuralNine tutorial video

pygame.joystick.init() # Initializes the joystick detection
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

class Player(object):

    def __init__(self):
        self.player = pygame.Rect((300,400,50,50))
        self.color = "white"

    def move(self, x_speed, y_speed):
        self.player.move_ip((x_speed, y_speed))

    def change_color(self,color):
        self.color = color
    
    def draw(self, game_screen):
        pygame.draw.rect(game_screen, self.color, self.player)

pygame.init()

player = Player()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.JOYBUTTONDOWN:
            print(event) # Outputs the type of buttons or joystick being used when program runs
            if pygame.joystick.Joystick(0).get_button(0):
                player.change_color("Blue")
            elif pygame.joystick.Joystick(0).get_button(1):
                player.change_color("Red")
            elif pygame.joystick.Joystick(0).get_button(2):
                player.change_color("Yellow")
            elif pygame.joystick.Joystick(0).get_button(3):
                player.change_color("Green")
                print(event)
            elif pygame.joystick.Joystick(0).get_button(8):
                player.change_color('White') # changes the color of the game object to white when pressing button 8

        if event.type == pygame.JOYAXISMOTION:
            print(event)
        
        
# If code block above changes the color of the object when certain buttons on the controller are pressed.

x_speed = round(pygame.joystick.Joystick(0).get_axis(0))
y_speed = round(pygame.joystick.Joystick(0).get_axis(4))
player.move(x_speed, y_speed)


screen.fill((0,0,0))
player.draw(screen)
pygame.display.update()

clock.tick(180)

