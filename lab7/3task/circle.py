import pygame

pygame.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Circle (Simplified)")

RADIUS = 25
x = WIDTH // 2
y = HEIGHT // 2
STEP = 20

running = True
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if y - STEP >= RADIUS:
            y -= STEP
    if keys[pygame.K_DOWN]:
        if y + STEP <= HEIGHT - RADIUS:
            y += STEP
    if keys[pygame.K_LEFT]:
        if x - STEP >= RADIUS:
            x -= STEP
    if keys[pygame.K_RIGHT]:
        if x + STEP <= WIDTH - RADIUS:
            x += STEP
    screen.fill((255, 255, 255))                      
    pygame.draw.circle(screen, (255, 0, 0), (x, y), RADIUS)  
    pygame.display.flip()                            

pygame.quit()
