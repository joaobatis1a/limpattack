import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTM',
    'pN.Z......u.................E..........M',
    't.........u.uuuuuu.uuu.uuuuuuuu.uuuuuu.M',
    'M.........u.uuuuUu.u.u.uuuuuuuu.uuuuuu.M',
    'M.........u..E...u.u.u.u..E.....uuuuuu.M',
    'M.........uuuuuuuu.u.u.uuuuuuuuuu......M',
    'M..................uuu.uuuuuuuuuu.uuuuuM',
    'Muuuuuuuuuuuuuuuuuuu...u...............M',
    'Muuuuuuuuuuuuuuuuuuuuuuu...............M',
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
    'M......................................p',
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
            if column == "U":
                item_cura = random.choices(itens_cura, weights=[60, 30, 8, 2])[0]
                ItemCuraSprite(game, j, i, item_cura)
            if column == "u":
                Toco(game, j, i)
            if column == "Z":
                Tenda(game, j, i)
    mapas_visitados[mapa_atual_index] = True

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