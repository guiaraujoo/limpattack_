import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

# este arquivo define o mapa 2 e os sprites especificos desse mapa
# tilemap contem a representacao do mapa usando caracteres
# create_tiled_map instancia os sprites de acordo com o tilemap
# classes como House2, Porta, Escada, Vaso, Fonte, Flores, Tenda, TendaMini, Toco, NPC4-8, NPCTenda1-5 e PortalTenda representam objetos, npcs e portais do mapa 2
# comentarios em minusculo e sem acento para facilitar entendimento

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'pN,...Z.....Z.....Z....Z......Z.....,3,p',
    't.,.................................,uut',
    'M.,.................................,..M',
    'M.,.....{.....}.....[....]......)...,..M',
    'M.,.................................,..M',
    'M.,,,,,,4,,,,,5,,,,,6,,,,7,,,,,,8,,,,..M',
    'M.,....,,...,,.......,,.....,,.....,,..M',
    'M.,....,,...,,.......,,.....,,.....,,..M',
    'M.,....A,...A,.......A,.....A,.....A,..M',
    'M.,....................................M',
    'M.,....................................M',
    'M.,....................................M',
    'M.,....................................M',
    'M.,,,,,,,,,,,,,,,,,....................M',
    'M......A,..A,.....,..QQQQQQQQQQQQQQQ...M',
    'M.................,..Q,,,,,,,Q,,U,,Q...M',
    'M.................,..Q,,,Q,Q,Q,,,,,Q...M',
    'M.................,..Q,,,Q,Q,Q,,,,,Q...M',
    'M.................,.1QQQ,Q,Q,Q,O,,,Q...M',
    'M.,,,,,,,,,,,,,,,,,,,,,Q,Q,Q,Q,,,,UQ...M',
    'M.,......A,..A,......Q,Q,Q,Q,Q,,,,,Q...M',
    'M.,..................Q,Q,Q,Q,Q,,U,,Q...M',
    'M.,..................Q,QUQ,Q,Q,,,,,Q...M',
    'M.,..................Q,QQQ,Q,QQQQQ,Q...M',
    'M.,..................Q,,,,,Q,,,,,,,Q...M',
    'M.,..................QQQQQQQQQQQQQQQ...M',
    'M.,2...................................M',
    'M......................................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

# funcao responsavel por criar o mapa baseado no tilemap
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
                enemy_names = [k for k in enemies.keys() if k != "Rei Mundiça"]
                enemy_name = random.choice(enemy_names)
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
            if column == "Z":
                Tenda(game, j, i)
            if column == "A":
                TendaMini(game, j, i)
                Ground2(game, j, i)    
            if column == "P":
                Porta(game, j, i)
            if column == "s":
                Escada(game, j, i)
            if column == "V":
                Vaso(game, j, i)
            if column == "O":
                Fonte(game, j, i)
                Ground2(game, j, i)
            if column == "Q":
                Flores(game, j, i)
                Ground2(game, j, i)
            if column == "u":
                Toco(game, j, i)
            if column == "U":
                pos = (j, i)
                if not hasattr(game, 'itens_cura_coletados'):
                    game.itens_cura_coletados = set()
                if pos not in game.itens_cura_coletados:
                    item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                    ItemCuraSprite(game, j, i, item_cura)
                Ground2(game, j, i) 
            if column == "1":
                NPC4(game, j, i, symbol="D")
            if column == "2":
                NPC5(game, j, i, symbol="E")
            if column == "3":
                npc6 = NPC6(game, j, i, symbol="F")
                Ground2(game, j, i)
                game.npc6_ref = npc6
                if npcs_data["F"]["status"].get("tocha_entregue", False):
                    npc6.rect.x -= 2 * TILESIZE
            if column == "4":
                npc = NPCTenda1(game, j, i, symbol="G")
                Ground2(game, j, i)
                if getattr(game, "npcs_moveram", False):
                    npc.rect.x -= TILESIZE
            if column == "5":
                npc = NPCTenda2(game, j, i, symbol="H")
                Ground2(game, j, i)
                if getattr(game, "npcs_moveram", False):
                    npc.rect.x -= TILESIZE
            if column == "6":
                npc = NPCTenda3(game, j, i, symbol="I")
                Ground2(game, j, i)
                if getattr(game, "npcs_moveram", False):
                    npc.rect.x -= TILESIZE
            if column == "7":
                npc = NPCTenda4(game, j, i, symbol="J")
                Ground2(game, j, i)
                if getattr(game, "npcs_moveram", False):
                    npc.rect.x -= TILESIZE
            if column == "8":
                npc = NPCTenda5(game, j, i, symbol="K")
                Ground2(game, j, i)
                if getattr(game, "npcs_moveram", False):
                    npc.rect.x -= TILESIZE
            if column == "{":
                PortalTenda(game, j, i, tenda_num=1)
            if column == "}":
                PortalTenda(game, j, i, tenda_num=2)
            if column == "[":
                PortalTenda(game, j, i, tenda_num=3)
            if column == "]":
                PortalTenda(game, j, i, tenda_num=4)
            if column == ")":
                PortalTenda(game, j, i, tenda_num=5)
    mapas_visitados[mapa_atual_index] = True

# classe que representa a casa 2
class House2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1638, 159, 319, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa a porta
class Porta(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1068, 1574, 27, 63, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    

# classe que representa a escada
class Escada(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1317, 1992, 48, 29, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y   

# classe que representa o vaso
class Vaso(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(586, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa a fonte
class Fonte(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1070 , 2993 , 92, 86, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y   

# classe que representa as flores
class Flores(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1100, 2574, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa a tenda
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
        self.image = self.game.terrain_spritesheet.get_sprite(2, 802, 160, 160, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa a tenda mini
class TendaMini(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(2066+TILESIZE*6, 2+TILESIZE*10, TILESIZE*2, TILESIZE*4, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o toco
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
        self.image = self.game.terrain_spritesheet.get_sprite(130, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc 4
class NPC4(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="D"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/rosa.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 120))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc 5
class NPC5(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="E"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc 6
class NPC6(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="F"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc tenda 1
class NPCTenda1(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="G"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/tigrebranco.png")
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(160, 192, 144)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc tenda 2
class NPCTenda2(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="H"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc tenda 3
class NPCTenda3(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="I"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc tenda 4
class NPCTenda4(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="J"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o npc tenda 5
class NPCTenda5(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="K"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe que representa o portal da tenda
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
        self.height = TILESIZE
        self.image = pygame.Surface((TILESIZE, TILESIZE * 2), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y