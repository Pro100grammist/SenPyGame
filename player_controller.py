import pygame

from random import randint


class PlayerController:
    def __init__(self, player, sfx, movement, skills_tree, character_menu):
        self.player = player
        self.sfx = sfx
        self.movement = movement
        self.skills_tree = skills_tree
        self.character_menu = character_menu

    def handle_events(self, event):
        if self.player.skills_menu_is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.skills_tree.move_cursor('up')
                elif event.key == pygame.K_DOWN:
                    self.skills_tree.move_cursor('down')
                elif event.key == pygame.K_LEFT:
                    self.skills_tree.move_cursor('left')
                elif event.key == pygame.K_RIGHT:
                    self.skills_tree.move_cursor('right')
                if event.key == pygame.K_SPACE:
                    self.skills_tree.open_skill()
                if event.key == pygame.K_b:
                    self.player.skills_menu_is_active = False
        elif self.player.character_menu_is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.character_menu.move_cursor('up')
                elif event.key == pygame.K_DOWN:
                    self.character_menu.move_cursor('down')
                elif event.key == pygame.K_LEFT:
                    self.character_menu.move_cursor('left')
                elif event.key == pygame.K_RIGHT:
                    self.character_menu.move_cursor('right')
                if event.key == pygame.K_c:
                    self.player.character_menu_is_active = False

        else:
            if event.type == pygame.KEYDOWN and not self.player.death_hit:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_UP:
                    self.player.attack_pressed = False
                    self.player.jump()
                if event.key == pygame.K_d:
                    self.player.dash()
                if event.key == pygame.K_SPACE:
                    self.player.attack()
                if event.key == pygame.K_e:
                    self.player.ranged_attack()
                if event.key == pygame.K_q:
                    self.player.cast_spell()
                if event.key == pygame.K_LCTRL:
                    self.player.selected_scroll += 1
                    sound = str(randint(1, 3))
                    self.sfx['flipping_scroll' + sound].play()
                if event.key == pygame.K_LSHIFT:
                    self.player.selected_item += 1
                    self.sfx['select'].play()
                if event.key == pygame.K_f:
                    self.player.use_item()
                if event.key == pygame.K_b:
                    if not self.player.skills_menu_is_active:
                        self.player.skills_menu_is_active = True
                    else:
                        self.player.skills_menu_is_active = False
                if event.key == pygame.K_c:
                    if not self.player.character_menu_is_active:
                        self.player.character_menu_is_active = True
                    else:
                        self.player.character_menu_is_active = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False


