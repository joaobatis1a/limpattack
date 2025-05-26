import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT',
    'pN,...Z.....Z.....Z....Z......Z.....,3,p',
    't.,.................................,uut',
    'M.,.................................,..M',
    'M.,.................................,..M',
    'M.,.....+.....+.....+....+......+...,..M',
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
                enemy_name = random.choice(list(enemies.keys()))
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
            if column == "4":
                NPCTenda1(game, j, i, symbol="G")
                Ground2(game, j, i)
            if column == "5":
                NPCTenda2(game, j, i, symbol="H")
                Ground2(game, j, i)
            if column == "6":
                NPCTenda3(game, j, i, symbol="I")
                Ground2(game, j, i)
            if column == "7":
                NPCTenda4(game, j, i, symbol="J")
                Ground2(game, j, i)
            if column == "8":
                NPCTenda5(game, j, i, symbol="K")
                Ground2(game, j, i)
            if column == "!":
                TochaSprite(game, j, i)
    mapas_visitados[mapa_atual_index] = True

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
        self.spritesheet = Spritesheet("img/kaiki.png")
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

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