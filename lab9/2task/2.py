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
wind.tracer(0)  

#голова змейки
head = turtle.Turtle()
head.shape("square")
head.color("yellow")
head.penup()
head.goto(0, 0)
head.direction = "stop"

segments = []

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

#счетчик и уровень
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0  High Score: 0  Level: 1",
          align="center", font=("Arial", 24, "bold"))

#управление
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
#движения головы
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

#привязываем к стрелкам
wind.listen()
wind.onkeypress(go_up, "Up")
wind.onkeypress(go_down, "Down")
wind.onkeypress(go_left, "Left")
wind.onkeypress(go_right, "Right")

#обновления текста 
def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}  Level: {level}",
              align="center", font=("Arial", 24, "bold"))

#сброса игры
def reset_game():
    global score, delay, level
    time.sleep(1)
    head.goto(0, 0)
    head.direction = "stop"

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

#функция для случайной генерации еды с разным весом
def generate_food():
    weight = random.choice([1, 2, 5])  
    new_food_x = random.randrange(-280, 280, 20)
    new_food_y = random.randrange(-280, 280, 20)
    
    while not position_is_free(new_food_x, new_food_y):  
        new_food_x = random.randrange(-280, 280, 20)
        new_food_y = random.randrange(-280, 280, 20)

    food.goto(new_food_x, new_food_y)
    return weight

#таймер еды 
food_timer = time.time() 
food_lifetime = 5  #время еды 5 секунд
food_weight = generate_food()

#основной цикл
while True:
    wind.update()  
    #проверяем на выход за границы
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    #столкновения с едой
    if head.distance(food) < 20:
        score += food_weight  
        if score > high_score:
            high_score = score

        level = score // 30 + 1  # Каждые 30 очков растёт уровень
        delay = 0.1 - (level - 1) * 0.01
        if delay < 0.01:
            delay = 0.01

        update_scoreboard()
        food_weight = generate_food()
        food_timer = time.time()

    if time.time() - food_timer > food_lifetime:
        food_weight = generate_food()
        food_timer = time.time()  

    #двигаем хвост
    for i in range(len(segments) - 1, 0, -1):
        x = segments[i - 1].xcor()
        y = segments[i - 1].ycor()
        segments[i].goto(x, y)
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())
    move()

    #проверка столкновения с хвостом
    for seg in segments:
        if seg.distance(head) < 20:
            reset_game()
            break

    time.sleep(delay)

wind.mainloop()
