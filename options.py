import pygame
from time import time
import os

## OPTIONS LIEES A L'AFFICHAGE

screen_width, screen_height = 1280, 720  # taille de la fenetre
show_interface = False  # afficher le classement

ticks_per_second = 60  # nombre de mise à jour par seconde

empty_ground_color = (210, 210, 210)  # couleur d'une terre inoccupée
background_color = (73, 200, 255)  # couleur du vide
port_color = (13, 143, 185)
map_height = 650  # taille de la carte en pixel

## PRECHARGEMENTS

pygame.font.init()
font = pygame.font.Font("img/Proxima Nova Font.otf", 30)
small_font = pygame.font.Font("img/Proxima Nova Font.otf", 20)
flag_img = pygame.image.load("img/flag.png")
disabled_flag_img = pygame.image.load("img/disabled_flag.png")

folder_name = "result/" + str(int(time())) + "/"
os.mkdir(folder_name)

## OPTIONS LIEES AUX MONTAGES VIDEOS

record_games = True  # enregistrement des vidéos
edit_when_finished = True  # faire le montage une fois la vidéo terminée

min_x, max_x, min_y, max_y = 99999, -1, 99999, -1
framerate = 30  # nombre d'image par seconde
duration = 60  # durée de la partie, en secondes
result_duration = 5  # durée d'affichage du gagnant, en secondes
width, height = 1080, 1920  # taille de la vidéo
source_width, source_height = 1280, 720  # taille des images d'origine
top_text = "Bataille de terrain"  # texte affiché en haut de la vidéo
bottom_text = ["Abonnez vous et", "commentez votre", "département pour", "recevoir un boost !"]  # text affiché au bas de la vidéo