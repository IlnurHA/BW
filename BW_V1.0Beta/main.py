import pygame
import classes, sprites, settings, new_game_choose, fun, load_game_choose

pygame.init()

size, volume, fullscreen = fun.load_settings()
FPS = 120

width, height = size

running = True
x, y, a, b = 0, 0, 0, 0
choosen = '.'
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height), fullscreen)
pygame.mouse.set_visible(0)
pygame.display.set_caption('BlockWars')

pygame.mixer.music.load('data/sound/track/BlockWarsSoundTrack.wav')
pygame.mixer.music.play(5)
pygame.mixer.music.set_volume(volume)

button_newgame = classes.Button((width // 2 - 125, height // 2 - 50), 'New Game')
button_loadgame = classes.Button((width // 2 - 125, height // 2 + 70 - 50), 'Load Game')
button_settings = classes.Button((width // 2 - 125, height // 2 + 140 - 50), 'Settings')
button_exit = classes.Button((width // 2 - 125, height // 2 + 210 - 50), 'Exit')
buttons = [button_newgame, button_loadgame, button_settings, button_exit]

image = pygame.transform.scale(sprites.BW.image, (width // 2, height // 4))

for lvl_preview in sprites.levels:
    lvl_preview.image = pygame.transform.scale(lvl_preview.image, (width // 2 - 50, height // 2 - 50))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.MOUSEMOTION:
            a, b = event.pos
            for button in buttons:
                button.crossing(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for button in buttons:
                if button.crossing((x, y)):
                    choosen = button.press()
            if choosen == 'Settings':
                settings.settings(screen)
            if choosen == 'Exit':
                exit(0)
            if choosen == 'New Game':
                new_game_choose.new_game_choose(width, height, fullscreen)
            if choosen == 'Load Game':
                load_game_choose.load_game_choose(width, height, fullscreen)
        if event.type == pygame.MOUSEBUTTONUP:
            for button in buttons:
                button.unpress()
    # screen.blit(pygame.transform.scale(sprites.BG.image, (width, height)), (0, 0))
    screen.fill((40, 40, 40))
    screen.blit(image, (width // 4, height // 8))
    for button in buttons:
        button.render(screen)
    if pygame.mouse.get_focused():
        screen.blit(sprites.mouse.image, (a, b))
    pygame.display.flip()
    clock.tick(FPS)
