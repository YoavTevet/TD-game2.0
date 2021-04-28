import pygame
import sys
import os
from enemies import Enemy
from defenses import Tank, TackShooter

pygame.init()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

current_path = os.path.dirname(__file__)
DISPLAY_SIZE = (600, 400)
screen = pygame.display.set_mode(DISPLAY_SIZE)  # main picture to have everything painted to.
background = pygame.image.load(os.path.join(current_path, 'background.jpg'))
font = pygame.font.SysFont('arial', 18, True)
clock = pygame.time.Clock()
pygame.display.set_caption("Tower Defense Game 2.0")
tank_icon = pygame.image.load(os.path.join(current_path, "tank_pic.png"))
tank_icon_nobg = pygame.image.load(os.path.join(current_path, "tank.png"))  # just like prev one with no background
tank_icon_rect = pygame.Rect(80, 350, tank_icon.get_width(), tank_icon.get_height())
tack_icon = pygame.image.load(os.path.join(current_path, "tack_shooter.png"))
tack_icon_red = pygame.image.load(os.path.join(current_path, "tack_shooter_red.png"))
tack_icon_rect = pygame.Rect(180, 350, tack_icon.get_width(), tack_icon.get_height())

mouse_rect = pygame.Rect((0, 0), (5, 5))
road_rectangles = [pygame.Rect((0, 200, 118, 35)),  # blocks on the way so you can't place towers on them.
                   pygame.Rect((80, 82, 32, 118)),
                   pygame.Rect((118, 82, 120, 38)),
                   pygame.Rect((200, 120, 39, 155)),
                   pygame.Rect((238, 240, 161, 36)),
                   pygame.Rect((360, 160, 38, 80)),
                   pygame.Rect((398, 160, 202, 38))]


def redraw_game_window():  # draws everything to the screen after their properties are changed
    screen.blit(background, (0, 0))  # background has to be redrawn to clear everything, then all is redrawn onto it.
    for enemy in hostiles:
        screen.blit(enemy.pics[enemy.walk_count // 3], (enemy.x, enemy.y))

    # mouse location
    mouse_pos = font.render('{}'.format(pygame.mouse.get_pos()), True, red)
    screen.blit(mouse_pos, (20, 20))

    # purchase button for tanks, red background and tank picture
    pygame.draw.rect(screen, red, (tank_icon_rect.x - 5, tank_icon_rect.y - 5,
                                   tank_icon.get_width() + 10, tank_icon.get_height() + 10))
    screen.blit(tank_icon, (tank_icon_rect.x, tank_icon_rect.y))
    screen.blit(tack_icon, (tack_icon_rect.x, tack_icon_rect.y))

    for tower in buildings:
        screen.blit(tower.pic, (tower.x, tower.y))

        # draws the tower's bullets
        for b in tower.bullets:
            pygame.draw.rect(screen, yellow, b.rect)

    if picked_tank:
        if red_bg:
            pygame.draw.rect(screen, red, (mouse_rect.x, mouse_rect.y, tank_icon.get_width(), tank_icon.get_height(),))
        else:
            pygame.draw.rect(screen, green,
                             (mouse_rect.x, mouse_rect.y, tank_icon.get_width(), tank_icon.get_height(),))
        screen.blit(tank_icon_nobg, (mouse_rect.x, mouse_rect.y))

    if picked_tack:
        if red_bg:
            screen.blit(tack_icon_red, (mouse_rect.x, mouse_rect.y))
        else:
            screen.blit(tack_icon, (mouse_rect.x, mouse_rect.y))


shoot_count = 0
speed = 1  # increased for speed motion.
hostiles = [Enemy(-30, 170, 1, 1), Enemy(70, 170, 7, 1)]
buildings = [Tank(400, 230), TackShooter(130, 140)]
picked_tank = False
picked_tack = False
mouse_counter = 0
red_bg = False  # red background if can't place defenses, else green
while True:
    clock.tick(60 * speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if X button is pressed on the app
            pygame.quit()
            sys.exit()

    mouse_rect.left, mouse_rect.top = pygame.mouse.get_pos()  # updates mouse location
    # makes sure users don't click 2234987 times per second
    can_click = False
    mouse_counter += 1
    if mouse_counter > 6:
        can_click = True

    if pygame.mouse.get_pressed(num_buttons=3)[0]:
        mouse_counter = 0

    # all actions done on the hostiles
    for char in hostiles:
        # walking animation
        char.walk()
        if char.walk_count >= 26:
            char.walk_count = 0
        else:
            char.walk_count += 1

        # looping through the buildings because the bullets are stored in their classes.
        for building in buildings:
            for bullet in building.bullets:
                # decreases character's health
                if bullet.rect.colliderect(char.rect):
                    char.health -= bullet.power
                    # keeps bullets that can deal more damage (after power reduction), gets rid of the others.
                    if bullet.power > char.health:
                        bullet.power -= char.health
                    else:
                        building.bullets.remove(bullet)

        # removes characters that are out of health
        if char.health < 1:
            hostiles.remove(char)
            print("character killed")  # just a check up

        # removes characters that have left the screen.
        if char.rect.left > DISPLAY_SIZE[0]:
            hostiles.remove(char)
            print("character removed")

    # all actions done on defenses
    for defence in buildings:
        # the lower the shoot_num is the more often the defense will shoot.
        if defence.shoot_count >= defence.shoot_num:
            defence.shoot()
            defence.shoot_count = 0
        else:
            defence.shoot_count += 1

        defence.move_bullets()

    # mechanism for placing a tank
    if not picked_tank:
        if mouse_rect.colliderect(tank_icon_rect) and pygame.mouse.get_pressed(num_buttons=3)[0]:
            picked_tank = True
            picked_tack = False
    else:
        picture_rectangle = pygame.Rect(mouse_rect.x, mouse_rect.y, tank_icon.get_width(), tank_icon.get_height())
        can_place = True
        red_bg = True
        # if tank is touching the road
        if picture_rectangle.colliderect(tank_icon_rect) or picture_rectangle.colliderect(tack_icon_rect):
            can_place = False

        if can_place:
            for block in road_rectangles:
                if block.colliderect(picture_rectangle):
                    can_place = False
                    break

        # only checks for collisions with other defenses if not colliding with the road.
        if can_place:
            for defense in buildings:
                if defense.rect.colliderect(picture_rectangle):
                    can_place = False
                    break

        if can_place:
            red_bg = False

        # actual placement of the tank
        if pygame.mouse.get_pressed(num_buttons=3)[0] and can_click:
            if can_place:
                picked_tank = False
                buildings.append(Tank(mouse_rect.left, mouse_rect.top))

    # mechanism to pick up and place a tack shooter.
    if not picked_tack:
        if mouse_rect.colliderect(tack_icon_rect) and can_click and pygame.mouse.get_pressed(num_buttons=3)[0]:
            picked_tack = True
            picked_tank = False
    else:
        picture_rectangle = pygame.Rect(mouse_rect.x, mouse_rect.y, tack_icon.get_width(), tack_icon.get_height())
        can_place = True
        red_bg = True

        # checks for collision with the icon
        if picture_rectangle.colliderect(tack_icon_rect) or picture_rectangle.colliderect(tank_icon_rect):
            can_place = False

        # checks for collision with the road
        if can_place:
            for block in road_rectangles:
                if block.colliderect(picture_rectangle):
                    can_place = False
                    break

        # checks for collisions with other buildings
        if can_place:
            for defense in buildings:
                if defense.rect.colliderect(picture_rectangle):
                    can_place = False
                    break

        if can_place:
            red_bg = False

        # actual placement of the tack shooter
        if pygame.mouse.get_pressed(num_buttons=3)[0] and can_click:
            if can_place:
                picked_tack = False
                buildings.append(TackShooter(mouse_rect.left, mouse_rect.top))

    # left click to take it back and not place a defense.
    if pygame.mouse.get_pressed(num_buttons=3)[2]:
        picked_tank = False
        picked_tack = False

    redraw_game_window()
    pygame.display.update()
