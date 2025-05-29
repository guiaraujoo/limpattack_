import pygame
from config import *
from sprites.sprites_base import *

# define o tilemap da tenda, 25x25, borda escura
tilemap = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.,.,.,.,.,.,.X',
    'X.,.,.,.,.,.,.,.,.,.,.,.,X',
    'X,.,.,.,.,.,.N.,.,.,.,.,.X',
    'XXXXXXXXXXXXX{XXXXXXXXXXXX',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    # instancia os tiles e paredes de sombra
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            if column == 'N':
                game.player = Player(game, j, i)
                GroundT2(game, j, i)
            if column == 'X':
                GroundB(game, j, i)  # piso da borda
                WallShadow(game, j, i)  # parede
            if column == '.':
                GroundT(game, j, i)  # piso 1
            if column == ',':
                GroundT2(game, j, i)  # piso 2
            if column == "{":
                PortalTenda(game, j, i, tenda_num=1) # portal de volta
    mapas_visitados[mapa_atual_index] = True  # marca tenda como visitada

    # SPAWN DA TOCHA DENTRO DA TENDA 1
    from npcs import npcs_data
    if not game.tocha_spawned and not npcs_data["F"]["status"].get("tocha_entregue", False):
        TochaSprite(game, 12, 22)  # ou a posição desejada
        game.tocha_spawned = True

class GroundT(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # piso claro da tenda
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(518, 2442, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GroundB(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # piso claro da tenda
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(518, 2442, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GroundT2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # piso alternado para efeito xadrez
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(518, 4722, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class WallShadow(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        # parede invisivel com gradiente de sombra nas bordas
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        dist = min(x, y, 24-x, 24-y)  # distancia ate a borda
        alpha = min(255, 80 + 35 * (3-dist) if dist < 4 else 80)  # calcula intensidade da sombra
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, max(80, alpha)))  # aplica sombra
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class PortalTenda(pygame.sprite.Sprite):
    def __init__(self, game, x, y, tenda_num):
        self.game = game
        self.tenda_num = tenda_num
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE * 1.1
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = pygame.Surface((TILESIZE, TILESIZE * 2))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y