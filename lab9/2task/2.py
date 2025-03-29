import turtle
import time
import random

delay = 0.1  
score = 0
high_score = 0
level = 1

wind = turtle.Screen()
wind.title("Snake Game (Arrow Keys)")
wind.bgcolor("green")
wind.setup(width=600, height=600)
wind.tracer(0)  # отключаем автообновление экрана

# Голова змейки
head = turtle.Turtle()
head.shape("square")
head.color("yellow")
head.penup()
head.goto(0, 0)
head.direction = "stop"

segments = []

# Еда
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Счётчик и уровень
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0  High Score: 0  Level: 1",
          align="center", font=("Arial", 24, "bold"))

# Управление
def go_up():
    if head.direction != "down":
        head.direction = "up"
def go_down():
    if head.direction != "up":
        head.direction = "down"
def go_left():
    if head.direction != "right":
        head.direction = "left"
def go_right():
    if head.direction != "left":
        head.direction = "right"

# Движения головы
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Привязываем к стрелкам
wind.listen()
wind.onkeypress(go_up, "Up")
wind.onkeypress(go_down, "Down")
wind.onkeypress(go_left, "Left")
wind.onkeypress(go_right, "Right")

# Обновления текста 
def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}  Level: {level}",
              align="center", font=("Arial", 24, "bold"))

# Сброс игры
def reset_game():
    global score, delay, level
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

    # Убираем хвост
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    score = 0
    level = 1
    delay = 0.1
    update_scoreboard()

def position_is_free(x, y):
    if round(head.xcor()) == x and round(head.ycor()) == y:
        return False
    for seg in segments:
        if round(seg.xcor()) == x and round(seg.ycor()) == y:
            return False
    return True

# Функция для случайной генерации еды с разным весом
def generate_food():
    weight = random.choice([1, 2, 5])  
    new_food_x = random.randrange(-280, 280, 20)
    new_food_y = random.randrange(-280, 280, 20)
    
    while not position_is_free(new_food_x, new_food_y):  
        new_food_x = random.randrange(-280, 280, 20)
        new_food_y = random.randrange(-280, 280, 20)

    food.goto(new_food_x, new_food_y)
    return weight

# Таймер еды 
food_timer = time.time() 
food_lifetime = 5  # Время еды 5 секунд
food_weight = generate_food()

# Нарисуем стену (границы)
wall = turtle.Turtle()
wall.speed(0)
wall.color("white")
wall.penup()
wall.goto(-290, 290)  # верхний левый угол
wall.pendown()
wall.pensize(3)
for _ in range(4):
    wall.forward(580)  # длина стенки
    wall.right(90)
wall.penup()

# Основной цикл
while True:
    wind.update()  # Ручное обновление экрана
    
    # Проверка на выход за границы
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    # Столкновение с едой
    if head.distance(food) < 20:
        score += food_weight  
        if score > high_score:
            high_score = score

        level = score // 30 + 1  # Каждые 30 очков растёт уровень
        delay = 0.1 - (level - 1) * 0.01
        if delay < 0.01:
            delay = 0.01

        update_scoreboard()

        # Добавление нового сегмента в хвост
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("orange")
        new_segment.penup()
        segments.append(new_segment)

        # Генерация новой еды
        food_weight = generate_food()
        food_timer = time.time()

    # Проверка, не истёк ли таймер для еды
    if time.time() - food_timer > food_lifetime:
        food_weight = generate_food()  # Генерация новой еды
        food_timer = time.time()  # Обновляем таймер

    # Двигаем хвост
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)

    # Первый сегмент в позицию головы
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # Двигаем голову
    move()

    # Проверка столкновения с хвостом
    for seg in segments:
        if seg.distance(head) < 20:
            reset_game()
            break

    # Пауза между кадрами (скорость змейки)
    time.sleep(delay)

wind.mainloop()
