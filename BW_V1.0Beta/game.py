import pygame
import fun, classes, sprites, esc
import time

# const
def game(width, height, fullscreen, lvl_name):
    FPS = 120
    WIDTH = width
    HEIGHT = height
    running = True
    drawing = False
    newturnanimation = False
    screen_3 = pygame.display.set_mode((width, height), fullscreen)

    clock = pygame.time.Clock()
    board = classes.board
    board.clear()
    board.set_level(lvl_name)
    board.resize(WIDTH, HEIGHT)
    DELTA = board.get_delta()
    hud = classes.hud
    bu = False

    players = [player_1, player_2, player_3, player_4] = board.get_players()

    turns = {
        player_1: player_2,
        player_2: player_3,
        player_3: player_4,
        player_4: player_1
    }
    turned = players[board.get_first_turned()]
    next_turned = turns[turned]
    while not next_turned.active:
        next_turned = turns[next_turned]
    turned.update()

    button_town = classes.Button((WIDTH - 275, 30), 'Build Town')
    button_gun = classes.Button((WIDTH - 275, 90), 'Set Gun')
    button_block = classes.Button((WIDTH - 275, 150), 'Set Block')
    button_destroy = classes.Button((WIDTH - 275, 210), 'Destroy')
    button_end_turn = classes.Button((WIDTH - 275, HEIGHT - 80), 'End Turn')

    buttons = [button_town, button_gun, button_block, button_destroy, button_end_turn]
    players = [player_1, player_2, player_3, player_4]
    pygame.mouse.set_visible(0)

    DELTA = board.resize(WIDTH, HEIGHT)
    classes.resize(DELTA, button_town, button_gun, button_block, button_destroy, button_end_turn)
    hud.resize()

    hud.set_turned_text(str(board.get_first_turned() + 1), turned)

    x, y, a, b = 0, 0, 0, 0
    turned_gun = None
    ch = 0
    choosen = '.'
    while running:
        ch += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                sprites.click.play()
                x, y = event.pos
                if 0 <= x < DELTA[0] * len(board.board[0]) and 0 <= y < DELTA[1] * len(board.board) and turned.action != 0:
                    x1, y1 = board.get_click(event.pos)
                    if board.board[y1][x1] is not None:
                        if board.board[y1][x1].player == turned:
                            if board.board[y1][x1].built or choosen == 'Destroy':
                                if choosen == 'Destroy':
                                    board.destroy_object(y1, x1)
                                    turned.use_action()
                                    hud.update_actions()
                                    for button in buttons:
                                        button.unpress()
                                    choosen = '.'
                                else:
                                    if board.board[y1][x1].__class__ == classes.Gun:
                                        turned_gun = board.board[y1][x1]
                            else:
                                board.board[y1][x1].build()
                                turned.use_action()
                                hud.update_actions()
                        elif board.board[y1][x1].__class__ == classes.Gun:
                            if turned_gun is not None and turned_gun.can_destroy(y1, x1):
                                board.attack(y1, x1, turned)
                                turned_gun = None
                                turned.use_action()
                                hud.update_actions()
                        elif board.board[y1][x1].__class__ == classes.Block:
                            if turned_gun is not None and turned_gun.can_destroy(y1, x1):
                                board.attack(y1, x1, turned)
                                turned_gun = None
                                turned.use_action()
                                hud.update_actions()
                        elif board.board[y1][x1].__class__ == classes.Town:
                            if turned_gun is not None and turned_gun.can_destroy(y1, x1):
                                board.attack(y1, x1, turned)
                                turned_gun = None
                                turned.use_action()
                                hud.update_actions()
                    else:
                        if choosen in 'GunTownBlock' and board.possible(y1, x1, turned):
                            board.board[y1][x1] = classes.get_class(choosen, (y1, x1), turned)
                            turned.add_own(board.board[y1][x1])
                            turned.update_max_actions()
                            turned.use_action()
                            hud.update_actions()
                            board.board[y1][x1].build()
                            choosen = '.'
                else:
                    find = False
                    for button in buttons:
                        button.unpress()
                        if button.crossing((x, y)):
                            choosen = button.press()
                            if choosen != 'Destroy' and choosen != 'End Turn':
                                choosen = choosen.split()[1]
                            find = True
                        if not find:
                            choosen = '.'
                    if choosen == 'End Turn':
                        newturnanimation = True
                        sprites.newturn.play()
                        choosen = '.'
                        button_end_turn.unpress()
                        turned.update(turn=False)
                        turned = next_turned
                        next_turned = turns[next_turned]
                        while not next_turned.active:
                            next_turned = turns[next_turned]
                        turned.update()
                        hud.set_turned_text(str(players.index(turned) + 1), turned)
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                for button in buttons:
                    button.crossing(event.pos)
                if 0 <= x < DELTA[0] * len(board.board[0]) and 0 <= y < DELTA[1] * len(board.board):
                    b, a = board.get_click(event.pos)
                else:
                    a, b = -1, -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not esc.menu(screen_3, board):
                        running = False
        if newturnanimation:
            count += 1
            if count == 60:
                newturnanimation = False
        if not newturnanimation:
            count = 0
        if not running:
            break
        screen_3.fill((0, 0, 0))
        hud.update_hud(screen_3)
        if (ch // 80) % 2 == 0:
            board.update(screen_3, True)
        else:
            board.update(screen_3)
        for button in buttons:
            button.render(screen_3)
        hud.draw_info((a, b), screen_3, board.board[a][b])
        if newturnanimation:
            screen_3.blit(sprites.newturnanim[count // 6], (0, 0))
        if pygame.mouse.get_focused():
            screen_3.blit(sprites.mouse.image, (x, y))

        k = 0
        for c in players:
            if c.active:
                k += 1
        if k == 1:
            for c in players:
                if c.active:
                    fun.win(c, screen_3, WIDTH, HEIGHT)
                    bu = True
        if bu:
            break

        pygame.display.flip()
        clock.tick(FPS)

