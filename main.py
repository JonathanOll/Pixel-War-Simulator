import pygame
import sys
from time import time
from options import *
from game import Game
import math


# setup
pygame.init()
clock = pygame.time.Clock()
start_time = time()
clock = pygame.time.Clock()
last_ranking_update = 0

# screen
screen = pygame.display.set_mode((screen_width, screen_height))

# game
game = Game((50, 50), [])
game.load("maps/Europe.sav")
# game.load("maps/Europe.sav")

cases = sum(i.count for i in game.teams)
ranking = []
ranking.extend(game.teams)
count = 0

selected_team = 0
pen_size = 5


def update_ranking():
    global count

    ranking.sort(key=lambda a: -a.count)
    count = 0
    for i in game.teams:
        if i.count != 0: count += 1

def draw(screen):
    if show_interface:

        pygame.draw.rect(screen, game.teams[selected_team - 1].color if selected_team > 0 else empty_ground_color, (10, 10, 25, 25))
        screen.blit(font.render(game.teams[selected_team - 1].name if selected_team > 0 else "Neutre", True, (255, 255, 255)), (40, 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        x = round((mouse_x - (screen_width // 2 - math.ceil(map_height / len(game.map)) * len(game.map[0]) // 2)) / (math.ceil(map_height / len(game.map))))
        y = round((mouse_y - (screen_height // 2 - map_height // 2)) / (math.ceil(map_height / len(game.map))))
        
        if game.is_valid(x, y) and game.get(x, y) != -1:
            screen.blit(font.render(game.teams[game.map[y][x] - 1].name if game.get(x, y) - 1 < len(game.teams) else "", True, (255, 255, 255)), (mouse_x + 10, mouse_y + 10))

        for i, team in enumerate(ranking[:10]):
            percent = round(team.count / game.total * 100, 2)
            if percent > 0:
                pygame.draw.rect(screen, team.color, (10, 100 + 25 * i, 5 + 255 * percent / 100, 20))
                screen.blit(small_font.render(team.name + " : " + str(percent) + "%", True, (255, 255, 255)), (10, 102 + 25 * i))

        screen.blit(small_font.render((" + " + str(count - 10) + " autres") if count - 10 > 0 else "", True, (255, 255, 255)), (10, 102 + 25 * 10))


# GAME LOOP
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game.resume()
            elif event.key == pygame.K_s:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    game.save("maps/" + str(int(time())) + ".sav")
            elif event.key == pygame.K_LEFT:
                selected_team = (selected_team - 1)
                if selected_team < 0 : selected_team += (len(game.teams) + 1)
            elif event.key == pygame.K_RIGHT:
                selected_team = (selected_team + 1) % (len(game.teams) + 1)
            elif event.key == pygame.K_c:
                print(count)
            elif event.key == pygame.K_p:
                show_interface = not show_interface
        if (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) or (event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            x = round((mouse_x - (screen_width // 2 - math.ceil(map_height / len(game.map)) * len(game.map[0]) // 2)) / (math.ceil(map_height / len(game.map))))
            y = round((mouse_y - (screen_height // 2 - map_height // 2)) / (math.ceil(map_height / len(game.map))))
            if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                print((x, y))
            elif pygame.key.get_pressed()[pygame.K_LCTRL]:
                selected_team  = game.map[y][x]
            else:
                if pen_size > 1:
                    for i in range(-pen_size, pen_size + 1):
                        for j in range(-pen_size**2, pen_size**2 + 1):
                            if i*i + j*j < pen_size ** 2 and game.is_valid(x+j, y+i) and game.map[y+i][x+j] != -1:
                                game.map[y+i][x+j] = selected_team
                else:
                    if game.is_valid(x, y) and game.map[y][x] != -1:
                        game.map[y][x] = selected_team
            game.update_counts()
        elif event.type == pygame.MOUSEWHEEL:
            pen_size += event.y
            if pen_size < 1 : pen_size = 1
    
    game.update()
    if time() - last_ranking_update > 1:
        update_ranking()
        last_ranking_update = time()

    screen.fill((0, 0, 0))
    game.draw(screen)
    draw(screen)

    pygame.display.flip()