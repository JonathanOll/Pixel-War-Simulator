from pygame import font as fon
import pygame

screen_width, screen_height = 1280, 720  # taille de la fenetre
show_interface = False  # afficher le classement

force_on_position = 2  # force d'une case si une troupe est placée dessus
force_around = 1  # force d'une case si une troupe est placée sur un case adjacente
area_force = 1  # force due au pourcentage de possession du terrain
power_point_force = 1  # force donnée par le contrôle d'une zone de pouvoir
flag_activation = 750  # tick à partir duquel sont activés les zones de pouvoir

rand_min, rand_max = 1, 10  # limites de force ajoutée au hasard

ticks_per_second = 60  # nombre de mise à jour par seconde

empty_ground_color = (210, 210, 210)  # couleur d'une terre inoccupée
background_color = (73, 200, 255)  # couleur du vide
port_color = (13, 143, 185)
map_height = 650  # taille de la carte en pixel

fon.init()
font = fon.SysFont(None, 40)
small_font = fon.SysFont(None, 30)
flag_img = pygame.image.load("img/flag.png")
disabled_flag_img = pygame.image.load("img/disabled_flag.png")