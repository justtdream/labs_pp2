import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer with Coins")

background = pygame.image.load('lab8/racer/res/AnimatedStreet.png')

running = True

clock = pygame.time.Clock()
FPS = 60

player_img = pygame.image.load('lab8/racer/res/Player.png')
enemy_img = pygame.image.load('lab8/racer/res/Enemy.png')
coin_img = pygame.image.load('lab8/racer/res/coin.png').convert_alpha()
coin_img = pygame.transform.scale(coin_img, (30, 30))  

background_music = pygame.mixer.music.load('lab8/racer/res/background.wav')
crash_sound = pygame.mixer.Sound('lab8/racer/res/crash.wav')

font_big = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

game_over_text = font_big.render("Game Over", True, "black")

pygame.mixer.music.play(-1)

PLAYER_SPEED = 5
ENEMY_SPEED = 5

#счетчик
coins_collected = 0

#на каком количестве монет ускоряем врага
COINS_FOR_SPEEDUP = 5
SPEED_UP = 1  #на сколько увеличиваем скорость врага

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH // 2 - self.rect.w // 2
        self.rect.y = HEIGHT - self.rect.h
    
    def move(self):
        keys = pygame.key.get_pressed()  #проверяем нажата ли клавиша
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-PLAYER_SPEED, 0) 
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(PLAYER_SPEED, 0) 
        #границы экрана
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
        #враг движется со скоростью ENEMY_SPEED
        self.rect.move_ip(0, ENEMY_SPEED)
        #проверяем чтоб не выходил за экран
        if self.rect.top > HEIGHT:
            self.generate_random_rect()
    
    def generate_random_rect(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = -self.rect.h  #появится чуть выше верхней границы

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_img
        self.rect = self.image.get_rect()
        # Монеты теперь имеют разный вес
        self.value = random.choice([1, 2, 5])
        self.generate_random_position()

    def move(self):
        self.rect.move_ip(0, 5)
        if self.rect.top > HEIGHT:
            self.generate_random_position()

    def generate_random_position(self):
        self.rect.x = random.randint(0, WIDTH - self.rect.w)
        self.rect.y = random.randint(-400, -40)
        #рандомим (чтобы при переезде сверху могла поменяться монета)
        self.value = random.choice([1, 2, 5])

#создаем объекты
player = Player()
enemy = Enemy()

#спрайты :)
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy)
enemy_sprites.add(enemy)

#генирируем монеты несколько монет
for _ in range(2):
    c = Coin()
    coin_sprites.add(c)
    all_sprites.add(c)

while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #двигаем игрока, врага и монеты
    player.move()
    enemy.move()
    for coin in coin_sprites:
        coin.move()

    #рисуем все спрайты
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    #проверяет столкновения с врагом
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        crash_sound.play()
        time.sleep(1)

        screen.fill("red")
        center_rect = game_over_text.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, center_rect)
        pygame.display.flip()
        time.sleep(2)
        running = False

    # Проверка столкновения с монетами
    # (spritecollide возвращает список монет, с которыми произошло столкновение)
    collided_coins = pygame.sprite.spritecollide(player, coin_sprites, dokill=False)
    for coin in collided_coins:
        # + значение монеты к счетчику
        coins_collected += coin.value
        coin.generate_random_position()

        #ускорение врага от количества монет
        if coins_collected >= COINS_FOR_SPEEDUP:
            ENEMY_SPEED += SPEED_UP
            

    #выводим счетчик
    score_text = font_small.render("Coins: " + str(coins_collected), True, "black")
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
