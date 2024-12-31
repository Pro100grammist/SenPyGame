import pygame

from random import randint

from pygame.locals import K_g, K_o, K_d


class PlayerController:
    def __init__(self, player, sfx, movement, skills_tree, character_menu, inventory, merchant):
        self.player = player
        self.sfx = sfx
        self.movement = movement
        self.skills_tree = skills_tree
        self.character_menu = character_menu
        self.inventory = inventory
        self.merchant = merchant

    @property
    def dialog(self):
        return self.player.game.active_dialog

    def handle_events(self, event, keys):
        # cheat_mod
        if keys[K_g] and keys[K_o] and keys[K_d]:
            self.player.cheat_mode_on()

        # dialog box
        if self.player.talks:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.game.active_dialog.move_selection("up")
                elif event.key == pygame.K_DOWN:
                    self.player.game.active_dialog.move_selection("down")
                elif event.key == pygame.K_SPACE:
                    self.player.game.active_dialog.select_option()
                if event.key in (pygame.K_x, pygame.K_ESCAPE):
                    self.player.talks = False

        # skills tree
        elif self.player.skills_menu_is_active:
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
                if event.key in (pygame.K_b, pygame.K_ESCAPE):
                    self.player.skills_menu_is_active = False
        # character menu
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
                if event.key in (pygame.K_c, pygame.K_ESCAPE):
                    self.player.character_menu_is_active = False
        # inventory
        elif self.player.inventory_menu_is_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.inventory.move_cursor('up')
                elif event.key == pygame.K_DOWN:
                    self.inventory.move_cursor('down')
                elif event.key == pygame.K_LEFT:
                    self.inventory.move_cursor('left')
                elif event.key == pygame.K_RIGHT:
                    self.inventory.move_cursor('right')
                if event.key == pygame.K_SPACE:
                    self.inventory.apply()
                elif event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                    self.player.inventory_menu_is_active = False
        # merchant window
        elif self.player.trading:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.merchant.move_cursor('up')
                elif event.key == pygame.K_DOWN:
                    self.merchant.move_cursor('down')
                elif event.key == pygame.K_LEFT:
                    self.merchant.move_cursor('left')
                elif event.key == pygame.K_RIGHT:
                    self.merchant.move_cursor('right')
                if event.key == pygame.K_SPACE:
                    self.merchant.buy()
                elif event.key == pygame.K_ESCAPE:
                    self.player.trading = False
                if event.key == pygame.K_e:
                    if not self.merchant.view_details:
                        self.merchant.view_details = True
                    else:
                        self.merchant.view_details = False
                if event.key == pygame.K_y:
                    if self.merchant.view_details:
                        self.merchant.buy()
                        self.merchant.move_cursor('right')
                if event.key == pygame.K_n:
                    self.merchant.view_details = False

        else:
            if event.type == pygame.KEYDOWN and not self.player.dying:
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
                if event.key == pygame.K_RSHIFT:
                    self.player.change_shuriken()
                if event.key == pygame.K_q:
                    self.player.cast_spell()
                if event.key == pygame.K_1:
                    self.player.use_magic(0)
                if event.key == pygame.K_2:
                    self.player.use_magic(1)
                if event.key == pygame.K_3:
                    self.player.use_magic(2)
                if event.key == pygame.K_4:
                    self.player.use_magic(3)
                if event.key == pygame.K_5:
                    self.player.use_magic(4)
                if event.key == pygame.K_6:
                    self.player.use_magic(5)
                if event.key == pygame.K_LCTRL:
                    self.player.selected_scroll += 1
                    sound = str(randint(1, 3))
                    self.sfx['flipping_scroll' + sound].play()
                if event.key == pygame.K_LSHIFT:
                    self.player.selected_item += 1
                    self.sfx['select'].play()
                if event.key == pygame.K_f:
                    self.player.use_item()
                if event.key == pygame.K_x:
                    chest = self.player.check_chest_collision()
                    merchant = self.player.check_merchant_collision()
                    npc = self.player.check_npc_collision()
                    if chest:
                        chest.open()
                    elif merchant:
                        merchant.look_stuff()
                    elif npc:
                        npc.create_dialog()
                        if self.dialog:
                            self.dialog.display_dialogue()
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
                if event.key == pygame.K_i:
                    if not self.player.inventory_menu_is_active:
                        self.player.inventory_menu_is_active = True
                    else:
                        self.player.inventory_menu_is_active = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False
