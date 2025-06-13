import pygame
from pygame import mixer
import importlib
import os
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
import math

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
    0: { "right": (38, 1), },
    1: { "left": (1, 1), "right": (38, 1), },
    2: { "left": (1, 1), "right": (38, 30), },
    3: { "left": (1, 1), "right": (38, 30), },
    4: { "left": (1, 1), "right": (38, 24), },
    5: { "left": (1, 24), },
}

class Game:
    def __init__(self):
        pygame.init()
        mixer.init()
        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.base_surface = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT))
        self.scale_factor = min(self.screen_width / BASE_WIN_WIDTH, self.screen_height / BASE_WIN_HEIGHT)
        self.scaled_width = int(BASE_WIN_WIDTH * self.scale_factor)
        self.scaled_height = int(BASE_WIN_HEIGHT * self.scale_factor)
        self.offset_x = (self.screen_width - self.scaled_width) // 2
        self.offset_y = (self.screen_height - self.scaled_height) // 2
        self.clock = pygame.time.Clock()
        self.running = True
        self.character_spritesheet = Spritesheet(resource_path('img/character.png'))
        self.terrain_spritesheet = Spritesheet(resource_path('img/terrain1.png'))
        self.tree_spritesheet = Spritesheet(resource_path('img/tree_Mid.png'))
        self.sabonete_spritesheet = Spritesheet(resource_path('img/sabonete.png'))
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
        self.save_file = "savegame.dat"
        self.paused = False

        self.pause_button_font = pygame.font.SysFont("arial", 24, bold=True)
        self.pause_button_text = "||"
        self.pause_button_color = GRAY
        self.pause_button_hover_color = LIGHT_ORANGE
        text_surf = self.pause_button_font.render(self.pause_button_text, True, BLACK)
        button_width = text_surf.get_width() + 20
        button_height = text_surf.get_height() + 10
        button_x = (BASE_WIN_WIDTH - button_width) // 2
        button_y = 10
        self.pause_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        mixer.music.load(resource_path("sounds/limpattack_ost_base.mp3"))
        mixer.music.set_volume(1)
        mixer.music.play(-1)

    def get_scaled_mouse_pos(self):
        mx, my = pygame.mouse.get_pos()
        scaled_mx = (mx - self.offset_x) / self.scale_factor
        scaled_my = (my - self.offset_y) / self.scale_factor
        return int(scaled_mx), int(scaled_my)

    def _render_final_screen(self):
        """Função auxiliar para escalar e desenhar a tela final."""
        self.screen.fill(BLACK)
        scaled_surface = pygame.transform.scale(self.base_surface, (self.scaled_width, self.scaled_height))
        self.screen.blit(scaled_surface, (self.offset_x, self.offset_y))
        pygame.display.update()

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
        if self.saved_state:
            self.mapa_atual_index = self.saved_state["mapa_atual_index"]
            self.fases = self.saved_state["fases"].copy()
            self.mapas_visitados = self.saved_state["mapas_visitados"].copy()
            self.inventario_cura = [item for item in self.saved_state["inventario_cura"]]
            self.inventario_chave = [item for item in self.saved_state["inventario_chave"]]
            self.fox_hp = self.saved_state["fox_hp"]
            self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
            self.new()

    def handle_battle(self):
        enemy_battle_images = {
            "Cárie": resource_path("img/carie_luta.png"),
            "Mão Podre": resource_path("img/mao_podre_luta.png"),
            "Caspa no Cabelo": resource_path("img/caspa_luta.png"),
            "Acne": resource_path("img/acne_luta.png"),
            "Bactéria de Resfriado": resource_path("img/resfriado_luta.png"),
            "Bactéria do Pé": resource_path("img/pe_luta.png"),
            "Gordura na Pele": resource_path("img/gordura_luta.png"),
            "Rei Mundiça": resource_path("img/rei_luta.png")
        }
        mixer.music.stop()
        mixer.music.load(resource_path("sounds/limpattack_ost_luta.mp3"))
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
        enemy_img = pygame.image.load(resource_path(enemy_battle_images[enemy_name])).convert()
        enemy_img.set_colorkey((184, 200, 168))
        enemy_img = pygame.transform.scale(enemy_img, (120, 120))
        player_img = pygame.image.load(resource_path('img/nala_luta.png')).convert()
        player_img.set_colorkey((184, 200, 168))
        player_img = pygame.transform.scale(player_img, (120, 120))
        if enemy_name == "Rei Mundiça":
            bg_img = pygame.transform.scale(pygame.image.load(resource_path("img/boss.luta.png")), (640, 480))
        else:
            bg_img = pygame.transform.scale(pygame.image.load(resource_path("img/luta_bg.png")), (640, 480))
        itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy_name)
        resultado = battle_screen(
            self,
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
            mixer.music.load(resource_path("sounds/limpattack_ost_base.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        elif resultado == "vitoria":
            mixer.music.stop()
            mixer.music.load(resource_path("sounds/limpattack_tune_vitoria.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play()
        elif resultado == "derrota":
            mixer.music.stop()
            mixer.music.load(resource_path("sounds/limpattack_tune_derrota.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play()
            self.game_over_flag = True
        if isinstance(resultado, int):
            self.fox_hp = resultado
            if self.fox_hp > 0:
                if self.battle_enemy.enemy_name == "Rei Mundiça":
                    self.rei_mundica_derrotado = True
                    self.fases[self.mapa_atual_index] = False
                    player_pos = (self.player.rect.x, self.player.rect.y) if hasattr(self, 'player') and self.player else None
                    self.new()
                    if player_pos and hasattr(self, 'player') and self.player:
                        self.player.rect.x, self.player.rect.y = player_pos
                else:
                    self.battle_enemy.kill()
                    self.fases[self.mapa_atual_index] = False
            else:
                self.game_over_flag = True
        elif resultado == "derrota":
            self.game_over_flag = True
            self.playing = False
        self.in_battle = False
        self.battle_started = False

    def new(self):
        self.playing = True
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemy = pygame.sprite.LayeredUpdates()
        self.portals = pygame.sprite.LayeredUpdates()
        mapas[self.mapa_atual_index]["create"]( self, self.mapa_atual_index, self.mapas_visitados, self.fases, enemies, itens_cura )
        map_width = len(mapas[self.mapa_atual_index]["tilemap"][0]) * TILESIZE
        map_height = len(mapas[self.mapa_atual_index]["tilemap"]) * TILESIZE
        self.camera = Camera(map_width, map_height)
        self.inimigos_total = len(self.enemy)

    def verificar_portal(self):
        if len(self.enemy) > 0:
            if not self.inimigos_aviso_exibido:
                self.draw_temporary_message("Derrote os inimigos para avançar!")
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

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused

            if self.paused:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = self.get_scaled_mouse_pos()
                    
                    button_width = 200
                    button_height = 40
                    spacing = 15
                    start_y = BASE_WIN_HEIGHT / 2 - 60

                    continue_rect_local = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y, button_width, button_height)
                    restart_rect_local = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y + button_height + spacing, button_width, button_height)
                    quit_rect_local = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y + 2 * (button_height + spacing), button_width, button_height)

                    if continue_rect_local.collidepoint(mouse_pos):
                        self.paused = False
                    elif restart_rect_local.collidepoint(mouse_pos):
                        self.reset_save()  
                        self.paused = False 
                    elif quit_rect_local.collidepoint(mouse_pos):
                        self.playing = False 
                        self.running = False
            
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    scaled_mouse_pos = self.get_scaled_mouse_pos()
                    if self.pause_button_rect.collidepoint(scaled_mouse_pos):
                        self.paused = True 
                
                if self.npc_dialog_active:
                    should_advance = False

                    if event.type == pygame.MOUSEBUTTONDOWN and self.npc_dialog_btn_rect:
                        scaled_mouse_pos = self.get_scaled_mouse_pos()
                        if self.npc_dialog_btn_rect.collidepoint(scaled_mouse_pos):
                            should_advance = True

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        should_advance = True

                    if should_advance:
                        if self.npc_dialog_char_index < len(self.npc_dialog_texts[self.npc_dialog_index]):
                            self.npc_dialog_char_index = len(self.npc_dialog_texts[self.npc_dialog_index])
                        else:
                            self.npc_dialog_index += 1
                            if self.npc_dialog_index >= len(self.npc_dialog_texts):
                                self.npc_dialog_active = False
                            else:
                                self.npc_dialog_char_index = 0
                                self.npc_dialog_last_update = pygame.time.get_ticks()
                            
    def update(self):
        if self.paused:
            return
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
                    if hasattr(sprite, 'add') and hasattr(self, 'blocks'):
                        sprite.add(self.blocks)
                    break
        if len(self.enemy) == 0:
            for sprite in self.blocks:
                if isinstance(sprite, ClosedPortal):
                    sprite.kill()
                    Portal(self, sprite.rect.x // TILESIZE, sprite.rect.y // TILESIZE)
            if self.mapa_atual_index == 4 and getattr(self, 'rei_mundica_derrotado', False):
                if not hasattr(self, 'path_spawned_mapa5'):
                    self.path_spawned_mapa5 = False
                if not self.path_spawned_mapa5:
                    from sprites.sprites_mapa5 import Path
                    for col in range(20, 39):
                        for sprite in list(self.blocks):
                            if sprite.rect.x // TILESIZE == col and sprite.rect.y // TILESIZE == 24 and sprite.__class__.__name__ == 'ParedeInv':
                                sprite.kill()
                    for col in range(20, 39):
                        Path(self, col, 24)
                    self.path_spawned_mapa5 = True
        else:
            if self.mapa_atual_index == 4:
                self.path_spawned_mapa5 = False
        if self.mapa_atual_index == 5:
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

    def trocar_mapa(self, direcao="proximo"):
        self.save_current_state()
        anterior = self.mapa_atual_index
        if direcao == "proximo":
            if self.mapa_atual_index < len(mapas) - 1:
                self.mapa_atual_index += 1
            else:
                print("ja esta no ultimo mapa. nao e possivel avancar.")
                return
            entrada = "left"
        elif direcao == "anterior":
            if self.mapa_atual_index > 0:
                self.mapa_atual_index -= 1
            else:
                print("ja esta no primeiro mapa. nao e possivel voltar.")
                return
            entrada = "right"
        else:
            entrada = "left"
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        print(f"mudando para o mapa {self.mapa_atual_index + 1}")
        self.new()
        spawn = MAPA_SPAWNS.get(self.mapa_atual_index, {}).get(entrada)
        if spawn and hasattr(self, "player") and self.player:
            self.player.rect.x = spawn[0] * TILESIZE
            self.player.rect.y = spawn[1] * TILESIZE
        if self.mapa_atual_index == 4:
            mixer.music.stop()
            mixer.music.load(resource_path("sounds/limpattack_ost_rei.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play(-1)
        if self.mapa_atual_index == 5:
            mixer.music.stop()
            mixer.music.load(resource_path("sounds/limpattack_ost_base.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play(-1)

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

    def draw(self):
        self.base_surface.fill(BLACK)
        for sprite in self.all_sprites:
            self.base_surface.blit(sprite.image, self.camera.apply(sprite))

        if self.mapa_atual_index == 2 and getattr(self, "sombra_ativa_mapa3", True):
            darkness = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT), pygame.SRCALPHA)
            darkness.fill((0, 0, 0, 255))
            nala_screen_x, nala_screen_y = self.camera.get_screen_pos(self.player.rect)
            max_radius, min_radius = 150, 78
            for r in range(max_radius, min_radius, -1):
                alpha = int(255 * ((r - min_radius) / (max_radius - min_radius)))
                pygame.draw.circle(darkness, (0, 0, 0, alpha), (int(nala_screen_x), int(nala_screen_y)), r)
            pygame.draw.circle(darkness, (0, 0, 0, 0), (int(nala_screen_x), int(nala_screen_y)), min_radius)
            self.base_surface.blit(darkness, (0, 0))

        if self.npc_dialog_active:
            self.draw_npc_dialog()

        self.draw_hud_itens_cura()

        if not self.paused:
            self.draw_visual_pause_button()

        if self.paused:
            overlay = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT), pygame.SRCALPHA)
            overlay.fill(MENU_OVERLAY_COLOR)
            self.base_surface.blit(overlay, (0, 0))

            menu_font = pygame.font.SysFont("arial", 40, bold=True)
            button_font = pygame.font.SysFont("arial", 28)

            title_text = menu_font.render("Jogo Pausado", True, WHITE)
            title_rect = title_text.get_rect(center=(BASE_WIN_WIDTH / 2, BASE_WIN_HEIGHT / 2 - 120))
            self.base_surface.blit(title_text, title_rect)

            button_width = 200
            button_height = 40
            spacing = 15
            
            start_y = BASE_WIN_HEIGHT / 2 - 60 

            self.continue_button_rect = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y, button_width, button_height)
            pygame.draw.rect(self.base_surface, LIGHT_ORANGE, self.continue_button_rect, border_radius=10)
            continue_text = button_font.render("Continuar", True, BLACK)
            self.base_surface.blit(continue_text, continue_text.get_rect(center=self.continue_button_rect.center))

            self.restart_button_rect_menu = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y + button_height + spacing, button_width, button_height)
            pygame.draw.rect(self.base_surface, LIGHT_ORANGE, self.restart_button_rect_menu, border_radius=10)
            restart_text = button_font.render("Reiniciar", True, BLACK)
            self.base_surface.blit(restart_text, restart_text.get_rect(center=self.restart_button_rect_menu.center))

            self.quit_button_rect_menu = pygame.Rect(BASE_WIN_WIDTH / 2 - button_width / 2, start_y + 2 * (button_height + spacing), button_width, button_height)
            pygame.draw.rect(self.base_surface, LIGHT_ORANGE, self.quit_button_rect_menu, border_radius=10)
            quit_text = button_font.render("Fechar Jogo", True, BLACK)
            self.base_surface.blit(quit_text, quit_text.get_rect(center=self.quit_button_rect_menu.center))
        
        if self.mapa_atual_index != 4:
            restantes = len(self.enemy)
            total = getattr(self, "inimigos_total", restantes)
            if total > 0:
                font = pygame.font.SysFont("arial", 22, bold=True)
                texto = f"Inimigos: {restantes}/{total}"
                text_surface = font.render(texto, True, WHITE)
                padding = 16
                self.base_surface.blit(text_surface, (BASE_WIN_WIDTH - text_surface.get_width() - padding, padding))

        self._render_final_screen()
        self.clock.tick(FPS)

    # def main(self):
    #     while self.playing:
    #         self.events()
    #         self.update()
    #         self.draw()

    def game_over(self):
        font = pygame.font.SysFont("Arial", 80)
        small_font = pygame.font.SysFont("Arial", 40)
        alpha = 0
        fade_in = True
        
        while self.game_over_flag:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    self.game_over_flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_over_flag = False
                        self.playing = True
                        mixer.music.stop()
                        mixer.music.load(resource_path("sounds/limpattack_ost_base.mp3"))
                        mixer.music.set_volume(1)
                        mixer.music.play(-1)
                        self.restore_saved_state()
                        return

            self.base_surface.fill(BLACK)
            if fade_in:
                alpha = min(alpha + 5, 255)
                if alpha == 255: fade_in = False
            else:
                alpha = max(alpha - 2, 100)
                if alpha == 100: fade_in = True

            text_surface = font.render("GAME OVER", True, (255, 0, 0))
            text_surface.set_alpha(alpha)
            rect = text_surface.get_rect(center=(BASE_WIN_WIDTH // 2, BASE_WIN_HEIGHT // 2 - 50))
            self.base_surface.blit(text_surface, rect)

            info_surface = small_font.render("aperte R para voltar a recuperar a higiene", True, WHITE)
            info_rect = info_surface.get_rect(center=(BASE_WIN_WIDTH // 2, BASE_WIN_HEIGHT // 2 + 50))
            self.base_surface.blit(info_surface, info_rect)
            
            self._render_final_screen()
            self.clock.tick(FPS)

    def intro_screen(self):
        try:
            title_font = pygame.font.Font(resource_path("img/pixel.ttf"), 72)
        except:
            title_font = pygame.font.SysFont("Arial", 72, bold=True)
        try:
            button_font = pygame.font.Font(resource_path("img/pixel.ttf"), 36)
        except:
            button_font = pygame.font.SysFont("Arial", 36, bold=True)
            
        running_intro = True
        button_w, button_h = 200, 50
        button_x = (BASE_WIN_WIDTH - button_w) // 2
        button_y = BASE_WIN_HEIGHT // 2 + 40
        button_rect = pygame.Rect(button_x, button_y, button_w, button_h)
        fade_out = False
        fade_alpha = 0
        fade_surface = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT))
        fade_surface.fill(BLACK)
        
        try:
            bg_img = pygame.image.load(resource_path("img/tela_inicio.png")).convert()
            bg_img = pygame.transform.scale(bg_img, (BASE_WIN_WIDTH, BASE_WIN_HEIGHT))
        except:
            bg_img = None

        while running_intro:
            mouse_pos = self.get_scaled_mouse_pos()
            mouse_over = button_rect.collidepoint(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    running_intro = False
                if event.type == pygame.MOUSEBUTTONDOWN and mouse_over and not fade_out:
                    fade_out = True

            if bg_img:
                self.base_surface.blit(bg_img, (0, 0))
            else:
                self.base_surface.fill((30, 30, 60))

            t = pygame.time.get_ticks() / 700.0
            float_offset = int(12 * math.sin(t))
            c1, c2 = (254, 217, 102), (28, 69, 135)
            interp = (math.sin(t) + 1) / 2
            color = (int(c1[0]*interp + c2[0]*(1-interp)), int(c1[1]*interp + c2[1]*(1-interp)), int(c1[2]*interp + c2[2]*(1-interp)))
            
            title_surface = title_font.render("LimpAttack", True, color)
            title_rect = title_surface.get_rect(center=(BASE_WIN_WIDTH//2, BASE_WIN_HEIGHT//2 - 80 + float_offset))
            self.base_surface.blit(title_surface, title_rect)

            cor_fundo = (28, 69, 135) if mouse_over else (58, 89, 175)
            pygame.draw.rect(self.base_surface, (0,0,0), button_rect.move(0, 6), 0)
            pygame.draw.rect(self.base_surface, (0,0,0), button_rect.inflate(6, 6), 0)
            pygame.draw.rect(self.base_surface, cor_fundo, button_rect, 0)
            highlight_rect = pygame.Rect(button_rect.x+4, button_rect.y+4, button_rect.width-8, 10)
            pygame.draw.rect(self.base_surface, WHITE, highlight_rect, 0)
            pygame.draw.rect(self.base_surface, (0,0,0), button_rect, 3)
            
            button_text = button_font.render("INICIAR", True, WHITE)
            text_rect = button_text.get_rect(center=button_rect.center)
            self.base_surface.blit(button_text, text_rect.move(0,-3))
            
            if fade_out:
                fade_alpha = min(fade_alpha + 10, 255)
                fade_surface.set_alpha(fade_alpha)
                self.base_surface.blit(fade_surface, (0, 0))
                if fade_alpha >= 255:
                    running_intro = False
            
            self._render_final_screen()
            self.clock.tick(FPS)

    def fade_out_and_restart(self, duration_ms=2000):
        fade_surface = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT))
        fade_surface.fill((0, 0, 0))
        clock = pygame.time.Clock()
        alpha = 0
        start_time = pygame.time.get_ticks()
        while alpha < 255:
            now = pygame.time.get_ticks()
            elapsed = now - start_time
            alpha = min(255, int(255 * (elapsed / duration_ms)))
            fade_surface.set_alpha(alpha)
            self.draw()
            self.base_surface.blit(fade_surface, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
        self.reset_save()
        self.intro_screen()

    def draw_hud_itens_cura(self):
        inventario_dict = {}
        for item in self.inventario_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        imagens = {
            "Curativo": resource_path("img/curativo.png"),
            "Pomada": resource_path("img/pomada.png"),
            "Xarope": resource_path("img/xarope.png"),
            "Chá Natural": resource_path("img/cha.png")
        }
        font = pygame.font.SysFont("arial", 18)
        hud_x = 10
        hud_y = 10
        for i, (nome, data) in enumerate(inventario_dict.items()):
            img_path = imagens.get(nome, resource_path("img/curativo.png"))
            sprite = HudItemCuraSprite(hud_x + i*48, hud_y, img_path, data["quantidade"])
            sprite.draw(self.base_surface, font)
        if hasattr(self, 'inventario_chave') and 'tocha' in self.inventario_chave:
            tocha_sprite = HudItemCuraSprite(hud_x, hud_y + 54, resource_path("img/tocha.png"), 1)
            tocha_sprite.draw(self.base_surface, font)
            font2 = pygame.font.SysFont("arial", 16)
            self.base_surface.blit(font2.render("Tocha", True, (255,255,255)), (hud_x + 40, hud_y + 60))
        elif hasattr(self, 'inventario_chave') and 'sabonete' in self.inventario_chave:
            sabonete_sprite = HudItemCuraSprite(hud_x, hud_y + 54, resource_path("img/sabonete.png"), 1)
            sabonete_sprite.draw(self.base_surface, font)
            font2 = pygame.font.SysFont("arial", 16)
            self.base_surface.blit(font2.render("Sabonete", True, (255,255,255)), (hud_x + 40, hud_y + 60))
        
    def draw_npc_dialog(self):
        dialog_box_rect = pygame.Rect(40, BASE_WIN_HEIGHT - 120, BASE_WIN_WIDTH - 80, 80)
        pygame.draw.rect(self.base_surface, (255, 255, 255), dialog_box_rect, border_radius=10)
        pygame.draw.rect(self.base_surface, (0, 0, 0), dialog_box_rect, 2, border_radius=10)
        nome_npc = ""
        npc_symbol = getattr(self, "npc_dialog_npc_symbol", None)
        if npc_symbol:
            npc_info = npcs_data.get(npc_symbol)
            if npc_info:
                nome_npc = npc_info["nome"]
        if nome_npc:
            name_box_rect = pygame.Rect(dialog_box_rect.x + 20, dialog_box_rect.y - 32, 180, 28)
            pygame.draw.rect(self.base_surface, (255, 230, 250), name_box_rect, border_radius=8)
            pygame.draw.rect(self.base_surface, (0, 0, 0), name_box_rect, 2, border_radius=8)
            name_font = pygame.font.SysFont("arial", 20, bold=True)
            name_text = name_font.render(nome_npc, True, (0, 0, 0))
            self.base_surface.blit(name_text, (name_box_rect.x + 12, name_box_rect.y + 3))
        font = pygame.font.SysFont("arial", 16)
        now = pygame.time.get_ticks()
        if self.npc_dialog_char_index < len(self.npc_dialog_texts[self.npc_dialog_index]):
            if now - self.npc_dialog_last_update > 20:
                self.npc_dialog_char_index += self.npc_dialog_speed
                self.npc_dialog_last_update = now
        self.npc_dialog_current = self.npc_dialog_texts[self.npc_dialog_index][:self.npc_dialog_char_index]
        text_surface = font.render(self.npc_dialog_current, True, (0, 0, 0))
        self.base_surface.blit(text_surface, (dialog_box_rect.x + 20, dialog_box_rect.y + 20))
        btn_rect = pygame.Rect(dialog_box_rect.right - 120, dialog_box_rect.bottom - 40, 100, 30)
        pygame.draw.rect(self.base_surface, (200, 200, 255), btn_rect, border_radius=8)
        pygame.draw.rect(self.base_surface, (0, 0, 0), btn_rect, 2, border_radius=8)
        btn_font = pygame.font.SysFont("arial", 18)
        btn_text = btn_font.render("Avançar", True, (0, 0, 0))
        self.base_surface.blit(btn_text, (btn_rect.x + 18, btn_rect.y + 5))
        self.npc_dialog_btn_rect = btn_rect

    def checar_inimigos(self):
        total = 0
        restantes = 0
        for sprite in self.all_sprites:
            if hasattr(sprite, "enemy_name"):
                total += 1
        for sprite in self.enemy:
            restantes += 1
        return restantes, total
    
    def reset_save(self):
        self.mapa_atual_index = 0
        self.mapa_atual = mapas[self.mapa_atual_index]["tilemap"]
        self.fases = [True] * len(mapas)
        self.mapas_visitados = [False] * len(mapas)
        self.inventario_cura = []
        self.inventario_chave = []
        self.fox_hp = 100
        self.sabonete_spawned = False
        self.tocha_spawned = False
        self.npcs_moveram = False
        self.spawn_tocha_apos_dialogo = False
        self.npc_moved = False
        self.sombra_ativa_mapa3 = True
        self.movimento_bloqueado = False
        self.saved_state = None
        self.rei_mundica_derrotado = False
        if hasattr(self, "path_spawned_mapa5"):
            self.path_spawned_mapa5 = False
        self.npc_dialog_active = False
        self.npc_dialog_texts = []
        self.npc_dialog_index = 0
        self.npc_dialog_current = ""
        self.npc_dialog_char_index = 0 
        self.npc_dialog_npc_symbol = ""
        self.npc_dialog_btn_rect = None
        if hasattr(self, "save_file") and os.path.exists(self.save_file):
            os.remove(self.save_file)
        self.new()
    
    def change_ost(self):
        if self.mapa_atual_index == 0:
            mixer.music.load(resource_path("sounds/limpattack_ost_rei.mp3"))
            mixer.music.set_volume(1)
            mixer.music.play(-1)

    def draw_visual_pause_button(self):
        mouse_pos = self.get_scaled_mouse_pos()
        
        current_color = self.pause_button_color
        if self.pause_button_rect.collidepoint(mouse_pos):
            current_color = self.pause_button_hover_color

        pygame.draw.rect(self.base_surface, current_color, self.pause_button_rect, border_radius=5)
        pygame.draw.rect(self.base_surface, BLACK, self.pause_button_rect, 2, border_radius=5)

        text_surf = self.pause_button_font.render(self.pause_button_text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.pause_button_rect.center)
        self.base_surface.blit(text_surf, text_rect)

g = Game()
g.intro_screen()

if g.running:
    g.new()

while g.running:
    if g.playing:
        g.events()
        g.update()
        g.draw()
    else:
        g.game_over()

pygame.quit()
sys.exit()