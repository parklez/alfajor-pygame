import sys
import pygame
import colors
import random


pygame.init()
clock = pygame.time.Clock()

window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
font = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 40)


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

    def __init__(self, pos=[400, -40], speed=4):
        self.pos = pos
        self.alive = True
        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], Alfajor.size[0], Alfajor.size[1])
        self.image = Alfajor.image
        self.speed = speed

    def resize(self, size):
        'Resizes the image and the hitbox'
        Alfajor.image = pygame.transform.smoothscale(Alfajor.image, size)
        Alfajor.size = Alfajor.image.get_size()
        self.update()

    def update(self):
        'attempts to keep the hitbox updated'
        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1])

    def move(self):
        self.pos[1] += self.speed
        self.update()


class Player:
    def __init__(self, pos=[0, 0]):
        self.path_to_sprite = "sprites/SurpriseRacc.png"
        self.image = pygame.image.load(self.path_to_sprite)
        self.size = self.image.get_size()
        self.pos = pos
        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1])
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
        self.rect = pygame.Rect(
            self.pos[0], self.pos[1], self.size[0], self.size[1])

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

    def __init__(self, screen):
        self.screen = screen
        self.player = Player(pos=[400-32, 600-57])
        self.snacks = []
        self.level = 0
        self.score = 0
        self.state = 'welcome'

    def reset_score(self):
        self.score = 0
        self.player = Player(pos=[400-32, 600-57])
        self.level = 0
        self.snacks = []

    @staticmethod
    def random_pos():
        # TODO: Make it left or right X amount but never away from screen
        return [random.randint(40, 560), -40]

    def get_speed(self):
        if not self.score:
            return 4
        return 4+self.score if self.score < 8 else 12

    def draw_background(self):
        self.screen.fill(colors.blue)
        grid(self.screen, 40, colors.icy)

    def draw_objects_and_player(self):
        self.screen.blit(self.player.image, self.player.pos)
        for item in self.snacks:
            self.screen.blit(item.image, item.rect)

    def draw_welcome_instructions(self):
        welcome_text = font.render('Raccoon Alfajor', True, colors.white)
        welcome_text_s = font.render('Raccoon Alfajor', True, colors.brown)

        help_text = font_small.render('Instructions:', True, colors.white)
        help_text_s = font_small.render('Instructions:', True, colors.brown)

        keys_text = font_small.render(
            'Move: A W S D - Run: Shift', True, colors.white)
        keys_text_s = font_small.render(
            'Move: A W S D - Run: Shift', True, colors.brown)

        start_text = font_small.render('Press [Space] to start!', True, colors.white)
        start_text_s = font_small.render('Press [Space] to start!', True, colors.brown)

        self.screen.blit(welcome_text_s, [100+4, 100+4])
        self.screen.blit(welcome_text, [100, 100])

        self.screen.blit(help_text_s, [50+3, 250+3])
        self.screen.blit(help_text, [50, 250])

        self.screen.blit(keys_text_s, [50+3, 300+3])
        self.screen.blit(keys_text, [50, 300])

        self.screen.blit(start_text_s, [200+4, 500+4])
        self.screen.blit(start_text, [200, 500])

    def draw_game_over_score(self):
        gameover_text = font.render('Game Over!', True, colors.white)
        gameover_text_s = font.render('Game Over!', True, colors.brown)

        score_text = font.render(f'Your score: {self.score}', True, colors.white)
        score_text_s = font.render(f'Your score: {self.score}', True, colors.brown)

        restart_text = font_small.render('Press [Space] to restart!', True, colors.white)
        restart_text_s = font_small.render('Press [Space] to restart!', True, colors.brown)

        self.screen.blit(gameover_text_s, [100+4, 100+4])
        self.screen.blit(gameover_text, [100, 100])
        self.screen.blit(score_text_s, [100+4, 300+4])
        self.screen.blit(score_text, [100, 300])
        self.screen.blit(restart_text_s, [100+4, 400+4])
        self.screen.blit(restart_text, [100, 400])

    def game_welcome(self):
        self.draw_background()
        self.draw_welcome_instructions()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = 'gameplay'

    def game_controller(self):
        if self.state == 'welcome':
            self.game_welcome()
        elif self.state == 'gameplay':
            self.game_play()
        else:
            self.game_over()

    def game_play(self):
        key = pygame.key.get_pressed()

        # Input
        if key[pygame.K_a]:
            self.player.move('Left')
        if key[pygame.K_d]:
            self.player.move('Right')
        if key[pygame.K_LSHIFT]:
            self.player.running = True
        else:
            self.player.running = False

        # logic
        if not self.snacks:
            self.snacks.append(
                Alfajor(self.random_pos(), self.get_speed()))
        for item in self.snacks:
            item.move()
            if self.player.rect.colliderect(item.rect):
                self.snacks.remove(item)
                self.score += 1
            if item.pos[1] > 600:
                self.state = 'game over'

        # Drawing
        self.draw_background()
        self.draw_objects_and_player()

    def game_over(self):
        self.draw_background()
        self.draw_objects_and_player()
        self.draw_game_over_score()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.state = 'gameplay'
            self.reset_score()

GameInstance = Game(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    GameInstance.game_controller()

    pygame.display.flip()
    clock.tick(60)
