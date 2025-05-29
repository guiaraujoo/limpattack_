import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'pN.............E.......................M',
    't......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)
            if column == ",":
                Ground2(game, j, i)
            if column == "N":
                game.player = Player(game, j, i)
                Ground2(game, j, i)
            if column == "E" and fases[mapa_atual_index]:
                enemy_name = "Rei Mundiça"
                game.battle_enemy = Enemy(game, j, i, enemy_name)
            if column == "t":
                Tree1(game, j, i)
            if column == "T":
                Tree2(game, j, i)
            if column == "M":
                Tree3(game, j, i)
            if column == "p":
                ClosedPortal(game, j, i)
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)
            if column == "U":
                item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                ItemCuraSprite(game, j, i, item_cura)
            if column == "1":
                NPC(game, j, i, symbol="X")
            if column == "2":
                NPC2(game, j, i, symbol="Y")
    mapas_visitados[mapa_atual_index] = True