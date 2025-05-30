import pygame
from config import *
from battleData import *
from sprites.sprites_base import *
from npcs import npcs_data
import random

tilemap = [
    'MTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTM',
    'MN...................,.................M',
    'M,,,,,,,,,,,,,,,,,,,.,,,,,,,,,,,,,,,,,,M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M..................,.,.................M',
    'M,,,,,,,,,,,,,,,,,,,.,,,,,,,,,,,,,,,,,,M',
    'M......................................M',
    'M...................E..................p',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'M......................................M',
    'MttttttttttttttttttttttttttttttttttttttM',
]

def create_tiled_map(game, mapa_atual_index, mapas_visitados, fases, enemies, itens_cura):
    for i, row in enumerate(tilemap):
        for j, column in enumerate(row):
            Ground(game, j, i)
            if column == ",":
                ParedeInv(game, j, i)
            if column == "N":
                game.player = Player(game, j, i)
            if column == "E" and fases[mapa_atual_index]:
                enemy_name = "Rei Mundiça"
                ReiMundicaEvento(game, j, i)
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
            
            # Gradiente preto de cima para baixo (vertical) mais suaveAdd commentMore actions
    grad_end = len(tilemap) - 20  # agora só os últimos 15 blocos são totalmente pretos
    grad_steps = grad_end if grad_end > 0 else 1 
    for i in range(grad_end):
        # Suave: alpha vai de 0 até 240 (deixa espaço para o preto total)
        alpha = int((i / (grad_steps - 1)) * 240)
        for j in range(len(tilemap[0])):
            BlackBlockGrad(game, j, i, alpha)

    # Últimos 15 blocos totalmente pretos
    for i in range(len(tilemap) - 20, len(tilemap)):
        for j in range(len(tilemap[0])):
            BlackBlockGrad(game, j, i, 255)

    mapas_visitados[mapa_atual_index] = True

# Classes de blocos pretos com opacidades diferentes (gradiente vertical)
class BlackBlockGrad(pygame.sprite.Sprite):
    def __init__(self, game, x, y, alpha):
        self.game = game
        self._layer = MID_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, alpha))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
class Path(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = UP_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.image.fill((255, 255, 255, 20))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y