import turtle
import time
import random

delay = 0.1  
score = 0
high_score = 0
level = 1

wind = turtle.Screen()
wind.title("Snake game")
wind.bgcolor("green")
wind.setup(width=600, height=600)
wind.tracer(0)  

#Головa змейки
head = turtle.Turtle()
head.shape("square")
head.color("yellow")
head.penup()
head.goto(0, 0)
head.direction = "stop"

segments = []

#еда
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

#счетчик и уровнь
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

#обновление текста
def update_scoreboard():
    pen.clear()
    pen.write(f"Score: {score}  High Score: {high_score}  Level: {level}",
              align="center", font=("Arial", 24, "bold"))

#сброс игры
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

while True:
    wind.update()  
    #выход за границы
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        reset_game()

    #столкновение с едой
    if head.distance(food) < 20:
        while True:
            new_x = random.randrange(-280, 280, 20)
            new_y = random.randrange(-280, 280, 20)
            if position_is_free(new_x, new_y):
                food.goto(new_x, new_y)
                break

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("orange")
        new_segment.penup()
        segments.append(new_segment)

        #счёт и уровень
        score += 10
        if score > high_score:
            high_score = score

        level = score // 30 + 1  #каждые 30 очков растёт уровень
        delay = 0.1 - (level - 1) * 0.01
        if delay < 0.01:
            delay = 0.01

        update_scoreboard()

    #движение хвоста
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
