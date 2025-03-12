import pygame

pygame.init()                         # 1. Включаем PyGame
screen = pygame.display.set_mode((800, 600))  # 2. Создаём окно
pygame.display.set_caption("Моя игра")

running = True                       # Флажок, показывает, что игра запущена

while running:                       # 3. Главный цикл
    # 3.1. Обрабатываем события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3.2. Обновляем логику игры (перемещения, столкновения и т.д.)
    # Допустим, пока тут ничего не делаем.

    # 3.3. Рисуем всё на экране
    screen.fill((0, 0, 0))  # Красим фон в чёрный цвет
    # Тут бы мы нарисовали героев, фон, текст и т.п.

    pygame.display.flip()   # Обновляем экран (все изменения «показываются»)

# 4. Выходим из игры
pygame.quit()
