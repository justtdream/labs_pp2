import pygame
import random
import time
import psycopg2

pygame.init()

username = input("Enter your username: ")

conn = psycopg2.connect(
    database='snake_db',
    user='postgres',
    password='_Avndfgt!',
    host='localhost',
    port='5432'
)
conn.autocommit = True
cursor = conn.cursor()

# Check if user exists
cursor.execute("SELECT id FROM users WHERE username = %s;", (username,))
user_data = cursor.fetchone()

if user_data:
    user_id = user_data[0]
    cursor.execute("SELECT score, level, length FROM user_score WHERE user_id = %s;", (user_id,))
    score_data = cursor.fetchone()

    if score_data:
        current_score, current_level, current_length = score_data
    else:
        cursor.execute(
            "INSERT INTO user_score (user_id, score, level, length) VALUES (%s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING;;",
            (user_id, 0, 1, 3)  # Initial length set to 3
        )
        current_score = 0
        current_level = 1
        current_length = 3
    print(f"Welcome back, {username}! Your score is {current_score} and you're on level {current_level}.")
else:
    # Create new user
    cursor.execute(
        "INSERT INTO users (username) VALUES (%s) RETURNING id;",
        (username,)
    )
    user_id = cursor.fetchone()[0]
    # Insert initial score and level
    cursor.execute(
        "INSERT INTO user_score (user_id, score, level, length) VALUES (%s, %s, %s, %s);",
        (user_id, 0, 1, 3)
    )
    current_score = 0
    current_level = 1
    current_length = 3
    print(f"New user created: {username}, starting with score {current_score} and level {current_level}.")


def save_game_over():
    conn = psycopg2.connect(
        database='snake_db',
        user='postgres',
        password='_Avndfgt!',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # check if the user already exists
    cursor.execute("SELECT * FROM user_score WHERE user_id = %s;", (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:  # If the user exists, update the data
        cursor.execute(
            "UPDATE user_score SET score = %s, level = %s, length = %s WHERE user_id = %s;",
            (snake_score, current_level, len(snake.body), user_id)
        )
        print("Score, level, and snake length updated for the existing user.")
    else:  # If the user does not exist, insert a new row
        cursor.execute(
            "INSERT INTO user_score (user_id, score, level, length) VALUES (%s, %s, %s, %s);",
            (user_id, snake_score, current_level, len(snake.body))
        )
        print("New user created and score, level, and snake length saved.")

    cursor.close()
    conn.close()


# Screen info
WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CELL = 30



running = True
waiting = False
paused = False
FPS = 5
clock = pygame.time.Clock()
last_level = 0

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BG_COLOR1 = (154, 205, 50)
BG_COLOR2 = (150, 180, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GOLD_YELLOW = (255, 215, 0)
DARK_GREEN = (0, 90, 0)


# Text - GAME OVER
font = pygame.font.SysFont("Verdana", 60)
text_game_over = font.render("Game Over", True, BLACK)
text_game_over_rect = text_game_over.get_rect(center = (WIDTH // 2, HEIGHT // 2))
small_font = pygame.font.SysFont("Verdana", 32)

# Score
snake_score = current_score
FPS = 5 + (snake_score // 5)


# BACKGROUND 
def draw_grid_chess():
    colors = [BG_COLOR1, BG_COLOR2]

    for i in range(HEIGHT // CELL): # amount of squares in a column (20)
        for j in range(WIDTH // CELL): # amount of squares in a row (20)
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))
                                    # alternnating colors |   # x   |   # y   |  W  |  H  |      
                                    # if even - BG_COLOR1
                                    # if odd - BG_COLOR2

# Class - Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Class - Walls
class Walls:
    def __init__(self, level):
        self.position = []
        self.level = level
    def generate_level_walls(self):
        if self.level == 1:
            for x in range(HEIGHT//CELL): 
                self.position.append(Point(x, 0)) # full wall on the top
        elif self.level == 2:
            for y in range(HEIGHT//CELL): 
                self.position.append(Point(0, y)) # half of the wall on the left
        elif self.level == 3:
            for x in range(HEIGHT//CELL): 
                self.position.append(Point(x, WIDTH // CELL - 1)) # bottom wall
                self.position.append(Point(x, 0)) # top wall
        elif self.level == 4:
            for y in range(HEIGHT//CELL): 
                self.position.append(Point(WIDTH // CELL - 1, y)) # right wall
        elif self.level >= 5:
            for i in range(HEIGHT//CELL): 
                self.position.append(Point(i, WIDTH // CELL - 1))
                self.position.append(Point(WIDTH // CELL - 1, i))
                self.position.append(Point(0, i))
                self.position.append(Point(i, 0))
            for i in range(7, 13):
                self.position.append(Point(i, 10))
                self.position.append(Point(10, i))
            
    def draw(self): # Drawing walls
        for pos in self.position:
            pygame.draw.rect(screen, DARK_GREEN, (pos.x * CELL, pos.y * CELL, CELL, CELL))
    def check_collision(self):
        for wall in self.position:
            if snake.body[0].x == wall.x and snake.body[0].y == wall.y:
                return True
        return False


level_walls = Walls(current_level)
level_walls.generate_level_walls()
# Class - Snake
class Snake:
    def __init__(self, initial_length):
        self.body = [Point(10, 11)]
        for i in range(1, initial_length):
            self.body.append(Point(10, 11 + i))
        self.dx = 1 # by default moves right
        self.dy = 0

    def move(self):
        global waiting
        # shifting each segment to the position of the one in front
        for i in range(len(self.body) - 1, 0, -1): # starting from last segment(except head), backward list
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        
        # movement of the head
        self.body[0].x += self.dx
        self.body[0].y += self.dy


        # wrap-around logic
        if self.body[0].x >= WIDTH // CELL:
            self.body[0].x = 0
        elif self.body[0].x < 0:
            self.body[0].x = WIDTH // CELL - 1
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT // CELL - 1
        elif self.body[0].y >= HEIGHT // CELL:
            self.body[0].y = 0
        
        # Checks collision with walls
        if level_walls.check_collision():
            screen.fill(RED)
            screen.blit(text_game_over, text_game_over_rect)
            # Save the score after game over
            save_game_over()

            

            pygame.display.flip()
            time.sleep(2)
            pygame.quit()
            exit()
            
            

        # Checks collision of snake's head with its body        
        for segment in self.body[1:]: # range excludes head
            if self.body[0].x == segment.x and self.body[0].y == segment.y:
                screen.fill(RED)
                screen.blit(text_game_over, text_game_over_rect)
    
                # save the score after game over
                save_game_over()


                pygame.display.flip()
                time.sleep(2)
                pygame.quit()
                exit()

                
            
        # Drawing head and body of the snake
    def draw(self):
        head = self.body[0]                  # (coordinate x, coordinate y) , w,   h  
        pygame.draw.rect(screen, GOLD_YELLOW, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]: # drawing body
            pygame.draw.rect(screen, YELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # Snake eating food - method
    def check_collision(self, food):
        global snake_score

        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            time.sleep(0.01)
            snake_score += food.weight # increasing score depending on weight
            if food.weight == 1: # appends 1 segment 
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
            if food.weight == 2: # appends 2 segments to the end of the snake's body
                self.body.append(Point(self.body[-1].x, self.body[-1].y))
                self.body.append(Point(self.body[-1].x, self.body[-1].y))

            food.generate_random_pos() 

snake = Snake(current_length)

# Class - Food
class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        self.expiration_time = 5 # food appears for 5 seconds
        self.appeared_time = time.time() # couns how many time passed after food appeared

    def draw(self):
        if self.weight == 1: # food with weight 1 is RED
            pygame.draw.rect(screen, RED, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        if self.weight == 2: # food with weight 2 is GREEN
            pygame.draw.rect(screen, BLUE, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))
        
    def generate_random_pos(self):
        while True:
            # random new coordinates for Food
            new_x = random.randint(0, WIDTH // CELL - 1)
            new_y = random.randint(0, HEIGHT // CELL - 1)

            self.weight = random.choice([1,2]) # randomizing weight: choice between 1 and 2
            collision = False 

            # collision with food
            for segment in snake.body: 
                if segment.x == new_x and segment.y == new_y:
                    collision = True  
                    break  

            for wall in level_walls.position:
                if wall.x == new_x and wall.y == new_y:
                    collision = True
                    break

            if not collision: # if no collision, set new position for food
                self.pos = Point(new_x, new_y) # and
                self.appeared_time = time.time() # reset time
                break

food = Food()

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # press 'P' to pause/unpause
                paused = not paused
                if paused:
                    # save score & level on pause
                    cursor.execute(
                        "UPDATE user_score SET score = %s, level = %s, length = %s WHERE user_id = %s;",
                        (snake_score, current_level, len(snake.body), user_id)
                    )
                    print("Game paused. Score and level saved to database.")
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
    if paused:
        pause_text = small_font.render("Paused - Press P to Resume", True, BLACK)
        screen.blit(pause_text, (WIDTH // 2 - 150, HEIGHT // 2))
        pygame.display.update()
        continue

    draw_grid_chess()
    snake.move()
    snake.check_collision(food)

    snake.draw()
    food.draw()
    level_walls.draw()


    # Making snake move faster with each next 5 points
    if snake_score % 5 == 0 and snake_score != 0:
        current_level = 1 + (snake_score // 5)
        if current_level != last_level:
            FPS = 5 + (snake_score // 5)
            level_walls = Walls(current_level)
            level_walls.generate_level_walls()
            last_level = current_level 


    if time.time() - food.appeared_time > food.expiration_time: # if 5 seconds passed,
        food.generate_random_pos()                              # food generates on another position with dif weight

    # text - Score
    text_score = small_font.render(f"Score: {snake_score}", True, YELLOW)
    text_score_rect = text_score.get_rect(center = (WIDTH // 2, (HEIGHT // CELL) + 20))
    screen.blit(text_score, text_score_rect)
    
    # text - Level
    text_level = small_font.render(f'Level: {current_level}', True, RED)
    text_level_rect = text_level.get_rect(center = ((WIDTH // 2, (HEIGHT // CELL) - 10)))
    screen.blit(text_level, text_level_rect)
    


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()