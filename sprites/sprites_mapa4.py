import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

# este arquivo define o mapa 4 e os sprites especificos desse mapa
# tilemap contem a representacao do mapa usando caracteres
# create_tiled_map instancia os sprites de acordo com o tilemap
# classes como Ground, Tree, Portal, NPC e outros representam objetos do mapa 4
# comentarios em minusculo e sem acento para facilitar entendimento

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'pN.....................................p',
    't......................................t',
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
    # percorre cada linha e coluna do tilemap
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)  # cria o chao em todas as posicoes
            if column == ",":
                Ground2(game, j, i)  # cria um tipo diferente de chao
            if column == "N":
                game.player = Player(game, j, i)  # posiciona o jogador
                Ground2(game, j, i)
            if column == "E" and fases[mapa_atual_index]:
                enemy_names = [k for k in enemies.keys() if k != "Rei Mundiça"]
                enemy_name = random.choice(enemy_names)
                game.battle_enemy = Enemy(game, j, i, enemy_name)
            if column == "t":
                Tree1(game, j, i)  # posiciona arvores tipo 1
            if column == "T":
                Tree2(game, j, i)  # posiciona arvores tipo 2
            if column == "M":
                Tree3(game, j, i)  # posiciona arvores tipo 3
            if column == "p":
                ClosedPortal(game, j, i)  # posiciona portal fechado
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)  # posiciona portal aberto se nao houver inimigos
            if column == "U":
                item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                ItemCuraSprite(game, j, i, item_cura)  # posiciona itens de cura
            if column == "1":
                NPC(game, j, i, symbol="X")  # posiciona NPC tipo 1
            if column == "2":
                NPC2(game, j, i, symbol="Y")  # posiciona NPC tipo 2
    mapas_visitados[mapa_atual_index] = True  # marca o mapa atual como visitado