import pygame, fun

pygame.init()

all_sprites = pygame.sprite.Group()
gun_sprite_group = pygame.sprite.Group()
block_sprite_group = pygame.sprite.Group()
town_sprite_group = pygame.sprite.Group()

build_image_1 = pygame.image.load('data/animations/BuildAnim/untildone_1.png')
build_image_2 = pygame.transform.rotate(build_image_1, 90)

gun_sprite = pygame.sprite.Sprite()
gun_sprite.image = fun.load_image('gun.png')

BW = pygame.sprite.Sprite()
BW.image = fun.load_image('BW_all.png')
colorkey = BW.image.get_at((0, 0))
BW.image.set_colorkey(colorkey)

right = pygame.sprite.Sprite()
right.image = fun.load_image('left.png')

left = pygame.sprite.Sprite()
left.image = pygame.transform.rotate(right.image, 180)

up = pygame.sprite.Sprite()
up.image = pygame.transform.rotate(right.image, 90)

down = pygame.sprite.Sprite()
down.image = pygame.transform.rotate(right.image, 270)

build_sprite = pygame.sprite.Sprite()
build_sprite.image = [build_image_1,
                      build_image_2]

mouse = pygame.sprite.Sprite()
mouse.image = fun.load_image_hud('arrow.png')

block_sprite = pygame.sprite.Sprite()
board_sprite = pygame.sprite.Sprite()

town_sprite = pygame.sprite.Sprite()
town_sprite.image = fun.load_image('town.png')

main_town_sprite = pygame.sprite.Sprite()
main_town_sprite.image = fun.load_image('main_town.png')

redblock = pygame.sprite.Sprite()
redblock.image = fun.load_image('redblock.png')

blueblock = pygame.sprite.Sprite()
blueblock.image = fun.load_image('blueblock.png')

yellowblock = pygame.sprite.Sprite()
yellowblock.image = fun.load_image('yellowblock.png')

greenblock = pygame.sprite.Sprite()
greenblock.image = fun.load_image('greenblock.png')

newturnanim = [pygame.image.load('data/animations/NewTurnAnim/anim_1.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_2.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_3.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_4.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_5.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_6.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_7.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_8.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_9.png'),
               pygame.image.load('data/animations/NewTurnAnim/anim_10.png')]

lvl_1_2 = pygame.sprite.Sprite()
lvl_1_3 = pygame.sprite.Sprite()
lvl_1_4 = pygame.sprite.Sprite()
lvl_2_2 = pygame.sprite.Sprite()
lvl_2_3 = pygame.sprite.Sprite()
lvl_2_4 = pygame.sprite.Sprite()

lvl_1_2.image = pygame.image.load('data/levels/lvlpreview/lvl_1_2.png')
lvl_1_3.image = pygame.image.load('data/levels/lvlpreview/lvl_1_3.png')
lvl_1_4.image = pygame.image.load('data/levels/lvlpreview/lvl_1_4.png')
lvl_2_2.image = pygame.image.load('data/levels/lvlpreview/lvl_2_2.png')
lvl_2_3.image = pygame.image.load('data/levels/lvlpreview/lvl_2_3.png')
lvl_2_4.image = pygame.image.load('data/levels/lvlpreview/lvl_2_4.png')

lvl_1_2.text = 'data/levels/lvl_1_2.txt'
lvl_1_3.text = 'data/levels/lvl_1_3.txt'
lvl_1_4.text = 'data/levels/lvl_1_4.txt'
lvl_2_2.text = 'data/levels/lvl_2_2.txt'
lvl_2_3.text = 'data/levels/lvl_2_3.txt'
lvl_2_4.text = 'data/levels/lvl_2_4.txt'

levels = [lvl_1_2, lvl_1_3, lvl_1_4, lvl_2_2, lvl_2_3, lvl_2_4]

click = pygame.mixer.Sound('data/sound/oneshots/click.wav')
shot = pygame.mixer.Sound('data/sound/oneshots/shot.wav')
newturn = pygame.mixer.Sound('data/sound/oneshots/newturn.wav')
