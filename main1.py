import copy
import random
import sys


import pygame
from board import BOARD

pygame.init()
size = width, height = 700, 600
screen = pygame.display.set_mode(size)

arial_font = pygame.font.match_font('arial')
arial_font_48 = pygame.font.Font(arial_font, 30)

fight_off = 0

# рекорд
record = 0

pygame.mixer.music.load('data/music.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)


class Game:
    def __init__(self, ):
        self.fight_off = 0
        self.game_over = False
        self.win = False
        self.speed = 8

        self.radius = 5
        self.ball_rect = pygame.rect.Rect(width / 2 - self.radius, height / 2 - self.radius, self.radius * 2,
                                          self.radius * 2)
        self.ball_speed = 3
        self.ball_speed_x = 0
        self.ball_speed_y = 3
        self.ball_beat_first = False

        self.platform_width, self.platform_height = 70, 10
        self.platform_rect = pygame.rect.Rect(width / 2 - self.platform_width, height - self.platform_height * 2 - 50,
                                              self.platform_width, self.platform_height)

        self.lose_area = pygame.rect.Rect(0, height - 5, width, 5)

        self.width = 80
        self.height = 25
        self.left = 0
        self.top = 25
        self.cell_size = 10
        self.objects = list()
        arr = list()
        for i in range(self.height):
            for j in range(self.width):
                arr.append(
                    pygame.rect.Rect((self.left + self.cell_size * j, self.top + self.cell_size * i,
                                      self.cell_size, self.cell_size)))
            self.objects.append(arr.copy())
            arr.clear()

        self.board = copy.deepcopy(BOARD)

    def update(self, screen):
        global fight_off
        if not self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.platform_rect.x < width - self.platform_width:
                self.platform_rect.x += self.speed
            elif keys[pygame.K_LEFT] and self.platform_rect.x > 0:
                self.platform_rect.x -= self.speed

            if self.platform_rect.colliderect(self.ball_rect):
                if not self.ball_beat_first:
                    if random.randint(0, 1) == 0:
                        self.ball_speed_x = self.ball_speed
                    else:
                        self.ball_speed_x = - self.ball_speed
                    self.ball_beat_first = True
                self.ball_speed_y = - self.ball_speed

            pygame.draw.rect(screen, (255, 255, 255), self.platform_rect)

        self.ball_rect.x += self.ball_speed_x
        self.ball_rect.y += self.ball_speed_y
        if self.ball_rect.bottom >= height:
            self.game_over = True
            self.ball_speed_y = - self.ball_speed
        elif self.ball_rect.top <= 0:
            self.ball_speed_y = self.ball_speed
        elif self.ball_rect.left <= 0:
            self.ball_speed_x = self.ball_speed
        elif self.ball_rect.right >= width:
            self.ball_speed_x = - self.ball_speed

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    if self.objects[i][j].colliderect(self.ball_rect):
                        self.ball_speed_y = - self.ball_speed_y
                        fight_off += 10
                        self.board[i][j] = 1

        pygame.draw.circle(screen, (255, 255, 255), self.ball_rect.center, self.radius)
        pygame.draw.rect(screen, (250, 40, 40), self.lose_area)

        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] == 0:
                    pygame.draw.rect(screen, (255, 255, 255), (
                        self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size,
                        self.cell_size))
        counter = 0
        for elem in self.board:
            if not all(elem):
                counter += 1
        if counter == len(self.board):
            self.win = True


class Menu:
    def __init__(self, punkts):
        self.punkts = punkts

    def render(self, cover, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                cover.blit(font.render(i[2], 1, i[4]), (i[0], i[1]))
            else:
                cover.blit(font.render(i[2], 1, i[3]), (i[0], i[1]))

    def menu(self):
        done = True
        font_menu = pygame.font.Font(arial_font, 70)
        punkt = 0
        while done:
            screen.fill((0, 100, 200))

            self.render(screen, font_menu, punkt)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if punkt > 0:
                            punkt -= 1
                    if event.key == pygame.K_DOWN:
                        if punkt < len(self.punkts) - 1:
                            punkt += 1
                    if event.key == pygame.K_SPACE:
                        if punkt == 0:
                            done = False

            screen.blit(screen, (0, 0))
            pygame.display.flip()


class GameOver(pygame.sprite.Sprite):
    image = pygame.image.load("data/gameover.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = GameOver.image
        self.rect = self.image.get_rect()
        self.rect.x = - width
        self.rect.y = (height - self.image.get_height()) // 2
        self.pos_x = - width

    def move(self, coordinate):
        self.pos_x += coordinate
        self.rect.x = self.pos_x

    def print_res(self):
        game_over_text_res = arial_font_48.render(f'Your earned points: {fight_off}', True, (255, 255, 255))
        screen.blit(game_over_text_res, [width / 2 - game_over_text_res.get_width() / 2, height / 3 + 20])


class Home(GameOver):
    image = pygame.image.load('data/home.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Home.image
        self.rect = self.image.get_rect()
        self.rect.y = (height // 2 - self.image.get_height()) // 2

    def move(self, coordinate):
        super().move(coordinate)


class Restart(GameOver):
    image = pygame.image.load('data/restart.png')

    def __init__(self, group):
        super().__init__(group)
        self.image = Restart.image
        self.rect = self.image.get_rect()
        self.rect.y = height // 2 + (height // 2 - self.image.get_height()) // 2

    def move(self, coordinate):
        super().move(coordinate)


def main():
    global fight_off
    pygame.display.set_caption('Game')
    pygame.mouse.set_visible(False)

    # Иницаилазайия класса Punkts:
    punkts = [(width / 2 - 70, height / 2 - 70, 'Play', (8, 7, 7), (217, 206, 206), 0),
              (width / 2 - 110, height / 2, 'Records', (8, 7, 7), (217, 206, 206), 1)]
    begin_frame = Menu(punkts)
    begin_frame.menu()

    sprite_game_over = pygame.sprite.Group()
    gameover = GameOver(sprite_game_over)

    sprite_home = pygame.sprite.Group()
    home = Home(sprite_home)

    sprite_restart = pygame.sprite.Group()
    restart = Restart(sprite_restart)

    game = Game()

    bg_color = (0, 0, 0)
    game_over_color = (0, 0, 100)
    fps = 60
    pps = 250
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and game.game_over:
                if home.rect.x <= event.pos[0] <= home.rect.x + home.rect.width and home.rect.y <= event.pos[1] \
                        <= home.rect.y + home.rect.height:
                    punkts = [(width / 2 - 70, height / 2 - 70, 'Play', (8, 7, 7), (217, 206, 206), 0),
                              (width / 2 - 110, height / 2, 'Records', (8, 7, 7), (217, 206, 206), 1)]
                    begin_frame = Menu(punkts)
                    begin_frame.menu()
                    sprite_game_over = pygame.sprite.Group()
                    gameover = GameOver(sprite_game_over)
                    sprite_home = pygame.sprite.Group()
                    home = Home(sprite_home)

                    sprite_restart = pygame.sprite.Group()
                    restart = Restart(sprite_restart)
                    game = Game()
                    pygame.mouse.set_visible(False)
                    fight_off = 0
                if restart.rect.x <= event.pos[0] <= restart.rect.x + restart.rect.width and restart.rect.y <= \
                        event.pos[1] <= restart.rect.y + restart.rect.height:
                    sprite_game_over = pygame.sprite.Group()
                    gameover = GameOver(sprite_game_over)

                    sprite_home = pygame.sprite.Group()
                    home = Home(sprite_home)

                    sprite_restart = pygame.sprite.Group()
                    restart = Restart(sprite_restart)

                    game = Game()
                    pygame.mouse.set_visible(False)
                    fight_off = 0

        if game.game_over:
            screen.fill(game_over_color)
            sprite_game_over.draw(screen)
            sprite_home.draw(screen)
            sprite_restart.draw(screen)
            if gameover.rect.x < (width - gameover.rect.width) / 2:
                gameover.move(pps / fps)
            if home.rect.x < (width - home.rect.width) / 2:
                home.move(pps / fps)
            if restart.rect.x < (width - restart.rect.width) / 2:
                restart.move(pps / fps)
            gameover.print_res()
            pygame.mouse.set_visible(True)
        else:
            screen.fill(bg_color)
            game.update(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
