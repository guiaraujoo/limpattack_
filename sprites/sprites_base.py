import pygame
from config import *
from battleData import *
import math
import random
from npcs import npcs_data

# este arquivo define as classes base de sprites e logica de movimento do jogador
# Spritesheet carrega e recorta sprites das imagens
# Player gerencia o movimento, animacao e colisao do jogador
# Enemy representa inimigos no mapa
# Ground, Ground2, Tree1, Tree2, Tree3 desenham o cenario
# Portal e ClosedPortal gerenciam portais do mapa
# ItemCuraSprite representa itens de cura no mapa
# NPC e NPC2 representam npcs comuns
# Camera controla o deslocamento da tela
# Sabonete e TochaSprite sao itens especiais
# comentarios em minusculo e sem acento para facilitar entendimento

# class Base(pygame.sprite.Sprite):
#     def __init__(self, game, x, y):
#         self.game = game
#         self._layer = BLOCK_LAYER
#         self.groups = self.game.all_sprites, self.game.blocks
#         pygame.sprite.Sprite.__init__(self, self.groups)
#         self.x = x * TILESIZE
#         self.y = y * TILESIZE
#         self.width = TILESIZE
#         self.height = TILESIZE
#         bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
#         self.image = self.game.terrain_spritesheet.get_sprite(x, y, self.width, self.height, bg_colors)
#         self.rect = self.image.get_rect()
#         self.rect.x = self.x
#         self.rect.y = self.y

# classe para gerenciar spritesheets (conjuntos de sprites em uma imagem)
class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert()
    # metodo para obter um sprite recortado da spritesheet
    def get_sprite(self, x, y, width, height, bg_colors):
        sprite = pygame.Surface([width, height], pygame.SRCALPHA)
        sprite.blit(self.sheet, (0, 0), (x, y, width, height))
        pixel_array = pygame.PixelArray(sprite)
        # remove a cor de fundo do sprite
        for color in bg_colors:
            pixel_array.replace(color, (0, 0, 0, 0))
        del pixel_array
        return sprite
    
# classe para o jogador, que herda de Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0
        self.facing = 'down'
        self.animation_loop = 1
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # carrega a imagem do jogador a partir da spritesheet
        self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.target_x = self.rect.x
        self.target_y = self.rect.y
        self.moving = False
    # metodo chamado a cada frame para atualizar o estado do jogador
    def update(self):
        self.grid_movement()
        self.animation()
        self.rect.x += self.x_change
        self.collide_blocks('x')
        self.rect.y += self.y_change
        self.collide_blocks('y')
        self.x_change = 0
        self.y_change = 0
        # verifica colisao com itens e portais
        for item in pygame.sprite.spritecollide(self, self.game.all_sprites, False):
            if hasattr(self.game, 'mapa1_state'):
                if item.__class__.__name__ == 'Sabonete':
                    if 'sabonete' not in self.game.inventario_chave:
                        self.game.inventario_chave.append('sabonete')
                        item.kill()
                        self.game.mapa1_state['sabonete_coletado'] = True
                if item.__class__.__name__ == 'ItemCuraSprite':
                    pos = (item.rect.x // TILESIZE, item.rect.y // TILESIZE)
                    if not hasattr(self.game, 'itens_cura_coletados'):
                        self.game.itens_cura_coletados = set()
                    if pos not in self.game.itens_cura_coletados:
                        self.game.inventario_cura.append(item.item_cura)
                        self.game.itens_cura_coletados.add(pos)
                        item.kill()
            if item.__class__.__name__ == 'TochaSprite':
                if 'tocha' not in self.game.inventario_chave:
                    self.game.inventario_chave.append('tocha')
                    item.kill()
                    self.game.tocha_spawned = True  # <-- Adicione esta linha aqui!
        # verifica colisao com portais para troca de cena
        for portal in self.game.all_sprites:
            if portal.__class__.__name__ == 'PortalTenda' and self.rect.colliderect(portal.rect):
                print(f"DEBUG: Colisão com PortalTenda {getattr(portal, 'tenda_num', '?')}")
                self.game.trocar_para_tenda(portal.tenda_num)
                return
        self.check_enemy_proximity()
    # verifica a proximidade de inimigos para iniciar batalha
    def check_enemy_proximity(self):
        if self.game.in_battle:
            return
        for enemy in self.game.enemy:
            dx = abs(self.rect.centerx - enemy.rect.centerx) // TILESIZE
            dy = abs(self.rect.centery - enemy.rect.centery) // TILESIZE
            if dx <= 1 and dy <= 1:
                print("⚔️ Iniciando batalha por proximidade!")
                self.game.in_battle = True
                self.game.battle_enemy = enemy
                self.game.handle_battle()
                break
    # metodo para movimentacao do jogador em grade
    def grid_movement(self):
        if self.game.in_battle:
            return
        keys = pygame.key.get_pressed()
        if not self.moving:
            dx, dy = 0, 0
            # verifica as teclas pressionadas e define a direcao
            if keys[pygame.K_a]  or keys[pygame.K_LEFT]:
                self.facing = 'left'
                dx = -TILESIZE
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.facing = 'right'
                dx = TILESIZE
            elif keys[pygame.K_w] or keys[pygame.K_UP]:
                self.facing = 'up'
                dy = -TILESIZE
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                self.facing = 'down'
                dy = TILESIZE
            # verifica se o jogador vai se mover
            if dx != 0 or dy != 0:
                next_rect = self.rect.copy()
                next_rect.x += dx
                next_rect.y += dy
                npc_hit = None
                # verifica colisao com npcs
                for npc in self.game.all_sprites:
                    if npc.__class__.__name__ in ['NPC', 'NPC2', 'NPC3',
                                                  'NPC4', 'NPC5', 'NPC6',
                                                  'NPCTenda1', 'NPCTenda2', 'NPCTenda3', 'NPCTenda4', 'NPCTenda5'] and next_rect.colliderect(npc.rect):
                        npc_hit = npc
                        break
                portal_hit = None
                # verifica colisao com portais
                for portal in self.game.all_sprites:
                    if portal.__class__.__name__ == 'PortalTenda' and next_rect.colliderect(portal.rect):
                        portal_hit = portal
                        break
                # troca de cena ao colidir com portal
                if portal_hit:
                    print(f"DEBUG: Colisão com PortalTenda {getattr(portal_hit, 'tenda_num', '?')}")
                    self.game.trocar_para_tenda(portal_hit.tenda_num)
                    return
                # interacao com npcs
                if npc_hit and not self.game.npc_dialog_active:
                    npc_symbol = npc_hit.symbol if hasattr(npc_hit, "symbol") else None
                    # logica de interacao com npc da classe 'C'
                    if npc_symbol == 'C':
                        if hasattr(self.game, 'inventario_chave') and 'sabonete' in self.game.inventario_chave and getattr(npc_hit, 'estado', None) == 'bloqueando':
                            npc_hit.estado = 'livre'
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_entrega']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            # movimenta o npc para fora do caminho
                            if not getattr(npc_hit, 'moved', False):
                                npc_hit.remove(self.game.blocks)
                                npc_hit.rect.x += TILESIZE
                                npc_hit.rect.y -= TILESIZE
                                npc_hit.moved = True
                            # atualiza o estado do mapa
                            if hasattr(self.game, 'mapa1_state'):
                                if 'sabonete' in self.game.inventario_chave:
                                    self.game.inventario_chave.remove('sabonete')
                                self.game.mapa1_state['npc3_estado'] = 'livre'
                                self.game.mapa1_state['npc3_moved'] = True
                                self.game.mapa1_state['npc3_pos'] = (npc_hit.rect.x // TILESIZE, npc_hit.rect.y // TILESIZE)
                            self.moving = False
                            return
                        # dialogo quando o npc esta bloqueando o caminho
                        elif getattr(npc_hit, 'estado', None) == 'bloqueando':
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_bloqueando']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            self.moving = False

                            # gera um sabonete no mapa
                            if not self.game.sabonete_spawned:
                                print("DEBUG: Tentando criar sabonete...")
                                Sabonete(self.game, 19, 2)
                                self.game.sabonete_spawned = True
                                print("DEBUG: Sabonete spawnado!")
                            return
                        # dialogo quando o npc esta livre
                        elif getattr(npc_hit, 'estado', None) == 'livre':
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npcs_data['C']['dialogos_livre']
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'C'
                            self.moving = False
                            return
                    # logica de interacao com npc da classe 'F'
                    if npc_symbol == 'F':
                        npc_info = npcs_data.get("F")
                        if not npc_info["status"].get("tocha_entregue", False):
                            if "tocha" in self.game.inventario_chave:
                                npc_info["status"]["tocha_entregue"] = True
                                self.game.npcs_moveram = True
                                self.game.npc_dialog_active = True
                                self.game.npc_dialog_texts = npc_info["dialogos_entrega"]
                                self.game.npc_dialog_index = 0
                                self.game.npc_dialog_current = ""
                                self.game.npc_dialog_char_index = 0
                                self.game.npc_dialog_last_update = pygame.time.get_ticks()
                                self.game.npc_dialog_npc_symbol = 'F'
                                self.game.inventario_chave.remove("tocha")
                                for npc in self.game.all_sprites:
                                    if hasattr(npc, "symbol") and npc.symbol == "F":
                                        npc.rect.x -= 2 * TILESIZE
                                self.moving = False
                                return
                            else:
                                self.game.npc_dialog_active = True
                                self.game.npc_dialog_texts = npc_info["dialogos_bloqueando"]
                                self.game.npc_dialog_index = 0
                                self.game.npc_dialog_current = ""
                                self.game.npc_dialog_char_index = 0
                                self.game.npc_dialog_last_update = pygame.time.get_ticks()
                                self.game.npc_dialog_npc_symbol = 'F'
                                if not getattr(self.game, "tocha_spawned", False) and not getattr(self.game, "npcs_moveram", False):
                                    for npc in self.game.all_sprites:
                                        if hasattr(npc, "symbol") and npc.symbol in ["G", "H", "I", "J", "K"]:
                                            npc.rect.x -= TILESIZE
                                    self.game.npcs_moveram = True
                                self.moving = False
                                return
                        else:
                            self.game.npc_dialog_active = True
                            self.game.npc_dialog_texts = npc_info["dialogos_livre"]
                            self.game.npc_dialog_index = 0
                            self.game.npc_dialog_current = ""
                            self.game.npc_dialog_char_index = 0
                            self.game.npc_dialog_last_update = pygame.time.get_ticks()
                            self.game.npc_dialog_npc_symbol = 'F'
                            self.moving = False
                            return
                    if npc_symbol in ["G", "H", "I", "J", "K"]:
                        if not getattr(self.game, "npcs_moveram", False):
                            dialogos = npcs_data[npc_symbol].get("dialogo_bloqueando", ["..."])
                        else:
                            dialogos = npcs_data[npc_symbol].get("dialogo_livre", ["..."])
                        self.game.npc_dialog_active = True
                        self.game.npc_dialog_texts = dialogos
                        self.game.npc_dialog_index = 0
                        self.game.npc_dialog_current = ""
                        self.game.npc_dialog_char_index = 0
                        self.game.npc_dialog_last_update = pygame.time.get_ticks()
                        self.game.npc_dialog_npc_symbol = npc_symbol
                        self.moving = False
                        return
                    # dialogos genericos para npcs
                    npc_info = npcs_data.get(npc_symbol)
                    if npc_info:
                        self.game.npc_dialog_active = True
                        if "dialogos" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos"]
                        elif "dialogos_bloqueando" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_bloqueando"]
                        elif "dialogos_entrega" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_entrega"]
                        elif "dialogos_livre" in npc_info:
                            self.game.npc_dialog_texts = npc_info["dialogos_livre"]
                        else:
                            self.game.npc_dialog_texts = ["..."]
                        self.game.npc_dialog_index = 0
                        self.game.npc_dialog_current = ""
                        self.game.npc_dialog_char_index = 0
                        self.game.npc_dialog_last_update = pygame.time.get_ticks()
                        self.game.npc_dialog_npc_symbol = npc_symbol
                        self.moving = False
                        # recompensa ao jogador ao interagir com npc da classe 'E'
                        if npc_symbol == "E" and not npc_info["status"].get("presente_entregue", False):
                            from battleData import ItemCura
                            self.game.inventario_cura.append(ItemCura("Xarope", 60))
                            npc_info["status"]["presente_entregue"] = True
                            self.game.npc_dialog_texts = npc_info["dialogos"] + ["Você recebeu um xarope!"]
                        return
                # se o dialogo com o npc esta ativo, nao faz mais nada
                if self.game.npc_dialog_active:
                    return
                # verifica colisao com blocos e inimigos
                will_collide = any(next_rect.colliderect(block.rect) for block in self.game.blocks)
                will_collide_enemy = any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy)
                # se nao houver colisao, atualiza a posicao alvo do jogador
                if not will_collide and not will_collide_enemy and not npc_hit:
                    self.target_x = self.rect.x + dx
                    self.target_y = self.rect.y + dy
                    self.moving = True
        # movimentacao do jogador em direcao a posicao alvo
        if self.moving:
            if self.rect.x < self.target_x:
                self.x_change = min(PLAYER_SPEED, self.target_x - self.rect.x)
            elif self.rect.x > self.target_x:
                self.x_change = -min(PLAYER_SPEED, self.rect.x - self.target_x)
            if self.rect.y < self.target_y:
                self.y_change = min(PLAYER_SPEED, self.target_y - self.rect.y)
            elif self.rect.y > self.target_y:
                self.y_change = -min(PLAYER_SPEED, self.rect.y - self.target_y)
            # chegou na posicao alvo
            if self.rect.x == self.target_x and self.rect.y == self.target_y:
                self.moving = False
    # verifica e corrige colisao com blocos
    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits += [npc for npc in self.game.all_sprites if (isinstance(npc, NPC) or isinstance(npc, NPC2)) and self.rect.colliderect(npc.rect)]
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            hits += [npc for npc in self.game.all_sprites if (isinstance(npc, NPC) or isinstance(npc, NPC2)) and self.rect.colliderect(npc.rect)]
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom
    # metodo para animacao do jogador
    def animation(self):
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # definicao dos frames de animacao para cada direcao
        down_animations = [self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 37, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(34, 37, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(67, 37, self.width, self.height, bg_colors)]
        up_animations = [self.game.character_spritesheet.get_sprite(83, 1, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 106, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(34, 106, self.width, self.height, bg_colors),
                          self.game.character_spritesheet.get_sprite(67, 106, self.width, self.height, bg_colors)]
        left_animations = [self.game.character_spritesheet.get_sprite(34, 3, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 72, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(50, 72, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(99, 72, 47, 32, bg_colors)]
        right_animations = [self.game.character_spritesheet.get_sprite(116, 3, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(1, 143, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(50, 143, 47, 32, bg_colors),
                          self.game.character_spritesheet.get_sprite(99, 143, 47, 32, bg_colors)]
        # atualiza a imagem do jogador de acordo com a direcao e movimento
        if self.facing == "down":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(1, 1, self.width, self.height, bg_colors)
            else:
                self.image = down_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "up":
            if self.y_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(83, 1, self.width, self.height, bg_colors)
            else:
                self.image = up_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "left":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(34, 3, 47, 32, bg_colors)
            else:
                self.image = left_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1
        if self.facing == "right":
            if self.x_change == 0:
                self.image = self.game.character_spritesheet.get_sprite(116, 3, 47, 32, bg_colors)
            else:
                self.image = right_animations[math.floor(self.animation_loop)]
                self.animation_loop += 0.3
                if self.animation_loop >= 3:
                    self.animation_loop = 1

# classe para inimigos, que herda de Sprite
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_name):
        bg_colors = [CHARACTER_BG]
        self.game = game
        self.enemy_name = enemy_name
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites, self.game.enemy
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = 64
        self.height = 64
        # carrega a spritesheet e os frames de animacao do inimigo
        self.spritesheet = Spritesheet(enemy_spritesheets[enemy_name])
        self.animation_frames = enemy_animations[enemy_name]
        self.animation_loop = 0
        img = self.spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    # metodo chamado a cada frame para atualizar o estado do inimigo
    def update(self):
        self.animate()
        self.random_movement()
    # metodo para animacao do inimigo
    def animate(self):
        frame = self.animation_frames[math.floor(self.animation_loop)]
        img = self.spritesheet.get_sprite(frame[0], frame[1], self.width, self.height, [CHARACTER_BG])
        self.image = pygame.transform.scale(img, (32, 32))
        self.animation_loop += 0.3
        if self.animation_loop >= len(self.animation_frames):
            self.animation_loop = 0
    # movimentacao aleatoria do inimigo
    def random_movement(self):
        if random.random() < 0.02:
            dx, dy = random.choice([(0, -TILESIZE), (0, TILESIZE), (-TILESIZE, 0), (TILESIZE, 0)])
            next_rect = self.rect.copy()
            next_rect.x += dx
            next_rect.y += dy
            # verifica se o movimento eh valido (sem colisao)
            if not any(next_rect.colliderect(block.rect) for block in self.game.blocks) and \
               not any(next_rect.colliderect(enemy.rect) for enemy in self.game.enemy if enemy != self):
                self.rect.x += dx
                self.rect.y += dy

# classe para o chao, que herda de Sprite
class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self. game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # carrega a imagem do chao a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(518, 2442, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para o chao alternativo, que herda de Sprite
class Ground2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self. game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # carrega a imagem do chao alternativo a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(518, 4722, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para arvores, que herda de Sprite
class Tree1(pygame.sprite.Sprite):
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
        # carrega a imagem da arvore a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2570, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y    

# classe para arvores alternativas, que herda de Sprite
class Tree2(pygame.sprite.Sprite):
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
        # carrega a imagem da arvore alternativa a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(1130, 2602, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
# classe para arvores especiais, que herda de Sprite
class Tree3(pygame.sprite.Sprite):
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
        # carrega a imagem da arvore especial a partir da spritesheet
        self.image = self.game.tree_spritesheet.get_sprite(0, 0, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para portais, que herda de Sprite
class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.portals
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # carrega a imagem do portal a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(550, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para portais fechados, que herda de Sprite
class ClosedPortal(pygame.sprite.Sprite):
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
        # carrega a imagem do portal fechado a partir da spritesheet
        self.image = self.game.terrain_spritesheet.get_sprite(582, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para itens de cura, que herda de Sprite
class ItemCuraSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item_cura):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.item_cura = item_cura
        # caminhos das imagens dos itens de cura
        imagens = {
            "Curativo": "img/curativo.png",
            "Pomada": "img/pomada.png",
            "Xarope": "img/xarope.png",
            "Chá Natural": "img/cha.png"
        }
        img_path = imagens.get(item_cura.nome, "img/curativo.png")
        img = pygame.image.load(img_path).convert()
        img.set_colorkey((184, 200, 168))
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para itens de cura na interface, que herda de Sprite
class HudItemCuraSprite(pygame.sprite.Sprite):
    def __init__(self, hud_x, hud_y, img_path, quantidade):
        super().__init__()
        img = pygame.image.load(img_path).convert()
        img.set_colorkey((184, 200, 168))
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect(topleft=(hud_x, hud_y))
        self.quantidade = quantidade

    # metodo para desenhar o item na tela
    def draw(self, surface, font):
        surface.blit(self.image, self.rect)
        qtd_surface = font.render(f"x{self.quantidade}", True, (255,255,255))
        surface.blit(qtd_surface, (self.rect.right - 18, self.rect.bottom - 18))

# classe para npcs, que herda de Sprite
class NPC(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="X"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a spritesheet do npc
        self.spritesheet = Spritesheet("img/carlos.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para npcs alternativos, que herda de Sprite
class NPC2(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol="Y"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a spritesheet do npc alternativo
        self.spritesheet = Spritesheet("img/will.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para a camera, que controla o deslocamento da tela
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    # aplica o deslocamento da camera ao objeto
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    # atualiza a posicao da camera de acordo com o alvo
    def update(self, target):
        x = -target.rect.centerx + WIN_WIDTH // 2
        y = -target.rect.centery + WIN_HEIGHT // 2
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIN_WIDTH), x)
        y = max(-(self.height - WIN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
    # retorna a posicao na tela de um retangulo no mundo
    def get_screen_pos(self, rect):
        return rect.centerx + self.camera.x, rect.centery + self.camera.y

# classe para o sabonete, que herda de Sprite
class Sabonete(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        # carrega a imagem do sabonete a partir da spritesheet
        img = self.game.sabonete_spritesheet.get_sprite(0, 0, 64, 64, bg_colors)
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

# classe para a tocha, que herda de Sprite
class TochaSprite(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a imagem da tocha
        img = pygame.image.load("img/tocha.png").convert()
        img.set_colorkey((184, 200, 168))
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y