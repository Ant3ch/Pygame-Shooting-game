import pygame, sys, random, os
from pygame.locals import *

os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

WIDTH, HEIGHT = 800, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
counter = 0
clock = pygame.time.Clock()


class Timer():
    def __init__(self):
        self.time = 5
        self.counter = 0
        self.default = self.time

    def cont(self):
        self.counter += 1
        if self.counter == 144:
            self.counter = 0
            self.time -= 1

        if self.time == 0:
            self.reset()
            game_state.state = "result"

        pygame.font.init()
        font = pygame.font.SysFont("Arial", 40)
        timer_text = font.render(str(self.time), True, (255, 255, 255))
        win.blit(timer_text, (WIDTH / 2, 1 / 20 * HEIGHT))

    def reset(self):
        self.time = self.default
        self.counter = 0


class Cible():
    def __init__(self):
        self.cibles_size = 50
        self.cible_coordx = random.randint(0, WIDTH)
        self.cible_coordy = random.randint(0, HEIGHT)
        self.cible = pygame.Rect(self.cible_coordx - self.cibles_size, self.cible_coordy - self.cibles_size,
                                 self.cibles_size, self.cibles_size)
        self.cibles2_size = 40
        self.cible2 = pygame.Rect(self.cible_coordx - self.cibles_size * (1 - 5 / self.cibles_size),
                                  self.cible_coordy - self.cibles_size * (1 - 5 / self.cibles_size), self.cibles2_size,
                                  self.cibles2_size)

    def spawn(self):
        pygame.draw.ellipse(win, (200, 0, 0), self.cible)
        pygame.draw.ellipse(win, (0, 0, 200), self.cible2)

    def random(self):
        self.cible_coordx = random.randint(0, WIDTH - self.cibles_size)
        self.cible_coordy = random.randint(0, HEIGHT - self.cibles_size)
        self.cible = pygame.Rect(self.cible_coordx - self.cibles_size, self.cible_coordy - self.cibles_size,
                                 self.cibles_size, self.cibles_size)
        self.cible2 = pygame.Rect(self.cible_coordx - self.cibles_size * (1 - 5 / self.cibles_size),
                                  self.cible_coordy - self.cibles_size * (1 - 5 / self.cibles_size), self.cibles2_size,
                                  self.cibles2_size)


class Cursor():
    def __init__(self):
        self.cursor = pygame.Rect(0 - 5, 0 - 5, 10, 10)
        self.cursor_color = (0, 0, 0)
        self.shoot_number = 0
        self.shoot_touch = 0
        self.shoot_miss = 0

    def move(self):
        pygame.mouse.set_visible(0)
        mouse_pos = pygame.mouse.get_pos()
        pygame.event.set_grab(1)
        # set the cursor pos with .x and .y arg
        self.cursor.x = mouse_pos[0] - 5  # to center
        self.cursor.y = mouse_pos[1] - 5
        # visual

        pygame.draw.ellipse(win, self.cursor_color, self.cursor)

    def shoot(self):
        if not game_state.not_in_menu:
            self.shoot_number += 1
        print('shoot')  # just simple print


class GameState():
    def __init__(self):
        self.state = 'intro'
        self.fullscreen_text_size_modifier = 1
        self.not_in_menu = True

    def menu(self):

        for event in pygame.event.get():
            # visual
            win.fill((200, 200, 200))
            pygame.font.init()
            font = pygame.font.SysFont('Arial', size=60 + self.fullscreen_text_size_modifier)
            intro_text = font.render("Shoot me to play !", True, (10, 10, 10))
            text_rect = intro_text.get_rect()

            text_rect.x = WIDTH / 2 - 150 - 30 - self.fullscreen_text_size_modifier
            text_rect.y = HEIGHT / 2 - 120

            win.blit(intro_text, (text_rect.x, text_rect.y))

            font2 = pygame.font.SysFont('Arial', size=30 + self.fullscreen_text_size_modifier)
            intro_text2 = font2.render("Press F for full screen and R for little one", True, (10, 10, 10))
            text_rect2 = intro_text.get_rect()

            text_rect2.x = WIDTH / 2 - 150 - 30 - self.fullscreen_text_size_modifier
            text_rect2.y = HEIGHT / 2 - 120 * (1 - 70 / 100) + self.fullscreen_text_size_modifier

            win.blit(intro_text2, (text_rect2.x, text_rect2.y))

            if pygame.key.get_pressed()[K_ESCAPE] or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if left click press shoot

            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0] and pygame.Rect.colliderect(
                    cursor.cursor, text_rect):
                cursor.shoot()
                cursor.cursor_color = (255, 255, 255)
                self.state = 'main_game'

            self.fullscreen()

    def fullscreen(self):
        global WIDTH, HEIGHT
        global win

        if pygame.key.get_pressed()[K_f]:
            WIDTH, HEIGHT = 1920, 1080
            win = pygame.display.set_mode((WIDTH, HEIGHT), FULLSCREEN)
            self.fullscreen_text_size_modifier = 35

        if pygame.key.get_pressed()[K_r]:
            WIDTH, HEIGHT = 800, 800
            win = pygame.display.set_mode((WIDTH, HEIGHT))
            self.fullscreen_text_size_modifier = 1

    def main_game(self):

        for event in pygame.event.get():
            if pygame.key.get_pressed()[K_ESCAPE] or event.type == pygame.QUIT:
                self.state = "intro"



            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
                cursor.shoot()
                if pygame.Rect.colliderect(cursor.cursor, cible.cible) or pygame.Rect.colliderect(cursor.cursor,
                                                                                                  cible.cible2):
                    cible.random()
                    cursor.shoot_touch += 1


        # visual
        win.fill((0, 0, 0))
        cible.spawn()
        self.fullscreen()
        times.cont()

    def result(self):

        win.fill((100, 100, 100))
        for event in pygame.event.get():
            if pygame.key.get_pressed()[K_ESCAPE] or event.type == pygame.QUIT:
                self.state = "intro"
            if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed(3)[0]:
                cursor.shoot()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", size=70)
        miss = font.render(str(cursor.shoot_miss), True, (200, 0, 0))
        cursor.shoot_miss = cursor.shoot_number - cursor.shoot_touch # set miss
        touch = font.render(str(cursor.shoot_touch), True, (0, 200, 0))
        total_shoot = font.render(str(cursor.shoot_number), True, (0, 0, 0))
        win.blit(touch, (WIDTH/8+WIDTH/10,HEIGHT*7/9))
        win.blit(miss, (WIDTH/3+WIDTH/10,HEIGHT*7/9))
        win.blit(total_shoot, (WIDTH/3+WIDTH/4+WIDTH/10,HEIGHT*7/9))
        res_text = font.render("Result", True, (0,0,0))
        win.blit(res_text, (WIDTH/2-60, HEIGHT/2-17))
        if times.time == 1:
            seconds = " seconde"
        else:
            seconds = " secondes"

        cps = font.render("cps: " + str(cursor.shoot_number/times.time) + " in " + str(times.time) + seconds, True, (0,0,0))
        win.blit(cps, (WIDTH/2-WIDTH/3, HEIGHT/2+100))
        cursor.cursor
        cursor.cursor_color = (0, 0, 0)

        self.fullscreen()

    def reset_result(self):
        cursor.shoot_number = 0
        cursor.shoot_miss = 0
        cursor.shoot_touch = 0


    def state_manager(self):
        if self.state == "intro":
            times.reset()
            self.reset_result()
            self.menu()
            self.not_in_menu = True
        if self.state == "main_game":
            self.main_game()
            self.not_in_menu = False
        if self.state == "result":
            self.result()
            self.not_in_menu = True



times = Timer()
cursor = Cursor()
game_state = GameState()
cible = Cible()

while True:
    game_state.state_manager()  # => load the menu

    cursor.move()  # => activate cursor

    clock.tick(144)
    pygame.display.flip()
