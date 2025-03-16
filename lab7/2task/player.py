import pygame

pygame.init()
pygame.mixer.init()

tracks = [
    "lab7/2task/track1.mp3",
    "lab7/2task/track2.mp3",
    "lab7/2task/track3.mp3"
    ]
current_index = 0

pygame.display.set_mode((300, 100))
pygame.display.set_caption("Super Simple Music Player")

def play_track(index):
    pygame.mixer.music.load(tracks[index])
    pygame.mixer.music.play()

play_track(current_index)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # P = Play 
            if event.key == pygame.K_p:
                play_track(current_index)
            
            # S = Stop
            if event.key == pygame.K_s:
                pygame.mixer.music.stop()
            
            # N = Next 
            if event.key == pygame.K_n:
                current_index = (current_index + 1) % len(tracks)
                play_track(current_index)
            
            # B = Back 
            if event.key == pygame.K_b:
                current_index = (current_index - 1) % len(tracks)
                play_track(current_index)

pygame.quit()
