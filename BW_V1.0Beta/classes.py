import pygame, fun, sprites

HEIGHT = 600
WIDTH = 800
DELTA = 0

next_turned = None

players = []
COLORS = [pygame.Color('blue'), pygame.Color('red'), pygame.Color('yellow'), pygame.Color('green')]
FONT = pygame.font.Font(None, 25)

volume = True
volume_value = 0.5

sprite = [sprites.blueblock, sprites.redblock, sprites.yellowblock, sprites.greenblock,
          sprites.gun_sprite, sprites.town_sprite, sprites.main_town_sprite]


def volume_update():
    global volume_value
    pygame.mixer_music.set_volume(volume_value)


def load_level(name, fullname=''):
    global DELTA
    players = create_player()
    if fullname == '':
        f = open('data/levels/' + name, 'r')
    else:
        f = open(fullname, 'r')
    alldata = f.readlines()
    x, y = map(int, alldata.pop(0).split())
    lvl_data = [[None] * x for _ in range(y)]
    for i in range(y):
        data_2 = alldata[i].strip().split(';')
        for j in range(x):
            if data_2[j] != '\n' and data_2[j] != '.' and data_2[j] not in '1234':
                data = data_2[j].split('*')
                color = fun.get_color(int(data[0][1]))
                if data[0][0] == '@':
                    for g in range(len(players)):
                        if players[g].color == color:
                            if not players[g].active:
                                players[g].active = True
                            lvl_data[i][j] = Town((i, j), players[g], sprites.all_sprites, main_town=True)
                            players[g].own.append(lvl_data[i][j])
                            sprites.main_town_sprite.add(sprites.all_sprites)
                elif data[0][0] == 'G':
                    data = data_2[j].split('*')
                    for g in range(len(players)):
                        if players[g].color == color:
                            lvl_data[i][j] = Gun((i, j), players[g], sprites.all_sprites)
                            players[g].own.append(lvl_data[i][j])
                            sprites.gun_sprite.add(sprites.all_sprites)
                elif data[0][0] == 'B':
                    data = data_2[j].split('*')
                    for g in range(len(players)):
                        if players[g].color == color:
                            if not players[g].active:
                                players[g].active = True
                            lvl_data[i][j] = Block((i, j), players[g], sprites.all_sprites)
                            players[g].own.append(lvl_data[i][j])
                            sprites.block_sprite.add((sprites.all_sprites))
                elif data[0][0] == 'T':
                    data = data_2[j].split('*')
                    for g in range(len(players)):
                        if players[g].color == color:
                            if not players[g].active:
                                players[g].active = True
                            lvl_data[i][j] = Town((i, j), players[g], sprites.all_sprites)
                            players[g].own.append(lvl_data[i][j])
                lvl_data[i][j].build_actions = int(data[1])
                if lvl_data[i][j].build_actions == lvl_data[i][j].to_be_built:
                    lvl_data[i][j].built = True
                lvl_data[i][j].life = int(data[2])
    turn = int(alldata[-1].strip()) - 1
    f.close()
    DELTA = DELTA_x, DELTA_y = (WIDTH - 300) // x, HEIGHT // y
    resize(DELTA)
    return lvl_data, DELTA, turn, players


def resize(x, *buttons):
    for s in sprite:
        s.image = pygame.transform.scale(s.image, (x[0], x[1]))

    for image in sprites.build_sprite.image:
        image = pygame.transform.scale(image, (x[0], x[1]))

    for i in range(len(players)):
        for j in range(len(players[i].own)):
            players[i].own[j].change_image()

    for i in range(len(buttons)):
        if len(buttons) != i + 1:
            buttons[i].change_coords((WIDTH - 275, 15 + i * 60))
        else:
            buttons[i].change_coords((WIDTH - 275, HEIGHT - 80))


class Board(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)

    def set_level(self, lvl_name):
        self.board, self.DELTA, self.first_turned, self.players = load_level(lvl_name,
                                                                             fullname=lvl_name)

    def destroy_object(self, x, y):
        self.board[x][y] = None

    def update(self, sc, second_form=False):
        c = 0
        coco = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if c % 2 == 0:
                    coco = 20  # немного отсебятины
                else:
                    coco = -20
                c += 1
                pygame.draw.rect(sc, (0, 200 + coco, 0), (j * DELTA[0], i * DELTA[1], DELTA[0], DELTA[1],))
                if self.board[i][j] is not None:
                    image = sprite[COLORS.index(self.board[i][j].player.color)].image
                    sc.blit(image, (j * DELTA[0], i * DELTA[1]))
                    if self.board[i][j].__class__ != Block and self.board[i][j].built:
                        sc.blit(self.board[i][j].image, (j * DELTA[0], i * DELTA[1]))
                    elif not self.board[i][j].built:
                        if second_form:
                            sc.blit(sprites.build_sprite.image[1], (j * DELTA[0], i * DELTA[1]))
                        else:
                            sc.blit(sprites.build_sprite.image[0], (j * DELTA[0], i * DELTA[1]))
            if len(self.board[i]) % 2 == 0:
                c += 1

    def clear(self):
        global players
        players = []

    def get_click(self, mousepos, fullcoord=False):
        if fullcoord:
            return mousepos
        x, y = mousepos
        x1 = x // self.DELTA[0]
        y1 = y // self.DELTA[1]
        return (x1, y1)

    def get_delta(self):
        return self.DELTA

    def resize(self, width, height):
        global WIDTH, HEIGHT, DELTA
        WIDTH = width
        HEIGHT = height
        self.DELTA = DELTA = ((WIDTH - 300) // len(self.board[0]), HEIGHT // len(self.board))
        return self.DELTA

    def attack(self, x, y, turned):
        sprites.shot.play()
        self.board[x][y].life -= 1
        if self.board[x][y].life <= 0:
            if self.board[x][y].__class__ == Town and self.board[x][y].main_town:
                self.board[x][y].player.active = False
                for building in self.board[x][y].player.own:
                    if self.board[x][y] == building:
                        continue
                    turned.add_own(building)
                    building.player = turned
                    building.change_image()
                self.destroy_object(x, y)
            else:
                self.destroy_object(x, y)

    def get_first_turned(self):
        return self.first_turned

    def get_players(self):
        return self.players

    def get_num(self):
        color = pygame.Color('blue')
        for player in players:
            if player.turn:
                color = player.color
        return COLORS.index(color) + 1

    def possible(self, y, x, player):
        if 0 <= x - 1 < len(self.board[0]) and 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x - 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
            pos = self.board[y - 1][x]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
            pos = self.board[y][x - 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        elif 0 <= x - 1 < len(self.board[0]):
            pos = self.board[y][x - 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        elif 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        if 0 <= x + 1 < len(self.board[0]) and 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x + 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
            pos = self.board[y + 1][x]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
            pos = self.board[y][x + 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        elif 0 <= x + 1 < len(self.board[0]):
            pos = self.board[y][x + 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        elif 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True

        if 0 <= x - 1 < len(self.board[0]) and 0 <= y + 1 < len(self.board):
            pos = self.board[y + 1][x - 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True

        if 0 <= x + 1 < len(self.board[0]) and 0 <= y - 1 < len(self.board):
            pos = self.board[y - 1][x + 1]
            if pos is not None and pos.player == player:
                if pos.__class__ == Town and pos.main_town:
                    return True
                if pos.__class__ == Block:
                    return True
        return False


class Block(pygame.sprite.Sprite):
    def __init__(self, coord, whose, group):
        super().__init__(group)
        self.image = sprite[COLORS.index(whose.color)].image
        self.x_coord = coord[0]
        self.y_coord = coord[1]
        self.player = whose
        self.max_life = 1
        self.life = 1
        self.built = False
        self.build_actions = 0
        self.to_be_built = 1

    def get_coords(self):
        return (self.x_coord, self.y_coord)

    def build(self):
        self.build_actions += 1
        if self.build_actions >= self.to_be_built:
            self.built = True

    def change_image(self):
        self.image = sprite[COLORS.index(self.player.color)].image


class Town(pygame.sprite.Sprite):
    def __init__(self, coord, whose, group, main_town=False):
        super().__init__(group)
        self.image = sprites.town_sprite.image
        self.x_coord = coord[0]
        self.y_coord = coord[1]
        self.player = whose
        self.max_life = 3
        self.life = 3
        self.built = False
        self.build_actions = 0
        self.to_be_built = 3
        if main_town:
            self.image = sprites.main_town_sprite.image
            self.max_life = 10
            self.life = 10
        self.main_town = main_town

    def get_coords(self):
        return (self.x_coord, self.y_coord)

    def get_image(self):
        return self.image

    def change_image(self):
        self.image = sprites.town_sprite.image
        if self.main_town:
            self.image = sprites.main_town_sprite.image

    def build(self):
        self.build_actions += 1
        if self.build_actions >= self.to_be_built:
            self.built = True


class Gun(pygame.sprite.Sprite):
    def __init__(self, coord, whose, group):
        super().__init__(group)
        self.image = sprites.gun_sprite.image
        self.x_coord = coord[0]
        self.y_coord = coord[1]
        self.player = whose
        self.max_life = 2
        self.life = 2
        self.built = False
        self.build_actions = 0
        self.to_be_built = 2
        self.radius = 1

    def get_coords(self):
        return (self.x_coord, self.y_coord)

    def get_image(self):
        return self.image

    def can_destroy(self, x, y):
        if (abs(self.x_coord - x) == abs(self.y_coord - y) == self.radius) or \
                (abs(self.x_coord - x) == self.radius and abs(self.y_coord - y) == 0) or \
                (abs(self.x_coord - x) == 0 and abs(self.y_coord - y) == self.radius):
            return True
        return False

    def change_image(self):
        self.image = sprites.gun_sprite.image

    def build(self):
        self.build_actions += 1
        if self.build_actions >= self.to_be_built:
            self.built = True


class Player:
    def __init__(self, color):
        self.turn = False
        self.color = color
        self.active = False
        self.max_actions = 1
        self.action = 1
        self.own = []

    def update(self, turn=True):
        self.turn = turn
        self.action = self.max_actions

    def add_own(self, struckt):
        self.own.append(struckt)

    def use_action(self):
        self.action -= 1

    def update_max_actions(self):
        k = 0
        for i in range(len(self.own)):
            if self.own[i].__class__ == Town and not self.own[i].main_town \
                    and self.own[i].built:
                k += 1
        self.max_actions = 1 + k // 5


class Hud:
    def __init__(self):
        x, y = WIDTH - 300, 800
        self.turn_text = 'Turn: Player 1'
        self.actions_text = 'Actions left: 1'
        self.actions = 1
        self.info_name = 'Name: '
        self.info_health = 'Health: '
        self.pos = (WIDTH - 300, HEIGHT)

    def update_hud(self, sc):
        pygame.draw.rect(sc, (40, 40, 40), (self.pos[0], 0, 300, self.pos[1]))
        sc.blit(FONT.render(self.turn_text, True, (255, 255, 255)), (self.pos[0] + 25, 270))
        sc.blit(FONT.render(self.actions_text, True, (255, 255, 255)), (self.pos[0] + 25, 290))
        self.actions_left = 'Actions to build over: '

    def set_turned_text(self, x, player):
        self.turn_text = 'Turn: Player ' + x
        self.actions_text = 'Actions left: ' + str(player.max_actions)
        self.actions = player.max_actions

    def update_actions(self):
        self.actions -= 1
        self.actions_text = 'Actions left: ' + str(self.actions)

    def draw_info(self, pos, sc, item):
        if item is not None:
            self.info_x, self.info_y = pos
            if self.info_x != -1 and self.info_y != -1:
                for i in range(1, 11):
                    if i <= (item.life / item.max_life) * 10:
                        color = pygame.Color('green')
                    else:
                        color = pygame.Color('red')
                    pygame.draw.rect(sc, color, (self.pos[0] + 140 + (i - 1) * 10, 330, 10, 17), 0)
                image = pygame.transform.scale(item.image, (50, 50))
                image_2 = pygame.transform.scale(sprite[COLORS.index(item.player.color)].image, (50, 50))
                sc.blit(FONT.render(self.info_name + item.__class__.__name__, True, (255, 255, 255)),
                        (self.pos[0] + 80, 310))
                sc.blit(FONT.render(self.info_health, True, (255, 255, 255)), (self.pos[0] + 80, 330))
                sc.blit(FONT.render(str(item.life), True, (0, 0, 0)), (self.pos[0] + 185, 330))
                sc.blit(image_2, (self.pos[0] + 25, 310))
                sc.blit(image, (self.pos[0] + 25, 310))
                if not item.built:
                    sc.blit(FONT.render(self.actions_left + str(item.to_be_built - item.build_actions), True,
                                        (255, 255, 255)), (self.pos[0] + 80, 350))

    def resize(self):
        self.pos = (WIDTH - 300, HEIGHT)


class Button:
    image_nonpress = fun.load_image_hud('button-nonclicked.png')
    image_press = fun.load_image_hud('button-clicked.png')
    size = height, width = 50, 250

    def __init__(self, pos, text, pressed=False):
        self.pressed = pressed
        self.crossed = False
        self.pos = pos
        self.text = text
        self.size = self.height, self.width = 50, 250

    def render(self, sc):
        if self.pressed:
            self.image = self.image_press
            color = (255, 255, 255)
        else:
            self.image = self.image_nonpress
            if self.crossed:
                color = (255, 255, 255)
            else:
                color = (0, 0, 0)
        sc.blit(self.image, self.pos)
        sc.blit(FONT.render(self.text, True, color), (self.pos[0] + 17, self.pos[1] + 17))

    def crossing(self, mousepos):
        x1, y1 = mousepos
        x2, y2, w2, h2 = self.pos[0], self.pos[1], self.width, self.height
        if x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2:
            self.crossed = True
            return True
        self.crossed = False
        return False

    def press(self):
        self.pressed = True
        return self.text

    def unpress(self):
        self.pressed = False

    def change_coords(self, pos):
        self.pos = pos


class Slider:
    def __init__(self, pos, value=0):
        self.pos = pos
        self.crossed = False
        self.width_rect = 400
        self.height_rect = 10
        self.xp = 200
        self.pressed = False

    def render(self, sc):
        pygame.draw.rect(sc, (255, 255, 255), (self.pos[0], self.pos[1] + 20, self.width_rect, self.height_rect))
        if self.crossed:
            pygame.draw.circle(sc, (0, 0, 0), (self.pos[0] + self.xp, self.pos[1] + 25), 15)
            pygame.draw.circle(sc, (255, 255, 255), (self.pos[0] + self.xp, self.pos[1] + 25), 12)
        else:
            pygame.draw.circle(sc, (255, 255, 255), (self.pos[0] + self.xp, self.pos[1] + 25), 15)
            pygame.draw.circle(sc, (0, 0, 0), (self.pos[0] + self.xp, self.pos[1] + 25), 12)

    def get_pos(self):
        return self.xp / 400

    def crossing(self, mousepos):
        x1, y1 = mousepos
        x2, y2, w2, h2 = self.pos[0] + self.xp - 15, self.pos[1] + 10, self.pos[0] + self.xp + 15, self.pos[1] + 40
        if x2 <= x1 <= x2 + w2 and y2 <= y1 <= y2 + h2:
            self.crossed = True
            return True
        self.crossed = False
        return False

    def press(self):
        self.pressed = True

    def unpress(self):
        self.pressed = False


def create_player():
    for i in range(4):
        players.append(Player(COLORS[i]))
    return players


def get_class(text, pos, whose):
    if 'Gun' in text:
        return Gun(pos, whose, sprites.all_sprites)
    if 'Block' in text:
        return Block(pos, whose, sprites.all_sprites)
    if 'Town' in text:
        return Town(pos, whose, sprites.all_sprites)


board = Board(sprites.all_sprites)
hud = Hud()


class LevelView:
    def __init__(self, levels, width, height, pos):
        self.levels = levels
        self.kol = height // 35
        self.height = height
        self.width = width
        self.x, self.y = pos
        self.view_levels = [None] * self.kol
        self.view_levels_pressed = [False] * self.kol
        self.view_levels_crossing = [False] * self.kol
        if len(self.levels) < self.kol:
            self.view_levels = [None] * len(self.levels)
            self.view_levels_pressed = [False] * len(self.levels)
            self.view_levels_crossing = [False] * len(self.levels)
        self.view_levels_setup()

    def view_levels_up(self):
        temp = self.view_levels.copy()
        for i in range(1, self.kol):
            self.view_levels[i] = temp[i - 1]
        self.view_levels[0] = self.levels[self.levels.index(temp[0]) - 1]
        self.view_levels_pressed = [False] * self.kol

    def view_levels_down(self):
        temp = self.view_levels.copy()
        for i in range(self.kol - 2, -1, -1):
            self.view_levels[i] = temp[i + 1]
        self.view_levels[self.kol - 1] = self.levels[self.levels.index(temp[self.kol - 1]) + 1]
        self.view_levels_pressed = [False] * self.kol

    def view_levels_update(self, screen):
        for i in range(len(self.view_levels)):
            level = self.view_levels[i]
            if self.view_levels_pressed[i]:
                pygame.draw.rect(screen, pygame.Color('white'), (self.x, self.y + i * 34, self.width, 34))
                color = pygame.Color('black')
            elif self.view_levels_crossing[i]:
                color = pygame.Color('white')
            else:
                color = pygame.Color('black')
            screen.blit(FONT.render(level, True, color), (self.x + 5, self.y + i * 34 + 7))

    def view_levels_setup(self):
        for i in range(self.kol):
            if len(self.levels) > i:
                self.view_levels[i] = self.levels[i]

    def crossing(self, mousepos):
        for i in range(len(self.view_levels)):
            if fun.crossing((self.x, self.y + i * 34, self.width, 34), mousepos, full=True):
                self.view_levels_crossing[i] = True
                return i
            else:
                self.view_levels_crossing[i] = False
        return None

    def press(self, x):
        self.view_levels_pressed[x] = True

    def upress(self):
        self.view_levels_pressed = [False] * self.kol
