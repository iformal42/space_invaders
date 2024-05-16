import pygame as pg



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
