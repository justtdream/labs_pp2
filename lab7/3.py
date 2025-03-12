import pygame

pygame.init()

# Настройки
width, height = 640, 480
screen = pygame.display.set_mode((width, height))  #создание экрана
pygame.display.set_caption("example")              #название окна где появляется экран 
clock = pygame.time.Clock() 

# Переменные для игрока
player_x = width // 2
player_y = height // 2
player_speed = 15
player_size = 50

running = True
while running:
    clock.tick(60)
    
    # 1. Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. Обновление логики
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    
    # Ограничим перемещение в пределах экрана
    if player_x < 0:
        player_x = 0
    elif player_x + player_size > width:
        player_x = width - player_size
    if player_y < 0:
        player_y = 0
    elif player_y + player_size > height:
        player_y = height - player_size
    
    # 3. Отрисовка
    screen.fill((0, 0, 0))  # очистка экрана
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_size, player_size))
    pygame.display.flip()

pygame.quit()
