import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

# este arquivo define o mapa 3 e os sprites especificos desse mapa
# tilemap contem a representacao do mapa usando caracteres
# create_tiled_map instancia os sprites de acordo com o tilemap
# classes como Tenda e Toco representam objetos do mapa 3
# comentarios em minusculo e sem acento para facilitar entendimento

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTM',
    'pN.Z......u............................M',
    't.........u.uuuuuu.uuu.uuuuuuuu.uuuuuu.M',
    'M.........u.uuuuUu.uuu.uuuuuuuu.uuuuuu.M',
    'M.........u.E....u.uuu.u........uuuuuu.M',
    'M.........uuuuuuuu.uuu.uuuuuuuuuu......M',
    'M........E.........uuu.uuuuuuuuuu.uuuuuM',
    'Muuuuuuuuuuuuuuuuuuu...u...............M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu.uuuuuM',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M.uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuM',
    'M.u...uU...............................M',
    'M.u.u.uuuuuuu.uuuuuuuuu................M',
    'M...u.........uuuuuuuuuu...............M',
    'Muuuuuuuuuuuuuuuuuuuuuuuu..............M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuu.............M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuu............M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuu...........M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuu..........M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuuu.........M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuuuu........M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu.......M',
    'Muuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu.......M',
    'M......................................M',
    'M......................................M',
    'M...uuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuM',
    'M......................................M',
    'M......................................M',
    'M......................................p',
    'MttttttttttttttttttttttttttttttttttttttM',
]

# funcao responsavel por criar o mapa baseado no tilemap
def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
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
                Tree1(game, j, i)  # posiciona tipo 1 de arvore
            if column == "T":
                Tree2(game, j, i)  # posiciona tipo 2 de arvore
            if column == "M":
                Tree3(game, j, i)  # posiciona tipo 3 de arvore
            if column == "p":
                ClosedPortal(game, j, i)  # posiciona portal fechado
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)  # posiciona portal aberto se nao houver inimigos
            if column == "U":
                pos = (j, i)
                if not hasattr(game, 'itens_cura_coletados'):
                    game.itens_cura_coletados = set()
                if pos not in game.itens_cura_coletados:
                    item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                    ItemCuraSprite(game, j, i, item_cura)
            if column == "u":
                Toco(game, j, i)  # posiciona tocos
            if column == "Z":
                Tenda(game, j, i)  # posiciona tendas
    mapas_visitados[mapa_atual_index] = True  # marca o mapa atual como visitado

# classe que representa a tenda no mapa
class Tenda(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # pega o sprite da tenda na spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(2, 802, 160, 160, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o toco no mapa
class Toco(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # pega o sprite do toco na spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(130, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y