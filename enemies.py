import pygame
import os

current_path = os.path.dirname(__file__)
img = [pygame.image.load(os.path.join(current_path, f"R{i}.png")) for i in range(1, 10)]


class Enemy:

    def __init__(self, x, y, health, vel):
        self.x = x
        self.y = y
        self.health = health
        self.original_health = health
        self.vel = vel
        self.rect = pygame.Rect((self.x + 18, self.y + 14, img[0].get_width() / 2.4, img[0].get_height() - 14))
        self.pics = img
        self.walk_count = 0
        self.width = img[0].get_width() / 2.6 + 18
        self.height = img[0].get_height() - 14

    def walk(self):
        # the self.rect has to be updated manually all the time.
        self.rect = pygame.Rect((self.x + 18, self.y + 14, img[0].get_width() / 2.6, img[0].get_height() - 14))

        # way to first corner
        if self.rect.right <= 110 and self.rect.top > 160:
            self.x += self.vel

        # way to second corner
        if 120 > self.rect.right > 110 and self.y > 55:
            self.y -= self.vel  # subtracting from y because that way you go up.

        # way to third corner
        if self.rect.right < 230 and 55 - self.vel < self.y < 55 + self.vel:
            self.x += self.vel

        # way to fourth corner
        if 230 + self.vel >= self.rect.right >= 230 and self.rect.bottom < 270:
            self.y += self.vel  # increasing y value makes character move down

        # way to fifth corner
        if self.rect.bottom >= 270 and self.rect.right < 390:
            self.x += self.vel

        # way to sixth corner
        if self.rect.right >= 390 and self.rect.bottom > 200:
            self.y -= self.vel  # decreasing y value means you are gong up.

        # way to the end.
        if self.rect.right >= 390 and 200 - self.vel < self.rect.bottom < 200 + self.vel:
            self.x += self.vel
