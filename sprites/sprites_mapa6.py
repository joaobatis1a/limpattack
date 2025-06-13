import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
    'i..i...........M.R.T.K..............i..i',
    'i..i..........J.......O.............i..i',
    'i..i..........C...P...U.............i..i',
    'i..i..........W.......E.............i..i',
    'i..i................................i..i',
    'i..iiiiiiiiiiiiiii.iiiiiiiiiiiiiiiiii..i',
    'i................i.i...................i',
    'i..........iiiiiii.i...................i',
    'i..........i.......i...................i',
    'i..........i.iiiiiii...................i',
    'i..........i.i.........................i',
    'i..........i.i.........................i',
    'i..........i.i.........................i',
    'i...+......i.i.........................i',
    'i..........i.i.........................i',
    'i..........i.iiiiiiiiiiiiiiiii.........i',
    'i....%.....i.................i.........i',
    'i..........iiiiiiiiiiiiiiiii.i.........i',
    'i..........................i.i./.......i',
    'i..............=...........i.i.........i',
    'i.....-....................i.i.........i',
    'i..........................i.i.........i',
    'iiiiiiiiiiiiiiiiiiiiiiiiiiii.i.........i',
    'pN...........................i.........i',
    'iiiiiiiiiiiiiiiiiiiiiiiiiiiiii.........i',
    'i......................................i',
    'i......................................i',
    'i......................................i',
    'iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Chao(game, j, i)
            if column == "N":
                game.player = Player(game, j, i)
            if column == "p":
                ClosedPortal(game, j, i)
            if column == "p" and len(game.enemy) == 0:
                Portal(game, j, i)
            if column == "i":
                ParedeInv(game, j, i)
            if column == "U":
                Piu(game, j, i)
            if column == "W":
                Will(game, j, i)
            if column == "T":
                Tigre(game, j, i)
            if column == "R":
                Rino(game, j, i)
            if column == "M":
                Mamute(game, j, i)
            if column == "K":
                Kaiki(game, j, i)
            if column == "O":
                Ouriço(game, j, i)
            if column == "J":
                Porco(game, j, i)
            if column == "E":
                Elefante(game, j, i)
            if column == "C":
                Cavalo(game, j, i)
            if column == "P":
                NPC9(game, j, i, symbol="P")
            if column == "-":
                AgCdt(game, j, i)
            if column == "+":
                GaCdt(game, j, i)
            if column == "/":
                GsCdt(game, j, i)
            if column == "=":
                JbCdt(game, j, i)
            if column == "%":
                PbCdt(game, j, i)

    mapas_visitados[mapa_atual_index] = True

class Chao(pygame.sprite.Sprite):
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
        self.image = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Piu(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a spritesheet do npc
        self.spritesheet = Spritesheet(resource_path("img/piu_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((160, 192, 144))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Will(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a spritesheet do npc
        self.spritesheet = Spritesheet(resource_path("img/will_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tigre(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/tigre_s.png"))
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(160, 192, 144)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Rino(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/rino_s.png"))
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(0, 176, 0)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mamute(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/mamute_s.png"))
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(0, 176, 0)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Kaiki(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/kaiki_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((184, 200, 168))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Ouriço(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/carlos_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Porco(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/jr_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 176, 120))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Elefante(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/elefante_s.png"))
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(0, 176, 0)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cavalo(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/cavalo_s.png"))
        sprite = self.spritesheet.get_sprite(0, 0, 64, 64, [(0, 184, 0)])  # ajuste a cor do fundo conforme necessário
        self.image = pygame.transform.scale(sprite, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class NPC9(pygame.sprite.Sprite):
    def __init__(self, game, x, y, symbol = "P"):
        self.game = game
        self.symbol = symbol
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        # carrega a spritesheet do npc
        self.spritesheet = Spritesheet(resource_path("img/kaua_s.png"))
        self.image = self.spritesheet.get_sprite(1, 1, self.width, self.height, [])
        self.image.set_colorkey((0, 184, 0))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class AgCdt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/ag_cdt.png"))
        self.image = self.spritesheet.get_sprite(0, 0, 96, 64, [(0,184,0)])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GaCdt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/ga_cdt.png"))
        self.image = self.spritesheet.get_sprite(0, 0, 96, 64, [(0,184,0)])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GsCdt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/gs_cdt.png"))
        self.image = self.spritesheet.get_sprite(0, 0, 96, 64, [(0,184,0)])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class JbCdt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/jb_cdt.png"))
        self.image = self.spritesheet.get_sprite(0, 0, 96, 64, [(0,184,0)])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class PbCdt(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.spritesheet = Spritesheet(resource_path("img/pb_cdt.png"))
        self.image = self.spritesheet.get_sprite(0, 0, 96, 64, [(0,184,0)])
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y