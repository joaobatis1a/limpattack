# este arquivo contem a classe principal do jogo e a logica de troca de mapas
# importa bibliotecas principais, modulos de sprites, dados de batalha e npcs
# mapas contem os dados de cada mapa do jogo, cada um com seu tilemap e funcao de criacao
# classe Game gerencia o estado geral do jogo, eventos, atualizacoes, transicoes de mapas e batalhas
# variaveis de instancia controlam sprites, inventario, dialogos, estado de batalha, progresso e flags de controle
# handle_battle gerencia toda a logica da tela de batalha, incluindo imagens, musica e resultado
# new reinicia o mapa atual, recriando todos os sprites e a camera
# verificar_portal checa se o jogador pode trocar de mapa, considerando inimigos restantes e colisao com portais
# events processa eventos do pygame, incluindo dialogos com npcs e saida do jogo
# update atualiza todos os sprites, gerencia dialogos, portais, inimigos e camera
# trocar_mapa troca o mapa atual para o proximo ou anterior, reiniciando o estado
# trocar_para_tenda troca o mapa para o interior de uma tenda, importando dinamicamente o modulo correto
# draw desenha todos os sprites, hud, dialogos e efeitos visuais na tela
# main e o loop principal do jogo, chamando eventos, update e draw
# game_over exibe a tela de game over e permite reiniciar o jogo
# draw_hud_itens_cura desenha o inventario de itens de cura e chaves no hud
# draw_npc_dialog desenha a caixa de dialogo dos npcs na tela
# checar_inimigos retorna a quantidade de inimigos restantes e o total no mapa
# ao final, o jogo e inicializado e o loop principal e executado ate o usuario sair

import pygame
from pygame import mixer
import importlib
from config import *
from sprites import *
from sprites.sprites_base import *
from sprites.sprites_mapa1 import tilemap as tilemap1, create_tiled_map as create_tiled_map1
from sprites.sprites_mapa2 import tilemap as tilemap2, create_tiled_map as create_tiled_map2
from sprites.sprites_mapa3 import tilemap as tilemap3, create_tiled_map as create_tiled_map3
from sprites.sprites_mapa4 import tilemap as tilemap4, create_tiled_map as create_tiled_map4
from sprites.sprites_mapa5 import tilemap as tilemap5, create_tiled_map as create_tiled_map5
from sprites.sprites_mapa6 import tilemap as tilemap6, create_tiled_map as create_tiled_map6
from battleData import *
from battle import *
from npcs import npcs_data
import sys
import random
sys.stdout.reconfigure(encoding='utf-8')

pygame.display.set_caption("LimpAttack")

mapas = [
    {"tilemap": tilemap1, "create": create_tiled_map1},
    {"tilemap": tilemap2, "create": create_tiled_map2},
    {"tilemap": tilemap3, "create": create_tiled_map3},
    {"tilemap": tilemap4, "create": create_tiled_map4},
    {"tilemap": tilemap5, "create": create_tiled_map5},
    {"tilemap": tilemap6, "create": create_tiled_map6},
]

MAPA_SPAWNS = {
    0: {  # mapa 1
        "right": (38, 1),
    },
    1: {  # mapa 2
        "left": (1, 1),    # entrada vinda do mapa 1
        "right": (38, 1),  # entrada vinda do mapa 3
    },
    2: {  # mapa 3
        "left": (1, 1),    # entrada vinda do mapa 2
        "right": (38, 30),  # entrada vinda do mapa 4
    },
    3: {  # mapa 4
        "left": (1, 1),    # entrada vinda do mapa 3
        "right": (38, 30),  # entrada vinda do mapa 5
    },
    4: {  # mapa 5
        "left": (1, 1),
        "right": (38, 24),
    },
    5: {  # mapa 6
        "left": (1, 24), 
    },
}

# esta e a classe principal do jogo, que gerencia o estado geral, eventos, atualizacoes e transicoes
class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        mixer.music.load("sounds/limpattack_ost_base.mp3")
        mixer.music.set_volume(1)
        mixer.music.play(-1)
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain1.png')
        self.tree_spritesheet = Spritesheet('img/tree_Mid.png')
        self.sabonete_spritesheet = Spritesheet('img/sabonete.png')
        self.in_battle = False
        self.battle_started = False
        self.battle_enemy = None
        self.fox_hp = 100
        self.battle_turn = "fox"
        self.inimigos_aviso_exibido = False
        self.trocando_mapa = False
        self.game_over_flag = False
        self.inventario_cura = []
        self.inventario_chave = []
        self.npc_dialog_active = False
        self.npc_dialog_texts = []
        self.npc_dialog_index = 0
        self.npc_dialog_current = ""
        self.npc_dialog_char_index = 0
        self.npc_dialog_speed = 2
        self.npc_dialog_last_update = 0
        self.npc_dialog_btn_rect = None
        self.npc_dialog_npc_symbol = "" 
        self.mapa_atual_index = 0
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        self.fases = [True] * len(mapas)
        self.mapas_visitados = [False] * len(mapas)
        self.sabonete_spawned = False
        self.tocha_spawned = False
        self.npcs_moveram = False
        self.spawn_tocha_apos_dialogo = False
        self.npc_moved = False
        self.sombra_ativa_mapa3 = True
        self.movimento_bloqueado = False
        self.saved_state = None
        self.rei_mundica_derrotado = False
    
    def save_current_state(self):
        self.saved_state = {
            "mapa_atual_index": self.mapa_atual_index,
            "fases": self.fases.copy(),
            "mapas_visitados": self.mapas_visitados.copy(),
            "inventario_cura": [item for item in self.inventario_cura],
            "inventario_chave": [item for item in self.inventario_chave],
            "fox_hp": self.fox_hp,
        }
    
    def restore_saved_state(self):
        # Restaura o estado salvo (após derrota)
        if self.saved_state:
            self.mapa_atual_index = self.saved_state["mapa_atual_index"]
            self.fases = self.saved_state["fases"].copy()
            self.mapas_visitados = self.saved_state["mapas_visitados"].copy()
            self.inventario_cura = [item for item in self.saved_state["inventario_cura"]]
            self.inventario_chave = [item for item in self.saved_state["inventario_chave"]]
            self.fox_hp = self.saved_state["fox_hp"]
            self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
            self.new()

    # essa funcao gerencia a tela de batalha, incluindo a musica, imagens e logica de vitoria/derrota
    def handle_battle(self):
        enemy_battle_images = {
            "Cárie": "img/carie_luta.png",
            "Mão Podre": "img/mao_podre_luta.png",
            "Caspa no Cabelo": "img/caspa_luta.png",
            "Acne": "img/acne_luta.png",
            "Bactéria de Resfriado": "img/resfriado_luta.png",
            "Bactéria do Pé": "img/pe_luta.png",
            "Gordura na Pele": "img/gordura_luta.png",
            "Rei Mundiça": "img/rei_luta.png"
        }
        mixer.music.stop()
        mixer.music.load("sounds/limpattack_ost_luta.mp3")
        mixer.music.set_volume(1)
        mixer.music.play(-1)
        enemy_name = self.battle_enemy.enemy_name
        from copy import deepcopy
        enemy_data = deepcopy(enemies[enemy_name])
        if hasattr(enemy_data, "hp"):
            if hasattr(enemies[enemy_name], "hp"):
                enemy_data.hp = enemies[enemy_name].hp
            else:
                enemy_data.hp = enemy_data.max_hp if hasattr(enemy_data, "max_hp") else 100
        enemy_img = pygame.image.load(enemy_battle_images[enemy_name]).convert()
        enemy_img.set_colorkey((184, 200, 168))
        enemy_img = pygame.transform.scale(enemy_img, (120, 120))
        player_img = pygame.image.load("img/nala_luta.png").convert()
        player_img.set_colorkey((184, 200, 168))
        player_img = pygame.transform.scale(player_img, (120, 120))
        if enemy_name == "Rei Mundiça":
            bg_img = pygame.transform.scale(pygame.image.load("img/boss.luta.png"), (640, 480))
        else:
            bg_img = pygame.transform.scale(pygame.image.load("img/luta_bg.png"), (640, 480))
        itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy_name)
        resultado = battle_screen(
            player_hp=self.fox_hp,
            player_max_hp=100,
            enemy=enemy_data,
            enemy_img=enemy_img,
            player_img=player_img,
            bg_img=bg_img,
            itens_selecionados=itens_selecionados,
            main_game_over_func=self.game_over,
            inventario_cura=self.inventario_cura
        )
        if isinstance(resultado, int) and resultado > 0:
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_ost_base.mp3")
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        elif resultado == "derrota":
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_tune_vitoria.mp3")
            mixer.music.set_volume(1)
            mixer.music.play()
            self.game_over_flag = True
        else:
            mixer.music.stop()
            mixer.music.load("sounds/limpattack_ost_base.mp3")
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        if isinstance(resultado, int):
            self.fox_hp = resultado
            if self.fox_hp > 0:
                if self.battle_enemy.enemy_name == "Rei Mundiça":
                    self.rei_mundica_derrotado = True
                    self.fases[self.mapa_atual_index] = False  # Marcar fase como concluída antes de reiniciar
                    # Salva a posição da Nala antes de recarregar o mapa
                    player_pos = (self.player.rect.x, self.player.rect.y) if hasattr(self, 'player') and self.player else None
                    self.new()  # recarrega o mapa para mostrar o Path
                    # Restaura a posição da Nala após recarregar o mapa
                    if player_pos and hasattr(self, 'player') and self.player:
                        self.player.rect.x, self.player.rect.y = player_pos
                else:
                    self.battle_enemy.kill()
                    self.fases[self.mapa_atual_index] = False
            else:
                self.game_over_flag = True
        elif resultado == "derrota":
            self.game_over_flag = True
        self.in_battle = False
        self.battle_started = False

    # esta funcao inicia um novo jogo ou reinicia o mapa atual
    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()
        mapas[self.mapa_atual_index]["create"](
            self, self.mapa_atual_index, self.mapas_visitados, self.fases, enemies, itens_cura
        )
        map_width = len(mapas[self.mapa_atual_index]["tilemap"][0]) * TILESIZE
        map_height = len(mapas[self.mapa_atual_index]["tilemap"]) * TILESIZE
        self.camera = Camera(map_width, map_height)
        self.inimigos_total = len(self.enemy)

    # verifica se o jogador colidiu com um portal ou se ainda ha inimigos no mapa
    def verificar_portal(self):
        if len(self.enemy) > 0:
            if not self.inimigos_aviso_exibido:
                print("Ainda há inimigos no mapa! Derrote-os antes de sair.")
                self.inimigos_aviso_exibido = True
            return False
        self.inimigos_aviso_exibido = False
        for portal in self.portals:
            if self.player.rect.colliderect(portal.rect):
                if not self.trocando_mapa:
                    self.trocando_mapa = True
                    if portal.rect.centerx < self.player.rect.centerx:
                        print("tentando trocar para o mapa anterior...")
                        self.trocar_mapa("anterior")
                    else:
                        print("tentando trocar para o proximo mapa...")
                        self.trocar_mapa("proximo")
                return True
        self.trocando_mapa = False
        return False

    # gerencia os eventos do jogo, incluindo entrada do jogador e interacoes com NPCs
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if self.npc_dialog_active:
                if (event.type == pygame.MOUSEBUTTONDOWN and self.npc_dialog_btn_rect and self.npc_dialog_btn_rect.collidepoint(event.pos)) \
                   or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                    if self.npc_dialog_char_index < len(self.npc_dialog_texts[self.npc_dialog_index]):
                        self.npc_dialog_char_index = len(self.npc_dialog_texts[self.npc_dialog_index])
                    else:
                        self.npc_dialog_index += 1
                        if self.npc_dialog_index >= len(self.npc_dialog_texts):
                            self.npc_dialog_active = False
                        else:
                            self.npc_dialog_char_index = 0
                            self.npc_dialog_last_update = pygame.time.get_ticks()

    # atualiza o estado dos sprites e verifica interacoes como colisao com NPCs e inimigos
    def update(self):
        self.all_sprites.update()
        if not self.npc_dialog_active and self.player is not None:
            for sprite in self.all_sprites:
                if hasattr(sprite, 'symbol') and sprite.symbol in npcs_data and self.player.rect.colliderect(sprite.rect):
                    print(f"DEBUG: Colisão detectada com NPC símbolo={sprite.symbol}")
                    npc_symbol = sprite.symbol
                    npc_info = npcs_data.get(npc_symbol)
                    if npc_info and "dialogos" in npc_info:
                        print(f"DEBUG: Diálogo encontrado para NPC símbolo={npc_symbol}")
                        self.npc_dialog_active = True
                        self.npc_dialog_texts = npc_info["dialogos"]
                        self.npc_dialog_index = 0
                        self.npc_dialog_current = ""
                        self.npc_dialog_char_index = 0
                        self.npc_dialog_last_update = pygame.time.get_ticks()
                        self.npc_dialog_npc_symbol = npc_symbol
                        if hasattr(self.player, "moving"):
                            self.player.moving = False
                    else:
                        print(f"DEBUG: Nenhum diálogo encontrado para NPC símbolo={npc_symbol}")
                break
        if self.npc_dialog_active:
            self.draw_npc_dialog()

        # Move Kauã (NPC 'O') para a esquerda após o diálogo no mapa 5
        if (
            not self.npc_dialog_active
            and self.mapa_atual_index == 4
            and hasattr(self, 'npc_dialog_npc_symbol')
            and self.npc_dialog_npc_symbol == 'O'
        ):
            for sprite in self.all_sprites:
                if (
                    hasattr(sprite, 'symbol')
                    and sprite.symbol == 'O'
                    and not getattr(sprite, 'moved', False)
                ):
                    sprite.rect.x -= 3 * TILESIZE
                    sprite.x = sprite.rect.x
                    sprite.moved = True
                    # Garante que o NPC continue bloqueando se necessário
                    if hasattr(sprite, 'add') and hasattr(self, 'blocks'):
                        sprite.add(self.blocks)
                    break
        if len(self.enemy) == 0:
            for sprite in self.blocks:
                if isinstance(sprite, ClosedPortal):
                    sprite.kill()
                    Portal(self, sprite.rect.x // TILESIZE, sprite.rect.y // TILESIZE)
            # --- LÓGICA DO PATH NO MAPA 5 ---
            if self.mapa_atual_index == 4 and getattr(self, 'rei_mundica_derrotado', False):
                if not hasattr(self, 'path_spawned_mapa5'):
                    self.path_spawned_mapa5 = False
                if not self.path_spawned_mapa5:
                    from sprites.sprites_mapa5 import Path
                    # Remove paredes invisíveis do caminho (linha 24, colunas 20 a 38)
                    for col in range(20, 39):
                        for sprite in list(self.blocks):
                            if sprite.rect.x // TILESIZE == col and sprite.rect.y // TILESIZE == 24 and sprite.__class__.__name__ == 'ParedeInv':
                                sprite.kill()
                    # Cria o Path alinhado, 1 tile de largura para cada coluna
                    for col in range(20, 39):
                        Path(self, col, 24)
                    self.path_spawned_mapa5 = True
        else:
            if self.mapa_atual_index == 4:
                self.path_spawned_mapa5 = False
        # --- FIM DA LÓGICA DO PATH NO MAPA 5 ---
        # --- FADE OUT E REINICIO APÓS DIÁLOGO DA SOMBRA DE KAUÃ (MAPA 6) ---
        if self.mapa_atual_index == 5:
            # Se acabou de sair do diálogo com a sombra de Kauã (símbolo 'P')
            if hasattr(self, 'npc_dialog_npc_symbol') and self.npc_dialog_npc_symbol == 'P' and not self.npc_dialog_active:
                self.fade_out_and_restart()
                return
        if self.verificar_portal():
            print("jogador colidiu com um portal.")
        if self.player is not None:
            self.camera.update(self.player)
        if hasattr(self, "spawn_tocha_apos_dialogo") and self.spawn_tocha_apos_dialogo and not self.npc_dialog_active and not self.tocha_spawned:
            TochaSprite(self, 38, 4)
            self.spawn_tocha_apos_dialogo = False
            self.tocha_spawned = True
        if self.mapa_atual_index == 2:
            if len(self.enemy) == 0:
                self.sombra_ativa_mapa3 = False
            else:
                self.sombra_ativa_mapa3 = True

    # troca o mapa atual pelo proximo ou anterior na lista de mapas
    def trocar_mapa(self, direcao="proximo"):
        self.save_current_state()  # <--- SALVA ANTES DE TROCAR
        anterior = self.mapa_atual_index
        if direcao == "proximo":
            if self.mapa_atual_index < len(mapas) - 1:
                self.mapa_atual_index += 1
            else:
                print("ja esta no ultimo mapa. nao e possivel avancar.")
                return
            entrada = "left"  # vindo da esquerda ao avançar
        elif direcao == "anterior":
            if self.mapa_atual_index > 0:
                self.mapa_atual_index -= 1
            else:
                print("ja esta no primeiro mapa. nao e possivel voltar.")
                return
            entrada = "right"  # vindo da direita ao voltar
        else:
            entrada = "left"
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        print(f"mudando para o mapa {self.mapa_atual_index + 1}")
        self.new()
        # Após criar o novo mapa, posicione a Nala no ponto correto
        spawn = MAPA_SPAWNS.get(self.mapa_atual_index, {}).get(entrada)
        if spawn and hasattr(self, "player") and self.player:
            self.player.rect.x = spawn[0] * TILESIZE
            self.player.rect.y = spawn[1] * TILESIZE

    # troca o mapa para o interior de uma tenda
    def trocar_para_tenda(self, tenda_num):
        import importlib
        if self.mapa_atual_index is None:
            self.mapa_atual_index = 1
            self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
            self.new()
            if hasattr(self, "tenda_entrada_num") and hasattr(self, "tenda_entrada_pos"):
                for sprite in self.all_sprites:
                    if hasattr(sprite, "tenda_num") and sprite.tenda_num == self.tenda_entrada_num:
                        self.player.rect.x = sprite.rect.x
                        self.player.rect.y = sprite.rect.y + 2*TILESIZE
                        break
            return
        self.tenda_entrada_num = tenda_num
        for sprite in self.all_sprites:
            if hasattr(sprite, "tenda_num") and sprite.tenda_num == tenda_num:
                self.tenda_entrada_pos = (sprite.rect.x, sprite.rect.y)
                break
        modulo = importlib.import_module(f'sprites.tendas.mapa_tenda{tenda_num}')
        self.mapa_atual = getattr(modulo, 'tilemap', None)
        self.mapa_atual_index = None
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()
        modulo.create_tiled_map(self, 0, [False], [True], {}, [])

    # desenha os sprites na tela, incluindo o fundo, personagens e elementos do mapa
    def draw(self):
        self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # Desenha a sombra primeiro
        if self.mapa_atual_index == 2 and getattr(self, "sombra_ativa_mapa3", True):
            darkness = pygame.Surface((int(WIN_WIDTH), int(WIN_HEIGHT)), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, 255))
            nala_screen_x, nala_screen_y = self.camera.get_screen_pos(self.player.rect)
            max_radius = 150
            min_radius = 78
            for r in range(max_radius, min_radius, -1):
                alpha = int(255 * ((r - min_radius) / (max_radius - min_radius)))
                pygame.draw.circle(
                    darkness,
                    (0, 0, 0, alpha),
                    (int(nala_screen_x), int(nala_screen_y)),
                    r
                )
            pygame.draw.circle(darkness, (0, 0, 0, 0), (int(nala_screen_x), int(nala_screen_y)), min_radius)
            self.screen.blit(darkness, (0, 0))

        # Agora desenha o diálogo por cima da sombra
        if self.npc_dialog_active:
            self.draw_npc_dialog()

        self.draw_hud_itens_cura()

        # Remover contador de inimigos apenas no mapa 5
        if self.mapa_atual_index != 4:
            restantes = len(self.enemy)
            total = getattr(self, "inimigos_total", restantes)
            if total > 0:
                font = pygame.font.SysFont("arial", 22, bold=True)
                texto = f"Inimigos: {restantes}/{total}"
                text_surface = font.render(texto, True, (255, 255, 255))
                padding = 16
                self.screen.blit(
                    text_surface,
                    (WIN_WIDTH - text_surface.get_width() - padding, padding)
                )

        self.clock.tick(FPS)
        pygame.display.update()

    # loop principal do jogo, gerencia a ordem de eventos, atualizacoes e desenho na tela
    def main(self):
        while self.playing:
            self.events()
            self.update()
            self.draw()
            if not any(isinstance(s, Player) for s in self.all_sprites):
                self.playing = False
                self.game_over_flag = True
            break

    # gerencia a tela de game over, incluindo opcoes de reinicio
    def game_over(self):
        font = pygame.font.SysFont("Arial", 80)
        small_font = pygame.font.SysFont("Arial", 40)
        alpha = 0
        fade_in = True
        while self.game_over_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.game_over_flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_over_flag = False
                        self.playing = True
                        mixer.music.stop()
                        mixer.music.load("sounds/limpattack_ost_base.mp3")
                        mixer.music.set_volume(1)
                        mixer.music.play(-1)
                        self.restore_saved_state()  # <--- RESTAURA O ESTADO SALVO
                        return
            self.screen.fill(BLACK)
            if fade_in:
                alpha += 5
                if alpha >= 255:
                    alpha = 255
                    fade_in = False
            else:
                alpha -= 2
                if alpha <= 100:
                    fade_in = True
            text_surface = font.render("GAME OVER", True, (255, 0, 0))
            text_surface.set_alpha(alpha)
            rect = text_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 50))
            self.screen.blit(text_surface, rect)
            info_surface = small_font.render("aperte R para voltar a recuperar a higiene", True, (255, 255, 255))
            info_rect = info_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50))
            self.screen.blit(info_surface, info_rect)
            pygame.display.update()
            self.clock.tick(FPS)

    def intro_screen(self):
        import math
        # Tela inicial do jogo com botão estilizado e transição fade-out
        # Fonte pixelada para o título (tenta usar uma fonte pixel, senão usa Arial)
        try:
            title_font = pygame.font.Font("img/pixel.ttf", 72)
        except Exception as e:
            print(f"Erro ao carregar fonte pixel para o título: {e}")
            title_font = pygame.font.SysFont("Arial", 72, bold=True)
        # Fonte pixelada para o botão (tenta usar uma fonte pixel, senão usa Arial)
        try:
            button_font = pygame.font.Font("img/pixel.ttf", 36)
        except:
            button_font = pygame.font.SysFont("Arial", 36, bold=True)
        running_intro = True
        button_w, button_h = 160, 44
        button_x = (WIN_WIDTH - button_w) // 2
        button_y = WIN_HEIGHT // 2 + 30
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        fade_out = False
        fade_alpha = 0
        fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        try:
            bg_img = pygame.image.load("img/tela_inicio.png").convert()
            bg_img = pygame.transform.scale(bg_img, (WIN_WIDTH, WIN_HEIGHT))
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo da intro: {e}")
            bg_img = None
        while running_intro:
            if bg_img:
                self.screen.blit(bg_img, (0, 0))
            else:
                self.screen.fill((30, 30, 60))
            # --- ANIMAÇÃO DO TÍTULO ---
            t = pygame.time.get_ticks() / 700.0
            float_offset = int(12 * math.sin(t))  # Oscilação vertical
            # Interpolação de cor entre amarelo e azul
            c1 = (254, 217, 102)
            c2 = (28, 69, 135)
            interp = (math.sin(t) + 1) / 2  # 0..1
            color = (
                int(c1[0] * interp + c2[0] * (1 - interp)),
                int(c1[1] * interp + c2[1] * (1 - interp)),
                int(c1[2] * interp + c2[2] * (1 - interp))
            )
            title_surface = title_font.render("LimpAttack", True, color)
            title_rect = title_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80 + float_offset))
            title_surface = pygame.transform.smoothscale(title_surface, (int(title_rect.width * 0.75), int(title_rect.height * 0.75)))
            title_rect = title_surface.get_rect(center=(WIN_WIDTH // 2, WIN_HEIGHT // 2 - 80 + float_offset))
            self.screen.blit(title_surface, title_rect)
            # --- RESTANTE DA FUNÇÃO (botão, fade, eventos) ---
            mouse_pos = pygame.mouse.get_pos()
            mouse_over = button_rect.collidepoint(mouse_pos)
            button_color = (60, 220, 120) if mouse_over else (255, 255, 255)
            text_color = (255, 255, 255) if mouse_over else (30, 30, 60)
            # Pixel art style: sombra
            sombra_offset = 4
            sombra_rect = button_rect.move(sombra_offset, sombra_offset)
            pygame.draw.rect(self.screen, (0, 0, 0), sombra_rect, 0)  # sombra preta
            # Pixel art style: botão principal (sem border_radius, bordas retas)
            pygame.draw.rect(self.screen, button_color, button_rect, 0)
            # Pixel art style: contorno preto grosso
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 4)
            # Pixel art style: contorno branco fino interno
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect.inflate(-8, -8), 2)
            button_text = button_font.render("INICIAR", True, text_color)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            # --- PIXEL ART BUTTON ESTILO POKEMON ---
            # Paleta de cores
            cor_fundo = (28, 69, 135) if mouse_over else (58, 89, 175)  # verde escuro/claro
            cor_borda = (0, 0, 0)  # preto
            cor_highlight = (255, 255, 255)  # branco
            cor_shadow = (48, 96, 48)  # verde sombra
            # Sombra "pixelada" embaixo
            shadow_rect = button_rect.move(0, 6)
            pygame.draw.rect(self.screen, cor_shadow, shadow_rect, 0)
            # Contorno preto grosso
            pygame.draw.rect(self.screen, cor_borda, button_rect.inflate(6, 6), 0)
            # Botão principal
            pygame.draw.rect(self.screen, cor_fundo, button_rect, 0)
            # Destaque branco em cima
            highlight_rect = pygame.Rect(button_rect.x+4, button_rect.y+4, button_rect.width-8, 10)
            pygame.draw.rect(self.screen, cor_highlight, highlight_rect, 0)
            # Contorno preto interno
            pygame.draw.rect(self.screen, cor_borda, button_rect, 3)
            # Texto pixelado
            button_text = button_font.render("INICIAR ", True, (30, 30, 60))
            text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, text_rect)
            if fade_out:
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                fade_alpha += 10
                if fade_alpha >= 255:
                    running_intro = False
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running_intro = False
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_over and not fade_out:
                    fade_out = True
            self.clock.tick(FPS)

    def fade_out_and_restart(self, duration_ms=2000):
        fade_surface = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()
        alpha = 0
        start_time = pygame.time.get_ticks()
        while alpha < 255:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            alpha = min(255, int(255 * (elapsed / duration_ms)))
            fade_surface.set_alpha(alpha)
            self.draw()  # Draw current frame
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
        # Reset game state and show intro
        self.__init__
        self.new()
        self.intro_screen()

# inicializa o jogo
g = Game()
g.new()
g.intro_screen()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()