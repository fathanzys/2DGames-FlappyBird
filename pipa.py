import pygame
import random
from pygame.locals import *

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
PIPE_GAP = 150
PIPE_COLOR = (0, 128, 0)  # Warna hijau tua
OUTLINE_COLOR = (0, 0, 0)  # Warna hitam untuk outline
END_SIZE = 20  # Ukuran persegi di ujung pipa

# Path untuk gambar background
BACKGROUND_PATH = '/assets/sprites/background-night.png'  # Ganti dengan path gambar latar belakang kamu

class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        super().__init__()
        self.rect = pygame.Rect(xpos, 0, PIPE_WIDTH, PIPE_HEIGHT)  # Membuat rectangle untuk pipa
        if inverted:
            self.rect.y = -(PIPE_HEIGHT - ysize)  # Pipa terbalik (atas)
        else:
            self.rect.y = SCREEN_HEIGHT - ysize  # Pipa biasa (bawah)

    def update(self):
        # Tidak ada update posisi karena pipa tidak bergerak
        pass

    def draw(self, surface):
        # Menggambar pipa dengan warna hijau tua
        pygame.draw.rect(surface, PIPE_COLOR, self.rect)
        
        # Menggambar outline hitam di sekitar pipa
        pygame.draw.rect(surface, OUTLINE_COLOR, self.rect, 5)  # Angka 5 untuk ketebalan outline

        # Menggambar persegi di setiap ujung pipa
        pygame.draw.rect(surface, OUTLINE_COLOR, pygame.Rect(self.rect.x - END_SIZE, self.rect.y, END_SIZE, END_SIZE))  # Ujung kiri
        pygame.draw.rect(surface, OUTLINE_COLOR, pygame.Rect(self.rect.x + self.rect.width, self.rect.y, END_SIZE, END_SIZE))  # Ujung kanan
        if self.rect.y != 0:  # Pipa bagian bawah
            pygame.draw.rect(surface, OUTLINE_COLOR, pygame.Rect(self.rect.x - END_SIZE, self.rect.y + self.rect.height - END_SIZE, END_SIZE, END_SIZE))  # Ujung kiri bawah
            pygame.draw.rect(surface, OUTLINE_COLOR, pygame.Rect(self.rect.x + self.rect.width, self.rect.y + self.rect.height - END_SIZE, END_SIZE, END_SIZE))  # Ujung kanan bawah

# Helper Function untuk mendapatkan pipa acak
def get_random_pipes(xpos):
    size = random.randint(100, 300)  # Ukuran pipa bagian bawah
    pipe = Pipe(False, xpos, size)  # Pipa bagian bawah
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)  # Pipa bagian atas
    return pipe, pipe_inverted

# Untuk menjalankan game
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Menambahkan background
background = pygame.image.load(BACKGROUND_PATH).convert()  # Memuat gambar background
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Menyesuaikan ukuran background

# Membuat grup untuk pipa
pipe_group = pygame.sprite.Group()

# Menambahkan pipa pertama
pipes = get_random_pipes(300)
pipe_group.add(pipes[0], pipes[1])

# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))  # Mengisi layar dengan warna hitam
    
    # Menggambar background terlebih dahulu
    screen.blit(background, (0, 0))  # Menampilkan gambar background pada posisi (0, 0)

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Tidak ada update posisi pipa karena tidak bergerak

    # Menggambar pipa
    for pipe in pipe_group:
        pipe.draw(screen)

    pygame.display.flip()
    clock.tick(60)  # Mengatur framerate

pygame.quit()
