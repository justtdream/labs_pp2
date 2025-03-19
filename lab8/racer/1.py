import pygame
import random
import time

pygame.init() 

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# set_mode() takes a tuple as an argument

background = pygame.image.load('lab8/racer/res/AnimatedStreet.png')

running = True

clock = pygame.time.Clock()
FPS = 60 

player_img = pygame.image.load('lab8/racer/res/Player.png')
enemy_img = pygame.image.load('lab8/racer/res/Enemy.png')

background_music = pygame.mixer.music.load('lab8/racer/res/background.wav')
crash_sound = pygame.mixer.Sound('lab8/racer/res/crash.wav')

font = pygame.font.SysFont("Verdana", 60)
game_over = font.render("Game Over", True, "black")

pygame.mixer.music.play(-1) 

PLAYER_SPEED = 5
ENEMY_SPEED = 10

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT - self.rect.h
    
    def move(self):
        keys = pygame.key.get_pressed()  #проверяет нажата ли клавиша
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0) 
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0) 
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.generate_random_rect()
    
    def move(self):
        self.rect.move_ip(0, ENEMY_SPEED)
        if self.rect.top > HEIGHT:
            self.generate_random_rect()
    
    def generate_random_rect(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = 0


player = Player() 
enemy = Enemy() 

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

all_sprites.add([player, enemy])
enemy_sprites.add([enemy])

while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background, (0, 0))

    player.move()
    enemy.move()

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(player, enemy_sprites):
        crash_sound.play()
        time.sleep(1)

        screen.fill("red")
        center_rect = game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over, center_rect)

        pygame.display.flip()

        time.sleep(2)
        running = False


    
    pygame.display.flip() 
    clock.tick(FPS) 

pygame.quit()