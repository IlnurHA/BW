import pygame, sprites, classes, fun, settings

pygame.init()


def menu(screen, board):
    running = True
    x, y, a, b = 0, 0, 0, 0
    FPS = 120
    choosen = '.'
    clock = pygame.time.Clock()
    button_continue = classes.Button((5, classes.HEIGHT - 205), 'Continue')
    button_save = classes.Button((5, classes.HEIGHT - 155), 'Save Game')
    button_settings = classes.Button((5, classes.HEIGHT - 105), 'Settings')
    button_exit = classes.Button((5, classes.HEIGHT - 55), 'Exit')
    buttons = [button_continue, button_save, button_settings, button_exit]
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEMOTION:
                a, b = event.pos
                for button in buttons:
                    button.crossing(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for button in buttons:
                    if button.crossing((x, y)):
                        choosen = button.press()
                if choosen == 'Continue':
                    return True
                if choosen == 'Save Game':
                    x, y = len(classes.board.board[0]), len(classes.board.board)
                    data = ''
                    data_1 = '{} {}\n'.format(x, y)
                    data_2 = [['.'] * x for i in range(y)]
                    data_3 = str(classes.board.get_num())
                    for i in range(y):
                        for j in range(x):
                            if classes.board.board[i][j] != None:
                                if classes.board.board[i][j].__class__ == classes.Town:
                                    if classes.board.board[i][j].main_town:
                                        data_2[i][j] = '@' + str(
                                            classes.COLORS.index(classes.board.board[i][j].player.color) + 1) + '*'\
                                                       + str(classes.board.board[i][j].build_actions) + '*'\
                                                       + str(classes.board.board[i][j].life)
                                    else:
                                        data_2[i][j] = 'T' + str(
                                            classes.COLORS.index(classes.board.board[i][j].player.color) + 1) + '*' \
                                                       + str(classes.board.board[i][j].build_actions) + '*' \
                                                       + str(classes.board.board[i][j].life)
                                if classes.board.board[i][j].__class__ == classes.Gun:
                                    data_2[i][j] = 'G' + str(
                                        classes.COLORS.index(classes.board.board[i][j].player.color) + 1) + '*'\
                                                   + str(classes.board.board[i][j].build_actions) + '*'\
                                                   + str(classes.board.board[i][j].life)
                                if classes.board.board[i][j].__class__ == classes.Block:
                                    data_2[i][j] = 'B' + str(
                                        classes.COLORS.index(classes.board.board[i][j].player.color) + 1) + '*'\
                                                   + str(classes.board.board[i][j].build_actions) + '*'\
                                                   + str(classes.board.board[i][j].life)
                        for j in range(1, x):
                            data_2[i][0] += ';' + data_2[i][j]
                    data += data_1
                    for i in range(len(data_2)):
                        data += data_2[i][0] + '\n'
                    data += data_3
                    fun.save_game(data)
                if choosen == 'Settings':
                    settings.settings(screen)
                if choosen == 'Exit':
                    return False
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.unpress()
        screen.fill((50, 50, 50))
        board.update(screen)
        for button in buttons:
            button.render(screen)
        if pygame.mouse.get_focused():
            screen.blit(sprites.mouse.image, (a, b))
        pygame.display.flip()
        clock.tick(FPS)
