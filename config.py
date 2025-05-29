# todas as variaveis globais deste arquivo sao usadas para configurar o jogo
# os valores de largura e altura da janela sao metade dos valores originais
# tilesize define o tamanho de cada bloco do mapa em pixels
# fps define a taxa de quadros por segundo do jogo
# as constantes *_LAYER definem a ordem de desenho dos sprites
# player_speed define a velocidade do jogador
# as constantes de cor sao usadas para desenhar elementos graficos
# fases indica se cada fase do jogo esta ativa ou nao
# todos os comentarios estao em minusculo e sem acento para facilitar entendimento da equipe

# define as dimensoes da janela do jogo
WIN_WIDTH = 1280/2 # largura da janela = 640
WIN_HEIGHT = 960/2 # altura da janela = 480
# define o tamanho de cada tile do mapa
TILESIZE = 32
# define o numero de frames por segundo
FPS = 30

# define as camadas de renderizacao dos sprites
PLAYER_LAYER = 3 # camada do jogador
BLOCK_LAYER = 2  # camada de blocos/obstaculos
GROUND_LAYER = 1 # camada do chao

# define a velocidade do jogador
PLAYER_SPEED = 10

# define as cores usadas no jogo em formato RGB
RED = (255,0,0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_ORANGE = (255, 204, 102)
CHARACTER_BG = (184, 200, 168) # cor de fundo do personagem
ENEYMY_BG = (0, 0, 0)          # cor de fundo do inimigo
TERRAIN_BG = (0, 0, 0)         # cor de fundo do terreno

# lista que indica se cada fase esta ativa
fases =  [True, True, True, True, True, True]
