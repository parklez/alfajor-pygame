import sys
import pygame
import colors
import random


pygame.init()
clock = pygame.time.Clock()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)


def grid(surface, size, color=(255, 0, 0)):
    'Draws a line every "size" pixels'
    screen_size = surface.get_size()
    
    x_lines = int(window_size[0]/size)
    y_lines = int(window_size[1]/size)

    y0 = size
    for line in range(0, y_lines):
        pygame.draw.line(surface, color, (0, y0), (screen_size[0], y0))
        y0 += size

    x0 = size
    for line in range(0, x_lines):
        pygame.draw.line(surface, color, (x0, 0), (x0, screen_size[1]))
        x0 += size

class Alfajor:

    path_to_sprite = "sprites/alfajor.png"
    image = pygame.image.load(path_to_sprite)
    image = pygame.transform.smoothscale(image, (40, 40))
    size = image.get_size()
    
    def __init__(self, pos=[400,0]):
        self.pos = pos
        self.alive = True
        self.rect = pygame.Rect(self.pos[0], self.pos[1], Alfajor.size[0], Alfajor.size[1])
        self.image = Alfajor.image
        self.speed = 4
        
    def resize(self, size):
        'Resizes the image and the hitbox'
        Alfajor.image = pygame.transform.smoothscale(Alfajor.image, size)
        Alfajor.size = Alfajor.image.get_size()
        self.update()
        
    def update(self):
        'attempts to keep the hitbox updated'
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def move(self):
        self.pos[1] += self.speed
        self.update()
        
class Player:
    def __init__(self):
        self.path_to_sprite = "sprites/SurpriseRacc.png"
        self.image = pygame.image.load(self.path_to_sprite)
        self.size = self.image.get_size()
        self.pos = [0, 0]
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.resize((64, 57))
        self.speed = 8
        self.fasterspeed = 16
        self.running = False

    def resize(self, size):
        'Resizes the image and the hitbox'
        self.image = pygame.transform.smoothscale(self.image, size)
        self.size = self.image.get_size()
        self.update()
        
    def update(self):
        'attempts to keep the hitbox updated'
        self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        
    def move(self, direction):
        'Moves the image to some direction X pixels and updates the hitbox'
        
        if self.running == False:
            speed = self.speed
        else:
            speed = self.fasterspeed
        
        if direction == 'Left':
            if self.pos[0] > 0:
                self.pos[0] -= speed
            
        elif direction == 'Right':
            if self.pos[0] + self.size[0] < 800:
                self.pos[0] += speed
        
        elif direction == 'Up':
            self.pos[1] -= speed
            
        elif direction == 'Down':
            self.pos[1] += speed
            
        self.update()
            
class Game:
    def __init__(self, quantity = 10, speed = 4):
        self.quantity = quantity
        self.speed = speed
        self.alfajores = list()
        
    def spawn(self, pos):
        self.alfajores(Alfajor(pos))
        
    
racc = Player()
racc.pos[1] = 600 - racc.size[1]
racc.update()

snacc = Alfajor()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    key = pygame.key.get_pressed()
        
    if key[pygame.K_a]:
        racc.move('Left')
        
    if key[pygame.K_d]:
        racc.move('Right')
        
    if key[pygame.K_LSHIFT]:
        racc.running = True
        
    else:
        racc.running = False
        
        
    ### GAME LOGIC 
    if snacc.alive:
        snacc.move()
        
        if racc.rect.colliderect(snacc.rect):
            snacc.alive = False
    
    
    ### BACKGROUND
    screen.fill(colors.grey3)
    grid(screen, 40, colors.grey2)
    
    ### CHARACTERS
    #pygame.draw.rect(screen, colors.yellow, racc.rect)
    screen.blit(racc.image, racc.pos)
    
    ## OBJECTS
    if snacc.alive:
        #pygame.draw.rect(screen, colors.yellow, snacc.rect)
        screen.blit(snacc.image, snacc.rect)
    
    pygame.display.flip()
    clock.tick(60)
    
