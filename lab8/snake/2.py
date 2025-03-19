import turtle
import time
import random

score = 0 
high_score=0
delay=0.1

#create a screen
wind = turtle.Screen()
wind.title("Snake")
wind.bgcolor("green")
wind.setup(600,600)
        #width, height
wind.tracer(0)

#head of snake
head = turtle.Turtle()
head.shape("square")
head.color("yellow")
head.penup()
head.goto(0,0)
head.direction ='Stop'

#food
food = turtle.Turtle()
colors = random.choice(['red', 'green', 'black'])
shapes = random.choice(['square', 'circle', 'triangle'])
food.speed (0)
food.shape(shapes)
food.color(colors)
food.penup()
food.goto(0, 100)

pen=turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score: 0   Heigh score: 0", align="center")
font = ("Arial", 24, "bold")

def group():
    if head.direction != "dowind":
        head.direction = "up"

def godowind():
    if head.direction != "up":
        head.direction = "dowind"

def goleft():
    if head.direction != "right":
        head.direction = "left" 

def goright():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    
    if head.direction == "left":
        x = head.xcor
        head.sety(x-20)

    if head.direction == "right":
        x = head.xcor
        head.sety(x+20)

wind.listen()
wind.onkeypress(group, "w")
wind.onkeypress(godowind, "s")
wind.onkeypress(goleft, "a")
wind.onkeypress(goright, "d")

