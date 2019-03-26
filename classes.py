""" MacGyvers's game Classes """

import random
import pygame
from pygame.locals import*
from constants import*


class Level:
    """ class who create the level """

    def __init__(self, fichier):
        self.fichier = fichier
        self.structure = 0

    def generate(self):
        """ enable the level creation thanks to the file 'level' """
        with open(self.fichier, 'r') as fichier:
            structure_level = []
            for line in fichier:
                line_level = []
                for sprite in line:
                    # do not take in count the end's line code '\n'
                    if sprite != '\n':
                        line_level.append(sprite)
                structure_level.append(line_level)
            self.structure = structure_level

    def display(self, window):
        """ display the level thanks to
        the structure's list sended by the 'generate' method """
        start = pygame.image.load(pic_start).convert()
        sand_wall = pygame.image.load(pic_w1).convert()
        grass_wall = pygame.image.load(pic_w2).convert()
        water_wall = pygame.image.load(pic_w3).convert()
        brick_wall = pygame.image.load(pic_w4).convert()
        guard = pygame.image.load(pic_gd).convert()
        end = pygame.image.load(pic_end).convert()
        # objects
        niddle = pygame.image.load(pic_nid).convert_alpha()
        ether = pygame.image.load(pic_eth).convert_alpha()
        tube = pygame.image.load(pic_tub).convert_alpha()
        # combine
        inject = pygame.image.load(pic_inj).convert()

        nbr_line = 0
        for line in self.structure:
            nbr_case = 0
            for sprite in line:
                x = nbr_case * sprite_size
                y = nbr_line * sprite_size
                if sprite == 's':
                    window.blit(sand_wall, (x, y))
                elif sprite == 'p':
                    window.blit(grass_wall, (x, y))
                elif sprite == 'q':
                    window.blit(water_wall, (x, y))
                elif sprite == 'r':
                    window.blit(brick_wall, (x, y))

                elif sprite == 'd':
                    window.blit(start, (x, y))
                elif sprite == 'a':
                    window.blit(end, (x, y))
                elif sprite == 'g':
                    window.blit(guard, (x, y))

                # not useful here !!!
                # only allow to test if the items are collected !!!
                elif sprite == 'n':
                    window.blit(niddle, (x, y))
                elif sprite == 'e':
                    window.blit(ether, (x, y))
                elif sprite == 't':
                    window.blit(tube, (x, y))

                nbr_case += 1
            nbr_line += 1


class Charac:
    """ class who create our character """

    def __init__(self, right, left, up, down, level):
        self.right = pygame.image.load(right).convert_alpha()
        self.left = pygame.image.load(left).convert_alpha()
        self.up = pygame.image.load(up).convert_alpha()
        self.down = pygame.image.load(down).convert_alpha()

        self.case_x = 0
        self.case_y = 0
        self.x = 0
        self.y = 0

        self.harvest_items = 0

        self.direction = self.right

        self.level = level

        # self.harvest_items = 0 collected items counter !

    def move(self, direction):
        """ method who allow our character to move """

        obstacles = ['s', 'p', 'q', 'r']

        if direction == 'right':
            # To not overtake the screen
            if self.case_x < (nbr_side_sprite - 1):
                # check if we do not send the character inside a wall
                if self.level.structure[self.case_y][self.case_x + 1]\
                            not in obstacles:
                    # move of 1 case
                    self.case_x += 1
                    # Calcul the pixels real position
                    self.x = self.case_x * sprite_size
            # picture set in the right direction
            self.direction = self.right

        if direction == 'left':
            if self.case_x > 0:
                if self.level.structure[self.case_y][self.case_x - 1]\
                             not in obstacles:
                    self.case_x -= 1
                    self.x = self.case_x * sprite_size
            self.direction = self.left

        if direction == 'up':
            if self.case_y > 0:
                if self.level.structure[self.case_y - 1][self.case_x]\
                             not in obstacles:
                    self.case_y -= 1
                    self.y = self.case_y * sprite_size
            self.direction = self.up

        if direction == 'down':
            if self.case_y < (nbr_side_sprite - 1):
                if self.level.structure[self.case_y + 1][self.case_x]\
                             not in obstacles:
                    self.case_y += 1
                    self.y = self.case_y * sprite_size
            self.direction = self.down

        # am i on a case with an item ?
        if self.level.structure[self.case_y][self.case_x] == 'i':
            self.harvest_items += 1
            self.level.structure[self.case_y][self.case_x] = '0'

        if self.harvest_items == 3:
            print("Congrats ! now you have the injection !")
            if self.level.structure[self.case_y][self.case_x] == 'f':
                self.level.structure[self.case_y][self.case_x] = '0'


class Items:
    """ class who create our items """

    def __init__(self, n, level):
        self.img = pygame.image.load(n).convert_alpha()
        self.level = level
        self.case_x = 0
        self.case_y = 0
        while self.level.structure[self.case_y][self.case_x] != '0':
            self.case_x = random.randint(1, 14)
            self.case_y = random.randint(1, 14)

        self.x = self.case_x * sprite_size
        self.y = self.case_y * sprite_size

        self.level.structure[self.case_y][self.case_x] = 'i'


class Foe:
    """ Here we take care of the guard """

    def __init__(self, foe, level):
        self.foe = pygame.image.load(foe).convert_alpha()
        self.level = level

        self.case_x = 13
        self.case_y = 13
        self.x = 0
        self.y = 0

        self.x = self.case_x * sprite_size
        self.y = self.case_y * sprite_size

        self.level.structure[self.case_y][self.case_x] = 'f'
        print(self.level.structure)
