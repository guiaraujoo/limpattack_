import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

# este arquivo define o mapa 1 e os sprites especificos desse mapa
# tilemap contem a representacao do mapa usando caracteres
# create_tiled_map instancia os sprites de acordo com o tilemap
# classes como House, Cerca, BigTree, Arbs, Espan, Poco, Sacos, Wind, Toco e NPC3 representam objetos e npcs do mapa 1
# comentarios em minusculo e sem acento para facilitar entendimento

tilemap = [ #40x30
    'MTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'M............Z................u.....,,Np',
    'M.H..........o......H.........u.....,..t',
    'M.......H.................H...u...,,,..M',
    'M.................................,....M',
    'M...............o.................,....M',
    'M.................................,....M',
    'M.................................,....M',
    'M..W.................W.........uuu3uuuuM',
    'M....,...W.............,...W......,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,.....,...........,.....,....,....M',
    'M....,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,....M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,..e..,..e..,..e..,..e..,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M....,.....,.....,.....,.....,.........M',
    'M..Ch9hF.Ch9hF...,...Ch9hF.Ch9hF.......M',
    'M..cYYYf.cYYYf...,...cYYYf.cYYYf.......M',
    'M..jS..i.jaaai1..Ç,.2jaaai.jS..i.......M',
    'M..j...iUjaaai...,ç..jaaai.j...i.......M',
    'M..JDDDI.JDDDI.......JDDDI.JDDDI.......M',
    'M..LlllK.LlllK.......LlllK.LlllK.......M',
    'M................U.....................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

# cria o mapa com base no tilemap definido acima
def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    if not hasattr(game, 'mapa1_state'):
        game.mapa1_state = {
            'npc3_estado': 'bloqueando',
            'npc3_moved': False,
            'npc3_pos': None,
            'sabonete_coletado': False
        }
    # percorre cada linha e coluna do tilemap
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            # cria o sprite de chao
            Ground(game, j, i)
            if column == "Z":
                class PortalMapa6(pygame.sprite.Sprite):
                    def __init__(self, game, x, y):
                        self.game = game
                        self._layer = BLOCK_LAYER
                        self.groups = self.game.all_sprites, self.game.portals
                        pygame.sprite.Sprite.__init__(self, self.groups)
                        self.x = x * TILESIZE
                        self.y = y * TILESIZE
                        self.width = TILESIZE
                        self.height = TILESIZE
                        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                        self.image.fill((255, 255, 0, 50))
                        self.rect = self.image.get_rect()
                        self.rect.x = self.x
                        self.rect.y = self.y
                    def update(self):
                        if self.game.player.rect.colliderect(self.rect):
                            self.game.mapa_atual_index = 5  # mapa 6
                            self.game.new()
                            self.game.player.rect.x = 1 * TILESIZE
                            self.game.player.rect.y = 1 * TILESIZE
                PortalMapa6(game, j, i)
            if column == ",":
                Ground2(game, j, i)
            if column == "N":
                Ground2(game, j, i)
                # posiciona o jogador no mapa, dependendo se o mapa foi visitado ou nao
                if not mapas_visitados[mapa_atual_index]:
                    game.player = Player(game, 5, 10)
                else:
                    game.player = Player(game, j, i)
                    Ground2(game, j, i)
            # cria inimigos aleatorios nas posicoes marcadas com "E" no tilemap
            if column == "E" and fases[mapa_atual_index]:
                enemy_names = [k for k in enemies.keys() if k != "Rei Mundiça"]
                enemy_name = random.choice(enemy_names)
                game.battle_enemy = Enemy(game, j, i, enemy_name)
            # cria diferentes tipos de arvores, dependendo do caractere no tilemap
            if column == "t":
                Tree1(game, j, i)
            if column == "T":
                Tree2(game, j, i)
            if column == "M":
                Tree3(game, j, i)
            # cria portais fechados e abertos, dependendo das condicoes do jogo
            if column == "p":
                ClosedPortal(game, j, i)
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)
            # cria as casas no mapa
            if column == "H":
                House(game, j, i)
            # cria as cercas superiores
            if column == "C":
                CercaTop1(game, j, i)
            if column == "h":
                CercaTop2(game, j, i)
            if column == "9":
                CercaTop2(game, j, i)
                Ground2(game, j, i)
            if column == "F":
                CercaTop3(game, j, i)
            # cria as cercas do meio
            if column == "c":
                CercaTopMid1(game, j, i)
            if column == "Y":
                CercaTopMid2(game, j, i)
            if column == "f":
                CercaTopMid3(game, j, i)
            # cria as cercas inferiores
            if column == "j":
                CercaMid1(game, j, i)
            if column == "i":
                CercaMid2(game, j, i)
            if column == "J":
                CercaBotMid1(game, j, i)
            if column == "D":
                CercaBotMid2(game, j, i)
            if column == "I":
                CercaBotMid3(game, j, i)
            # cria as cercas na parte inferior do mapa
            if column == "L":
                CercaBot1(game, j, i)
            if column == "l":
                CercaBot2(game, j, i)
            if column == "K":
                CercaBot3(game, j, i)
            # cria objetos como arvores grandes, arbustos, poços, sacos e elementos de vento
            if column == "o":
                BigTree(game, j, i)
            if column == "a":
                Arbs(game, j, i)
            if column == "e":
                Espan(game, j, i)
            if column == "Ç":
                Poco(game, j, i)
                Ground2(game, j, i)
            if column == "ç":
                Poco2(game, j, i)
                Ground2(game, j, i)
            if column == "S":
                Sacos(game, j, i)
            if column == "W":
                Wind(game, j, i)
            if column == "u":
                Toco(game, j, i)
            # cria itens de cura em posicoes especificas do mapa
            if column == "U":
                pos = (j, i)
                if not hasattr(game, 'itens_cura_coletados'):
                    game.itens_cura_coletados = set()
                if pos not in game.itens_cura_coletados:
                    item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                    ItemCuraSprite(game, j, i, item_cura)
            # cria os NPCs do mapa
            if column == "1":
                NPC(game, j, i, symbol="A")
            if column == "2":
                NPC2(game, j, i, symbol="B")
            if column == "3":
                Ground2(game, j, i)
                npc3_x, npc3_y = j, i
                # posiciona o NPC3 dependendo do estado salvo no jogo
                if game.mapa1_state['npc3_moved'] and game.mapa1_state['npc3_pos']:
                    npc3_x, npc3_y = game.mapa1_state['npc3_pos']
                npc3 = NPC3(game, npc3_x, npc3_y, symbol="C")
                npc3.estado = game.mapa1_state['npc3_estado']
                npc3.moved = game.mapa1_state['npc3_moved']
                # remove o NPC3 da sua posicao anterior, se necessario
                if npc3.moved:
                    try:
                        npc3.remove(game.blocks)
                    except Exception:
                        pass
                game.npc3_ref = npc3
            # cria o sabonete apenas uma vez, se ainda nao foi coletado
            if column == "B":
                if not game.mapa1_state['sabonete_coletado'] and 'sabonete' not in getattr(game, 'inventario_chave', []):
                    Sabonete(game, j, i)
    mapas_visitados[mapa_atual_index] = True

# classe para criar as casas no mapa
class House(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(518, 3178, 160, 256, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classes para criar as cercas superiores do mapa
class CercaTop1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTop2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTop3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classes para criar as cercas do meio do mapa
class CercaTopMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTopMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaTopMid3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*1), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classes para criar as cercas inferiores do mapa
class CercaMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*2), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*2), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classes para criar as cercas na parte inferior do mapa
class CercaBotMid1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBotMid2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBotMid3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*3), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066, 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*1), 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class CercaBot3(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1066+(TILESIZE*2), 1126+(TILESIZE*4), self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar arvores grandes no mapa
class BigTree(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1678, 1414, 1796-1678, 1574-1414, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar arbustos no mapa
class Arbs(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar espinhos no mapa
class Espan(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1034, 1414, self.width, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar poços no mapa
class Poco(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1162, 1350, 64, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar poços duplos no mapa
class Poco2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(1226, 1382, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar sacos no mapa
class Sacos(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(2324, 1862, 96, 64, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar vento no mapa
class Wind(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(550, 3114, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para criar tocos no mapa
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

# classe para criar o NPC3 no mapa
class NPC3(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="3"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet("img/piu.png")
        self.image = self.spritesheet.get_sprite(1, 1, 23, 25, [])
        self.image.set_colorkey((160, 192, 144))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.estado = 'bloqueando'
        self.portal_pos = (x, y)
        self.moved = False

    def update(self):
        pass