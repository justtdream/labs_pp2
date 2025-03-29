import pygame
import random
import time

pygame.init()

# про экран
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 30

running = True
FPS = 5
clock = pygame.time.Clock()

# цвета
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# текст
font = pygame.font.SysFont("Verdana", 60) # создаем шрифт 
text_game_over = font.render("Game Over", True, BLACK) # генирируем текст
text_game_over_rect = text_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))

# счетчик и уровень
snake_score = 0
small_font = pygame.font.SysFont("Verdana", 32) #создаем шрифт для отображения счёта и уровня.
current_level = 1

# клеточки
def draw_grid_chess():  # рисует игровое поле в виде клеточек, чередующихся цветов
    colors = [WHITE, GRAY]

    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

# классы
class Point:  #хранения координат змейки и еды
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1  
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):

            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # проверяет столкновение с границами
        if (self.body[0].x > WIDTH // CELL - 1 or self.body[0].x < 0 or 
            self.body[0].y > HEIGHT // CELL - 1 or self.body[0].y < 0):
                screen.fill(RED)
                screen.blit(text_game_over, text_game_over_rect)
                pygame.display.flip()
                time.sleep(3)
                pygame.quit() 
                exit()

        # Проверка столкновений головы с хвостом       
        for segment in self.body[1:]:
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                screen.fill(RED)
                screen.blit(text_game_over, text_game_over_rect)
                pygame.display.flip()
                time.sleep(3)
                pygame.quit()
                exit()


    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, RED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, YELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        global snake_score
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            snake_score += 1
            self.body.append(Point(head.x, head.y))
            food.generate_random_pos()
            

snake = Snake()

class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self):
        while True:
            # рандомная генерация координатов еды
            new_x = random.randint(0, WIDTH // CELL - 1)
            new_y = random.randint(0, HEIGHT // CELL - 1)
            collision = False 
            for segment in snake.body:
                if segment.x == new_x and segment.y == new_y:
                    collision = True  
                    break  

            if not collision:
                self.pos = Point(new_x, new_y)
                break

food = Food()

# основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1
            


    draw_grid_chess()

    snake.move()

    # текст счета
    text_score = small_font.render(f"Score: {snake_score}", True, YELLOW)
    text_score_rect = text_score.get_rect(center = (WIDTH // 2, (HEIGHT // CELL) + 20))
    screen.blit(text_score, text_score_rect)
    
    # текст уровня
    text_level = small_font.render(f'Level: {current_level}', True, RED)
    text_level_rect = text_level.get_rect(center = ((WIDTH // 2, (HEIGHT // CELL) - 10)))
    screen.blit(text_level, text_level_rect)

    snake.check_collision(food)

    snake.draw()
    food.draw()


    # быстрее каждые 5 счетов
    if snake_score % 5 == 0 and snake_score != 0:
        FPS = 5 + (snake_score // 5)
        current_level = 1 + (snake_score // 5)

    


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()