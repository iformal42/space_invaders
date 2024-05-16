import pygame as pg
img_path = "./img/"
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
