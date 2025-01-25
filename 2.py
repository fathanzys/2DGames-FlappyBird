import pygame
import random
import time
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150

# Audio Files
WING_SOUND = 'assets/audio/wing.wav'
HIT_SOUND = 'assets/audio/hit.wav'

pygame.mixer.init()

# Bird Class
class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_images):
        super().__init__()
        self.images = bird_images
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH // 6
        self.rect[1] = SCREEN_HEIGHT // 2
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

# OpenGL-based Pipe Class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        super().__init__()
        self.xpos = xpos
        self.ysize = ysize
        self.inverted = inverted
        self.width = PIPE_WIDTH
        self.height = ysize if not inverted else PIPE_HEIGHT - ysize

        # Gambar pipa
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))  # Warna hijau

        # Atur posisi pipa berdasarkan orientasi
        if inverted:
            self.rect = self.image.get_rect(topleft=(xpos, 0))  # Pipa terbalik menempel di atas
        else:
            self.rect = self.image.get_rect(topleft=(xpos, SCREEN_HEIGHT - self.height))  # Pipa normal menempel di bawah

        self.scored = False  # Menandai apakah skor sudah dihitung

    def update(self):
        # Pindahkan pipa ke kiri
        self.rect.x -= GAME_SPEED

    def is_off_screen(self):
        # Cek apakah pipa keluar dari layar
        return self.rect.right < 0
    
# Ground Class
class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        super().__init__()
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

# Helper Functions
def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]

def get_random_pipes(xpos):
    # Tentukan ukuran pipa secara acak
    size = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 200)
    pipe = Pipe(False, xpos, size)  # Pipa normal (di bawah)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)  # Pipa terbalik (di atas)
    return pipe, pipe_inverted

# Game Initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load Assets
BACKGROUND = pygame.image.load('assets/sprites/background-day.png').convert()
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

# Load Bird Character Images
CHARACTER_IMAGES = {
    "blue": [
        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
    ],
    "red": [
        pygame.image.load('assets/sprites/redbird-upflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/redbird-midflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/redbird-downflap.png').convert_alpha()
    ],
    "yellow": [
        pygame.image.load('assets/sprites/yellowbird-upflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/yellowbird-midflap.png').convert_alpha(),
        pygame.image.load('assets/sprites/yellowbird-downflap.png').convert_alpha()
    ]
}
#CHARACTER_IMAGES["blue"] = [
#    pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha(), (50, 50)),
#   pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(), (50, 50)),
#    pygame.transform.scale(pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(), (50, 50))
#]

# Character Selection Screen
def select_character():
    font = pygame.font.Font(None, 36)
    select_text = font.render('Select Your Character:', True, (255, 255, 255))
    characters = list(CHARACTER_IMAGES.keys())
    selected_index = 0

    while True:
        screen.blit(BACKGROUND, (0, 0))
        screen.blit(select_text, (50, 100))

        for i, character in enumerate(characters):
            color = (255, 255, 0) if i == selected_index else (255, 255, 255)
            character_image = CHARACTER_IMAGES[character][0]
            character_rect = character_image.get_rect(center=(100 + i * 100, 300))
            pygame.draw.rect(screen, color, character_rect.inflate(10, 10), 2)
            screen.blit(character_image, character_rect.topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    selected_index = (selected_index - 1) % len(characters)
                elif event.key == K_RIGHT:
                    selected_index = (selected_index + 1) % len(characters)
                elif event.key == K_RETURN:
                    return CHARACTER_IMAGES[characters[selected_index]]

# Main Game Execution
selected_bird_images = select_character()
bird_group = pygame.sprite.Group()
bird = Bird(selected_bird_images)
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

# Initialize Score
score = 0
font = pygame.font.Font(None, 36)

def draw_score():
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

# Main Game Loop
clock = pygame.time.Clock()
begin = True

while begin:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            bird.bump()
            pygame.mixer.Sound(WING_SOUND).play()
            begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))
    bird_group.draw(screen)
    pygame.display.update()

while True:
    clock.tick(15)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
            bird.bump()
            pygame.mixer.Sound(WING_SOUND).play()

    screen.blit(BACKGROUND, (0, 0))
    bird_group.update()
    pipe_group.update()
    pipe_group.draw(screen)
    ground_group.update()

    # Check for Passing Pipes to Update Score
    for pipe in pipe_group:
        if pipe.is_off_screen():
            pipe_group.remove(pipe)
            pipes = get_random_pipes(SCREEN_WIDTH * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])
        elif not pipe.scored and pipe.rect.right < bird.rect.left:
            score += 1
            pipe.scored = True  # Tandai pipa sudah dihitung

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])
        pipes = get_random_pipes(SCREEN_WIDTH * 2)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    draw_score()  # Draw the score on the screen
    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
            pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.mixer.Sound(HIT_SOUND).play()
        time.sleep(1)
        break
