import pygame
from pygame import mixer
import random
from config import *
from battleData import *

pygame.init()
pygame.font.init()

font = pygame.font.SysFont("arial", 20)
dialog_font = pygame.font.SysFont("arial", 16)
small_button_font = pygame.font.SysFont("arial", 14)

def battle_screen(game, player_hp, player_max_hp, enemy, enemy_img, player_img, bg_img, itens_selecionados, main_game_over_func, inventario_cura):
    surface = game.base_surface

    if not hasattr(enemy, "max_hp"): enemy.max_hp = enemy.hp
    if not hasattr(enemy, "damage_flash"): enemy.damage_flash = 0

    player_damage_flash = 0
    selected_move = 0
    message = "O que Nala fará?"
    battle_phase = 0
    current_item = None
    running = True
    phase_timer = 0
    phase_delay = 2500
    modo_cura = False
    boss_estado = None
    itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy.nome)
    ultimo_estado_boss = None
    boss_primeiro_ataque = False

    def draw_text(text, x, y, font=font, color=BLACK):
        rendered = font.render(text, True, color)
        surface.blit(rendered, (x, y))

    def draw_hp_bar(name, x, y, hp, max_hp):
        bar_width, bar_height = 150, 10
        hp_ratio = hp / max_hp if max_hp > 0 else 0
        pygame.draw.rect(surface, WHITE, (x - 8, y - 28, 170, 70))
        pygame.draw.rect(surface, BLACK, (x - 8, y - 28, 170, 70), 2)
        draw_text(name, x, y - 24)
        pygame.draw.rect(surface, RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(surface, GREEN, (x, y, bar_width * hp_ratio, bar_height))
        draw_text(f"HP: {int(hp)}/{int(max_hp)}", x, y + 14, font)

    def draw_dialog_box(message):
        box_width, box_height = 220, 90
        box_x, box_y = BASE_WIN_WIDTH - box_width - 10, BASE_WIN_HEIGHT - box_height - 10
        pygame.draw.rect(surface, WHITE, (box_x, box_y, box_width, box_height), border_radius=8)
        pygame.draw.rect(surface, BLACK, (box_x, box_y, box_width, box_height), 2)
        for i, line in enumerate(message.split('\n')):
            draw_text(line, box_x + 8, box_y + 8 + i * 18, dialog_font)

    def draw_attack_buttons(moves, mouse_pos):
        container_x = 10
        container_y = BASE_WIN_HEIGHT - 100
        container_width = 390
        container_height = 90
        pygame.draw.rect(surface, WHITE, (container_x, container_y, container_width, container_height), border_radius=10)
        pygame.draw.rect(surface, BLACK, (container_x, container_y, container_width, container_height), 2)
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, move in enumerate(moves):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, LIGHT_ORANGE, button_rect, border_radius=8)
            else:
                pygame.draw.rect(surface, GRAY, button_rect, border_radius=8)
            pygame.draw.rect(surface, BLACK, button_rect, 2)
            draw_text(move.nome, button_rect.x + 8, button_rect.y + 6)

    def draw_cura_buttons(itens_cura, mouse_pos):
        inventario_dict = {}
        for item in itens_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        itens_unicos = list(inventario_dict.values())

        container_x = 10
        container_y = 380
        container_width = 390
        container_height = 90
        pygame.draw.rect(surface, WHITE, (container_x, container_y, container_width, container_height), border_radius=10)
        pygame.draw.rect(surface, BLACK, (container_x, container_y, container_width, container_height), 2)
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, data in enumerate(itens_unicos):
            item = data["item"]
            quantidade = data["quantidade"]
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, LIGHT_ORANGE, button_rect, border_radius=8)
            else:
                pygame.draw.rect(surface, GRAY, button_rect, border_radius=8)
            pygame.draw.rect(surface, BLACK, button_rect, 2)
            color = (0, 200, 255)
            pygame.draw.rect(surface, color, (button_rect.x + 4, button_rect.y + 4, 22, 22), border_radius=4)
            draw_text(f"{item.nome} (+{item.cura} HP)", button_rect.x + 32, button_rect.y + 6, small_button_font)
            draw_text(f"x{quantidade}", button_rect.x + button_width - 28, button_rect.y + 6, small_button_font)
            imagens = {
                "Curativo": "img/curativo.png",
                "Pomada": "img/pomada.png",
                "Xarope": "img/xarope.png",
                "Chá Natural": "img/cha.png"
            }
            img_path = imagens.get(item.nome, "img/curativo.png")
            try:
                img = pygame.image.load(img_path).convert()
                img.set_colorkey((184, 200, 168))
                img = pygame.transform.scale(img, (22, 22))
                surface.blit(img, (button_rect.x + 4, button_rect.y + 4))
            except Exception as e:
                pygame.draw.rect(surface, (255, 0, 0), (button_rect.x + 4, button_rect.y + 4, 22, 22), border_radius=4)

    def draw_toggle_cura_button(mouse_pos, modo_cura):
        btn_x = 410
        btn_y = 335
        btn_w = 130
        btn_h = 30
        btn_rect = pygame.Rect(btn_x, btn_y, btn_w, btn_h)
        cor_btn = (180, 255, 180) if not modo_cura else (255, 220, 180)
        if btn_rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, cor_btn, btn_rect, border_radius=10)
        else:
            pygame.draw.rect(surface, WHITE, btn_rect, border_radius=10)
        pygame.draw.rect(surface, BLACK, btn_rect, 2)
        texto = "Modo Cura" if not modo_cura else "Modo Ataque"
        draw_text(f"{texto}", btn_x + 10, btn_y + 5)

    def draw_text_centered(text, font, color):
        surface.fill(BLACK)
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(BASE_WIN_WIDTH // 2, BASE_WIN_HEIGHT // 2))
        surface.blit(rendered, rect)

    def fade_text(text):
        font_intro = pygame.font.SysFont("arial", 32)
        for alpha in range(0, 256, 16):
            draw_text_centered(text, font_intro, (alpha, alpha, alpha))
            game._render_final_screen()
            game.clock.tick(60)
        pygame.time.delay(800)
        for alpha in range(255, -1, -16):
            draw_text_centered(text, font_intro, (alpha, alpha, alpha))
            game._render_final_screen()
            game.clock.tick(60)

    def transition_to_battle():
        for alpha in range(0, 256, 16):
            surface.blit(bg_img, (0,0))
            veil = pygame.Surface((BASE_WIN_WIDTH, BASE_WIN_HEIGHT))
            veil.fill(BLACK)
            veil.set_alpha(255 - alpha)
            surface.blit(veil, (0,0))
            game._render_final_screen()
            game.clock.tick(60)

    def show_battle_intro(enemy_name):
        fade_text(f"Um inimigo apareceu: {enemy_name}!")
        pygame.time.delay(200)
        fade_text("Vamos Combater, Nala!")
        transition_to_battle()

    def handle_button_click(mouse_pos, moves):
        nonlocal selected_move
        container_x = 10
        container_y = 380
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, move in enumerate(moves):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                selected_move = i
                return True
        return False

    def handle_cura_button_click(mouse_pos, itens_cura):
        inventario_dict = {}
        for item in itens_cura:
            if item.nome not in inventario_dict:
                inventario_dict[item.nome] = {"item": item, "quantidade": 1}
            else:
                inventario_dict[item.nome]["quantidade"] += 1
        itens_unicos = list(inventario_dict.values())

        container_x = 10
        container_y = 380
        button_width = 180
        button_height = 30
        spacing_x = 10
        spacing_y = 10
        start_x = container_x + 8
        start_y = container_y + 8
        for i, data in enumerate(itens_unicos):
            col = i % 2
            row = i // 2
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)
            if button_rect.collidepoint(mouse_pos):
                return data["item"].nome
        return None

    def ataque_do_jogador(item_usado, inimigo):
        nonlocal boss_estado
        if inimigo.nome == "Rei Mundiça":
            if random.random() < 0.20:
                return "desviou", 0
        else:
            if random.random() < 0.15:
                return "desviou", 0

        nome_para_eficacia = boss_estado if (inimigo.nome == "Rei Mundiça" and boss_estado) else inimigo.nome
        dano = int(item_usado.calcular_dano(nome_para_eficacia))

        if inimigo.nome == "Rei Mundiça":
            x_rei, y_rei = 420, 60
            inimigo.tomar_dano(dano, surface, x_rei, y_rei, font, draw_hp_bar)
        else:
            inimigo.hp -= dano
            inimigo.hp = max(inimigo.hp, 0)

        if hasattr(inimigo, "vida"):
            inimigo.hp = inimigo.vida
            inimigo.max_hp = inimigo.vida_max

        if hasattr(inimigo, "damage_flash"):
            inimigo.damage_flash = 4
        else:
            setattr(inimigo, "damage_flash", 4)
        return "acertou", dano

    def ataque_do_inimigo(inimigo):
        nonlocal player_hp, player_damage_flash, boss_estado
        atk_nome, atk_dano = inimigo.ataque_aleatorio()
        boss_estado = None
        if inimigo.nome == "Rei Mundiça":
            for nome, enemy in enemies.items():
                if nome != "Rei Mundiça" and atk_nome in enemy.ataques:
                    boss_estado = nome
                    break
        player_hp -= atk_dano
        player_hp = max(player_hp, 0)
        player_damage_flash = 4
        return atk_nome, atk_dano
    
    show_battle_intro(enemy.nome)

    while running:
        mouse_pos = game.get_scaled_mouse_pos()
        now = pygame.time.get_ticks()

        surface.blit(bg_img, (0, 0))

        if player_damage_flash % 2 == 1:
            tinted = player_img.copy(); tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT); surface.blit(tinted, (110, 240))
        else:
            surface.blit(player_img, (110, 240))

        if getattr(enemy, "damage_flash", 0) % 2 == 1:
            tinted = enemy_img.copy(); tinted.fill((255, 0, 0, 100), special_flags=pygame.BLEND_RGBA_MULT); surface.blit(tinted, (400, 130))
        else:
            surface.blit(enemy_img, (400, 130))

        if player_damage_flash > 0: player_damage_flash -= 1
        if getattr(enemy, "damage_flash", 0) > 0: enemy.damage_flash -= 1

        draw_hp_bar("Nala", 60, 180, player_hp, player_max_hp)
        draw_hp_bar(enemy.nome, 420, 60, enemy.hp, enemy.max_hp)
        draw_dialog_box(message)

        if modo_cura:
            draw_cura_buttons(inventario_cura, mouse_pos)
        else:
            if enemy.nome == "Rei Mundiça" and boss_estado:
                if boss_estado != ultimo_estado_boss:
                    itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(boss_estado)
                    ultimo_estado_boss = boss_estado
            else:
                if ultimo_estado_boss != enemy.nome:
                    itens_selecionados = selecionar_ataques_eficazes_e_aleatorios(enemy.nome)
                    ultimo_estado_boss = enemy.nome
            draw_attack_buttons(itens_selecionados, mouse_pos)
        draw_toggle_cura_button(mouse_pos, modo_cura)

        game._render_final_screen()
        game.clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = game.get_scaled_mouse_pos()
                btn_x, btn_y, btn_w, btn_h = 410, 335, 130, 30
                if pygame.Rect(btn_x, btn_y, btn_w, btn_h).collidepoint(click_pos):
                    modo_cura = not modo_cura
                    continue
                if event.button == 1 and battle_phase == 0:
                    if not modo_cura:
                        if handle_button_click(click_pos, itens_selecionados):
                            current_item = itens_selecionados[selected_move]
                            message = f"Nala escolheu...\n{current_item.nome}!"
                            battle_phase = 1
                            phase_timer = now
                    else:
                        nome_item_clicado = handle_cura_button_click(click_pos, inventario_cura)
                        if nome_item_clicado:
                            for idx, item in enumerate(inventario_cura):
                                if item.nome == nome_item_clicado:
                                    cura = item.cura
                                    player_hp = min(player_hp + cura, player_max_hp)
                                    message = f"Nala usou {item.nome}!\nRecuperou {cura} de vida."
                                    inventario_cura.pop(idx)
                                    battle_phase = 2
                                    phase_timer = now
                                    break

        if battle_phase == 1 and now - phase_timer > phase_delay:
            resultado_ataque, dano = ataque_do_jogador(current_item, enemy)
            if resultado_ataque == "desviou":
                message = f"E {enemy.nome}...\nDesviou do ataque!"
            else:
                if dano >= enemy.hp + dano:
                    eficiencia_msg = "Dano crítico! Muito bem!"
                elif dano >= 0.6 * enemy.max_hp:
                    eficiencia_msg = "O ataque foi MUITO EFICIENTE!"
                elif dano >= 0.4 * enemy.max_hp:
                    eficiencia_msg = "O ataque foi eficiente!"
                elif dano >= 0.2 * enemy.max_hp:
                    eficiencia_msg = "O ataque foi bom..."
                else:
                    eficiencia_msg = "O ataque não foi eficiente..."
                message = f"Nala usou...\n{current_item.nome}!\nCausou {dano} de dano.\n{eficiencia_msg}"
            battle_phase = 2
            phase_timer = now

        if battle_phase == 2 and now - phase_timer > phase_delay:
            if enemy.hp > 0:
                atk_nome, atk_dano = ataque_do_inimigo(enemy)
                if enemy.nome == "Rei Mundiça" and boss_estado:
                    message = f"Rei Mundiça se personificou de...\n{boss_estado}!\nUsou {atk_nome} e...\nCausou {atk_dano} de dano!"
                else:
                    message = f"{enemy.nome} usou...\n{atk_nome}!\nCausou {atk_dano} de dano."
            else:
                victory_messages = [
                    "Higiene é tudo!",
                    "A higiene venceu denovo!",
                    "Viva aos bons hábitos!",
                    "Nala venceu com muita higiene!",
                    "Bactérias não tem vez aqui!",
                    "Vitória brilhante e cheirosa!",
                    "Nada resiste à higiene!",
                    "Bons hábitos sempre vencem!",
                    "Continue com a higiene!",
                    "Mostrou quem manda na limpeza!"
                ]
                message = f"E {enemy.nome}...\nFoi derrotado!\n{random.choice(victory_messages)}"
            battle_phase = 3
            phase_timer = now

        if battle_phase == 3 and now - phase_timer > phase_delay:
            if enemy.hp <= 0 or player_hp <= 0:
                if player_hp <= 0:
                    main_game_over_func()
                    return "derrota"
                else:
                    mostrar_vitoria(game, "Vitória! Nala venceu!", 2500)
                    return player_hp
            else:
                message = "O que Nala fará?"
                battle_phase = 0

        if enemy.nome == "Rei Mundiça" and not boss_primeiro_ataque:
            atk_nome, atk_dano = ataque_do_inimigo(enemy)
            if boss_estado:
                message = f"Rei Mundiça se personificou de...\n{boss_estado}!\nUsou {atk_nome} e...\nCausou {atk_dano} de dano!"
            else:
                message = f"Rei Mundiça atacou!\nUsou {atk_nome} e...\nCausou {atk_dano} de dano!"
            boss_primeiro_ataque = True
            battle_phase = 3
            phase_timer = pygame.time.get_ticks()
            continue


def mostrar_vitoria(game, mensagem, tempo_ms=2500):
    mixer.music.stop()
    mixer.music.load("sounds/limpattack_tune_vitoria.mp3")
    mixer.music.set_volume(1)
    mixer.music.play()
    
    font_vitoria = pygame.font.SysFont("arial", 32)
    start = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start < tempo_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
        
        game.base_surface.fill(BLACK)
        texto = font_vitoria.render(mensagem, True, WHITE)
        rect = texto.get_rect(center=(BASE_WIN_WIDTH / 2, BASE_WIN_HEIGHT / 2))
        game.base_surface.blit(texto, rect)
        
        game._render_final_screen()
        game.clock.tick(30)
        
    mixer.music.stop()