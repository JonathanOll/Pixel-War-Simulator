from options import *
from random import randint
from time import time
import pygame
from PIL import Image
from numpy import asarray

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
    
    def save(self, file_path):
        file = open(file_path, "w+")

        file.write(str(len(self.map[0])) + " " + str(len(self.map)) + "\n")

        for row in self.map:

            file.write(" ".join(str(i) for i in row) + "\n")

        file.write("|")

        for team in self.teams:

            file.write(team.name + "," + str(team.color[0]) + " " + str(team.color[1]) + " " + str(team.color[2]) + "," + str(team.power) + "\n")

        file.close()

        print("map saved to", file_path)
    
    def load(self, file_path):
        
        self.teams.clear()

        file = open(file_path, "r")

        s = file.read()

        ints = []


        for i in s.split("\n"):
            ints.extend(i.split(" "))

        file.close()

        self.map = [[-1] * int(ints[0]) for i in range(int(ints[1]))]

        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                self.map[y][x] = int(ints[2 + y * int(ints[0]) + x])

        teams = s.split("|")[-1].split("\n")
        
        for team in teams[:-1]:
            properties = team.split(",")
            rgb = properties[1].split(" ")
            t = Team(properties[0], (int(rgb[0]), int(rgb[1]), int(rgb[2])), int(properties[2]))
            self.teams.append(t)
        
        self.update_counts()
        
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
        return self.map[y][x]

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
        res = [0] * len(self.teams)
        for dx, dy in dirs:
            pos = (x+dx, y+dy)
            if self.is_valid(pos) and self.get(pos) > 0:
                res[self.get(pos) - 1] += force_around
        if self.is_valid(x, y) and self.get(x, y) > 0:
            res[self.get(x, y) - 1] += force_on_position
        total = sum(i.count for i in self.teams) 
        for i in range(len(self.teams)):
            if res[i] != 0:
                res[i] += self.teams[i].power + round(self.teams[i].count / total * area_force)
        return res

    def battle(self, forces):
        zeros = 0
        for i in range(len(forces)):
            if forces[i] == 0: 
                zeros += 1
                forces[i] = -999
            else:
                forces[i] += randint(rand_min, rand_max)
        if zeros == len(self.teams):
            return -1
        elif zeros == len(self.teams) - 1:
            for i in range(len(forces)):
                if forces[i] > 0: return i
        max_index = 0
        for i in range(len(forces)):
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
    
    def update(self):  # mettre à jour en fonction du temps passé depuis la derniere mise à jour
        if self.check_end():
            self.running = False
        if self.running and time() - self.last_update > 1 / ticks_per_second:
            self.tick()

    def draw(self, screen, rect=(290, 10, 700, 700)):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                team = self.get(x, y)
                r = (round(rect[0] + x / len(self.map[y]) * rect[2]), round(rect[1] + y / len(self.map) * rect[3]), rect[2] / len(self.map[y]), rect[3] / len(self.map))
                if team > 0:
                    pygame.draw.rect(screen, self.teams[self.get(x, y) - 1].color, r)
                elif team == 0:
                    pygame.draw.rect(screen, empty_ground_color, r)
                else:
                    pygame.draw.rect(screen, background_color, r)
        if self.check_end():
            text = font.render("Partie terminée", True, (0, 0, 0))
            screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - text.get_height() // 2))