import pygame, os
import classes, sprites, game, fun

pygame.init()

FPS = 120
width = 1200
height = 800
volume = 0.5


def load_game_choose(width, height, fullscreen):
    running = True
    x, y, a, b = 0, 0, 0, 0
    FPS = 60
    choosen = '.'
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(0)
    screen_2 = pygame.display.set_mode((width, height), fullscreen)

    button_start_game = classes.Button((int(width * 3 / 4) - classes.Button.size[1], int(height * 3 / 4)), 'Start Game')
    button_back = classes.Button((width // 4, int(height * 3 / 4)), 'Back')
    buttons = [button_start_game, button_back]
    choose_text = 'Choose Level'
    choosed_level = ''
    levels = fun.find_levels()
    font = classes.FONT
    view_levels = classes.LevelView(levels, width // 2 - 10, height // 2 - 75, (width // 4 + 5, height // 4 + 75))
    i, j = 0, 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                a, b = event.pos
                for button in buttons:
                    button.crossing(event.pos)
                view_levels.crossing(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    if button.crossing((x, y)):
                        choosen = button.press()
                if choosen == 'Start Game':
                    if choosed_level != '':
                        fullname = os.path.join('data/saves/' + choosed_level)
                        game.game(width, height, fullscreen, fullname)
                        running = False
                if choosen == 'Back':
                    running = False
                if fun.crossing((width // 2, height // 4 + 40), (x, y)):
                    if j != 0:
                        view_levels.view_levels_up()
                        j -= 1
                        if i != 0:
                            i -= 1
                if fun.crossing((width // 2, int((height * 3) / 4) - 25), (x, y)):
                    if j + view_levels.kol < len(view_levels.levels):
                        view_levels.view_levels_down()
                        j += 1
                        if i != view_levels.kol - 1:
                            i += 1
                x = view_levels.crossing(event.pos)
                if x is not None:
                    view_levels.press(x)
                    choosed_level = view_levels.view_levels[x]
                    for i in range(len(view_levels.levels)):
                        if view_levels.view_levels[i] != view_levels.view_levels[x]:
                            view_levels.view_levels_pressed[i] = False
                else:
                    choosed_level = ''
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.unpress()
        screen_2.fill((40, 40, 40))
        screen_2.fill((100, 100, 100), (width // 4, height // 4, width // 2, height // 2))
        screen_2.blit(font.render(choose_text, True, pygame.Color('white')), (width // 2 - 50, height // 4 + 17))
        if j != 0:
            screen_2.blit(sprites.up.image, (width // 2, height // 4 + 40))
        if j + view_levels.kol < len(view_levels.levels) and len(view_levels.levels) > view_levels.kol:
            screen_2.blit(sprites.down.image, (width // 2, int((height * 3) / 4) - 25))
        for button in buttons:
            button.render(screen_2)
        view_levels.view_levels_update(screen_2)
        if pygame.mouse.get_focused():
            screen_2.blit(sprites.mouse.image, (a, b))
        pygame.display.flip()
        clock.tick(FPS)
