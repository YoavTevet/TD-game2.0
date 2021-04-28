import pygame


class Bullet:

    def __init__(self, x, y, xvel=-5, yvel=0, power=1, max_distance=80):
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.distance = 0
        self.max_distance = max_distance
        self.power = power
        self.rect = pygame.Rect(self.x, self.y, 4, 4)
