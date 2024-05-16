import pygame as pg


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


if __name__ == "__main__":
    pg.init()

    clock = pg.time.Clock()

    # window
    window = pg.display.set_mode((800, 920))
    exp = Explosion(window)
    img = pg.image.load(f"explosion/exp1.png")
    running = True
    animate = False
    while running:
        # 60 FPS
        window.fill((20, 255, 40))
        clock.tick(60)
        for i in pg.event.get():
            # stop condition
            if i.type is pg.QUIT:
                running = False
            pressed = pg.key.get_pressed()

            if i.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                exp.rect.x, exp.rect.y = pos
                animate = True
                exp.is_done = True

                print(pos)

        if animate:
            exp.u()
            animate = exp.is_done

        pg.display.update()
