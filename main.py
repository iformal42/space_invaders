import asyncio
import sys
import pygame as pg
import random as rd
import time

from os import path
def newPath(relPath: str):
    return path.join(path.abspath(""), relPath)

"""Note: All the classes is in main.py no need import any other file


"""

# friends_list = [f"frends/a{image}.png" for image in range(1, 3)]
# print(friends_list)
img_path = newPath("img/")
sound_path = newPath("sfx/")
ICON = pg.image.load(f"{img_path}space-game.png")
BACKGROUND = pg.image.load(f"{img_path}space1.png")
SPACE_SHIP = f"{img_path}spaceship.png"
ENEMY = f"{img_path}alien.png"
shoot = False
is_boundary_cross = False
enemy_speed = 2.0
enemy_count = 6


class Enemy(object):
    def __init__(self, img, screen):
        self.enemy = pg.image.load(img).convert_alpha()
        self.window = screen
        self.rect_1 = self.enemy.get_rect()
        self.rect_1.width, self.rect_1.height = 40, 55
        self.enemy_list = []
        self.enemy_x_list = []
        self.enemy_y_list = []
        self.enemy_direction = []
        self.enemy_rect = []

    def appear(self, x, y):
        # pg.draw.rect(self.window, (255, 0, 0), self.rect_1)
        self.window.blit(self.enemy, (x - 10, y - 5))
        self.rect_1.x = x
        self.rect_1.y = y

    # def cooked_enemy(self,list1,list2,list3,list4,list5):


ORIGIN = (368, 820)
b_position = (-20, 0)
# b = pg.image.load("space1.png")
BULLET = pg.image.load(f"{img_path}bullet.png")


class Player(object):
    def __init__(self, img, screen, position=ORIGIN):
        self.x = position[0]
        self.y = position[1]
        self.player = pg.image.load(img)
        self.window = screen
        self.rect_1 = self.player.get_rect()
        self.rect_2 = BULLET.get_rect()
        self.rect_2.width, self.rect_2.height = 10, 30
        self.window.blit(self.player, (self.x, self.y))

    def appear(self):
        self.rect_1.x, self.rect_1.y = self.x, self.y
        # pg.draw.rect(self.window, (255, 0, 0), self.rect_1)
        self.window.blit(self.player, (self.x, self.y))

    def move(self):

        self.window.blit(self.player, (self.x, self.y))

    def move_left(self):
        if self.x >= 22:
            self.x -= 15
            self.move()

    def move_right(self):
        if self.x <= 725:
            self.x += 15
            self.move()

    def move_down(self):
        if self.y <= 858:
            self.y += 15
            self.move()

    def move_up(self):
        if self.y >= 22:
            self.y -= 15
            self.move()

    def fire(self, x, y):
        # pg.draw.circle(self.window, (255, 0, 0), self.rect_2.center, 5)
        # pg.draw.rect(self.window, (255, 0, 0), self.rect_2)
        self.window.blit(BULLET, (x + 19, y))
        self.rect_2.x = x + 30
        self.rect_2.y = y
        self.window.blit(self.player, (self.x, self.y))


class Explosion(pg.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.is_done = True
        self.window = screen
        self.sprites = []
        self.index = 0
        for im in range(1, 6):
            img = pg.image.load(f"./img/explosion/exp{im}.png")
            self.sprites.append(img)
        self.rect = self.sprites[self.index].get_rect()
        self.animation = 0

    def u(self):

        self.animation += 0.15
        self.index = int(self.animation)
        if self.index >= len(self.sprites) - 1:
            self.kill()
            self.index = 0
            self.animation = 0
            self.is_done = False
        else:
            self.window.blit(self.sprites[self.index], self.rect)


class Board:
    def __init__(self, screen, font="freesansbold.ttf"):
        with open(newPath("highscore.txt")) as s:
            self.high_score = int(s.read())
        self.font_style = font
        self.window = screen

    def show_score(self, size: int, msg: str, color: tuple, pos: tuple):
        """color should be rgb"""
        font = pg.font.Font(self.font_style, size)
        text = f"{msg}| Highest: {self.high_score}"
        score_board = font.render(text, True, color)
        self.window.blit(score_board, pos)

    def reset_board(self, score: int):
        """update board if highest score achieved"""
        if score > self.high_score:
            self.high_score = score
            print("HIGHEST SCORE HAS BEEN ACHIEVED", self.high_score)
            with open("highscore.txt", "w") as s:
                highest = s.write(str(self.high_score))

    def game_over(self, size: int, color: tuple, pos: tuple, msg: str = "GAME OVER"):
        """game over text"""
        g_font = pg.font.Font(self.font_style, size)
        score_board = g_font.render(msg, True, color)
        self.window.blit(score_board, pos)


async def main():
    global enemy_count, shoot, enemy_speed, is_boundary_cross

    def enemy_pos():
        new_y = rd.randint(10, 200)
        new_x = rd.randint(200, 700)
        return new_x, new_y

    def cook_enemy(count):
        for _ in range(count):
            enemy = Enemy(img=ENEMY, screen=window)  # rd.choice(friends_list)#ENEMY
            enemy_list.append(enemy)
            x, y = enemy_pos()
            enemy_x_list.append(x)
            enemy_y_list.append(y)
            enemy_direction.append(-1)
            enemy_rect.append(enemy.rect_1)

    # initialize the pygame
    pg.init()

    if sys.platform == 'emscripten':
        pg.mixer.SoundPatch()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((800, 920))  # , pg.FULLSCREEN | pg.SCALED)

    # background music
    pg.mixer.music.load(f'{sound_path}backgroundmusic.mp3')
    pg.mixer.music.play(-1)

    # sounds
    bullet_sound = pg.mixer.Sound(f"{sound_path}bullet_sound.mp3")
    destroy_sound = pg.mixer.Sound(f"{sound_path}destroy_sound.mp3")
    enemy_destroy = pg.mixer.Sound(f"{sound_path}enemy_destroy.mp3")

    # window icon and title
    pg.display.set_icon(ICON)
    pg.display.set_caption("viman tod")

    # window filling color
    window.blit(BACKGROUND, (-20, 0))

    # adding player object
    player = Player(SPACE_SHIP, window)

    # controlling bullet
    bullet_y = player.rect_2.y
    bullet_x = player.rect_2.x
    # is_bullet_disappear = True

    # controlling enemy
    # adding enemy object
    enemy_list = []
    enemy_x_list = []
    enemy_y_list = []
    enemy_direction = []
    enemy_rect = []
    cook_enemy(enemy_count)

    explode = Explosion(window)
    blast = False
    # board
    board = Board(screen=window)
    score = 0
    running = True

    while running:

        # 60 FPS
        clock.tick(60)
        window.fill(color=(255, 0, 0))
        window.blit(BACKGROUND, (-20, 0))
        for i in pg.event.get():
            # stop condition
            if i.type is pg.QUIT:
                running = False
            # moving player
            pressed = pg.key.get_pressed()

            if pressed[pg.K_d] or pressed[pg.K_RIGHT]:
                player.move_right()
            if pressed[pg.K_a] or pressed[pg.K_LEFT]:
                player.move_left()
            if pressed[pg.K_w] or pressed[pg.K_UP]:
                player.move_up()
            if pressed[pg.K_s] or pressed[pg.K_DOWN]:
                player.move_down()
            if pressed[pg.K_SPACE]:
                """command to fire a bullet"""
                if not shoot:
                    bullet_sound.play()
                    bullet_x = player.x
                    bullet_y = player.y
                    shoot = True
        # firing a bullet
        if shoot:
            bullet_y -= 10
            player.fire(bullet_x, bullet_y)
            if bullet_y <= -35:
                player.rect_2.y = player.y
                player.rect_2.x = player.x
                shoot = False

        # moving  multiple enemies on screen
        for i in range(enemy_count):
            enemy_x = enemy_x_list[i]
            enemy_y = enemy_y_list[i]
            if enemy_x <= 20 or enemy_x >= 720:
                enemy_direction[i] *= -1
                enemy_y_list[i] += 35

            enemy_x_list[i] += enemy_speed * enemy_direction[i]
            enemy_list[i].appear(enemy_x_list[i], enemy_y_list[i])
            if enemy_y >= 910:
                is_boundary_cross = True

        # checking collision of bullet and enemy and making position of both default state
        n = player.rect_2.collidelist(enemy_rect)
        if n >= 0:
            blast = True
            explode.is_done = True
            pos = (enemy_x_list[n], enemy_y_list[n])
            explode.rect.x, explode.rect.y = pos
            enemy_destroy.play()
            player.rect_2.x = player.x
            player.rect_2.y = player.y
            shoot = False
            enemy_x_list[n] = rd.randint(200, 700)
            enemy_y_list[n] = rd.randint(10, 200)
            enemy_list[n].appear(enemy_x_list[n], enemy_y_list[n])
            # increasing score
            score += 1

            # increasing enemy
            if score % 10 == 0:
                enemy_count += 1
                cook_enemy(1)

            # increasing enemy speed
            if score % 5 == 0 and enemy_speed <= 10:
                enemy_speed *= 1.1

        if blast:
            explode.u()
            blast = explode.is_done

        # game over condition
        if player.rect_1.collidelist(enemy_rect) >= 0 or is_boundary_cross:
            destroy_sound.play()
            board.game_over(70, (255, 255, 255), (200, 380))
            time.sleep(4)
            break

        # showing score board
        board.show_score(32, f"score: {score}", (255, 255, 255), (10, 10))
        player.appear()
        pg.display.update()
        await asyncio.sleep(0)

    board.reset_board(score)
    pg.quit()


asyncio.run(main())

# richmond kleinson was here lol