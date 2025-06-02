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
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTM',
    'pN..............................U......M',
    't.........1............................M',
    'M....R..E...........R..2...............M',
    'M..........................1...........M',
    'M1...............................R.....M',
    'M..U2.....R....................E.......M',
    'M......................................M',
    'M.....R.........2........R.......2.....M',
    'M.1....................................M',
    'M......................................M',
    'M.......1............1.................M',
    'M..2......E............................M',
    'M................R........1.......2....M',
    'M.....R................................M',
    'M............2.........................M',
    'M...1.......................1..........M',
    'M.............................E........M',
    'M...................................R..M',
    'M.......1........R.....................M',
    'M......................................M',
    'M...............................U......M',
    'M..1..1..1..1..1..1..1..1..1..1..1..1..M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M............E.........................M',
    'M......................................T',
    'M...............................U......p',
    'Mttttttttttttttttttttttttttttttttttttttt',
]

# tilemap = [
#     'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTM',
#     'pNp.............................U......M',
#     't.........1............................M',
#     'M....R..............R..2...............M',
#     'M..........................1...........M',
#     'M1...............................R.....M',
#     'M..U2.....R............................M',
#     'M......................................M',
#     'M.....R.........2........R.......2.....M',
#     'M.1....................................M',
#     'M......................................M',
#     'M.......1............1.................M',
#     'M..2...................................M',
#     'M................R........1.......2....M',
#     'M.....R................................M',
#     'M............2.........................M',
#     'M...1.......................1..........M',
#     'M......................................M',
#     'M...................................R..M',
#     'M.......1........R.....................M',
#     'M......................................M',
#     'M...............................U......M',
#     'M..1..1..1..1..1..1..1..1..1..1..1..1..M',
#     'M......................................M',
#     'M......................................M',
#     'M......................................M',
#     'M................U.....................M',
#     'M......................................T',
#     'M......................................p',
#     'Mttttttttttttttttttttttttttttttttttttttt',
# ]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    # percorre cada linha e coluna do tilemap
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)  # cria o chao em todas as posicoes
            if random.random() < 0.50:
                nivel = random.randint(1, 2)
                DirtSprite(game, j, i, nivel) 
            if column == ",":
                Ground2(game, j, i)  # cria um tipo diferente de chao
            if column == "N":
                game.player = Player(game, j, i)
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
                pos = (j, i)
                if not hasattr(game, 'itens_cura_coletados'):
                    game.itens_cura_coletados = set()
                if pos not in game.itens_cura_coletados:
                    item_cura = random.choices(itens_cura, weights=[50, 30, 10, 10])[0]
                    ItemCuraSprite(game, j, i, item_cura)
            if column == "1":
                Tronco1(game, j, i)
            if column == "2":
                Tronco2(game, j, i)
            if column == "R":
                Pedra(game, j, i)
            
    mapas_visitados[mapa_atual_index] = True  # marca o mapa atual como visitado

class Tronco1(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(390, 551, (483-390), (577-551), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tronco2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(485, 548, (515-485), (641-548), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Pedra(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(582, 386, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y