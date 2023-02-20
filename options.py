from pygame import font as fon

screen_width, screen_height = 1280, 720

force_on_position = 2  # force d'une case si une troupe est placée dessus
force_around = 1  # force d'une case si une troupe est placée sur un case adjacente
area_force = 3  # force due au pourcentage de possession du terrain

rand_min, rand_max = 1, 6  # limites de force ajoutée au hasard

ticks_per_second = 60  # nombre de mise à jour par seconde

empty_ground_color = (210, 210, 210)  # couleur d'une terre inoccupée
background_color = (73, 200, 255)
map_size = (700, 700)

fon.init()
font = fon.SysFont(None, 40)
small_font = fon.SysFont(None, 30)