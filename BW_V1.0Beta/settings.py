import pygame
import sprites, classes, fun

pygame.init()


def settings(screen):
    running = True
    FPS = 120
    choosen = '.'
    clock = pygame.time.Clock()
    x, y, a, b = 0, 0, 0, 0
    volume_slider = classes.Slider((20, 80))
    button_exit = classes.Button((5, classes.HEIGHT), 'Back')
    button_save_settings = classes.Button((classes.WIDTH, classes.HEIGHT), 'Save Setting')
    buttons = [button_exit, button_save_settings]
    sliders = [volume_slider]
    FONT = classes.FONT
    while running:
        choosen = '.'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                a, b = event.pos
                for slider in sliders:
                    if slider.pressed:
                        if a - 15 > 0 and a - 15 < 400:
                            slider.xp = a - 15
                    slider.crossing(event.pos)
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
                for slider in sliders:
                    if slider.crossing((x, y)):
                        slider.press()
                if choosen == 'Back':
                    running = False
            if event.type == pygame.MOUSEBUTTONUP:
                for button in buttons:
                    button.unpress()
                for slider in sliders:
                    if slider.pressed:
                        classes.volume_value = slider.get_pos()
                        classes.volume_update()
                    slider.unpress()

        screen.fill((50, 50, 50))

        screen.blit(FONT.render('Settings', True, (255, 255, 255)), (20, 20))
        screen.blit(FONT.render('Music', True, (255, 255, 255)), (20, 60))

        for button in buttons:
            button.render(screen)
        for slider in sliders:
            slider.render(screen)
        if pygame.mouse.get_focused():
            screen.blit(sprites.mouse.image, (a, b))

        pygame.display.flip()
        clock.tick(FPS)
