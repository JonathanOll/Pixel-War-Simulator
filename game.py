from options import *
from random import randint
from time import time
import pygame
from PIL import Image
from numpy import asarray
import math
from pygame import transform

class Team:
    def __init__(self, name, color, power=0):
        self.name = name
        self.color = color
        self.power = power
        self.count = 0

dirs = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]

class Game:
    """
    map: tilemap
    -1: pas de terrain
    0: terrain vierge
    n > 0: n-ième équipe
    """
    def __init__(self, map_size, teams):
        self.map = [[-1] * map_size[0] for i in range(map_size[1])]
        self.teams = teams
        self.last_update = time()
        self.running = False
        self.winner = ""
        self.total = 999999
        self.power_points = []
        self.tick_count = 0

    def update_total(self):
        res = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] != -1:
                    res += 1
        self.total = res
    
    def save(self, file_path):
        file = open(file_path, "wb+")

        file.write((str(len(self.map[0])) + " " + str(len(self.map)) + "\n").encode())

        for row in self.map:

            file.write((" ".join(str(i) for i in row) + "\n").encode())

        file.write("|".encode())

        for point in self.power_points:
            file.write((str(point[0]) + "," + str(point[1])).encode())

        file.write("|".encode())

        for team in self.teams:

            file.write((team.name + "," + str(team.color[0]) + " " + str(team.color[1]) + " " + str(team.color[2]) + "," + str(team.power) + "\n").encode())

        file.close()

        print("map saved to", file_path)
    
    def load(self, file_path):
        
        self.teams.clear()

        file = open(file_path, "rb")

        s = file.read().decode()

        ints = []

        for i in s.split("\n"):
            ints.extend(i.split(" "))

        file.close()

        self.map = [[-1] * int(ints[0]) for i in range(int(ints[1]))]

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.map[y][x] = int(ints[2 + y * int(ints[0]) + x])

        points = s.split("|")[1].split("\n")

        for point in points[:-1]:
            coords = point.split(",")
            self.power_points.append((int(coords[0]), int(coords[1])))

        teams = s.split("|")[-1].split("\n")
        
        for team in teams[:-1]:
            properties = team.split(",")
            rgb = properties[1].split(" ")
            t = Team(properties[0], (int(rgb[0]), int(rgb[1]), int(rgb[2])), int(properties[2]))
            self.teams.append(t)
        
        self.update_counts()

        self.update_total()
        
        print("map loaded from", file_path)

    def load_from_img(self, file_path):

        self.teams.clear()

        matrix = asarray(Image.open(file_path))
        self.map = [[-1] * len(matrix[0]) for i in range(len(matrix))]
        teams = {}
        
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                color = (matrix[y][x][0], matrix[y][x][1], matrix[y][x][2])
                if matrix[y][x][3] == 0:
                    self.map[y][x] = -1
                elif color in teams:
                    self.map[y][x] = teams[color]
                else:
                    teams[color] = len(self.teams)
                    t = Team(str(len(self.teams)), color)
                    self.teams.append(t)
                    self.map[y][x] = teams[color]
        
        self.update_counts()
        
        self.update_total()


    def gen(self, func):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] == 0:
                    r = func(x, y)
                    self.map[y][x] = r
                    self.teams[r-1].count += 1

    def get(self, *args):  # récuperer la valeur à une position sur la map
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        try:
            return self.map[y][x]
        except:
            print(x, y, len(self.map[0]), len(self.map))

    def is_valid(self, *args):  # vérifier la validité d'une position
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        return 0 <= x < len(self.map[0]) and 0 <= y < len(self.map)

    def update_counts(self):
        for i in range(len(self.teams)):
            self.teams[i].count = 0
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                r = self.get(x, y)
                if r > 0:
                    self.teams[r - 1].count += 1

    def resume(self):
        self.update_counts()
        self.running = not self.running

    def count_around(self, *args):  # compter les forces adjacentes
        if len(args) == 1:
            x, y = args[0]
        elif len(args) == 2:
            x, y = args
        res = {}
        for dx, dy in dirs:
            pos = (x+dx, y+dy)
            if self.is_valid(pos) and self.get(pos) > 0:
                team = self.get(pos) - 1
                if team in res:
                    res[team] += force_around
                else:
                    res[team] = force_around
        if self.is_valid(x, y) and self.get(x, y) > 0:
            team = self.get(x, y) - 1
            if team in res:
                res[team] += force_on_position
            else:
                res[team] = force_on_position
        for i in res.keys():
            if res[i] != 0:
                res[i] += self.teams[i].power + round(self.teams[i].count / self.total * area_force)
        if self.tick_count >= flag_activation:
            for point in self.power_points:
                if self.get(point) - 1 in res:
                    res[self.get(point) - 1] += power_point_force
        return res

    def battle(self, forces):
        if len(forces) == 0:
            return -1
        elif len(forces) == 1:
            return list(forces.keys())[0]
        for i in forces.keys():
            forces[i] += randint(rand_min, rand_max)
        max_index = list(forces.keys())[0]
        for i in forces.keys():
            if forces[i] > forces[max_index]:
                max_index = i
            elif forces[i] == forces[max_index] and randint(1, 2) == 1:
                max_index = i
        return max_index

    def check_end(self):
        zeros = 0
        for i in range(len(self.teams)):
            if self.teams[i].count == 0:
                zeros += 1
            else:
                self.winner = i
        return zeros >= len(self.teams) - 1

    def tick(self):  # mettre à jour pour un cycle
        result = [[0] * len(self.map[0]) for i in range(len(self.map))]
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if self.map[y][x] >= 0:
                    self.teams[self.get(x, y) - 1].count -= 1
                    r = self.battle(self.count_around(x, y)) + 1
                    self.teams[r-1].count += 1
                    result[y][x] = r
                else:
                    result[y][x] = self.map[y][x]
        self.map = result
        self.last_update = time()
        self.tick_count += 1
    
    def update(self):  # mettre à jour en fonction du temps passé depuis la derniere mise à jour
        if self.check_end():
            self.running = False
        if self.running and time() - self.last_update > 1 / ticks_per_second:
            self.tick()

    def draw(self, screen, rect=(290, 10, 700, 700)):
        size = math.ceil(map_height / len(self.map))
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                team = self.get(x, y)
                r = (round(rect[0] + x / len(self.map[y]) * rect[2]), round(rect[1] + y / len(self.map) * rect[3]), rect[2] / len(self.map[y]), rect[3] / len(self.map))
                r = (round(screen_width / 2 - size * len(self.map[0]) / 2) + x * size, 10 + y * size, size, size)
                if team > 0:
                    pygame.draw.rect(screen, self.teams[self.get(x, y) - 1].color, r)
                elif team == 0:
                    pygame.draw.rect(screen, empty_ground_color, r)
                else:
                    pygame.draw.rect(screen, background_color, r)
        flag = transform.scale(flag_img, (4*size, 5*size))
        disabled_flag = transform.scale(disabled_flag_img, (4*size, 5*size))
        for x, y in self.power_points:
            r = (round(screen_width / 2 - size * len(self.map[0]) / 2) + x * size, 10 + y * size - flag.get_height(), 20, 20)
            screen.blit((flag if self.tick_count >= flag_activation else disabled_flag), r)
        if self.check_end():
            text = font.render(self.teams[self.winner].name + " remporte la partie", True, (0, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))