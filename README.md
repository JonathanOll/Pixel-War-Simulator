# Pixel-War-Simulator
[![image](https://img.shields.io/badge/Language-Python-yellow)](https://www.python.org/)
[![image](https://img.shields.io/badge/Library-Pygame-orange)](https://www.pygame.org/)
[![image](https://img.shields.io/badge/Author-JonathanOll-blue)](https://github.com/JonathanOll/)

Programme de simulation de "guerre" de territoire sur une carte

## Fonctionnement

  Vous pouvez créer une carte à partir d'une image, puis ajouter des équipes et leur assigner un terrain (flèches directionnelles pour sélectionner l'équipe et la molette pour changer la taille du pinceau), avec possibilité d'avoir des zones neutres. Appuyez sur espace pour lancer la bataille. 

À chaque itération, tous les pixels de la map sont rafraichis de la manière suivante: 
- On prend la couleur de tous les pixels adjacents et on ajoute 1 au pouvoir de l'équipe auquel il appartient
- On ajoute 2 de pouvoir à l'équipe qui possède déjà le pixel
- On rajoute le pouvoir correspondant au pourcentage du terrain possédé par l'équipe (3 points au total)
- S'ils sont activés, on rajoute à chaque équipe les points qui leur sont dûs pour le contrôle de points de contrôle (les drapeaux)
- On ajoute à chaque équipe un pouvoir aléatoire entre 1 et 6
- L'équipe possédant le plus de pouvoir sur la case la remporte

le cycle continue jusqu'à l'éradication de toutes les autres équipes par les vainqueurs.

## Exemple

https://user-images.githubusercontent.com/70845195/220421981-ad7ba32e-4d17-450e-bef6-7a6d6193d2f3.mp4

## Installation

- Installer une version de [python](https://www.python.org/) supérieure ou égale à 3.7
- Installer pygame (éxécuter la commande `pip install pygame`)
- Télécharger le code et lancer le fichier main.py
