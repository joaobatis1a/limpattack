import pygame
from config import *
from sprites.sprites_base import *

# define o tilemap da tenda, 25x25, borda escura
tilemap = [
    'XXXXXXXXXXXXXXXXXXXXXXXXXX',
    'X.YCCQA.B.B.L.u.u.M....L.X',
    'X........................X',
    'X........................X',
    'X........................X',
    'X........................X',
    'X.........III............X',
    'X........Vp..............X',
    'X.........ZZZ............X',
    'X........................X',
    'X........................X',
    'X...........T............X',
    'X............N...........X',
    'XXXXXXXXXXXXX]XXXXXXXXXXXX',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    # instancia os tiles e paredes de sombra
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            GroundT(game, j, i)
            if column == 'N':
                game.player = Player(game, j, i)
                Chao(game, j, i)
            if column == 'X':
                WallShadow(game, j, i)  # parede
            if column == 'C':
                Bad(game, j, i)  # cama
            if column == 'u':
                Movel(game, j, i) #movel
            if column == 'p':
                Mesa(game, j, i) # mesa
            if column == 'Z':
                Cadeira(game, j, i) # cadeira
            if column == 'I':
                Cadeira2(game, j, i) # cadeira 2
            if column == 'V':
                Cadeira3(game, j, i) # cadeira 3
            if column == 'Q':
                Penteadeira(game, j, i) # penteadeira
            if column == 'A':
                Abajur(game, j, i) # abajur
            if column == 'B':
                Bau(game, j, i) # baú
            if column == 'L':
                Planta(game, j, i) # chao
            if column == 'T':
                Tapete(game, j, i)  # tapete
            if column == 'Y':
                Lampada(game, j, i) # chao
            if column == 'M':
                Chamine(game, j, i) # chaminé
            if column == ',':
                GroundT2(game, j, i)  # piso 2
            if column == "]":
                PortalTenda(game, j, i, tenda_num=4) # portal de volta
    mapas_visitados[mapa_atual_index] = True  # marca tenda como visitada

    # Controle persistente do spawn da tocha na tenda 4
    if not hasattr(game, "tocha_coletada_tenda4"):
        game.tocha_coletada_tenda4 = False
    if not game.tocha_coletada_tenda4:
        TochaSprite(game, 12, 22)  # ajuste a posição se necessário

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
        self.image = self.game.terrain_spritesheet.get_sprite(2226, 2118, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class GroundT2(pygame.sprite.Sprite):
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
        self.image = self.game.terrain_spritesheet.get_sprite(518, 4722, self.width, self.height, bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bad(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(484, 1781, (515-484), (1847-1781), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Lampada(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(1006, 1927, (1025-1006), (1989-1927), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Planta(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(487, 3086, (515-487), (3145-3086), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Movel(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(940, 1746, (994-940), (1812-1746), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cadeira(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(714, 4085, (741-714), (4123-4085), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cadeira2(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(682, 4095, (709-682), (4139-4095), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Cadeira3(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(615, 4090, (645-615), (4131-4090), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Penteadeira(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(292, 3146, (322-293), (3208-3146), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Abajur(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(1516, 3242, (1547-1516), (3273-3242), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Bau(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(427, 3162, (477-427), (3194-3162), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Tapete(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(356, 2868, (451-356), (2943-2868), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Mesa(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(264, 1656, (354-264), (1720-1656), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chamine(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(888, 2890, (951-888), (2950-2890), bg_colors)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Chao(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        bg_colors = [TERRAIN_BG]
        self.image = self.game.terrain_spritesheet.get_sprite(34, 1190, 32, 32, bg_colors)
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
        self.height = TILESIZE
        bg_colors = [CHARACTER_BG, ENEYMY_BG, TERRAIN_BG]
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill((0, 0, 0, 50))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y