import pygame
import math
import datetime

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Часы")

clock_face = pygame.image.load("lab7/1task/clock.png").convert_alpha()
minute_hand_img = pygame.image.load("lab7/1task/min_hand.png").convert_alpha()
second_hand_img = pygame.image.load("lab7/1task/sec_hand.png").convert_alpha()

center_x = WIDTH // 2
center_y = HEIGHT // 2

clock_face_rect = clock_face.get_rect(center=(center_x, center_y))
minute_hand_rect = minute_hand_img.get_rect()
second_hand_rect = second_hand_img.get_rect()

def rotate_image(image, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=pivot)
    return rotated_image, new_rect

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    seconds = now.second
    second_angle = - (seconds * 6)  
    minutes = now.minute
    minute_angle = - (minutes * 6)

    screen.fill((255, 255, 255))  
    screen.blit(clock_face, clock_face_rect)
    rotated_minute, minute_rect = rotate_image(minute_hand_img, minute_angle, (center_x, center_y))
    screen.blit(rotated_minute, minute_rect)
    rotated_second, second_rect = rotate_image(second_hand_img, second_angle, (center_x, center_y))
    screen.blit(rotated_second, second_rect)
    
    pygame.display.flip()

pygame.quit()
