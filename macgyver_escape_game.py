#!/usr/bin/python3
# -*- coding: Utf-8 -*

""" Main structure of the program/game """

import random
import pygame
from pygame.locals import*

from classes import*
from constants import*

pygame.init()

window = pygame.display.set_mode((window_side, window_side))
icon = pygame.image.load(icon_picture)
pygame.display.set_icon(icon)
pygame.display.set_caption(window_title)

background = pygame.image.load(pic_bg).convert()
# level creation
level = Level('level1')
level.generate()
level.display(window)

# characters and items creation
mg = Charac("ressources/MacGyver.png", "ressources/MacGyver.png",
            "ressources/MacGyver.png", "ressources/MacGyver.png", level)

gd = Foe("ressources/Gardien.png", level)

net1 = Items("ressources/aiguille.png", level)
net2 = Items("ressources/ether.png", level)
net3 = Items("ressources/tube_plastique.png", level)

# main loop
continuer = 1
while continuer:

    for event in pygame.event.get():

        if event.type == QUIT or\
                     event.type == KEYDOWN and event.key == K_ESCAPE:
            continuer = 0

    pygame.time.Clock().tick(30)  # Spare the processor !

    for event in pygame.event.get():

        if event.type == QUIT:
            continuer = 0

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                continuer = 0

            elif event.key == K_RIGHT:
                mg.move('right')
            elif event.key == K_LEFT:
                mg.move('left')
            elif event.key == K_UP:
                mg.move('up')
            elif event.key == K_DOWN:
                mg.move('down')

    # refresh to the most recent position
    window.blit(background, (0, 0))
    level.display(window)
    # set the picture in the right direction
    window.blit(mg.direction, (mg.x, mg.y))

    window.blit(gd.foe, (gd.x, gd.y))

    if level.structure[net1.case_y][net1.case_x] == 'i':
        window.blit(net1.img, (net1.x, net1.y))
    if level.structure[net2.case_y][net2.case_x] == 'i':
        window.blit(net2.img, (net2.x, net2.y))
    if level.structure[net3.case_y][net3.case_x] == 'i':
        window.blit(net3.img, (net3.x, net3.y))
    pygame.display.flip()

    # Terms of defeat and victory :
    if level.structure[mg.case_y][mg.case_x] == 'f':

        if mg.harvest_items == 3:
            guard_can_be_defeated = True
            level.structure[gd.case_y][gd.case_x] = '0'
            window.blit(gd.foe, (gd.x, gd.y))
            print("Congratulation ! you won !")
            continuer = 1

        elif mg.harvest_items != 3:
            guard_can_be_defeated = False
            print("You've been taken down by the guard !")
            continuer = 0

    if level.structure[mg.case_y][mg.case_x] == 'a':
        continuer = 0
        print("Nice escape !  ;-)")
